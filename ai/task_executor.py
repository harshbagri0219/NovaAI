from core.controlled_router import handle_controlled_command
from core.execution_service import get_execution_service
from core.tool_catalog import get_registry


def execute_plan(plan, memory):
    results = []

    if not plan:
        return results

    registry = get_registry()
    service = get_execution_service()

    for task in plan:
        task_name = task.get("task")

        if task_name == "battery":
            response = handle_controlled_command(
                "battery",
                memory,
                registry=registry,
                execution_service=service,
            )
            results.append({
                "task": task_name,
                "result": response,
            })

        elif task_name == "storage":
            response = handle_controlled_command(
                "storage",
                memory,
                registry=registry,
                execution_service=service,
            )
            results.append({
                "task": task_name,
                "result": response,
            })

        elif task_name == "analyze":
            results.append({
                "task": task_name,
                "result": (
                    "Analysis will be performed after collecting "
                    "the required results."
                ),
            })

        else:
            results.append({
                "task": task_name,
                "result": "Task is not supported yet.",
            })

    return results