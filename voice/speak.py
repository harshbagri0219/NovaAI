import os

def speak(text):
    print(f"Nova: {text}")
    os.system(f'termux-tts-speak "{text}"')