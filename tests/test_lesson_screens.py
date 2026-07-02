from kubert.lesson_screens import LessonItem, LessonPickerScreen, LessonScreen
from kubert.models import Lesson, ManualCheck


def _make_lesson() -> Lesson:
    return Lesson(
        id="x/y",
        title="t",
        module="m",
        order=1,
        intro="hi",
        task="do it",
        check=ManualCheck(type="manual"),
    )


def test_lesson_screen_holds_lesson() -> None:
    lesson = _make_lesson()
    screen = LessonScreen(lesson)
    assert screen.lesson is lesson


def test_lesson_picker_screen_can_be_instantiated() -> None:
    screen = LessonPickerScreen()
    assert screen is not None


def test_lesson_item_stores_lesson() -> None:
    lesson = _make_lesson()
    item = LessonItem(lesson, "[x]")
    assert item.lesson is lesson


def test_lesson_screen_check_req_no_requirements() -> None:
    lesson = _make_lesson()
    screen = LessonScreen(lesson)
    ok, _ = screen._check_req()
    assert ok is True


def test_lesson_screen_has_next_binding() -> None:
    keys = [b.key for b in LessonScreen.BINDINGS]
    assert "n" in keys


def test_lesson_screen_no_copy_binding() -> None:
    keys = [b.key for b in LessonScreen.BINDINGS]
    assert "y" not in keys
