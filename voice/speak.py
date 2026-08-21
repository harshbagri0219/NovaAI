import os
import platform
import subprocess

from config import VOICE_ENABLED


def speak(text):
    """
    Speak text using the appropriate TTS system for the current platform.

    Windows:
        Uses PowerShell System.Speech.

    Android/Termux:
        Uses termux-tts-speak.

    Other platforms:
        Falls back to text-only output.
    """

    print(f"Nova: {text}")

    if not VOICE_ENABLED:
        return

    system = platform.system().lower()

    try:
        # ---------------------------------
        # Windows
        # ---------------------------------
        if system == "windows":
            escaped_text = text.replace("'", "''")

            command = (
                "Add-Type -AssemblyName System.Speech; "
                "$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
                f"$speaker.Speak('{escaped_text}')"
            )

            subprocess.run(
                ["powershell", "-NoProfile", "-Command", command],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

        # ---------------------------------
        # Android / Termux
        # ---------------------------------
        elif os.path.exists("/data/data/com.termux/files/usr/bin/termux-tts-speak"):
            subprocess.run(
                ["termux-tts-speak", text],
                check=False,
            )

        # ---------------------------------
        # Linux / other systems
        # ---------------------------------
        else:
            print("[Voice] No supported TTS backend found.")

    except Exception as exc:
        print(f"[Voice] TTS error: {exc}")