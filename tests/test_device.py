from system.device import get_device_info


def test_device_info():
    info = get_device_info()

    assert isinstance(info, dict)

    if "error" not in info:
        assert "brand" in info
        assert "model" in info
        assert "android" in info