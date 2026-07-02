from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Footer, Header, Label, ListItem, ListView, Static

from kubert import cluster
from kubert.cluster_screens import InitScreen, ResetConfirmScreen
from kubert.lesson import discover_lessons, get_default_lessons_root
from kubert.lesson_screens import LessonPickerScreen, LessonScreen
from kubert.state import load_progress, reset_progress

MENU = [
    ("next",     "Run next unfinished lesson"),
    ("pick",     "Pick a lesson from the list"),
    ("init",     "Check tools / create cluster"),
    ("status",   "Show cluster status"),
    ("reset",    "Delete cluster"),
    ("progress", "Reset my lesson progress"),
    ("quit",     "Quit"),
]


class MainMenuScreen(Screen[None]):
    BINDINGS = [Binding("q", "app.quit", "Quit")]
    CSS = """
    Screen { align: center middle; }
    #welcome { margin: 1 4; text-align: center; }
    ListView { margin: 0 4; width: 60; border: round $accent; padding: 0 1; }
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
        action = (event.item.id or "").removeprefix("a-")
        if action == "quit":
            self.app.exit()
        elif action == "next":
            self._open_next()
        elif action == "pick":
            self.app.push_screen(LessonPickerScreen())
        elif action == "init":
            self.app.push_screen(InitScreen())
        elif action == "status":
            self._show_status()
        elif action == "reset":
            self.app.push_screen(ResetConfirmScreen())
        elif action == "progress":
            reset_progress()
            self.app.notify("Progress cleared. Start from lesson 1.", severity="information")

    def _open_next(self) -> None:
        progress = load_progress()
        for lesson in discover_lessons(get_default_lessons_root()):
            if lesson.id not in progress.completed_lessons:
                self.app.push_screen(LessonScreen(lesson))
                return
        self.app.notify("All lessons complete!", severity="information")

    def _show_status(self) -> None:
        if cluster.exists() and cluster.is_reachable():
            self.app.notify(f"Cluster '{cluster.name()}' is running.", severity="information")
        elif cluster.exists():
            self.app.notify("Cluster exists but kubectl cannot reach it.", severity="warning")
        else:
            self.app.notify("No cluster. Pick 'Check tools / create cluster'.", severity="warning")


class KubertApp(App[None]):
    TITLE = "kuberT"
    SUB_TITLE = "learn Kubernetes in your terminal"

    def on_mount(self) -> None:
        self.push_screen(MainMenuScreen())


def run() -> None:
    KubertApp().run()
