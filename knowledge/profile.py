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
    """Store a memory value using the canonical structured format."""

    memory = load_memory()
    data = _get_data_dict(memory)

    # Known legacy keys go into their canonical category.
    if key in LEGACY_TO_CATEGORICAL:
        category, subkey = LEGACY_TO_CATEGORICAL[key]

        if category not in data or not isinstance(data[category], dict):
            data[category] = {}

        data[category][subkey] = value

    # Unknown values go into the profile category.
    else:
        if "profile" not in data or not isinstance(data["profile"], dict):
            data["profile"] = {}

        data["profile"][key] = value

    save_memory(memory)


def recall(key):
    """Retrieve a memory value."""

    memory = load_memory()
    data = _get_data_dict(memory)

    # Known legacy keys.
    if key in LEGACY_TO_CATEGORICAL:
        category, subkey = LEGACY_TO_CATEGORICAL[key]

        category_data = data.get(category, {})

        if isinstance(category_data, dict):
            if subkey in category_data:
                return category_data[subkey]

    # Direct top-level compatibility lookup.
    if key in data:
        return data[key]

    # Profile fallback.
    profile = data.get("profile", {})

    if isinstance(profile, dict):
        if key in profile:
            return profile[key]

    # Final compatibility search through structured categories.
    for category_data in data.values():
        if isinstance(category_data, dict):
            if key in category_data:
                return category_data[key]

    return None


def forget(key):
    """Remove a memory value."""

    memory = load_memory()
    data = _get_data_dict(memory)

    # Known legacy keys.
    if key in LEGACY_TO_CATEGORICAL:
        category, subkey = LEGACY_TO_CATEGORICAL[key]

        category_data = data.get(category)

        if isinstance(category_data, dict):
            if subkey in category_data:
                del category_data[subkey]
                save_memory(memory)
                return True

    # Profile fallback.
    profile = data.get("profile")

    if isinstance(profile, dict):
        if key in profile:
            del profile[key]
            save_memory(memory)
            return True

    # Direct top-level fallback.
    if key in data:
        del data[key]
        save_memory(memory)
        return True

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
    """Add a programming language without creating duplicates."""

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