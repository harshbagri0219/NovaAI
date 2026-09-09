from ai.planner import choose_action
from core.execution_service import ExecutionService, get_execution_service
from core.interfaces import ResultStatus, StructuredResult
from core.tool_catalog import get_registry
from knowledge.profile import recall


def handle_controlled_command(
    command,
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

    intent = choose_action(command)

    # -------------------------------------------------
    # Knowledge / profile responses
    # -------------------------------------------------

    if intent == "owner":
        owner = recall("owner")

        if owner:
            return f"I was created by {owner}."

        return "I don't know who created me yet."

    if intent == "favorite_language":
        language = recall("favorite_language")

        if language:
            return f"Your favourite language is {language}."

        return "I don't know your favourite language yet."

    if intent == "favorite_food":
        food = recall("favorite_food")

        if food:
            return f"Your favourite food is {food}."

        return "I don't know your favourite food yet."

    # -------------------------------------------------
    # Controlled tool lookup
    # -------------------------------------------------

    tool = registry.get(intent)

    if tool is None:
        return None

    if intent == "memory":
        context = memory
    else:
        context = None

    # -------------------------------------------------
    # Authorized execution
    # -------------------------------------------------

    result = service.execute(
        tool,
        context=context,
    )

    if result.status == ResultStatus.SUCCESS:

        if isinstance(result.payload, str):
            return result.payload

        return (
            str(result.payload)
            if result.payload is not None
            else None
        )

    if result.status == ResultStatus.CONFIRMATION_REQUIRED:
        return result

    if result.status == ResultStatus.ERROR:
        return result.error or "Tool execution failed."

    return None
