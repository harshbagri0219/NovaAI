from ai.task_planner import create_plan
from ai.task_executor import execute_plan


def coordinate(user, memory):

    plan = create_plan(user)

    if not plan:
        return None

    results = execute_plan(plan, memory)

    return {
        "plan": plan,
        "results": results
    }
