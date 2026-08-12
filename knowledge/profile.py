from memory.memory import load_memory, save_memory


def remember(key, value):
    data = load_memory()
    data[key] = value
    save_memory(data)


def recall(key):
    data = load_memory()
    return data.get(key)


def forget(key):
    data = load_memory()

    if key in data:
        del data[key]
        save_memory(data)
        return True

    return False
