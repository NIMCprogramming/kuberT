from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import Footer, Header, Markdown, Static

from kubert.models import Lesson, Question
from kubert.state import load_progress, record_missed_concept


class QuizScreen(Screen[None]):
    BINDINGS = [
        Binding("space", "reveal_or_next", "Reveal / Next"),
        Binding("enter", "reveal_or_next", "Reveal / Next"),
        Binding("y",     "mark_known",     "I knew it"),
        Binding("n",     "mark_missed",    "I missed it"),
        Binding("escape", "app.pop_screen", "Exit quiz"),
    ]
    CSS = """
    QuizScreen { layout: vertical; }
    #quiz-title  { padding: 0 2; margin: 1 2 0 2; color: $accent; }
    #quiz-progress { padding: 0 2; margin: 0 2; color: $primary; }
    #quiz-prompt { padding: 1 2; margin: 1 2; border: round $warning; }
    #quiz-answer { padding: 1 2; margin: 0 2 1 2; border: round $success; }
    #quiz-hint   { padding: 0 2; color: $primary; }
    """

    def __init__(self, lesson: Lesson, questions: list[Question], title: str) -> None:
        super().__init__()
        self.lesson = lesson
        self.questions = questions
        self.title_text = title
        self.index = 0
        self.revealed = False

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(f"[b]{self.title_text}[/b] — lesson {self.lesson.id}", id="quiz-title")
        yield Static("", id="quiz-progress")
        with VerticalScroll():
            yield Markdown("", id="quiz-prompt")
            yield Markdown("", id="quiz-answer")
        yield Static(
            "Press [b]Space[/b] to reveal, then [b]y[/b]/[b]n[/b]. [b]Esc[/b] to leave.",
            id="quiz-hint",
        )
        yield Footer()

    def on_mount(self) -> None:
        if not self.questions:
            self.app.notify("No questions to show.", severity="warning")
            self.app.pop_screen()
            return
        self._refresh_view()

    def _current(self) -> Question:
        return self.questions[self.index]

    def _refresh_view(self) -> None:
        q = self._current()
        self.query_one("#quiz-progress", Static).update(
            f"Question {self.index + 1} of {len(self.questions)} — [dim]{q.kind}[/dim]"
        )
        body = q.prompt
        if q.kind == "multiple_choice" and q.options:
            body += "\n\n" + "\n".join(f"- {opt}" for opt in q.options)
        self.query_one("#quiz-prompt", Markdown).update(body)
        answer_md = self.query_one("#quiz-answer", Markdown)
        hint = self.query_one("#quiz-hint", Static)
        if self.revealed:
            answer_md.update(f"**Answer:** {q.answer}")
            hint.update("Did you get it? [b]y[/b] = yes, [b]n[/b] = no.")
        else:
            answer_md.update("")
            hint.update("Think first. Press [b]Space[/b] to reveal.")

    def action_reveal_or_next(self) -> None:
        if not self.revealed:
            self.revealed = True
            self._refresh_view()
        else:
            self._advance()

    def action_mark_known(self) -> None:
        if not self.revealed:
            return
        self._advance()

    def action_mark_missed(self) -> None:
        if not self.revealed:
            return
        q = self._current()
        if q.concept:
            progress = load_progress()
            record_missed_concept(progress, q.concept, self.lesson.id)
            self.app.notify(f"Logged missed concept: {q.concept}", severity="information")
        self._advance()

    def _advance(self) -> None:
        self.index += 1
        self.revealed = False
        if self.index >= len(self.questions):
            self.app.notify("Quiz done.", severity="information")
            self.app.pop_screen()
            return
        self._refresh_view()
