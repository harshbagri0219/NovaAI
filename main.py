from brain.brain import Brain
from brain.context import remember
from memory.memory import load_memory, save_memory
from voice.speak import speak
from voice.listen import listen
from startup import startup
from utils.logger import write_log
from monitor.system_monitor import check_system
from ai.decision import decide
from brain.context_manager import ContextManager

brain = Brain()
context = ContextManager()
memory = load_memory()

startup()

while True:

    # Check phone status before waiting for a command
    alerts = check_system()

    for alert in alerts:
        speak(alert)

    user = listen()

    if user.lower() == "exit":

        speak("Goodbye!")

        write_log(user, "Goodbye!")

        remember(user, "Goodbye!")

        break

    elif user.lower().startswith("remember my name is "):

        name = user[len("remember my name is "):].strip()

        memory["owner"] = name

        save_memory(memory)

        response = f"I will remember your name is {name}."

        speak(response)

        write_log(user, response)

        remember(user, response)

    else:

        # ---------- Decision Engine ----------
        response = decide(user, memory)

        if response:

            speak(response)

            write_log(user, response)

            remember(user, response)

            continue

        # ---------- AI Brain ----------
        reply = brain.think(user)

        speak(reply)

        write_log(user, reply)

        remember(user, reply)