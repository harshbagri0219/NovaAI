from brain.context import get_recent_context


def resolve_reference(user):

    text = user.lower().strip()
    history = get_recent_context(5)

    # No previous conversation
    if not history:
        return None

    # Resolve "it"
    if "it" in text:

        for item in reversed(history):

            previous_user = item.get("user", "").strip()

            if previous_user:
                return {
                    "reference": "it",
                    "previous_message": previous_user
                }

    # Resolve "that"
    if "that" in text:

        for item in reversed(history):

            previous_user = item.get("user", "").strip()

            if previous_user:
                return {
                    "reference": "that",
                    "previous_message": previous_user
                }

    # Resolve "which one"
    if "which one" in text:

        for item in reversed(history):

            previous_user = item.get("user", "").strip()

            if previous_user:
                return {
                    "reference": "which one",
                    "previous_message": previous_user
                }

    return None
