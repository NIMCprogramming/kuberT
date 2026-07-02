import shutil
import subprocess


_TOOLS: list[tuple[str, list[str]]] = [
    ("wl-copy", ["wl-copy"]),
    ("xclip",   ["xclip", "-selection", "clipboard"]),
    ("xsel",    ["xsel", "--clipboard", "--input"]),
]


def copy(text: str) -> str | None:
    """Copy text to the system clipboard. Return the tool name used, or None."""
    for name, cmd in _TOOLS:
        if shutil.which(cmd[0]) is None:
            continue
        try:
            subprocess.run(cmd, input=text, text=True, check=True, timeout=3)
            return name
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            continue
    return None
