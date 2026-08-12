from ai.planner import choose_action
from core.plugin_manager import load_plugins
from plugins import memory as memory_plugin
from knowledge.profile import recall


plugins = load_plugins()


def handle_command(command, memory):

    intent = choose_action(command)

    if intent == "owner":
        owner = recall("owner")

        if owner:
            return f"Your name is {owner}."

        return "I don't know your name yet."

    if intent == "favorite_language":
        language = recall("favorite_language")

        if language:
            return f"Your favourite language is {language}."

        return "I don't know your favourite language yet."

    if intent == "favorite_food":
        food = recall("favorite_food")

        if food:
            return f"Your favourite food is {food}."

        return "I don't know your favourite food yet."

    if intent in plugins:
        return plugins[intent]()

    return None
