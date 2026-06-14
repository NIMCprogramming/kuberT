from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Header, Label, ListItem, ListView, Static

from kubert import bootstrap, cluster
from kubert.lesson import discover_lessons, get_default_lessons_root
from kubert.models import Lesson
from kubert.runner import run_lesson
from kubert.state import load_progress
from kubert.ui import console

MENU = [
    ("next",   "Run next unfinished lesson"),
    ("pick",   "Pick a lesson from the list"),
    ("init",   "Check tools / create cluster"),
    ("status", "Show cluster status"),
    ("reset",  "Delete cluster"),
    ("quit",   "Quit"),
]


class KubertApp(App[None]):
    TITLE = "kuberT"
    SUB_TITLE = "learn Kubernetes in your terminal"
    BINDINGS = [Binding("q", "quit", "Quit")]
    CSS = """
    Screen { align: center middle; }
    #welcome { margin: 1 4; text-align: center; }
    ListView { margin: 0 4; border: round $accent; padding: 0 1; }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(
            "\n[b]Welcome to kuberT[/b]\n"
            "Use [yellow]↑/↓[/yellow] to move, [yellow]Enter[/yellow] to choose.\n",
            id="welcome",
        )
        yield ListView(
            *[ListItem(Label(label), id=f"a-{key}") for key, label in MENU],
            id="menu",
        )
        yield Footer()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item_id = event.item.id or ""
        action = item_id.removeprefix("a-")
        if action == "quit":
            self.exit()
            return
        with self.suspend():
            _dispatch(action)
            console.input("\n[dim]Press Enter to return to menu...[/dim]")


def _dispatch(action: str) -> None:
    handlers = {
        "next":   _next,
        "pick":   _pick,
        "init":   lambda: bootstrap.init_cluster(),
        "status": _status,
        "reset":  _reset,
    }
    handler = handlers.get(action)
    if handler:
        try:
            handler()
        except KeyboardInterrupt:
            console.print("\n[yellow]Cancelled.[/yellow]")


def _lessons() -> list[Lesson]:
    return discover_lessons(get_default_lessons_root())


def _next() -> None:
    p = load_progress()
    for lesson in _lessons():
        if lesson.id not in p.completed_lessons:
            run_lesson(lesson, p)
            return
    console.print("[green]All lessons complete![/green]")


def _pick() -> None:
    lessons = _lessons()
    p = load_progress()
    for i, lesson in enumerate(lessons, 1):
        mark = "[green][x][/green]" if lesson.id in p.completed_lessons else "[dim][ ][/dim]"
        console.print(f"{i:2}. {mark} {lesson.id} - {lesson.title}")
    raw = console.input("\nLesson number (Enter to cancel): ").strip()
    if not raw.isdigit():
        return
    idx = int(raw) - 1
    if 0 <= idx < len(lessons):
        run_lesson(lessons[idx], p)


def _status() -> None:
    if cluster.exists():
        console.print(f"[green]Cluster '{cluster.name()}' is running.[/green]")
    else:
        console.print("[yellow]No cluster. Pick 'Check tools / create cluster' first.[/yellow]")


def _reset() -> None:
    if not cluster.exists():
        console.print("[yellow]No cluster to delete.[/yellow]")
        return
    if console.input(f"Delete cluster '{cluster.name()}'? (y/N): ").strip().lower() == "y":
        cluster.delete()
        console.print("[green]Cluster deleted.[/green]")


def run() -> None:
    KubertApp().run()
