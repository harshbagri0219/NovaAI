from ai.intent import detect_intent


def choose_action(user):
    return detect_intent(user)
