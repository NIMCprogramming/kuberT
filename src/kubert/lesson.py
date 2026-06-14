from pathlib import Path

import yaml

from kubert.models import Lesson


def load_lesson_file(path: Path) -> Lesson:
    raw = yaml.safe_load(path.read_text())
    return Lesson.model_validate(raw)


def discover_lessons(lessons_root: Path) -> list[Lesson]:
    lessons: list[Lesson] = []
    for yaml_file in sorted(lessons_root.rglob("*.yaml")):
        lessons.append(load_lesson_file(yaml_file))
    return lessons


def get_default_lessons_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent / "lessons"
