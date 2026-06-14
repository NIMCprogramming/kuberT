from kubert.shell import COMMANDS

EXPECTED = ["init", "next", "list", "lesson", "status", "reset", "help"]


def test_expected_shell_commands_present() -> None:
    for name in EXPECTED:
        assert name in COMMANDS, f"missing shell command: {name}"


def test_each_command_has_callable_and_description() -> None:
    for name, (fn, desc) in COMMANDS.items():
        assert callable(fn), f"command {name} fn not callable"
        assert isinstance(desc, str) and desc, f"command {name} missing description"
