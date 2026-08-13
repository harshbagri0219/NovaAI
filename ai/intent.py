import re


def detect_intent(user):
    text = user.lower().strip()

    intents = {
        "battery": [
            "battery",
            "charge",
            "power",
            "battery percentage"
        ],

        "storage": [
            "storage",
            "memory",
            "space"
        ],

        "device": [
            "phone",
            "device",
            "model",
            "android"
        ],

        "time": [
            "time",
            "clock"
        ],

        "greeting": [
            "hello",
            "hi",
            "hey"
        ],

        "identity": [
            "who are you",
            "what is your name"
        ],

        "owner": [
            "who created you",
            "who made you",
            "what is my name"
        ],

        "favorite_language": [
            "what is my favourite language",
            "what's my favourite language",
            "what is my favorite language",
            "what's my favorite language"
        ],

        "favorite_food": [
            "what is my favourite food",
            "what's my favourite food",
            "what is my favorite food",
            "what's my favorite food"
        ],

        "languages": [
            "what languages do i like",
            "which languages do i like",
            "what programming languages do i like",
            "which programming languages do i like"
        ]
    }

    for intent, keywords in intents.items():

        for keyword in keywords:

            # Multi-word phrases
            if " " in keyword:
                if keyword in text:
                    return intent

            # Single words — require a complete word
            else:
                if re.search(r"\b" + re.escape(keyword) + r"\b", text):
                    return intent

    return None
