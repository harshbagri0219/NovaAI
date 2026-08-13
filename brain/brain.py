from ai.intent import detect_intent
from brain.context import last_conversation
from brain.context_builder import build_context
from brain.context_resolver import resolve_reference
from brain.reasoning import reason
from knowledge.profile import recall


class Brain:

    def think(self, user):

        # -----------------------------
        # Build Context
        # -----------------------------
        context = build_context(user)

        reference = resolve_reference(user)

        # -----------------------------
        # Detect Intent
        # -----------------------------
        intent = detect_intent(user)

        user = user.lower()

        # -----------------------------
        # Nova Identity
        # -----------------------------
        if intent == "identity":

            return "My name is NOVA. I am your personal AI assistant."

        # -----------------------------
        # Owner
        # -----------------------------
        if intent == "owner":

            owner = recall("owner")

            if owner:

                return f"I was created by {owner}."

            else:

                return "I was created by my developer."

        # -----------------------------
        # Favourite Language
        # -----------------------------
        if intent == "favorite_language":

            language = recall("favorite_language")

            if language:

                return f"Your favourite language is {language}."

            return "You haven't told me your favourite language."

        # -----------------------------
        # Favourite Languages
        # -----------------------------
        if intent == "languages":

            languages = recall("languages")

            if isinstance(languages, list) and languages:

                if len(languages) == 1:

                    return f"You like {languages[0]}."

                if len(languages) == 2:

                    return f"You like {languages[0]} and {languages[1]}."

                return (
                    "You like "
                    + ", ".join(languages[:-1])
                    + ", and "
                    + languages[-1]
                    + "."
                )

            return "You haven't told me which languages you like."

        # -----------------------------
        # Favourite Food
        # -----------------------------
        if intent == "favorite_food":

            food = recall("favorite_food")

            if food:

                return f"Your favourite food is {food}."

            return "You haven't told me your favourite food."

        # -----------------------------
        # Last Conversation Memory
        # -----------------------------
        history = last_conversation()

        if "what language did i just mention" in user:

            for item in reversed(history):

                text = item["user"].lower()

                if "language is" in text:

                    language = text.split("language is")[-1].strip()

                    return f"You just mentioned {language}."

            return "You haven't mentioned any language."

        # -----------------------------
        # Reasoning Engine
        # -----------------------------
        reasoning_response = reason(user)

        if reasoning_response:

            return reasoning_response

        # -----------------------------
        # Context-aware Fallback
        # -----------------------------
        if reference:

            previous = reference["previous_message"]

            if reference["reference"] == "which one":

                return (
                    f"You were previously talking about: {previous}. "
                    "Tell me what aspect you want to compare."
                )

            if reference["reference"] in ("it", "that"):

                return (
                    f"I understand that you're referring to: {previous}."
                )

        # -----------------------------
        # Default Response
        # -----------------------------
        return "I am still learning."
