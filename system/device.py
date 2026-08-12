import subprocess
import json
import shutil


def get_battery():
    try:
        output = subprocess.check_output(
            ["termux-battery-status"],
            text=True
        )
        return json.loads(output)

    except Exception as e:
        return {"error": str(e)}


def get_device_info():
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
    total, used, free = shutil.disk_usage("/data/data/com.termux/files/home")

    return {
        "total": round(total / (1024 ** 3), 2),
        "used": round(used / (1024 ** 3), 2),
        "free": round(free / (1024 ** 3), 2),
        "percent": round((used / total) * 100, 2)
    }