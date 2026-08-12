class ContextManager:

    def __init__(self):

        self.history = []

    def add(self, user, assistant):

        self.history.append({
            "user": user,
            "assistant": assistant
        })

        if len(self.history) > 10:
            self.history.pop(0)

    def last_user(self):

        if self.history:
            return self.history[-1]["user"]

        return ""

    def last_reply(self):

        if self.history:
            return self.history[-1]["assistant"]

        return ""

    def all(self):

        return self.history