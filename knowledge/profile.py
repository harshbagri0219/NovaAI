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
