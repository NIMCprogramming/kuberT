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
    show_intro(lesson.intro)

    if isinstance(lesson.check, ManualCheck):
        console.input("\n[dim]Press Enter when you finish reading...[/dim]")
        _mark_complete(lesson, progress)
        show_success(f"Lesson complete: {lesson.title}")
        return True

    show_task(lesson.task)

    while True:
        choice = (
            console.input(
                "\n[bold]Type [green]check[/green] when ready, "
                "[yellow]hint[/yellow] for a hint, or [red]skip[/red]:[/bold] "
            )
            .strip()
            .lower()
        )

        if choice == "skip":
            show_info("Lesson skipped.")
            return False
        if choice == "hint":
            show_hint(lesson.hint or "No hint for this lesson.")
            continue
        if choice == "check":
            result = run_check(lesson.check)
            if result.passed:
                show_success(result.detail)
                _mark_complete(lesson, progress)
                return True
            show_failure(result.detail)
            continue
        show_info("Unknown choice. Type check, hint, or skip.")


def _mark_complete(lesson: Lesson, progress: UserProgress) -> None:
    if lesson.id not in progress.completed_lessons:
        progress.completed_lessons.append(lesson.id)
    save_progress(progress)
