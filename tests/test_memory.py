from memory.memory import load_memory, save_memory

data = load_memory()

data["owner"] = "Hanzo"

save_memory(data)

print(load_memory())