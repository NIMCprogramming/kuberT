import os
from pathlib import Path

from kubert.models import UserProgress


def _file() -> Path:
    base = os.getenv("KUBERT_STATE_DIR")
    return (Path(base) if base else Path.home() / ".kubert") / "progress.json"


def load_progress() -> UserProgress:
    f = _file()
    return UserProgress.model_validate_json(f.read_text()) if f.exists() else UserProgress()


def save_progress(progress: UserProgress) -> None:
    f = _file()
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(progress.model_dump_json(indent=2))
