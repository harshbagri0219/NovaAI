from ai.intent import detect_intent
from brain.context import last_conversation
from brain.context_builder import build_context
from brain.context_resolver import resolve_reference
from brain.reasoning import reason
from brain.topic_tracker import TopicTracker, extract_topic
from knowledge.profile import recall


class Brain:

    def __init__(self):
        self.topic_tracker = TopicTracker()

    def think(self, user):

        # -----------------------------
        # Track conversation topic
        # -----------------------------
        topic = extract_topic(user)

        if topic:
            self.topic_tracker.add(topic)

        # -----------------------------
        # Build Context
        # -----------------------------
        context = build_context(user)
        reference = resolve_reference(user)

        # -----------------------------
        # Detect Intent
        # -----------------------------
        intent = detect_intent(user)
        user = user.lower().strip()

        # -----------------------------
        # NOVA Identity
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
        # Topic-aware references
        #
        # IMPORTANT:
        # Handle references BEFORE the
        # reasoning engine so that the
        # reasoning fallback cannot swallow
        # the reference request.
        # -----------------------------
        current_topic = self.topic_tracker.current()
        previous_topic = self.topic_tracker.previous()

        if reference:

            reference_type = reference["reference"]

            if reference_type == "it":
                if current_topic:
                    return (
                        f"You're referring to {current_topic}. "
                        f"What would you like to know about {current_topic}?"
                    )

                return (
                    f"I understand that you're referring to: "
                    f"{reference['previous_message']}."
                )

            if reference_type == "that":
                if current_topic:
                    return (
                        f"You're referring to {current_topic}. "
                        f"What would you like to know about {current_topic}?"
                    )

                return (
                    f"I understand that you're referring to: "
                    f"{reference['previous_message']}."
                )

            if reference_type == "which one":

                if current_topic and previous_topic:
                    return (
                        f"You're currently talking about {current_topic}. "
                        f"Previously, we were discussing {previous_topic}. "
                        f"Which one would you like to compare?"
                    )

                if current_topic:
                    return (
                        f"You're currently talking about {current_topic}. "
                        f"What aspect of {current_topic} do you want to compare?"
                    )

                return (
                    f"You were previously talking about: "
                    f"{reference['previous_message']}. "
                    f"Tell me what aspect you want to compare."
                )

        # -----------------------------
        # Reasoning Engine
        # -----------------------------
        reasoning_response = reason(user)

        if reasoning_response:
            return reasoning_response

        # -----------------------------
        # Topic fallback
        # -----------------------------
        if current_topic:

            if "speed" in user:
                return (
                    f"{current_topic} can be discussed in terms of "
                    f"execution speed, performance, and efficiency."
                )

            if "difficult" in user or "hard" in user:
                return (
                    f"{current_topic} can be easy or difficult depending "
                    f"on your experience and what you are trying to do."
                )

            return (
                f"We are currently discussing {current_topic}. "
                f"What would you like to know about it?"
            )

        # -----------------------------
        # Default Response
        # -----------------------------
        return "I am still learning."