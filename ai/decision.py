from ai.learning import learn
from ai.task_coordinator import coordinate
from ai.result_analyzer import analyze_results
from brain.brain import Brain
from core.controlled_router import handle_controlled_command
from core.execution_service import ExecutionService, get_execution_service
from core.tool_catalog import get_registry
from core.interfaces import StructuredResult


brain = Brain()


def decide(
    user,
    memory,
    registry=None,
    executor=None,
    execution_service=None,
):
    registry = registry or get_registry()

    # -------------------------------------------------
    # Execution service selection
    # -------------------------------------------------
    #
    # executor= is retained only as a compatibility seam
    # for existing tests. Normal production execution
    # uses the single runtime ExecutionService.
    #
    if execution_service is not None:
        service = execution_service
    elif executor is not None:
        service = ExecutionService(executor=executor)
    else:
        service = get_execution_service()

    # -------------------------------------------------
    # Learning Engine
    # -------------------------------------------------

    learned = learn(user)

    if learned:
        return learned

    # -------------------------------------------------
    # Task Coordinator
    # -------------------------------------------------

    task_result = coordinate(user, memory)

    if task_result:

        response = analyze_results(task_result["results"])

        if response:
            return response

    # -------------------------------------------------
    # Controlled Plugin Router
    # -------------------------------------------------

    response = handle_controlled_command(
        user,
        memory,
        registry=registry,
        execution_service=service,
    )

    if isinstance(response, StructuredResult):
        return response

    if response:
        return response

    # -------------------------------------------------
    # AI Brain
    # -------------------------------------------------

    response = brain.think(user)

    if response:
        return response

    return "I am still learning."
