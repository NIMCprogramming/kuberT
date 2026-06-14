from unittest.mock import patch

from kubert.prereq import check_all


@patch("kubert.prereq.shutil.which")
def test_all_installed_when_which_finds_everything(mock_which) -> None:
    mock_which.return_value = "/usr/bin/x"
    results = check_all()
    assert len(results) == 3
    assert all(r.installed for r in results)


@patch("kubert.prereq.shutil.which")
def test_none_installed_when_which_finds_nothing(mock_which) -> None:
    mock_which.return_value = None
    results = check_all()
    assert not any(r.installed for r in results)


@patch("kubert.prereq.shutil.which")
def test_results_carry_install_urls(mock_which) -> None:
    mock_which.return_value = None
    for r in check_all():
        assert r.install_url.startswith("https://")
