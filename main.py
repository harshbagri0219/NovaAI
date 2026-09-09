from brain.context import remember
from memory.memory import load_memory, save_memory
from voice.speak import speak
from voice.listen import listen
from startup import startup
from utils.logger import write_log
from monitor.system_monitor import check_system
from ai.decision import decide
from core.execution_service import get_execution_service
from core.tool_catalog import get_registry
from core.interfaces import ResultStatus, StructuredResult


if __name__ == "__main__":
    memory = load_memory()
    startup()
    registry = get_registry()
    execution_service = get_execution_service()

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
            response = decide(
                user,
                memory,
                registry=registry,
                execution_service=execution_service,
            )

            if isinstance(response, StructuredResult):

                # ---------- Human Confirmation ----------
                if response.status == ResultStatus.CONFIRMATION_REQUIRED:
                    request = response.confirmation_request

                    if request is not None:
                        speak(
                            f"{response.error or 'Confirmation required'} "
                            "Do you want to proceed?"
                        )

                        answer = listen()

                        if answer and answer.lower().strip() in (
                            "yes",
                            "y",
                            "yeah",
                            "yep",
                            "sure",
                            "ok",
                            "approve",
                        ):
                            executed = execution_service.execute_approved(
                                request.request_id,
                                registry=registry,
                            )

                            if executed.status == ResultStatus.SUCCESS:
                                response = (
                                    executed.payload
                                    if isinstance(executed.payload, str)
                                    else str(executed.payload)
                                    if executed.payload is not None
                                    else "Done."
                                )
                            else:
                                response = (
                                    executed.error
                                    or "Execution failed."
                                )

                        else:
                            response = "Action cancelled."

                    else:
                        speak(
                            response.error
                            or "Confirmation required."
                        )
                        response = (
                            response.error
                            or "Confirmation required."
                        )

                    write_log(user, response)
                    remember(user, response)
                    continue

                # ---------- Tool Error ----------
                if response.status == ResultStatus.ERROR:
                    error_message = (
                        response.error
                        or "Tool execution failed."
                    )

                    speak(error_message)
                    write_log(user, error_message)
                    remember(user, error_message)
                    continue

            # ---------- Normal Response ----------
            if not response:
                response = "I am still learning."

            speak(response)
            write_log(user, response)
            remember(user, response)