class Task:

    def __init__(self, name):

        self.name = name

        self.steps = []

    def add_step(self, step):

        self.steps.append(step)

    def run(self):

        completed = []

        for step in self.steps:

            completed.append(step)

        return completed