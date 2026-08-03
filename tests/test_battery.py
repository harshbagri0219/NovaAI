from system.device import battery
from voice.speak import speak

info = battery()

speak(f"Battery is {info['percentage']} percent.")