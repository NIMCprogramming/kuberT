from pathlib import Path

import pytest

from kubert.lesson import discover_lessons, get_default_lessons_root, load_lesson_file
from kubert.models import CommandCheck, Lesson, ManualCheck, MultipleCheck

LESSONS_ROOT = get_default_lessons_root()


def test_lessons_root_exists() -> None:
    assert LESSONS_ROOT.exists(), f"Lessons folder missing: {LESSONS_ROOT}"


def test_at_least_one_lesson_exists() -> None:
    lessons = discover_lessons(LESSONS_ROOT)
    assert len(lessons) > 0


@pytest.mark.parametrize(
    "yaml_path",
    sorted(LESSONS_ROOT.rglob("*.yaml")),
    ids=lambda p: str(p.relative_to(LESSONS_ROOT)),
)
def test_every_lesson_yaml_is_valid(yaml_path: Path) -> None:
    lesson = load_lesson_file(yaml_path)
    assert isinstance(lesson, Lesson)
    assert lesson.id
    assert lesson.title
    assert lesson.intro


def test_lesson_ids_are_unique() -> None:
    lessons = discover_lessons(LESSONS_ROOT)
    ids = [lesson.id for lesson in lessons]
    assert len(ids) == len(set(ids)), "duplicate lesson ids"


def test_manual_check_loads() -> None:
    lessons = discover_lessons(LESSONS_ROOT)
    overview = next(lesson for lesson in lessons if lesson.id.endswith("overview"))
    assert isinstance(overview.check, ManualCheck)


def test_command_check_loads() -> None:
    lessons = discover_lessons(LESSONS_ROOT)
    pods = next(lesson for lesson in lessons if lesson.id.endswith("pods"))
    assert isinstance(pods.check, MultipleCheck)
    assert any(
        isinstance(c, CommandCheck) and "Running" in c.expect
        for c in pods.check.checks
    )


def test_every_lesson_has_cheat_notes() -> None:
    for lesson in discover_lessons(LESSONS_ROOT):
        assert lesson.cheat.strip(), f"lesson {lesson.id} has empty cheat"


def test_pods_lesson_declares_cluster_requirement() -> None:
    lessons = discover_lessons(LESSONS_ROOT)
    pods = next(lesson for lesson in lessons if lesson.id.endswith("pods"))
    assert "cluster" in pods.requires


def test_overview_lesson_has_no_requirements() -> None:
    lessons = discover_lessons(LESSONS_ROOT)
    overview = next(lesson for lesson in lessons if lesson.id.endswith("overview"))
    assert overview.requires == []
