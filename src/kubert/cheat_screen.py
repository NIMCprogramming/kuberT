from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import Footer, Header, Markdown, Static

from kubert.lesson import discover_lessons, get_default_lessons_root
from kubert.state import load_progress


class CheatPanelScreen(Screen[None]):
    BINDINGS = [Binding("escape", "app.pop_screen", "Back")]
    CSS = """
    CheatPanelScreen { layout: vertical; }
    #cheat-title { padding: 0 2; margin: 1 2 0 2; color: $accent; }
    #cheat-empty { padding: 1 2; color: $warning; }
    .cheat-lesson-title { padding: 0 2; margin: 1 2 0 2; color: $success; }
    .cheat-body { padding: 0 2; margin: 0 2 1 2; }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("[b]Cheat panel[/b] — only lessons you finished are shown.", id="cheat-title")
        progress = load_progress()
        done = [l for l in discover_lessons(get_default_lessons_root()) if l.id in progress.completed_lessons]
        with VerticalScroll():
            if not done:
                yield Static(
                    "You have not finished any lessons yet. Complete a lesson, then come back here.",
                    id="cheat-empty",
                )
            else:
                for lesson in done:
                    yield Static(f"[b]{lesson.id}[/b] — {lesson.title}", classes="cheat-lesson-title")
                    body = lesson.cheat or "_(no cheat notes yet for this lesson)_"
                    yield Markdown(body, classes="cheat-body")
        yield Footer()
