from ai.intent import detect_intent


def test_battery_intent():
    assert detect_intent("What is my battery percentage?") == "battery"


def test_storage_intent():
    assert detect_intent("How much storage do I have?") == "storage"


def test_device_intent():
    assert detect_intent("What phone am I using?") == "device"


def test_time_intent():
    assert detect_intent("What time is it?") == "time"


def test_greeting_intent():
    assert detect_intent("Hello NOVA") == "greeting"


def test_identity_intent():
    assert detect_intent("Who are you?") == "identity"


def test_owner_intent():
    assert detect_intent("Who created you?") == "owner"


def test_favorite_language_intent():
    assert detect_intent("What is my favorite language?") == "favorite_language"


def test_favorite_food_intent():
    assert detect_intent("What is my favorite food?") == "favorite_food"


def test_languages_intent():
    assert detect_intent("Which programming languages do I like?") == "languages"


def test_unknown_intent():
    assert detect_intent("Tell me something completely random") is None