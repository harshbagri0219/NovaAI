history = []

MAX_CONTEXT = 10


def remember(user, nova):
    history.append({
        "user": user,
        "nova": nova
    })

    if len(history) > MAX_CONTEXT:
        history.pop(0)


def last_conversation():
    return history[-MAX_CONTEXT:]


def get_recent_context(limit=5):
    return history[-limit:]


def clear_context():
    history.clear()
