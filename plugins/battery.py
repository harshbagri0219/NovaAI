from system.device import get_battery

def run():

    battery = get_battery()

    if "error" in battery:
        return battery["error"]

    return f"Battery is {battery['percentage']} percent."