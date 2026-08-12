from memory.manager import MemoryManager

memory = MemoryManager()

memory.set("preferences", "language", "Python")
memory.set("preferences", "food", "Baigan")
memory.set("profile", "city", "Delhi")

print(memory.all())