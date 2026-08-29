from brain.context_resolver import resolve_reference
from brain.followup import detect_followup_intent
from knowledge.profile import recall


def reason(user, current_topic=None):
    """
    Generate a reasoning-based response.

    current_topic is supplied by Brain so follow-up questions
    can be answered in the context of the active topic.
    """

    if not isinstance(user, str):
        return None

    text = user.lower().strip()

    if not text:
        return None

    # --------------------------------
    # Follow-up intent
    # --------------------------------
    followup_intent = detect_followup_intent(user)

    if current_topic and followup_intent:

        topic = current_topic

        # -----------------------------
        # Performance
        # -----------------------------
        if followup_intent == "performance":
            return (
                f"You're asking about the speed and performance of {topic}. "
                f"{topic} can be evaluated based on execution speed, "
                "efficiency, workload, and the environment where it is used."
            )

        # -----------------------------
        # Learning
        # -----------------------------
        if followup_intent == "learning":
            return (
                f"{topic} can be learned step by step. "
                f"Start with the fundamentals of {topic}, practice small "
                "projects, and gradually move toward more advanced concepts."
            )

        # -----------------------------
        # Advantages
        # -----------------------------
        if followup_intent == "advantages":
            return (
                f"The main advantages of {topic} depend on how it is used. "
                f"Common strengths include productivity, useful tools and "
                "libraries, community support, and practical applications."
            )

        # -----------------------------
        # Disadvantages
        # -----------------------------
        if followup_intent == "disadvantages":
            return (
                f"The main disadvantages of {topic} depend on the use case. "
                f"Potential limitations can include performance, complexity, "
                "resource requirements, or a smaller ecosystem in some areas."
            )

        # -----------------------------
        # Use Cases
        # -----------------------------
        if followup_intent == "use_cases":
            return (
                f"{topic} can be used for many different tasks. "
                "Its practical applications depend on the ecosystem, tools, "
                "and the problem you are trying to solve."
            )

        # -----------------------------
        # Examples
        # -----------------------------
        if followup_intent == "examples":
            return (
                f"Some examples involving {topic} include automation, "
                "software development, scripting, and building practical "
                "applications."
            )

        # -----------------------------
        # Career
        # -----------------------------
        if followup_intent == "career":
            return (
                f"{topic} can be useful for a career depending on the field "
                "you want to enter. Job opportunities may include development, "
                "automation, data, testing, security, or related roles."
            )

        # -----------------------------
        # Cost
        # -----------------------------
        if followup_intent == "cost":
            return (
                f"The cost of using {topic} depends on the tools, services, "
                "hardware, and resources involved. The core technology may "
                "be free or open source, while some related services can cost money."
            )

        # -----------------------------
        # Security
        # -----------------------------
        if followup_intent == "security":
            return (
                f"Security for {topic} depends on how it is configured and "
                "used. Important areas include keeping dependencies updated, "
                "protecting sensitive data, validating input, and following "
                "secure development practices."
            )

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