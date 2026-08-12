class TaskEngine:

    def __init__(self):

        self.tasks = []

    def add(self, action):

        self.tasks.append(action)

    def clear(self):

        self.tasks.clear()

    def run(self):

        results = []

        for action in self.tasks:

            results.append(action())

        self.clear()

        return "\n".join(results)