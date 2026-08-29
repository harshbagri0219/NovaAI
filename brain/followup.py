def detect_followup_intent(user):
    """
    Detect the specific subject of a conversational follow-up.

    Returns:
        performance
        learning
        advantages
        disadvantages
        use_cases
        examples
        career
        cost
        security
        None
    """

    if not isinstance(user, str):
        return None

    text = user.lower().strip()

    if not text:
        return None

    # -----------------------------
    # Disadvantages
    # -----------------------------
    # Check this BEFORE "advantages"
    # because "disadvantages" contains
    # the word "advantages".
    disadvantage_words = [
        "disadvantages",
        "disadvantage",
        "drawbacks",
        "drawback",
        "cons",
        "weaknesses",
        "limitations",
    ]

    if any(word in text for word in disadvantage_words):
        return "disadvantages"

    # -----------------------------
    # Performance / Speed
    # -----------------------------
    performance_words = [
        "speed",
        "performance",
        "fast",
        "slow",
        "efficiency",
        "efficient",
    ]

    if any(word in text for word in performance_words):
        return "performance"

    # -----------------------------
    # Learning
    # -----------------------------
    learning_phrases = [
        "learn",
        "learning",
        "study",
        "how to learn",
        "how do i learn",
        "difficult to learn",
        "easy to learn",
    ]

    if any(phrase in text for phrase in learning_phrases):
        return "learning"

    # -----------------------------
    # Advantages
    # -----------------------------
    advantage_words = [
        "advantages",
        "advantage",
        "benefits",
        "benefit",
        "pros",
        "strengths",
    ]

    if any(word in text for word in advantage_words):
        return "advantages"

    # -----------------------------
    # Use Cases
    # -----------------------------
    use_case_phrases = [
        "uses",
        "use cases",
        "use case",
        "used for",
        "what can i use it for",
        "what is it used for",
    ]

    if any(phrase in text for phrase in use_case_phrases):
        return "use_cases"

    # -----------------------------
    # Examples
    # -----------------------------
    example_phrases = [
        "examples",
        "example",
        "show me an example",
        "show examples",
    ]

    if any(phrase in text for phrase in example_phrases):
        return "examples"

    # -----------------------------
    # Career
    # -----------------------------
    career_words = [
        "career",
        "careers",
        "jobs",
        "job",
        "employment",
        "salary",
        "salaries",
    ]

    if any(word in text for word in career_words):
        return "career"

    # -----------------------------
    # Cost
    # -----------------------------
    cost_words = [
        "cost",
        "price",
        "pricing",
        "expensive",
        "free",
    ]

    if any(word in text for word in cost_words):
        return "cost"

    # -----------------------------
    # Security
    # -----------------------------
    security_words = [
        "security",
        "secure",
        "safe",
        "vulnerability",
        "vulnerabilities",
    ]

    if any(word in text for word in security_words):
        return "security"

    return None


def detect_followup(user):
    """
    Detect the general category of a conversational follow-up.

    Returns:
        topic_followup
        reference
        continuation
        comparison
        None
    """

    if not isinstance(user, str):
        return None

    text = user.lower().strip()

    if not text:
        return None

    # -----------------------------
    # Comparison
    # -----------------------------
    comparison_phrases = [
        "which one",
        "which is better",
        "which one is better",
        "what is better",
        "which should i choose",
        "which should i use",
        "compare",
        "comparison",
    ]

    if any(phrase in text for phrase in comparison_phrases):
        return "comparison"

    # -----------------------------
    # Reference
    # -----------------------------
    reference_words = [
        "it",
        "that",
        "this",
        "they",
        "them",
    ]

    for word in reference_words:
        if (
            text == word
            or text.startswith(word + " ")
            or f" {word} " in text
            or text.endswith(" " + word + "?")
        ):
            return "reference"

    # -----------------------------
    # Topic Follow-up
    # -----------------------------
    topic_phrases = [
        "what about",
        "how about",
        "and its",
        "and their",
        "about its",
        "about their",
    ]

    if any(phrase in text for phrase in topic_phrases):
        return "topic_followup"

    # -----------------------------
    # Continuation
    # -----------------------------
    continuation_phrases = [
        "tell me more",
        "more about it",
        "more about that",
        "continue",
        "go on",
        "keep going",
        "what else",
        "anything else",
        "then",
        "next",
    ]

    if any(phrase in text for phrase in continuation_phrases):
        return "continuation"

    return None


def is_followup(user):
    """
    Return True when the message is a conversational follow-up.
    """

    return detect_followup(user) is not None