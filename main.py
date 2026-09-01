from brain.context import remember
from memory.memory import load_memory, save_memory
from voice.speak import speak
from voice.listen import listen
from startup import startup
from utils.logger import write_log
from monitor.system_monitor import check_system
from ai.decision import decide
from core.interfaces import ResultStatus, StructuredResult


if __name__ == "__main__":

    memory = load_memory()

    startup()

    while True:

        # ---------- System Monitoring ----------
        alerts = check_system()

        for alert in alerts:
            speak(alert)

        # ---------- Listen ----------
        user = listen()

        # ---------- Exit ----------
        if user.lower() == "exit":

            speak("Goodbye!")

            write_log(user, "Goodbye!")

            remember(user, "Goodbye!")

            break

        # ---------- Remember Owner ----------
        elif user.lower().startswith("remember my name is "):

            name = user[len("remember my name is "):].strip()

            memory["owner"] = name

            save_memory(memory)

            response = f"I will remember your name is {name}."

            speak(response)

            write_log(user, response)

            remember(user, response)

        # ---------- Central Decision Engine ----------
        else:

            response = decide(user, memory)

            if isinstance(response, StructuredResult):

                if response.status == ResultStatus.CONFIRMATION_REQUIRED:

                    speak(response.error or "Confirmation required.")

                    write_log(user, response.error or "Confirmation required.")

                    remember(user, response.error or "Confirmation required.")

                    continue

                if response.status == ResultStatus.ERROR:

                    speak(response.error or "Tool execution failed.")

                    write_log(user, response.error or "Tool execution failed.")

                    remember(user, response.error or "Tool execution failed.")

                    continue

            if not response:
                response = "I am still learning."

            speak(response)

            write_log(user, response)

            remember(user, response)