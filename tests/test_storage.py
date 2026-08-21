from system.device import get_storage


def test_storage():
    info = get_storage()

    assert isinstance(info, dict)
    assert "total" in info
    assert "used" in info
    assert "free" in info
    assert "percent" in info

    assert info["total"] >= 0
    assert info["used"] >= 0
    assert info["free"] >= 0
    assert 0 <= info["percent"] <= 100