from brain.context import get_recent_context


def build_context(user, limit=5):

    history = get_recent_context(limit)

    context = []

    for item in history:
        context.append(
            f"User: {item['user']}\n"
            f"NOVA: {item['nova']}"
        )

    context.append(f"User: {user}")

    return "\n".join(context)
