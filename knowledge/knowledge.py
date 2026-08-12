from knowledge.profile import recall


def answer(question):

    question = question.lower()

    if "favorite language" in question:

        language = recall("favorite_language")

        if language:
            return f"Your favourite language is {language}."

        return "You haven't told me your favourite language yet."

    return None