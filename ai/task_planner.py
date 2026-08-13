def create_plan(user):

    text = user.lower().strip()

    # -----------------------------
    # Multi-step device request
    # -----------------------------
    if "battery" in text and "storage" in text:

        return [
            {
                "task": "battery",
                "description": "Check the current battery status."
            },
            {
                "task": "storage",
                "description": "Check available device storage."
            },
            {
                "task": "analyze",
                "description": "Analyze the battery and storage results."
            }
        ]

    # -----------------------------
    # Battery request
    # -----------------------------
    if "battery" in text:

        return [
            {
                "task": "battery",
                "description": "Check the current battery status."
            }
        ]

    # -----------------------------
    # Storage request
    # -----------------------------
    if "storage" in text:

        return [
            {
                "task": "storage",
                "description": "Check available device storage."
            }
        ]

    # -----------------------------
    # No multi-step plan
    # -----------------------------
    return None
