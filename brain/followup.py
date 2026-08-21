import re


FOLLOWUP_PATTERNS = [
    r"^tell me more$",
    r"^more about (.+)$",
    r"^what about (.+)$",
    r"^what about (it|that)$",
    r"^is it (.+)$",
    r"^is that (.+)$",
    r"^how about (.+)$",
    r"^what are its (.+)$",
    r"^what is its (.+)$",
    r"^what are the (.+)$",
    r"^how does it (.+)$",
    r"^why is it (.+)$",
    r"^which one\??$",
]


def is_followup(user):
    """Return True when the message depends on previous context."""

    if not isinstance(user, str):
        return False

    text = user.lower().strip()

    if not text:
        return False

    for pattern in FOLLOWUP_PATTERNS:
        if re.search(pattern, text):
            return True

    return False


def extract_followup_question(user):
    """
    Extract the meaningful part of a follow-up question.

    Example:
        'What about its speed?' -> 'speed'
        'What are its advantages?' -> 'advantages'
    """

    if not isinstance(user, str):
        return None

    text = user.lower().strip()

    patterns = [
        r"^what about (?:its|the) (.+)$",
        r"^what is its (.+)$",
        r"^what are its (.+)$",
        r"^how does it (.+)$",
        r"^why is it (.+)$",
        r"^is it (.+)$",
        r"^more about (.+)$",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)

        if match:
            value = match.group(1).strip()
            value = value.rstrip(".,!?;:")

            if value:
                return value

    return None