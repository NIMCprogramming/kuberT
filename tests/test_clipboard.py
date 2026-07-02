from unittest.mock import patch

from kubert import clipboard


def test_copy_uses_first_available_tool() -> None:
    with patch("kubert.clipboard.shutil.which", side_effect=lambda t: "/bin/" + t if t == "xclip" else None), \
         patch("kubert.clipboard.subprocess.run") as run:
        run.return_value = None
        assert clipboard.copy("hello") == "xclip"
        run.assert_called_once()
        assert run.call_args.kwargs["input"] == "hello"


def test_copy_returns_none_when_no_tool_available() -> None:
    with patch("kubert.clipboard.shutil.which", return_value=None):
        assert clipboard.copy("hello") is None
