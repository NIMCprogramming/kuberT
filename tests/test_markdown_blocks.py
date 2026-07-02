from kubert.markdown_blocks import extract_code_blocks, preview


def test_no_blocks() -> None:
    assert extract_code_blocks("just some text") == []


def test_one_block() -> None:
    text = "before\n```\nkubectl get pods\n```\nafter"
    assert extract_code_blocks(text) == ["kubectl get pods"]


def test_multiple_blocks_with_lang_tag() -> None:
    text = "```bash\nls -la\n```\n\n```yaml\napiVersion: v1\nkind: Pod\n```"
    assert extract_code_blocks(text) == ["ls -la", "apiVersion: v1\nkind: Pod"]


def test_preview_short() -> None:
    assert preview("hello") == "hello"


def test_preview_truncates() -> None:
    long = "x" * 80
    assert preview(long, width=10).endswith("…")
    assert len(preview(long, width=10)) == 10


def test_preview_first_line_only() -> None:
    assert preview("first line\nsecond line") == "first line"
