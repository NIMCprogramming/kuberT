from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()


def show_title(text: str) -> None:
    console.print(Panel.fit(text, style="bold cyan"))


def show_intro(text: str) -> None:
    console.print(Markdown(text))


def show_task(text: str) -> None:
    console.print(Panel(Markdown(text), title="Task", border_style="yellow"))


def show_hint(text: str) -> None:
    console.print(Panel(text, title="Hint", border_style="blue"))


def show_success(text: str) -> None:
    console.print(f"[bold green][OK][/bold green] {text}")


def show_failure(text: str) -> None:
    console.print(f"[bold red][FAIL][/bold red] {text}")


def show_info(text: str) -> None:
    console.print(f"[cyan][i][/cyan] {text}")


def show_extras(text: str) -> None:
    if not text.strip():
        return
    console.print(Panel(Markdown(text), title="Recall / Review", border_style="magenta"))
