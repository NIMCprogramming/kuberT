from unittest.mock import patch

from kubert.models import Lesson, ManualCheck
from kubert.runner import _check_requirements


def _lesson(requires: list[str] | None = None) -> Lesson:
    return Lesson(
        id="t/x",
        title="t",
        module="m",
        order=1,
        intro="i",
        task="t",
        hint="",
        check=ManualCheck(type="manual"),
        requires=requires or [],  # type: ignore[arg-type]
    )


def test_no_requirements_passes() -> None:
    ok, _ = _check_requirements(_lesson())
    assert ok is True


@patch("kubert.runner.cluster.exists", return_value=False)
def test_cluster_required_but_missing(_mock_exists) -> None:
    ok, msg = _check_requirements(_lesson(requires=["cluster"]))
    assert ok is False
    assert "cluster" in msg.lower()


@patch("kubert.runner.cluster.exists", return_value=True)
@patch("kubert.runner.cluster.is_reachable", return_value=False)
def test_cluster_exists_but_unreachable(_mock_reachable, _mock_exists) -> None:
    ok, msg = _check_requirements(_lesson(requires=["cluster"]))
    assert ok is False
    assert "reach" in msg.lower()


@patch("kubert.runner.cluster.exists", return_value=True)
@patch("kubert.runner.cluster.is_reachable", return_value=True)
def test_cluster_ready(_mock_reachable, _mock_exists) -> None:
    ok, _ = _check_requirements(_lesson(requires=["cluster"]))
    assert ok is True
