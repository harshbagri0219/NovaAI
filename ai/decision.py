from ai.learning import learn
from core.router import handle_command
from brain.brain import Brain
from ai.task_coordinator import coordinate
from ai.result_analyzer import analyze_results


brain = Brain()


def decide(user, memory):

    # -----------------------------
    # Learning Engine
    # -----------------------------
    learned = learn(user)

    if learned:
        return learned

    # -----------------------------
    # Task Coordinator
    # -----------------------------
    task_result = coordinate(user, memory)

    if task_result:

        response = analyze_results(task_result["results"])

        if response:
            return response

    # -----------------------------
    # Plugin Router
    # -----------------------------
    response = handle_command(user, memory)

    if response:
        return response

    # -----------------------------
    # AI Brain
    # -----------------------------
    response = brain.think(user)

    if response:
        return response

    return "I am still learning."
