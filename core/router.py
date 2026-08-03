from system.device import get_battery
from system.time_utils import current_time


def handle_command(command, memory):
    command = command.lower()

    if command == "battery":
        battery = get_battery()

        if "error" in battery:
            return battery["error"]

        return f"Battery is {battery['percentage']} percent."

    elif command == "time":
        return current_time()

    elif command == "what is my name":

        if "owner" in memory:
            return f"Your name is {memory['owner']}."

        return "I don't know your name yet."

    return None