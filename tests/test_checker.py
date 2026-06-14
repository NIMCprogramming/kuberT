import subprocess
from unittest.mock import patch

from kubert.checker import run_check
from kubert.models import CommandCheck, ManualCheck, MultipleCheck


def test_manual_check_always_passes() -> None:
    assert run_check(ManualCheck(type="manual")).passed is True


@patch("kubert.checker.subprocess.run")
def test_command_check_passes_when_output_contains_expected(mock_run) -> None:
    mock_run.return_value = subprocess.CompletedProcess(
        args=[], returncode=0, stdout="Running", stderr=""
    )
    result = run_check(CommandCheck(type="command", cmd="echo", expect="Running"))
    assert result.passed is True


@patch("kubert.checker.subprocess.run")
def test_command_check_fails_when_output_differs(mock_run) -> None:
    mock_run.return_value = subprocess.CompletedProcess(
        args=[], returncode=0, stdout="Pending", stderr=""
    )
    result = run_check(CommandCheck(type="command", cmd="echo", expect="Running"))
    assert result.passed is False
    assert "Running" in result.detail
    assert "Pending" in result.detail


@patch("kubert.checker.subprocess.run")
def test_command_check_timeout_returns_failure(mock_run) -> None:
    mock_run.side_effect = subprocess.TimeoutExpired(cmd="x", timeout=5)
    result = run_check(CommandCheck(type="command", cmd="sleep", expect="x"))
    assert result.passed is False
    assert "timed out" in result.detail


@patch("kubert.checker.subprocess.run")
def test_multiple_check_all_pass(mock_run) -> None:
    mock_run.return_value = subprocess.CompletedProcess(
        args=[], returncode=0, stdout="ok", stderr=""
    )
    check = MultipleCheck(
        type="multiple",
        checks=[
            CommandCheck(type="command", cmd="echo", expect="ok"),
            CommandCheck(type="command", cmd="echo", expect="ok"),
        ],
    )
    assert run_check(check).passed is True


@patch("kubert.checker.subprocess.run")
def test_multiple_check_stops_at_first_fail(mock_run) -> None:
    mock_run.return_value = subprocess.CompletedProcess(
        args=[], returncode=0, stdout="nope", stderr=""
    )
    check = MultipleCheck(
        type="multiple",
        checks=[CommandCheck(type="command", cmd="echo", expect="ok")],
    )
    assert run_check(check).passed is False
