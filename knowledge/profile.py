from memory.memory import load_memory, save_memory

# Compatibility imports for structured memory
from memory.models import LEGACY_TO_CATEGORICAL, CATEGORICAL_TO_LEGACY


def _get_data_dict(memory_data):
    """Extract the data dict from memory structure.

    Works with both v0.1 flat format and v0.2 structured format.

    v0.1 flat: memory_data = {"owner": "Hanzo", ...}
    v0.2 structured: memory_data = {"schema_version": "0.2.0", "data": {"profile": {...}, ...}}

    Args:
        memory_data: output of load_memory()

    Returns:
        dict containing the actual key-value data (without schema_version wrapper)
    """
    if not isinstance(memory_data, dict):
        return {}

    # v0.2 structured format - has schema_version and data wrapper
    if "schema_version" in memory_data and "data" in memory_data:
        return memory_data["data"]

    # v0.1 flat format - the memory_data itself is the data dict
    return memory_data


def remember(key, value):
    """Remember a key-value pair in memory.

    Preserves existing API: remember(key, value) continues to work exactly as before.
    Internal implementation now uses structured memory beneath the flat API.

    Args:
        key: memory key (e.g., "owner", "languages", "favorite_language")
        value: value to store
    """
    memory = load_memory()
    data = _get_data_dict(memory)

    # Store in flat key for backward compatibility
    data[key] = value

    # Also store in structured section if applicable
    _store_in_structured(key, value)

    save_memory(memory)


def _store_in_structured(key, value):
    """Store key-value in structured memory categories.

    Internal implementation detail. Maps legacy keys to structured categories.

    Args:
        key: memory key
        value: value to store
    """
    # Map legacy keys to structured categories
    if key in LEGACY_TO_CATEGORICAL:
        category, subkey = LEGACY_TO_CATEGORICAL[key]
        # Ensure structured data exists
        memory = load_memory()
        if "data" not in memory:
            memory["data"] = {}
        if category not in memory["data"]:
            memory["data"][category] = {}
        memory["data"][category][subkey] = value
        save_memory(memory)
    # For unknown keys, also store in profile structured section
    elif key not in ("owner", "location", "favorite_language", "favorite_food", "languages"):
        # Store generically in profile
        memory = load_memory()
        data = _get_data_dict(memory)
        if "profile" not in data:
            data["profile"] = {}
        if key not in data["profile"]:
            data["profile"][key] = value
        save_memory(memory)


def recall(key):
    """ Recall a value from memory.

    Preserves existing API: recall(key) continues to work exactly as before.

    Args:
        key: memory key to look up

    Returns:
        stored value, or None if not found
    """
    memory = load_memory()
    data = _get_data_dict(memory)

    # First try flat key
    if key in data:
        return data[key]

    # Try structured categories
    if key in CATEGORICAL_TO_LEGACY:
        # Find which category contains this key
        for category, subkey in CATEGORICAL_TO_LEGACY.items():
            memory = load_memory()
            if "data" in memory and category in memory["data"]:
                if subkey in memory["data"][category]:
                    return memory["data"][category][subkey]

    # Fallback: search all structured categories
    memory = load_memory()
    if "data" in memory:
        for category, category_data in memory["data"].items():
            if key in category_data:
                return category_data[key]

    return None


def forget(key):
    """ Forget a key from memory.

    Preserves existing API: forget(key) continues to work exactly as before.

    Args:
        key: memory key to remove

    Returns:
        True if key was found and removed, False otherwise
    """
    memory = load_memory()
    data = _get_data_dict(memory)

    # Remove from flat key
    if key in data:
        del data[key]
        save_memory(memory)
        return True

    # Remove from structured categories
    memory = load_memory()
    if "data" in memory:
        for category in memory["data"]:
            if key in memory["data"][category]:
                del memory["data"][category][key]
                save_memory(memory)
                return True

    return False
from memory.memory import load_memory, save_memory

# Compatibility imports for structured memory
from memory.models import LEGACY_TO_CATEGORICAL, CATEGORICAL_TO_LEGACY


def _get_data_dict(memory_data):
    """Extract the data dict from memory structure.

    Works with both v0.1 flat format and v0.2 structured format.

    v0.1 flat: memory_data = {"owner": "Hanzo", ...}
    v0.2 structured: memory_data = {"schema_version": "0.2.0", "data": {"profile": {...}, ...}}

    Args:
        memory_data: output of load_memory()

    Returns:
        dict containing the actual key-value data (without schema_version wrapper)
    """
    if not isinstance(memory_data, dict):
        return {}

    # v0.2 structured format - has schema_version and data wrapper
    if "schema_version" in memory_data and "data" in memory_data:
        return memory_data["data"]

    # v0.1 flat format - the memory_data itself is the data dict
    return memory_data


def remember(key, value):
    """Remember a key-value pair in memory.

    Preserves existing API: remember(key, value) continues to work exactly as before.
    Internal implementation now uses structured memory beneath the flat API.

    Args:
        key: memory key (e.g., "owner", "languages", "favorite_language")
        value: value to store
    """
    memory = load_memory()
    data = _get_data_dict(memory)

    # Store in flat key for backward compatibility
    data[key] = value

    # Also store in structured section if applicable
    _store_in_structured(key, value)

    save_memory(memory)


def _store_in_structured(key, value):
    """Store key-value in structured memory categories.

    Internal implementation detail. Maps legacy keys to structured categories.

    Args:
        key: memory key
        value: value to store
    """
    # Map legacy keys to structured categories
    if key in LEGACY_TO_CATEGORICAL:
        category, subkey = LEGACY_TO_CATEGORICAL[key]
        # Ensure structured data exists
        memory = load_memory()
        if "data" not in memory:
            memory["data"] = {}
        if category not in memory["data"]:
            memory["data"][category] = {}
        memory["data"][category][subkey] = value
        save_memory(memory)
    # For unknown keys, also store in profile structured section
    elif key not in ("owner", "location", "favorite_language", "favorite_food", "languages"):
        # Store generically in profile
        memory = load_memory()
        data = _get_data_dict(memory)
        if "profile" not in data:
            data["profile"] = {}
        if key not in data["profile"]:
            data["profile"][key] = value
        save_memory(memory)


def recall(key):
    """ Recall a value from memory.

    Preserves existing API: recall(key) continues to work exactly as before.

    Args:
        key: memory key to look up

    Returns:
        stored value, or None if not found
    """
    memory = load_memory()
    data = _get_data_dict(memory)

    # First try flat key
    if key in data:
        return data[key]

    # Try structured categories
    if key in CATEGORICAL_TO_LEGACY:
        # Find which category contains this key
        for category, subkey in CATEGORICAL_TO_LEGACY.items():
            memory = load_memory()
            if "data" in memory and category in memory["data"]:
                if subkey in memory["data"][category]:
                    return memory["data"][category][subkey]

    # Fallback: search all structured categories
    memory = load_memory()
    if "data" in memory:
        for category, category_data in memory["data"].items():
            if key in category_data:
                return category_data[key]

    return None


def forget(key):
    """ Forget a key from memory.

    Preserves existing API: forget(key) continues to work exactly as before.

    Args:
        key: memory key to remove

    Returns:
        True if key was found and removed, False otherwise
    """
    memory = load_memory()
    data = _get_data_dict(memory)

    # Remove from flat key
    if key in data:
        del data[key]
        save_memory(memory)
        return True

    # Remove from structured categories
    memory = load_memory()
    if "data" in memory:
        for category in memory["data"]:
            if key in memory["data"][category]:
                del memory["data"][category][key]
                save_memory(memory)
                return True

    return False


    # ---------------------------------
# Text Normalization


# ---------------------------------
# Text Normalization
# ---------------------------------

def normalize_text(value):
    """
    Clean a text value by removing
    unnecessary whitespace and punctuation.
    """

    if not isinstance(value, str):
        return value

    value = value.strip()

    value = value.rstrip(".,!?;:")

    value = " ".join(value.split())

    return value


# ---------------------------------
# Language Normalization
# ---------------------------------

def normalize_language(language):
    """
    Normalize a programming language name.
    """

    language = normalize_text(language)

    if not isinstance(language, str):
        return language

    language_map = {
        "python": "Python",
        "java": "Java",
        "javascript": "JavaScript",
        "js": "JavaScript",
        "typescript": "TypeScript",
        "ts": "TypeScript",
        "c": "C",
        "c++": "C++",
        "cpp": "C++",
        "c#": "C#",
        "csharp": "C#",
        "go": "Go",
        "golang": "Go",
        "rust": "Rust",
        "php": "PHP",
        "ruby": "Ruby",
        "kotlin": "Kotlin",
        "swift": "Swift",
    }

    return language_map.get(language.lower(), language.title())


# ---------------------------------
# Language List
# ---------------------------------

def remember_language(language):
    """
    Add a programming language to the user's
    language list without creating duplicates.
    """

    language = normalize_language(language)

    if not language:
        return False

    languages = recall("languages")

    if not isinstance(languages, list):
        languages = []

    normalized_languages = []

    for item in languages:

        item = normalize_language(item)

        if item and item not in normalized_languages:
            normalized_languages.append(item)

    if language not in normalized_languages:
        normalized_languages.append(language)

    remember("languages", normalized_languages)

    return True


def recall_languages():
    """
    Return a clean list of languages.
    """

    languages = recall("languages")

    if not isinstance(languages, list):
        return []

    cleaned = []

    for language in languages:

        language = normalize_language(language)

        if language and language not in cleaned:
            cleaned.append(language)

    return cleaned
