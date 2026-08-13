from core.router import handle_command


def execute_plan(plan, memory):

    results = []

    if not plan:
        return results

    for task in plan:

        task_name = task.get("task")

        # -----------------------------
        # Device task
        # -----------------------------
        if task_name == "battery":

            response = handle_command("battery", memory)

            results.append({
                "task": task_name,
                "result": response
            })

        # -----------------------------
        # Storage task
        # -----------------------------
        elif task_name == "storage":

            response = handle_command("storage", memory)

            results.append({
                "task": task_name,
                "result": response
            })

        # -----------------------------
        # Analysis task
        # -----------------------------
        elif task_name == "analyze":

            results.append({
                "task": task_name,
                "result": "Analysis will be performed after collecting the required results."
            })

        # -----------------------------
        # Unknown task
        # -----------------------------
        else:

            results.append({
                "task": task_name,
                "result": "Task is not supported yet."
            })

    return results
