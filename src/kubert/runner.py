import questionary

from kubert import cluster
from kubert.checker import run_check
from kubert.models import Lesson, ManualCheck, UserProgress
from kubert.state import save_progress
from kubert.ui import (
    console,
    show_failure,
    show_hint,
    show_info,
    show_intro,
    show_success,
    show_task,
    show_title,
)


def run_lesson(lesson: Lesson, progress: UserProgress) -> bool:
    show_title(f"{lesson.id} - {lesson.title}")

    ok, msg = _check_requirements(lesson)
    if not ok:
        show_failure(msg)
        return False

    show_intro(lesson.intro)

    if isinstance(lesson.check, ManualCheck):
        console.input("\n[dim]Press Enter when you finish reading...[/dim]")
        _mark_complete(lesson, progress)
        show_success(f"Lesson complete: {lesson.title}")
        return True

    show_task(lesson.task)

    choices = [
        questionary.Choice("Check my work", "check"),
        questionary.Choice("Show hint",     "hint"),
        questionary.Choice("Skip lesson",   "skip"),
    ]

    while True:
        choice = questionary.select("What now?", choices=choices).ask()
        if choice in (None, "skip"):
            show_info("Lesson skipped.")
            return False
        if choice == "hint":
            show_hint(lesson.hint or "No hint for this lesson.")
            continue
        result = run_check(lesson.check)
        if result.passed:
            show_success(result.detail)
            _mark_complete(lesson, progress)
            return True
        show_failure(result.detail)


def _check_requirements(lesson: Lesson) -> tuple[bool, str]:
    if "cluster" in lesson.requires:
        if not cluster.exists():
            return False, (
                "This lesson needs a Kubernetes cluster. "
                "From the menu, pick 'Check tools / create cluster' first."
            )
        if not cluster.is_reachable():
            return False, (
                "A cluster exists but kubectl cannot reach it (the container may be stopped). "
                "From the menu, pick 'Delete cluster' and then 'Check tools / create cluster'."
            )
    return True, ""


def _mark_complete(lesson: Lesson, progress: UserProgress) -> None:
    if lesson.id not in progress.completed_lessons:
        progress.completed_lessons.append(lesson.id)
    save_progress(progress)
