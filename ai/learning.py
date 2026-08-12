from knowledge.profile import remember, recall


def learn(user):
    text = user.lower().strip()

    # Name / owner
    if "my name is " in text:
        value = user.lower().split("my name is ", 1)[1].strip()
        if value:
            remember("owner", value.title())
            return f"I'll remember that your name is {value.title()}."

    # Favourite language
    if "my favourite language is " in text:
        value = user.split("is", 1)[1].strip()
        if value:
            remember("favorite_language", value)
            return f"I'll remember that your favourite language is {value}."

    if "my favorite language is " in text:
        value = user.split("is", 1)[1].strip()
        if value:
            remember("favorite_language", value)
            return f"I'll remember that your favourite language is {value}."

    # Favourite food
    if "my favourite food is " in text:
        value = user.split("is", 1)[1].strip()
        if value:
            remember("favorite_food", value)
            return f"I'll remember that your favourite food is {value}."

    if "my favorite food is " in text:
        value = user.split("is", 1)[1].strip()
        if value:
            remember("favorite_food", value)
            return f"I'll remember that your favourite food is {value}."

    # Location
    if "i live in " in text:
        value = user.lower().split("i live in ", 1)[1].strip()
        if value:
            remember("location", value.title())
            return f"I'll remember that you live in {value.title()}."

    # Additional language preference
    if "i also like " in text:
        value = user.lower().split("i also like ", 1)[1].strip()

        if value:
            profile = recall("languages")

            if not isinstance(profile, list):
                profile = []

    # Don't create duplicates
            if value.title() not in profile:
                profile.append(value.title())

            remember("languages", profile)

            return f"I'll remember that you also like {value.title()}."

    # No new information detected
    return None
