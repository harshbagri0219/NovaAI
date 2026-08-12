def is_followup(user):

    user = user.lower()

    words = [
        "and",
        "also",
        "what about",
        "then",
        "next",
        "it"
    ]

    for word in words:
        if user.startswith(word):
            return True

    return False