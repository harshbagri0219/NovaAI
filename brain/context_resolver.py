import re

from brain.context import get_recent_context


def resolve_reference(user):
    """
    Resolve references such as:
    - it
    - that
    - which one

    Uses recent conversation history to identify what
    the user is referring to.
    """

    text = user.lower().strip()
    history = get_recent_context(5)

    # No previous conversation
    if not history:
        return None

    # -----------------------------
    # Normalize words
    # -----------------------------

    words = set(re.findall(r"\b[\w']+\b", text))

    reference = None

    # -----------------------------
    # Detect reference
    # -----------------------------

    if "which one" in text:
        reference = "which one"

    elif "it" in words:
        reference = "it"

    elif "that" in words:
        reference = "that"

    # No reference detected
    if not reference:
        return None

    # -----------------------------
    # Find previous user message
    # -----------------------------

    for item in reversed(history):

        previous_user = item.get("user", "").strip()

        if previous_user:
            return {
                "reference": reference,
                "previous_message": previous_user
            }

    return None