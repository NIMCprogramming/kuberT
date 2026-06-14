from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import Footer, Header, Label, ListItem, ListView, Markdown, RichLog, Static

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
    #title { margin: 1 0; text-align: center; }
    ListView { width: 80%; height: 70%; border: round $accent; padding: 0 1; }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Pick a lesson", id="title")
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
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("c",      "do_primary",     "Check / Confirm"),
        Binding("h",      "do_hint",        "Hint"),
        Binding("s",      "app.pop_screen", "Skip"),
    ]
    CSS = """
    LessonScreen { layout: vertical; }
    #intro   { padding: 0 2; margin: 1 2 0 2; }
    #task    { border: round $warning; padding: 1 2; margin: 1 2; }
    #output  { border: round $primary; padding: 0 1; margin: 0 2 1 2; height: 10; }
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
        yield Footer()

    def on_mount(self) -> None:
        ok, msg = self._check_req()
        log = self.query_one("#output", RichLog)
        if not ok:
            log.write(f"[red]{msg}[/red]")
        else:
            tip = "Press [b]c[/b] to mark as read." if isinstance(
                self.lesson.check, ManualCheck
            ) else "Press [b]c[/b] to check, [b]h[/b] for a hint, [b]s[/b] to skip."
            log.write(f"[dim]{tip}[/dim]")

    def _check_req(self) -> tuple[bool, str]:
        if "cluster" in self.lesson.requires:
            if not cluster.exists():
                return False, (
                    "This lesson needs a cluster. Press Esc, then pick "
                    "'Check tools / create cluster'."
                )
            if not cluster.is_reachable():
                return False, "Cluster exists but is unreachable. Delete it and recreate."
        return True, ""

    def action_do_primary(self) -> None:
        if isinstance(self.lesson.check, ManualCheck):
            self._mark_complete()
            self.app.notify("Lesson complete!", severity="information")
            self.app.pop_screen()
            return
        ok, msg = self._check_req()
        log = self.query_one("#output", RichLog)
        if not ok:
            log.write(f"[red]{msg}[/red]")
            return
        result = run_check(self.lesson.check)
        if result.passed:
            log.write(f"[green]OK: {result.detail}[/green]")
            self._mark_complete()
            self.app.notify("Lesson complete!", severity="information")
        else:
            log.write(f"[red]FAIL: {result.detail}[/red]")

    def action_do_hint(self) -> None:
        log = self.query_one("#output", RichLog)
        if isinstance(self.lesson.check, ManualCheck):
            log.write("[dim]No hint for reading lessons.[/dim]")
            return
        log.write(f"[blue]Hint: {self.lesson.hint or 'No hint.'}[/blue]")

    def _mark_complete(self) -> None:
        p = load_progress()
        if self.lesson.id not in p.completed_lessons:
            p.completed_lessons.append(self.lesson.id)
        save_progress(p)
