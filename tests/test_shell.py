from kubert import shell


def test_shell_run_is_callable() -> None:
    assert callable(shell.run)


def test_all_expected_actions_present() -> None:
    for name in ["next", "pick", "init", "status", "reset"]:
        assert name in shell.ACTIONS, f"missing action: {name}"
