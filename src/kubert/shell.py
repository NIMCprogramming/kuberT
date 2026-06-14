from collections.abc import Callable

from kubert import bootstrap, cluster
from kubert.lesson import discover_lessons, get_default_lessons_root
from kubert.models import Lesson
from kubert.runner import run_lesson
from kubert.state import load_progress
from kubert.ui import console, show_failure, show_info, show_success, show_title


def _all() -> list[Lesson]:
    return discover_lessons(get_default_lessons_root())


def cmd_init(_: str) -> None:
    bootstrap.init_cluster()


def cmd_list(_: str) -> None:
    p = load_progress()
    for lesson in _all():
        mark = "[green][x][/green]" if lesson.id in p.completed_lessons else "[dim][ ][/dim]"
        console.print(f"{mark} {lesson.id} - {lesson.title}")


def cmd_next(_: str) -> None:
    p = load_progress()
    for lesson in _all():
        if lesson.id not in p.completed_lessons:
            run_lesson(lesson, p)
            return
    show_success("All lessons complete!")


def cmd_lesson(arg: str) -> None:
    if not arg:
        show_failure("Usage: lesson <id>")
        return
    p = load_progress()
    for lesson in _all():
        if lesson.id == arg:
            run_lesson(lesson, p)
            return
    show_failure(f"No lesson with id '{arg}'.")


def cmd_status(_: str) -> None:
    if cluster.exists():
        show_success(f"Cluster '{cluster.name()}' is running.")
    else:
        show_info("No cluster. Type 'init' to create one.")


def cmd_reset(_: str) -> None:
    if not cluster.exists():
        show_info("No cluster to delete.")
        return
    if console.input("[yellow]Delete cluster? (y/N): [/yellow]").strip().lower() == "y":
        cluster.delete()
        show_success("Cluster deleted.")


def cmd_help(_: str) -> None:
    for name, (_fn, desc) in COMMANDS.items():
        console.print(f"  [cyan]{name:<8}[/cyan] {desc}")
    console.print(f"  [cyan]{'quit':<8}[/cyan] exit the app")


COMMANDS: dict[str, tuple[Callable[[str], None], str]] = {
    "init":   (cmd_init,   "check tools and create a Kind cluster"),
    "next":   (cmd_next,   "run the next unfinished lesson"),
    "list":   (cmd_list,   "list all lessons with progress"),
    "lesson": (cmd_lesson, "run a lesson by id (e.g. lesson 04-running-apps/01-pods)"),
    "status": (cmd_status, "show cluster status"),
    "reset":  (cmd_reset,  "delete the cluster"),
    "help":   (cmd_help,   "show this help"),
}


def run() -> None:
    show_title("kuberT shell")
    show_info("Type 'help' for commands. Type 'quit' to exit.")
    if not cluster.exists():
        show_info("No cluster found yet. Type 'init' to create one.")
    while True:
        try:
            raw = console.input("\n[bold cyan]kubert>[/bold cyan] ").strip()
        except (EOFError, KeyboardInterrupt):
            console.print()
            return
        if not raw:
            continue
        if raw in ("quit", "exit", "q"):
            return
        cmd, _, arg = raw.partition(" ")
        action = COMMANDS.get(cmd)
        if not action:
            show_failure(f"Unknown command: {cmd}. Type 'help'.")
            continue
        try:
            action[0](arg.strip())
        except KeyboardInterrupt:
            console.print()
            show_info("Cancelled.")
