from brain.context import last_conversation
from brain.personality import get_personality

from ai.llm_provider import OllamaProvider


def think(user):
    """
    Build conversational context for NOVA.

    This function intentionally has no access to:
    - ToolExecutor
    - ToolRegistry
    - ToolAdapter
    - ControlledRouter
    - ConfirmationManager
    - plugins
    """
    context = last_conversation()
    personality = get_personality()

    return {
        "user": user,
        "context": context,
        "personality": personality,
    }


def respond(user):
    """
    Generate a conversational response through the local LLM.

    The LLM receives only conversational information.
    It has no execution capabilities.
    """
    data = think(user)

    provider = OllamaProvider()

    return provider.generate(
        user=data["user"],
        context=data["context"],
        personality=data["personality"],
    )