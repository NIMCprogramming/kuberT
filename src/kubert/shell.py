from collections.abc import Callable

import questionary

from kubert import bootstrap, cluster
from kubert.lesson import discover_lessons, get_default_lessons_root
from kubert.models import Lesson
from kubert.runner import run_lesson
from kubert.state import load_progress
from kubert.ui import show_info, show_success, show_title


def _lessons() -> list[Lesson]:
    return discover_lessons(get_default_lessons_root())


def _run_next() -> None:
    p = load_progress()
    for lesson in _lessons():
        if lesson.id not in p.completed_lessons:
            run_lesson(lesson, p)
            return
    show_success("All lessons complete!")


def _pick_lesson() -> None:
    p = load_progress()
    lessons = _lessons()
    choices = [
        questionary.Choice(
            title=("[x] " if lesson.id in p.completed_lessons else "[ ] ")
            + f"{lesson.id} - {lesson.title}",
            value=lesson.id,
        )
        for lesson in lessons
    ]
    choices.append(questionary.Choice(title="← Back", value="back"))
    choice = questionary.select("Pick a lesson:", choices=choices).ask()
    if choice in (None, "back"):
        return
    for lesson in lessons:
        if lesson.id == choice:
            run_lesson(lesson, p)
            return


def _init() -> None:
    bootstrap.init_cluster()


def _status() -> None:
    if cluster.exists():
        show_success(f"Cluster '{cluster.name()}' is running.")
    else:
        show_info("No cluster. Pick 'Check tools / create cluster' first.")


def _reset() -> None:
    if not cluster.exists():
        show_info("No cluster to delete.")
        return
    if questionary.confirm(f"Delete cluster '{cluster.name()}'?", default=False).ask():
        cluster.delete()
        show_success("Cluster deleted.")


ACTIONS: dict[str, Callable[[], None]] = {
    "next":   _run_next,
    "pick":   _pick_lesson,
    "init":   _init,
    "status": _status,
    "reset":  _reset,
}


def _menu_choices() -> list[questionary.Choice]:
    return [
        questionary.Choice("Run next unfinished lesson", "next"),
        questionary.Choice("Pick a lesson from the list",  "pick"),
        questionary.Choice("Check tools / create cluster", "init"),
        questionary.Choice("Show cluster status",          "status"),
        questionary.Choice("Delete cluster",               "reset"),
        questionary.Choice("Quit",                         "quit"),
    ]


def run() -> None:
    show_title("kuberT")
    if not cluster.exists():
        show_info("No cluster yet. Pick 'Check tools / create cluster' to set up.")
    while True:
        choice = questionary.select("What do you want to do?", choices=_menu_choices()).ask()
        if choice in (None, "quit"):
            return
        action = ACTIONS.get(choice)
        if not action:
            continue
        try:
            action()
        except KeyboardInterrupt:
            show_info("Cancelled.")
