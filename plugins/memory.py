def run(memory):

    if "owner" in memory:
        return f"Your name is {memory['owner']}."

    return "I don't know your name yet."