from brain.context_resolver import resolve_reference
from knowledge.profile import recall


def reason(user):

    text = user.lower().strip()

    # --------------------------------
    # Compare programming languages
    # --------------------------------
    if "which one is better for ai" in text:
        languages = recall("languages")

        if isinstance(languages, list) and languages:
            return (
                f"You previously mentioned {', '.join(languages)}. "
                "For AI development, Python is generally the strongest choice "
                "because of its extensive machine-learning and AI ecosystem."
            )

        reference = resolve_reference(user)

        if reference:
            return (
                "You're referring to the previous topic. "
                "For AI development, Python is generally a strong choice."
            )

    # --------------------------------
    # Basic comparison
    # --------------------------------
    if "which is better" in text:

        reference = resolve_reference(user)

        if reference:
            return (
                f"I understand you're comparing something from your previous "
                f"conversation: {reference['previous_message']}."
            )

    return None
