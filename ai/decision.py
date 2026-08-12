from ai.learning import learn
from core.router import handle_command
from ai.intent import detect_intent
from ai.response import generate_response


def decide(user, memory):

    # 1. Learn something new
    learned = learn(user)

    if learned:
        return learned

    # 2. Try the command router
    response = handle_command(user, memory)

    if response:
        return response

    # 3. Detect intent
    intent = detect_intent(user)

    if intent:
        response = generate_response(intent, memory)

        if response:
            return response

    # 4. Nothing matched
    return "I am still learning."
