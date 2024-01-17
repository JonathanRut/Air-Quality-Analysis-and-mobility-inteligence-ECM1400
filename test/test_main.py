import pytest
import main


def test_about():
    result = main.about()
    assert result is None


def test_quit():
    with pytest.raises(SystemExit):
        main.quit()
