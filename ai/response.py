def generate_response(intent, memory):

    if intent == "identity":
        return "I am Nova AI."

    if intent == "owner":
        owner = memory.get("owner")

        if owner:
            return f"You are {owner}."

        return "I don't know your name yet."

    if intent == "favorite_language":
        language = memory.get("favorite_language")

        if language:
            return f"Your favourite language is {language}."

        return "I don't know your favourite language yet."

    if intent == "favorite_food":
        food = memory.get("preferences", {}).get("food")

        if food:
            return f"Your favourite food is {food}."

        return "I don't know your favourite food yet."

    if intent == "greeting":
        return "Hello. How can I help you?"

    if intent == "languages":
        languages = memory.get("languages", [])

        if languages:
            if len(languages) == 1:
                return f"You like {languages[0]}."

            return "You like " + ", ".join(languages[:-1]) + " and " + languages[-1] + "."

        return "I don't know which languages you like yet."

    return None
