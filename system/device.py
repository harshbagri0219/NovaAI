import subprocess
import json

def get_battery():
    try:
        output = subprocess.check_output(
            ["termux-battery-status"],
            text=True
        )
        return json.loads(output)
    except Exception as e:
        return {"error": str(e)}