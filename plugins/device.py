from system.device import get_device_info


def run():

    info = get_device_info()

    if "error" in info:
        return info["error"]

    return (
        f"Brand : {info['brand']}\n"
        f"Model : {info['model']}\n"
        f"Android : {info['android']}"
    )