from core.controlled_router import handle_controlled_command
from core.tool_catalog import get_registry
from core.tool_executor import ToolExecutor


_executor = ToolExecutor()


def execute_plan(plan, memory):

    results = []

    if not plan:
        return results

    registry = get_registry()

    for task in plan:

        task_name = task.get("task")

        # -----------------------------
        # Device task
        # -----------------------------
        if task_name == "battery":

            response = handle_controlled_command(
                "battery",
                memory,
                registry=registry,
                executor=_executor,
            )

            results.append({
                "task": task_name,
                "result": response
            })

        # -----------------------------
        # Storage task
        # -----------------------------
        elif task_name == "storage":

            response = handle_controlled_command(
                "storage",
                memory,
                registry=registry,
                executor=_executor,
            )

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
