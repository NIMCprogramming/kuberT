from unittest.mock import MagicMock, patch

from kubert.cluster_screens import InitScreen, ResetConfirmScreen, _stream


def test_init_screen_can_be_instantiated() -> None:
    assert InitScreen() is not None


def test_reset_confirm_screen_can_be_instantiated() -> None:
    assert ResetConfirmScreen() is not None


@patch("kubert.cluster_screens.subprocess.Popen")
def test_stream_returns_exit_code(mock_popen) -> None:
    mock_proc = MagicMock()
    mock_proc.stdout = iter(["line1\n", "line2\n"])
    mock_proc.wait.return_value = 0
    mock_popen.return_value = mock_proc

    output: list[str] = []
    code = _stream(["echo"], output.append)

    assert code == 0
    assert output == ["line1", "line2"]


@patch("kubert.cluster_screens.subprocess.Popen", side_effect=FileNotFoundError)
def test_stream_handles_missing_command(_mock_popen) -> None:
    output: list[str] = []
    code = _stream(["nope"], output.append)
    assert code == 127
    assert any("not found" in line.lower() for line in output)


@patch("kubert.cluster_screens.subprocess.Popen")
def test_stream_returns_nonzero_on_failure(mock_popen) -> None:
    mock_proc = MagicMock()
    mock_proc.stdout = iter([])
    mock_proc.wait.return_value = 1
    mock_popen.return_value = mock_proc

    code = _stream(["false"], lambda _line: None)
    assert code == 1
