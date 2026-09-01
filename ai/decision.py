from ai.learning import learn
from ai.task_coordinator import coordinate
from ai.result_analyzer import analyze_results
from brain.brain import Brain
from core.controlled_router import handle_controlled_command
from core.tool_catalog import get_registry
from core.tool_executor import ToolExecutor
from core.interfaces import ResultStatus, StructuredResult


brain = Brain()

_registry = get_registry()
_executor = ToolExecutor()


def decide(user, memory, registry=None, executor=None):
    registry = registry or _registry
    executor = executor or _executor

    # -----------------------------
    # Learning Engine
    # -----------------------------
    learned = learn(user)

    if learned:
        return learned

    # -----------------------------
    # Task Coordinator
    # -----------------------------
    task_result = coordinate(user, memory)

    if task_result:

        response = analyze_results(task_result["results"])

        if response:
            return response

    # -----------------------------
    # Plugin Router
    # -----------------------------
    response = handle_controlled_command(
        user,
        memory,
        registry=registry,
        executor=executor,
    )

    if isinstance(response, StructuredResult):
        return response

    if response:
        return response

    # -----------------------------
    # AI Brain
    # -----------------------------
    response = brain.think(user)

    if response:
        return response

    return "I am still learning."
