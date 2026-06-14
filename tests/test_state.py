from kubert.models import UserProgress
from kubert.state import load_progress, save_progress


def test_load_returns_empty_when_no_file(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("KUBERT_STATE_DIR", str(tmp_path))
    assert load_progress().completed_lessons == []


def test_save_then_load(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("KUBERT_STATE_DIR", str(tmp_path))
    save_progress(UserProgress(completed_lessons=["a", "b"]))
    assert load_progress().completed_lessons == ["a", "b"]


def test_save_creates_directory(tmp_path, monkeypatch) -> None:
    nested = tmp_path / "nested" / "dir"
    monkeypatch.setenv("KUBERT_STATE_DIR", str(nested))
    save_progress(UserProgress(completed_lessons=["x"]))
    assert (nested / "progress.json").exists()
