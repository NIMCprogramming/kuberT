import subprocess
from collections.abc import Callable

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen, Screen
from textual.widgets import Button, Footer, Header, Label, RichLog, Static
from textual import work

from kubert import cluster, prereq


class InitScreen(Screen[None]):
    BINDINGS = [Binding("escape", "app.pop_screen", "Back")]
    CSS = """
    Static { padding: 1 2; }
    RichLog { border: round $primary; padding: 0 1; margin: 0 2; height: 1fr; }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(
            "[b]Setting up the cluster...[/b]  ([yellow]Esc[/yellow] to return when done)"
        )
        yield RichLog(id="log", markup=True)
        yield Footer()

    def on_mount(self) -> None:
        self.do_init()

    @work(thread=True, exclusive=True)
    def do_init(self) -> None:
        log = self.query_one("#log", RichLog)

        def write(text: str) -> None:
            self.app.call_from_thread(log.write, text)

        write("[b]Checking prerequisites...[/b]")
        tools = prereq.check_all()
        all_ok = True
        for t in tools:
            if t.installed:
                write(f"[green]OK[/green] {t.name} found")
            else:
                write(f"[red]MISSING[/red] {t.name} - install: {t.install_url}")
                all_ok = False
        if not all_ok:
            write("\n[red]Cannot continue. Install missing tools and come back.[/red]")
            return

        if cluster.exists():
            write(f"\n[yellow]Cluster '{cluster.name()}' already exists.[/yellow]")
            write("[green]Done. Press Esc to return.[/green]")
            return

        write(f"\n[b]Pulling node image ({cluster.node_image()})...[/b]")
        code = _stream(["docker", "pull", cluster.node_image()], write)
        if code != 0:
            write(f"[red]docker pull failed (exit {code}).[/red]")
            return

        write(f"\n[b]Creating Kind cluster '{cluster.name()}'...[/b]")
        code = _stream(
            ["kind", "create", "cluster", "--name", cluster.name(),
             "--image", cluster.node_image()],
            write,
        )
        if code != 0:
            write(f"[red]kind create failed (exit {code}).[/red]")
            return

        write("\n[green]Cluster ready. Press Esc to return to the menu.[/green]")


def _stream(cmd: list[str], write: Callable[[str], None]) -> int:
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
    except FileNotFoundError:
        write(f"[red]Command not found: {cmd[0]}[/red]")
        return 127
    assert proc.stdout is not None
    for line in proc.stdout:
        write(line.rstrip())
    return proc.wait()


class ResetConfirmScreen(ModalScreen[None]):
    BINDINGS = [Binding("escape", "app.pop_screen", "Cancel")]
    CSS = """
    ResetConfirmScreen { align: center middle; }
    #box { width: 60; height: 11; border: round $error; padding: 1 2; background: $panel; }
    .buttons { dock: bottom; height: 3; align: center middle; }
    Button { margin: 0 1; }
    """

    def compose(self) -> ComposeResult:
        with Container(id="box"):
            yield Label(f"Delete cluster '{cluster.name()}'?\nThis cannot be undone.")
            with Horizontal(classes="buttons"):
                yield Button("Yes, delete", id="yes", variant="error")
                yield Button("Cancel", id="no", variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "yes":
            self._delete()
        else:
            self.app.pop_screen()

    def _delete(self) -> None:
        if not cluster.exists():
            self.app.notify("No cluster to delete.", severity="warning")
        else:
            try:
                cluster.delete()
                self.app.notify("Cluster deleted.", severity="information")
            except subprocess.CalledProcessError as e:
                self.app.notify(f"Delete failed: {e}", severity="error")
        self.app.pop_screen()
