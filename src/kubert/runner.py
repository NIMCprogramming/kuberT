import questionary

from kubert import cluster
from kubert.checker import run_check
from kubert.models import Lesson, ManualCheck, UserProgress
from kubert.state import save_progress
from kubert.ui import (
    console,
    show_extras,
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

    if lesson.learning_goal:
        show_info(f"Goal: {lesson.learning_goal}")

    show_intro(lesson.intro)

    if isinstance(lesson.check, ManualCheck):
        show_extras(_build_extras(lesson))
        console.input("\n[dim]Press Enter when you finish reading...[/dim]")
        _mark_complete(lesson, progress)
        show_success(f"Lesson complete: {lesson.title}")
        return True

    show_task(lesson.task)
    show_extras(_build_extras(lesson))

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


def _build_extras(lesson: Lesson) -> str:
    parts: list[str] = []
    if lesson.prerequisites:
        parts.append("## Builds on\n" + ", ".join(f"`{p}`" for p in lesson.prerequisites))
    if lesson.warm_up:
        lines = ["## Warm-up recall"]
        for i, q in enumerate(lesson.warm_up, 1):
            lines.append(f"{i}. {q.prompt}\n   _Answer:_ {q.answer}")
        parts.append("\n".join(lines))
    if lesson.troubleshooting:
        ts = lesson.troubleshooting
        parts.append(
            f"## Troubleshooting scenario\n{ts.scenario}\n\n"
            f"**Question:** {ts.question}\n\n"
            f"**Diagnosis:** {ts.diagnosis}"
        )
    if lesson.review_questions:
        lines = ["## Review questions"]
        for i, q in enumerate(lesson.review_questions, 1):
            block = f"{i}. ({q.kind}) {q.prompt}"
            if q.kind == "multiple_choice" and q.options:
                block += "\n" + "\n".join(f"   - {opt}" for opt in q.options)
            block += f"\n   _Answer:_ {q.answer}"
            lines.append(block)
        parts.append("\n".join(lines))
    if lesson.common_mistakes:
        lines = ["## Common mistakes"]
        for m in lesson.common_mistakes:
            lines.append(f"- **{m.mistake}** — {m.fix}")
        parts.append("\n".join(lines))
    if lesson.summary:
        parts.append(f"## Mini summary\n{lesson.summary}")
    return "\n\n".join(parts)


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
