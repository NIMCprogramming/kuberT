from kubert import app


def test_app_module_importable() -> None:
    assert callable(app.run)
    assert hasattr(app, "KubertApp")


def test_menu_has_expected_actions() -> None:
    keys = [key for key, _label in app.MENU]
    for expected in ("next", "pick", "init", "status", "reset", "quit"):
        assert expected in keys, f"missing menu action: {expected}"


def test_kubert_app_can_be_instantiated() -> None:
    instance = app.KubertApp()
    assert instance.TITLE == "kuberT"


def test_dispatch_unknown_action_is_noop() -> None:
    app._dispatch("nonexistent")
