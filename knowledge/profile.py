from memory.memory import load_memory, save_memory
from memory.models import LEGACY_TO_CATEGORICAL


def _get_data_dict(memory_data):
    """Return the canonical v0.2 data section."""

    if not isinstance(memory_data, dict):
        return {}

    if (
        memory_data.get("schema_version") == "0.2.0"
        and isinstance(memory_data.get("data"), dict)
    ):
        return memory_data["data"]

    return memory_data


def remember(key, value):
    """Store a memory value using one load and one save operation."""

    memory = load_memory()
    data = _get_data_dict(memory)

    # Known legacy keys → canonical category.
    if key in LEGACY_TO_CATEGORICAL:
        category, subkey = LEGACY_TO_CATEGORICAL[key]

        if category not in data or not isinstance(data[category], dict):
            data[category] = {}

        data[category][subkey] = value

    # Compatibility list.
    elif key == "languages":
        data["languages"] = value

    # Unknown values → profile.
    else:
        if "profile" not in data or not isinstance(data["profile"], dict):
            data["profile"] = {}

        data["profile"][key] = value

    return save_memory(memory)


def recall(key):
    """Retrieve a memory value using one load operation."""

    memory = load_memory()
    data = _get_data_dict(memory)

    # Known legacy keys.
    if key in LEGACY_TO_CATEGORICAL:
        category, subkey = LEGACY_TO_CATEGORICAL[key]

        category_data = data.get(category, {})

        if isinstance(category_data, dict):
            if subkey in category_data:
                return category_data[subkey]

    # Compatibility languages list.
    if key == "languages":
        languages = data.get("languages")

        if isinstance(languages, list):
            return languages

    # Direct top-level lookup.
    if key in data:
        return data[key]

    # Profile fallback.
    profile = data.get("profile", {})

    if isinstance(profile, dict):
        if key in profile:
            return profile[key]

    # Final compatibility search.
    for category_data in data.values():

        if isinstance(category_data, dict):
            if key in category_data:
                return category_data[key]

    return None


def forget(key):
    """Remove a memory value using one load and one save operation."""

    memory = load_memory()
    data = _get_data_dict(memory)

    # Known legacy keys.
    if key in LEGACY_TO_CATEGORICAL:
        category, subkey = LEGACY_TO_CATEGORICAL[key]

        category_data = data.get(category)

        if isinstance(category_data, dict):
            if subkey in category_data:
                del category_data[subkey]
                return save_memory(memory)

    # Compatibility languages list.
    if key == "languages" and key in data:
        del data[key]
        return save_memory(memory)

    # Profile fallback.
    profile = data.get("profile")

    if isinstance(profile, dict):
        if key in profile:
            del profile[key]
            return save_memory(memory)

    # Direct top-level fallback.
    if key in data:
        del data[key]
        return save_memory(memory)

    return False


# ---------------------------------
# Text Normalization
# ---------------------------------

def normalize_text(value):
    """Clean a text value by removing unnecessary whitespace and punctuation."""

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
    """Normalize a programming language name."""

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
    """Add a programming language without duplicates."""

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

    return remember("languages", normalized_languages)


def recall_languages():
    """Return the user's normalized programming language list."""

    languages = recall("languages")

    if not isinstance(languages, list):
        return []

    cleaned = []

    for language in languages:
        language = normalize_language(language)

        if language and language not in cleaned:
            cleaned.append(language)

    return cleaned