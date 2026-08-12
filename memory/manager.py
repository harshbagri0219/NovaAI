from memory.memory import load_memory, save_memory


class MemoryManager:

    def __init__(self):
        self.data = load_memory()

    def set(self, category, key, value):

        if category not in self.data:
            self.data[category] = {}

        self.data[category][key] = value

        save_memory(self.data)

    def get(self, category, key):

        if category in self.data:
            return self.data[category].get(key)

        return None

    def all(self):

        return self.data