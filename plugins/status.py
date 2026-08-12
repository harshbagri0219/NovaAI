from system.device import get_battery
from system.time_utils import current_time
from config import VERSION


def run():

    battery = get_battery()

    if "error" in battery:
        battery_text = "Battery information unavailable."
    else:
        battery_text = (
            f"Battery: {battery['percentage']}% "
            f"({battery['status']})"
        )

    return (
        f"{battery_text}\n"
        f"Time: {current_time()}\n"
        f"Nova Version: {VERSION}"
    )