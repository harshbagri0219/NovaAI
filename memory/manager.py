from memory.memory import load_memory, save_memory


class MemoryManager:
    """
    High-level interface for NOVA's structured v0.2 memory.
    """

    def __init__(self):
        self.memory = load_memory()

        if not isinstance(self.memory, dict):
            self.memory = load_memory()

        if not isinstance(self.memory.get("data"), dict):
            self.memory["data"] = {}

    @property
    def data(self):
        """Return the canonical memory data section."""
        return self.memory["data"]

    def set(self, category, key, value):
        """Store a value inside a memory category."""

        if not isinstance(category, str):
            return False

        if not isinstance(key, str):
            return False

        category = category.strip()
        key = key.strip()

        if not category or not key:
            return False

        if category not in self.data:
            self.data[category] = {}

        if not isinstance(self.data[category], dict):
            self.data[category] = {}

        self.data[category][key] = value

        return save_memory(self.memory)

    def get(self, category, key, default=None):
        """Retrieve a value from a memory category."""

        if not isinstance(category, str):
            return default

        if not isinstance(key, str):
            return default

        category_data = self.data.get(category)

        if not isinstance(category_data, dict):
            return default

        return category_data.get(key, default)

    def has(self, category, key):
        """Return True if a memory key exists in a category."""

        if not isinstance(category, str):
            return False

        if not isinstance(key, str):
            return False

        category_data = self.data.get(category)

        if not isinstance(category_data, dict):
            return False

        return key in category_data

    def delete(self, category, key):
        """Delete a value from a memory category."""

        if not isinstance(category, str):
            return False

        if not isinstance(key, str):
            return False

        category_data = self.data.get(category)

        if not isinstance(category_data, dict):
            return False

        if key not in category_data:
            return False

        del category_data[key]

        return save_memory(self.memory)

    def get_category(self, category):
        """Return a copy of an entire memory category."""

        category_data = self.data.get(category)

        if isinstance(category_data, dict):
            return dict(category_data)

        return {}

    def all(self):
        """Return the complete canonical memory object."""

        return self.memory
