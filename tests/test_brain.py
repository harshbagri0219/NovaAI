from brain.brain import Brain


def test_brain_identity():
    brain = Brain()
    result = brain.think("Who are you?")

    assert isinstance(result, str)
    assert "NOVA" in result


def test_brain_owner():
    brain = Brain()
    result = brain.think("Who created you?")

    assert isinstance(result, str)


def test_brain_favorite_language():
    brain = Brain()
    result = brain.think("What is my favorite language?")

    assert isinstance(result, str)


def test_brain_favorite_food():
    brain = Brain()
    result = brain.think("What is my favorite food?")

    assert isinstance(result, str)


def test_brain_unknown():
    brain = Brain()
    result = brain.think("Tell me something completely random")

    assert isinstance(result, str)