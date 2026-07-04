from textual import events
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import Footer, Header, Label, ListItem, ListView, Markdown, RichLog, Static

from kubert import clipboard, cluster
from kubert.checker import run_check
from kubert.lesson import discover_lessons, get_default_lessons_root
from kubert.models import Lesson, ManualCheck, Question
from kubert.quiz_screen import QuizScreen
from kubert.state import load_progress, save_progress


class LessonItem(ListItem):
    def __init__(self, lesson: Lesson, marker: str) -> None:
        super().__init__(Label(f"{marker} {lesson.id} - {lesson.title}", markup=False))
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
        Binding("w",      "do_warmup",      "Warm-up quiz"),
        Binding("r",      "do_review",      "Review quiz"),
        Binding("n",      "do_next",        "Next lesson"),
        Binding("s",      "app.pop_screen", "Skip"),
    ]
    CSS = """
    LessonScreen { layout: vertical; }
    #lesson-title { padding: 0 2; margin: 1 2 0 2; color: $accent; }
    #learning-goal { padding: 0 2; margin: 0 2 1 2; color: $primary; }
    #intro   { padding: 0 2; margin: 1 2 0 2; }
    #task    { border: round $warning; padding: 1 2; margin: 1 2; }
    #extras  { padding: 0 2; margin: 0 2 1 2; }
    #output  { border: round $primary; padding: 0 1; margin: 0 2 1 2; height: 10; }
    """

    def __init__(self, lesson: Lesson) -> None:
        super().__init__()
        self.lesson = lesson

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(
            f"[b]{self.lesson.id}[/b] — {self.lesson.title}",
            id="lesson-title",
        )
        if self.lesson.learning_goal:
            yield Static(f"[b]Goal:[/b] {self.lesson.learning_goal}", id="learning-goal")
        with VerticalScroll():
            yield Markdown(self.lesson.intro, id="intro")
            if not isinstance(self.lesson.check, ManualCheck):
                yield Markdown(self.lesson.task, id="task")
            extras = self._build_extras()
            if extras:
                yield Markdown(extras, id="extras")
        yield RichLog(id="output", markup=True)
        yield Footer()

    def _build_extras(self) -> str:
        parts: list[str] = []
        if self.lesson.prerequisites:
            parts.append(
                "## Builds on\n" + ", ".join(f"`{p}`" for p in self.lesson.prerequisites)
            )
        if self.lesson.warm_up:
            parts.append("## Warm-up recall\nPress **w** to start the warm-up quiz.")
        if self.lesson.troubleshooting:
            ts = self.lesson.troubleshooting
            parts.append(
                f"## Troubleshooting scenario\n{ts.scenario}\n\n"
                f"**Question:** {ts.question}\n\n"
                f"<details>\n\n**Diagnosis:** {ts.diagnosis}\n\n</details>"
            )
        if self.lesson.review_questions:
            parts.append("## Review\nPress **r** to start the review quiz.")
        if self.lesson.common_mistakes:
            lines = ["## Common mistakes"]
            for m in self.lesson.common_mistakes:
                lines.append(f"- **{m.mistake}** — {m.fix}")
            parts.append("\n".join(lines))
        if self.lesson.summary:
            parts.append(f"## Mini summary\n{self.lesson.summary}")
        return "\n\n".join(parts)

    def on_mount(self) -> None:
        ok, msg = self._check_req()
        log = self.query_one("#output", RichLog)
        if not ok:
            log.write(f"[red]{msg}[/red]")
        else:
            if isinstance(self.lesson.check, ManualCheck):
                tip = "[b]c[/b] read  [b]w[/b] warm-up  [b]r[/b] review  [b]n[/b] next"
            else:
                tip = (
                    "[b]c[/b] check  [b]h[/b] hint  [b]w[/b] warm-up  "
                    "[b]r[/b] review  [b]n[/b] next  [b]s[/b] skip"
                )
            log.write(f"[dim]{tip}[/dim]")
            log.write("[dim]Drag the mouse to select text — it's copied to the clipboard on release.[/dim]")

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
        log = self.query_one("#output", RichLog)
        if isinstance(self.lesson.check, ManualCheck):
            self._mark_complete()
            log.write("[green]Marked as read.[/green]")
            log.write("[dim]Press [b]n[/b] for the next lesson, or [b]Esc[/b] to go back.[/dim]")
            self.app.notify("Lesson complete! Press n for next.", severity="information")
            return
        ok, msg = self._check_req()
        if not ok:
            log.write(f"[red]{msg}[/red]")
            return
        result = run_check(self.lesson.check)
        if result.passed:
            log.write(f"[green]OK: {result.detail}[/green]")
            log.write("[dim]Press [b]n[/b] for the next lesson.[/dim]")
            self._mark_complete()
            self.app.notify("Lesson complete! Press n for next.", severity="information")
        else:
            log.write(f"[red]FAIL: {result.detail}[/red]")

    def action_do_hint(self) -> None:
        log = self.query_one("#output", RichLog)
        if isinstance(self.lesson.check, ManualCheck):
            log.write("[dim]No hint for reading lessons.[/dim]")
            return
        log.write(f"[blue]Hint: {self.lesson.hint or 'No hint.'}[/blue]")

    def action_do_warmup(self) -> None:
        self._push_quiz(self.lesson.warm_up, "Warm-up quiz")

    def action_do_review(self) -> None:
        self._push_quiz(self.lesson.review_questions, "Review quiz")

    def _push_quiz(self, questions: list[Question], title: str) -> None:
        if not questions:
            self.app.notify("No questions for this lesson yet.", severity="information")
            return
        self.app.push_screen(QuizScreen(self.lesson, questions, title))

    def on_mouse_up(self, event: events.MouseUp) -> None:
        self.call_after_refresh(self._copy_selection)

    def _copy_selection(self) -> None:
        text = self.get_selected_text()
        if not text:
            return
        tool = clipboard.copy(text)
        if tool is None:
            self.app.copy_to_clipboard(text)
        n = len(text)
        self.app.notify(f"Copied {n} character{'s' if n != 1 else ''}.", severity="information")

    def action_do_next(self) -> None:
        progress = load_progress()
        for lesson in discover_lessons(get_default_lessons_root()):
            if lesson.id == self.lesson.id:
                continue
            if lesson.id not in progress.completed_lessons:
                self.app.pop_screen()
                self.app.push_screen(LessonScreen(lesson))
                return
        self.app.notify("No more unfinished lessons.", severity="information")

    def _mark_complete(self) -> None:
        p = load_progress()
        if self.lesson.id not in p.completed_lessons:
            p.completed_lessons.append(self.lesson.id)
        save_progress(p)
