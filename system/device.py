import json
import os
import shutil
import subprocess


def battery():
    """
    Get battery information.

    Works on Android/Termux.
    Returns an error dictionary when unavailable.
    """
    try:
        output = subprocess.check_output(
            ["termux-battery-status"],
            text=True
        )
        return json.loads(output)

    except Exception as e:
        return {"error": str(e)}


def get_battery():
    """
    Backward-compatible alias for battery().
    """
    return battery()


def get_device_info():
    """
    Get Android device information.

    Works on Android/Termux.
    Returns an error dictionary when unavailable.
    """
    try:
        model = subprocess.check_output(
            ["getprop", "ro.product.model"],
            text=True
        ).strip()

        brand = subprocess.check_output(
            ["getprop", "ro.product.brand"],
            text=True
        ).strip()

        android = subprocess.check_output(
            ["getprop", "ro.build.version.release"],
            text=True
        ).strip()

        return {
            "brand": brand,
            "model": model,
            "android": android
        }

    except Exception as e:
        return {"error": str(e)}


def get_storage():
    """
    Get storage information.

    Uses the Termux home directory on Android.
    Uses the current user's home directory on Windows/Linux.
    """

    if os.path.exists("/data/data/com.termux/files/home"):
        path = "/data/data/com.termux/files/home"
    else:
        path = os.path.expanduser("~")

    total, used, free = shutil.disk_usage(path)

    return {
        "total": round(total / (1024 ** 3), 2),
        "used": round(used / (1024 ** 3), 2),
        "free": round(free / (1024 ** 3), 2),
        "percent": round((used / total) * 100, 2)
    }