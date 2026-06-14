from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, VerticalScroll
from textual.screen import Screen
from textual.widgets import (
    Button,
    Footer,
    Header,
    Label,
    ListItem,
    ListView,
    Markdown,
    RichLog,
    Static,
)

from kubert import cluster
from kubert.checker import run_check
from kubert.lesson import discover_lessons, get_default_lessons_root
from kubert.models import Lesson, ManualCheck
from kubert.state import load_progress, save_progress


class LessonItem(ListItem):
    def __init__(self, lesson: Lesson, marker: str) -> None:
        super().__init__(Label(f"{marker} {lesson.id} - {lesson.title}"))
        self.lesson = lesson


class LessonPickerScreen(Screen[None]):
    BINDINGS = [Binding("escape", "app.pop_screen", "Back")]
    CSS = """
    Screen { align: center middle; }
    #title { margin: 1 0; }
    ListView { width: 80%; height: 70%; border: round $accent; padding: 0 1; }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Pick a lesson  ([yellow]Esc[/yellow] to go back)", id="title")
        progress = load_progress()
        items = [
            LessonItem(lesson, "[x]" if lesson.id in progress.completed_lessons else "[ ]")
            for lesson in discover_lessons(get_default_lessons_root())
        ]
        yield ListView(*items, id="lessons")
        yield Footer()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if isinstance(event.item, LessonItem):
            self.app.pop_screen()
            self.app.push_screen(LessonScreen(event.item.lesson))


class LessonScreen(Screen[None]):
    BINDINGS = [Binding("escape", "app.pop_screen", "Back to menu")]
    CSS = """
    #intro, #task { padding: 1 2; }
    #task { border: round $warning; margin: 0 2; }
    #output { border: round $primary; height: 8; margin: 0 2; padding: 0 1; }
    .buttons { dock: bottom; height: 3; padding: 0 2; align: center middle; }
    Button { margin: 0 1; }
    """

    def __init__(self, lesson: Lesson) -> None:
        super().__init__()
        self.lesson = lesson

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll():
            yield Markdown(self.lesson.intro, id="intro")
            if not isinstance(self.lesson.check, ManualCheck):
                yield Markdown(self.lesson.task, id="task")
            yield RichLog(id="output", markup=True)
        with Horizontal(classes="buttons"):
            if isinstance(self.lesson.check, ManualCheck):
                yield Button("Mark as read", id="manual", variant="success")
            else:
                yield Button("Check", id="check", variant="success")
                yield Button("Hint", id="hint", variant="primary")
                yield Button("Skip", id="skip", variant="error")
        yield Footer()

    def on_mount(self) -> None:
        ok, msg = self._check_req()
        if not ok:
            self.query_one("#output", RichLog).write(f"[red]{msg}[/red]")
            for btn in self.query(Button):
                btn.disabled = True

    def _check_req(self) -> tuple[bool, str]:
        if "cluster" in self.lesson.requires:
            if not cluster.exists():
                return False, (
                    "This lesson needs a cluster. Go back and pick "
                    "'Check tools / create cluster'."
                )
            if not cluster.is_reachable():
                return False, "Cluster exists but is unreachable. Delete it and recreate."
        return True, ""

    def on_button_pressed(self, event: Button.Pressed) -> None:
        handlers = {
            "manual": self._on_manual,
            "check":  self._on_check,
            "hint":   self._on_hint,
            "skip":   self._on_skip,
        }
        handler = handlers.get(event.button.id or "")
        if handler:
            handler()

    def _on_manual(self) -> None:
        self._mark_complete()
        self.app.notify("Lesson complete!", severity="information")
        self.app.pop_screen()

    def _on_check(self) -> None:
        log = self.query_one("#output", RichLog)
        result = run_check(self.lesson.check)
        if result.passed:
            log.write(f"[green]OK: {result.detail}[/green]")
            self._mark_complete()
            self.app.notify("Lesson complete!", severity="information")
        else:
            log.write(f"[red]FAIL: {result.detail}[/red]")

    def _on_hint(self) -> None:
        self.query_one("#output", RichLog).write(
            f"[blue]Hint: {self.lesson.hint or 'No hint.'}[/blue]"
        )

    def _on_skip(self) -> None:
        self.app.pop_screen()

    def _mark_complete(self) -> None:
        p = load_progress()
        if self.lesson.id not in p.completed_lessons:
            p.completed_lessons.append(self.lesson.id)
        save_progress(p)
