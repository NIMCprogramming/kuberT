import os
from pathlib import Path

from kubert.models import MissedConcept, UserProgress


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


def reset_progress() -> None:
    f = _file()
    if f.exists():
        f.unlink()


def record_missed_concept(progress: UserProgress, concept: str, lesson_id: str) -> None:
    if not concept:
        return
    for entry in progress.missed_concepts:
        if entry.concept == concept and entry.lesson_id == lesson_id:
            entry.count += 1
            save_progress(progress)
            return
    progress.missed_concepts.append(MissedConcept(concept=concept, lesson_id=lesson_id))
    save_progress(progress)
