from brain.brain import Brain
from memory.memory import load_memory, save_memory
from voice.speak import speak
from voice.listen import listen
from core.router import handle_command

brain = Brain()
memory = load_memory()

print("Nova AI Started")

while True:

    user = listen()

    if user.lower() == "exit":
        speak("Goodbye!")
        break

    elif user.lower().startswith("remember my name is "):

        name = user[len("remember my name is "):].strip()

        memory["owner"] = name

        save_memory(memory)

        speak(f"I will remember your name is {name}.")

    else:

        response = handle_command(user, memory)

        if response:
            speak(response)
            continue

        speak(brain.think(user))