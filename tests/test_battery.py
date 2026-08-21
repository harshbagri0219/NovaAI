import pytest
from system.device import battery


def test_battery():
    info = battery()

    if "error" in info:
        pytest.skip("Battery API unavailable on this system")

    assert "percentage" in info
    assert isinstance(info["percentage"], (int, float))
    assert 0 <= info["percentage"] <= 100