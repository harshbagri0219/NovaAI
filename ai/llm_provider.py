import json
import os
from urllib.error import URLError
from urllib.request import Request, urlopen


class OllamaProvider:
    """
    Local Ollama LLM provider.

    Security boundary:
    - accepts conversational text only
    - returns text only
    - has no access to NOVA tools
    - has no access to ToolExecutor
    - has no access to ToolRegistry
    """

    def __init__(
        self,
        base_url=None,
        model=None,
        timeout=None,
    ):
        self.base_url = (
            base_url
            or os.getenv("NOVA_OLLAMA_URL")
            or "http://127.0.0.1:11434"
        )

        self.model = (
            model
            or os.getenv("NOVA_OLLAMA_MODEL")
            or "qwen2.5-coder:7b"
        )

        self.timeout = int(
            timeout
            or os.getenv("NOVA_OLLAMA_TIMEOUT", "60")
        )

    def generate(self, user, context=None, personality=None):
        """
        Ask Ollama for a conversational response.

        Only strings/conversational context are sent.
        No executable NOVA objects are accepted.
        """

        prompt = self._build_prompt(
            user=user,
            context=context,
            personality=personality,
        )

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }

        request = Request(
            f"{self.base_url.rstrip('/')}/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urlopen(request, timeout=self.timeout) as response:
                data = json.loads(
                    response.read().decode("utf-8")
                )

            result = data.get("response")

            if not isinstance(result, str):
                return None

            result = result.strip()

            return result or None

        except (
            OSError,
            URLError,
            TimeoutError,
            ValueError,
            json.JSONDecodeError,
        ):
            # LLM availability must never break NOVA's
            # deterministic or security-critical paths.
            return None

    @staticmethod
    def _build_prompt(user, context=None, personality=None):
        context_text = str(context) if context else "No previous conversation."
        personality_text = (
            str(personality)
            if personality
            else "Calm, intelligent, helpful, concise."
        )

        return (
            "You are NOVA, a personal AI assistant.\n"
            "You are operating as a conversational reasoning system.\n"
            "You do not execute tools or perform actions.\n"
            "Do not claim that you executed an action.\n"
            "Answer the user's request directly and clearly.\n\n"
            f"Personality:\n{personality_text}\n\n"
            f"Conversation context:\n{context_text}\n\n"
            f"User:\n{user}\n\n"
            "NOVA:"
        )