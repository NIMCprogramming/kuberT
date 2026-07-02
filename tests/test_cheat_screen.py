from kubert.cheat_screen import CheatPanelScreen


def test_cheat_screen_can_be_instantiated() -> None:
    screen = CheatPanelScreen()
    assert screen is not None
