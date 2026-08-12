from brain.context import last_conversation
from brain.personality import get_personality


def think(user):

    context = last_conversation()

    personality = get_personality()

    return {
        "user": user,
        "context": context,
        "personality": personality
    }