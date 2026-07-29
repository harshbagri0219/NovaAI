class Brain:

    def think(self,question):
        question = question.lower()

        if "hello" in question:
            return "Hello Hanzo."

        elif "who are you" in question:
            return "I am Nova"

        else:
            return "I am still learning"
