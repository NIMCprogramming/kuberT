from kubert.lesson_screens import LessonScreen
from kubert.models import (
    CommandCheck,
    Lesson,
    ManualCheck,
    Mistake,
    Question,
    SpacedHook,
    Troubleshooting,
)


def _lesson_with_reviews() -> Lesson:
    return Lesson(
        id="04-running-apps/01-pods",
        title="Pods",
        module="running-apps",
        order=1,
        intro="Pods intro.",
        task="Do it.",
        check=CommandCheck(type="command", cmd="true", expect=""),
        learning_goal="Build a Pod from YAML and inspect it.",
        prerequisites=["kubectl", "containers"],
        warm_up=[
            Question(
                prompt="What is a container?",
                answer="A running image.",
                concept="containers",
            ),
        ],
        troubleshooting=Troubleshooting(
            scenario="Pod stays in Pending.",
            question="Why?",
            diagnosis="Image tag is wrong.",
            concept="images",
        ),
        review_questions=[
            Question(
                prompt="Pick the right one.",
                answer="B",
                kind="multiple_choice",
                options=["A", "B", "C"],
                concept="pods",
            ),
        ],
        common_mistakes=[Mistake(mistake="Forgot label.", fix="Add metadata.labels.")],
        summary="A Pod is the smallest unit.",
        spaced_hooks=[SpacedHook(concept="pods", when="next")],
    )


def test_lesson_accepts_all_new_fields() -> None:
    lesson = _lesson_with_reviews()
    assert lesson.learning_goal.startswith("Build")
    assert lesson.prerequisites == ["kubectl", "containers"]
    assert len(lesson.warm_up) == 1
    assert lesson.troubleshooting is not None
    assert lesson.troubleshooting.concept == "images"
    assert lesson.review_questions[0].kind == "multiple_choice"
    assert lesson.common_mistakes[0].fix.startswith("Add")
    assert lesson.summary
    assert lesson.spaced_hooks[0].when == "next"


def test_lesson_defaults_are_empty() -> None:
    minimal = Lesson(
        id="x/y",
        title="t",
        module="m",
        order=1,
        intro="i",
        task="t",
        check=ManualCheck(type="manual"),
    )
    assert minimal.learning_goal == ""
    assert minimal.prerequisites == []
    assert minimal.warm_up == []
    assert minimal.troubleshooting is None
    assert minimal.review_questions == []
    assert minimal.common_mistakes == []
    assert minimal.summary == ""
    assert minimal.spaced_hooks == []


def test_lesson_screen_extras_contains_all_sections() -> None:
    lesson = _lesson_with_reviews()
    screen = LessonScreen(lesson)
    extras = screen._build_extras()
    assert "Builds on" in extras
    assert "Warm-up recall" in extras
    assert "Troubleshooting scenario" in extras
    assert "Review" in extras
    assert "Common mistakes" in extras
    assert "Mini summary" in extras


def test_lesson_screen_extras_empty_for_minimal_lesson() -> None:
    lesson = Lesson(
        id="x/y",
        title="t",
        module="m",
        order=1,
        intro="i",
        task="t",
        check=ManualCheck(type="manual"),
    )
    screen = LessonScreen(lesson)
    assert screen._build_extras() == ""


def test_lesson_screen_has_warmup_and_review_bindings() -> None:
    keys = [b.key for b in LessonScreen.BINDINGS]
    assert "w" in keys
    assert "r" in keys
