from brain.brain import Brain


def test_brain_identity():
    brain = Brain()

    result = brain.think("Who are you?")

    assert isinstance(result, str)
    assert "NOVA" in result


def test_brain_tracks_topic():
    brain = Brain()

    brain.think("Tell me about Python")

    assert brain.topic_tracker.current() == "Python"


def test_brain_tracks_multiple_topics():
    brain = Brain()

    brain.think("Tell me about Python")
    brain.think("What is Java?")

    assert brain.topic_tracker.current() == "Java"
    assert brain.topic_tracker.previous() == "Python"


def test_brain_owner():
    brain = Brain()

    result = brain.think("Who created you?")

    assert isinstance(result, str)
    assert result


def test_brain_favorite_language():
    brain = Brain()

    result = brain.think("What is my favorite language?")

    assert isinstance(result, str)
    assert result


def test_brain_favorite_food():
    brain = Brain()

    result = brain.think("What is my favorite food?")

    assert isinstance(result, str)
    assert result


def test_brain_unknown():
    brain = Brain()

    result = brain.think("Tell me something completely random")

    assert isinstance(result, str)
    assert result


def test_brain_language_memory_question():
    brain = Brain()

    result = brain.think("What language did I just mention?")

    assert isinstance(result, str)
    assert result


def test_brain_context_reference():
    brain = Brain()

    result = brain.think("Which one?")

    assert isinstance(result, str)
    assert result


def test_brain_it_reference_uses_topic():
    brain = Brain()

    brain.think("Tell me about Python")

    result = brain.think("Is it difficult?")

    assert isinstance(result, str)
    assert "Python" in result


def test_brain_that_reference_uses_topic():
    brain = Brain()

    brain.think("Tell me about Python")

    result = brain.think("What about that?")

    assert isinstance(result, str)
    assert "Python" in result


def test_brain_which_one_uses_topic():
    brain = Brain()

    brain.think("Tell me about Python")

    result = brain.think("Which one?")

    assert isinstance(result, str)
    assert "Python" in result