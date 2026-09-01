from typing import Any, Optional

from ai.planner import choose_action
from core.interfaces import Capability, ResultStatus, StructuredResult
from core.tool_catalog import get_registry
from core.tool_executor import ToolExecutor
from knowledge.profile import recall


_executor = None


def _get_executor():
    global _executor
    if _executor is None:
        _executor = ToolExecutor()
    return _executor


def handle_controlled_command(command, memory, registry=None, executor=None):
    registry = registry or get_registry()
    executor = executor or _get_executor()

    intent = choose_action(command)

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

    tool = registry.get(intent)
    if tool is None:
        return None

    if intent == "memory":
        context = memory
    else:
        context = None

    result = executor.execute(tool, context=context)

    if result.status == ResultStatus.SUCCESS:
        if isinstance(result.payload, str):
            return result.payload
        return str(result.payload) if result.payload is not None else None

    if result.status == ResultStatus.CONFIRMATION_REQUIRED:
        return result

    if result.status == ResultStatus.ERROR:
        return result.error or "Tool execution failed."

    return None
