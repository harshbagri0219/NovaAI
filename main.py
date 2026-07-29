from brain.brain import Brain

brain = Brain()

print("Nova AI Started")

while True:

    user = input("You : ")

    if user.lower() == "exit":
        break

    answer = brain.think(user)

    print("Nova :", answer)