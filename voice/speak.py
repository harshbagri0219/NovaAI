import os
from config import VOICE_ENABLED

def speak(text):

    print(f"Nova: {text}")

    if VOICE_ENABLED:
        os.system(f'termux-tts-speak "{text}"')