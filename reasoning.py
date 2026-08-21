from brain.context_resolver import resolve_reference
from brain.followup import is_followup
from knowledge.profile import recall


def reason(user, topic=None):

    text = user.lower().strip()

    # --------------------------------
    # No topic available
    # --------------------------------
    if not topic:
        return None

    # --------------------------------
    # Follow-up about current topic
    # --------------------------------
    if is_followup(user):

        if "difficult" in text or "hard" in text:
            return (
                f"{topic} can be difficult at first, but the difficulty "
                f"depends on your experience and what you're trying to do."
            )

        if "speed" in text or "fast" in text or "faster" in text:
            return (
                f"When discussing the speed of {topic}, performance depends "
                f"on the workload, implementation, and environment."
            )

        if "easy" in text or "easier" in text:
            return (
                f"{topic} can be relatively easy to start with, depending "
                f"on your background and goal."
            )

        if "what about" in text or "tell me more" in text:
            return (
                f"We're still discussing {topic}. "
                f"What specifically would you like to know about it?"
            )

        if "it" in text or "that" in text:
            return (
                f"You're referring to {topic}. "
                f"What would you like to know about {topic}?"
            )

    # --------------------------------
    # Compare programming languages
    # --------------------------------
    if "which one is better for ai" in text:

        languages = recall("languages")

        if isinstance(languages, list) and languages:
            return (
                f"You previously mentioned {', '.join(languages)}. "
                "For AI development, Python is generally the strongest "
                "choice because of its extensive machine-learning and "
                "AI ecosystem."
            )

        return (
            "For AI development, Python is generally a strong choice "
            "because of its extensive machine-learning and AI ecosystem."
        )

    # --------------------------------
    # Basic comparison
    # --------------------------------
    if "which is better" in text:

        reference = resolve_reference(user)

        if reference:
            return (
                "I understand you're comparing something from your "
                f"previous conversation: {reference['previous_message']}."
            )

    return None