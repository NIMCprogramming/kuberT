from kubert.models import Lesson, ManualCheck, MissedConcept, Question
from kubert.quiz_screen import QuizScreen
from kubert.state import load_progress, record_missed_concept


def _lesson() -> Lesson:
    return Lesson(
        id="m/x",
        title="t",
        module="m",
        order=1,
        intro="i",
        task="t",
        check=ManualCheck(type="manual"),
    )


def _q(concept: str = "pods") -> Question:
    return Question(prompt="What is a Pod?", answer="Smallest unit", concept=concept)


def test_quiz_screen_holds_questions() -> None:
    lesson = _lesson()
    qs = [_q(), _q("labels")]
    screen = QuizScreen(lesson, qs, "Warm-up")
    assert screen.lesson is lesson
    assert screen.questions == qs
    assert screen.index == 0
    assert screen.revealed is False
    assert screen.title_text == "Warm-up"


def test_quiz_screen_bindings_are_keyboard_only() -> None:
    screen = QuizScreen(_lesson(), [_q()], "Warm-up")
    keys = [b.key for b in screen.BINDINGS]
    assert {"space", "enter", "y", "n", "escape"}.issubset(set(keys))


def test_record_missed_concept_new(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("KUBERT_STATE_DIR", str(tmp_path))
    progress = load_progress()
    record_missed_concept(progress, "pods", "04-running-apps/01-pods")
    reloaded = load_progress()
    assert reloaded.missed_concepts == [
        MissedConcept(concept="pods", lesson_id="04-running-apps/01-pods", count=1),
    ]


def test_record_missed_concept_increments(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("KUBERT_STATE_DIR", str(tmp_path))
    progress = load_progress()
    record_missed_concept(progress, "labels", "l/x")
    record_missed_concept(progress, "labels", "l/x")
    record_missed_concept(progress, "labels", "l/x")
    reloaded = load_progress()
    assert len(reloaded.missed_concepts) == 1
    assert reloaded.missed_concepts[0].count == 3


def test_record_missed_concept_ignores_empty(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("KUBERT_STATE_DIR", str(tmp_path))
    progress = load_progress()
    record_missed_concept(progress, "", "l/x")
    reloaded = load_progress()
    assert reloaded.missed_concepts == []
