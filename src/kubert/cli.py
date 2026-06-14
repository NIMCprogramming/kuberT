import typer
from dotenv import load_dotenv

from kubert import bootstrap, cluster
from kubert.lesson import discover_lessons, get_default_lessons_root
from kubert.runner import run_lesson
from kubert.state import load_progress
from kubert.ui import console, show_failure, show_info, show_success

load_dotenv()

app = typer.Typer(help="kuberT - learn Kubernetes in your terminal.", no_args_is_help=True)


@app.command()
def shell() -> None:
    """Open the interactive kuberT app (full-screen, recommended)."""
    from kubert.app import run

    run()


@app.command()
def init() -> None:
    """Check tools and create a local cluster."""
    if not bootstrap.init_cluster():
        raise typer.Exit(code=1)


@app.command(name="list")
def list_lessons() -> None:
    """List all lessons."""
    progress = load_progress()
    for lesson in discover_lessons(get_default_lessons_root()):
        mark = "[green][x][/green]" if lesson.id in progress.completed_lessons else "[dim][ ][/dim]"
        console.print(f"{mark} {lesson.id} - {lesson.title}")


@app.command(name="next")
def next_lesson() -> None:
    """Run the next unfinished lesson."""
    progress = load_progress()
    for lesson in discover_lessons(get_default_lessons_root()):
        if lesson.id not in progress.completed_lessons:
            run_lesson(lesson, progress)
            return
    show_success("All lessons complete. Well done!")


@app.command()
def lesson(lesson_id: str) -> None:
    """Run a specific lesson by id."""
    progress = load_progress()
    for entry in discover_lessons(get_default_lessons_root()):
        if entry.id == lesson_id:
            run_lesson(entry, progress)
            return
    show_failure(f"No lesson with id '{lesson_id}'.")
    raise typer.Exit(code=1)


@app.command()
def reset() -> None:
    """Delete the Kind cluster."""
    if not cluster.exists():
        show_info("No cluster to delete.")
        return
    cluster.delete()
    show_success("Cluster deleted.")
