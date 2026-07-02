import re

_FENCE = re.compile(r"```[^\n]*\n(.*?)```", re.DOTALL)


def extract_code_blocks(text: str) -> list[str]:
    """Return the contents of every fenced code block in the markdown text."""
    return [m.group(1).rstrip("\n") for m in _FENCE.finditer(text)]


def preview(block: str, width: int = 60) -> str:
    """One-line preview of a code block for a picker list."""
    first = block.strip().splitlines()[0] if block.strip() else "(empty)"
    return first if len(first) <= width else first[: width - 1] + "…"
