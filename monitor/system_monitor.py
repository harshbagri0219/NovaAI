from system.device import get_battery
from state.system_state import (
    last_battery_percentage,
    last_charging_status
)

import state.system_state as state


def check_system():

    battery = get_battery()

    messages = []

    if "error" in battery:
        return messages

    percentage = battery.get("percentage", 0)
    status = battery.get("status", "")

    if (
        percentage <= 20
        and state.last_battery_percentage != percentage
    ):
        messages.append(
            f"Warning! Battery is only {percentage}%."
        )

    if state.last_charging_status != status:

        if status.upper() == "CHARGING":
            messages.append("Charging started.")

        elif status.upper() == "DISCHARGING":
            messages.append("Charging stopped.")

    state.last_battery_percentage = percentage
    state.last_charging_status = status

    return messages