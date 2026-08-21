from core.router import handle_command


def test_owner_command():
    result = handle_command("Who created you?", {})
    assert isinstance(result, str)


def test_favorite_language_command():
    result = handle_command("What is my favorite language?", {})
    assert isinstance(result, str)


def test_favorite_food_command():
    result = handle_command("What is my favorite food?", {})
    assert isinstance(result, str)


def test_battery_command():
    result = handle_command("What is my battery percentage?", {})
    assert result is not None


def test_storage_command():
    result = handle_command("How much storage do I have?", {})
    assert result is not None


def test_unknown_command():
    result = handle_command("Tell me something completely random", {})
    assert result is None