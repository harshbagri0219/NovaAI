from brain.brain import Brain


def test_brain_performance_followup():
    brain = Brain()

    brain.think("Tell me about Python")

    result = brain.think("speed")

    assert isinstance(result, str)
    assert "Python" in result


def test_brain_learning_followup():
    brain = Brain()

    brain.think("Tell me about Python")

    result = brain.think("learn")

    assert isinstance(result, str)
    assert "Python" in result


def test_brain_advantages_followup():
    brain = Brain()

    brain.think("Tell me about Python")

    result = brain.think("advantages")

    assert isinstance(result, str)
    assert "Python" in result


def test_brain_disadvantages_followup():
    brain = Brain()

    brain.think("Tell me about Python")

    result = brain.think("disadvantages")

    assert isinstance(result, str)
    assert "Python" in result


def test_brain_use_cases_followup():
    brain = Brain()

    brain.think("Tell me about Python")

    result = brain.think("uses")

    assert isinstance(result, str)
    assert "Python" in result


def test_brain_examples_followup():
    brain = Brain()

    brain.think("Tell me about Python")

    result = brain.think("examples")

    assert isinstance(result, str)
    assert "Python" in result


def test_brain_career_followup():
    brain = Brain()

    brain.think("Tell me about Python")

    result = brain.think("career")

    assert isinstance(result, str)
    assert "Python" in result


def test_brain_cost_followup():
    brain = Brain()

    brain.think("Tell me about Python")

    result = brain.think("cost")

    assert isinstance(result, str)
    assert "Python" in result


def test_brain_security_followup():
    brain = Brain()

    brain.think("Tell me about Python")

    result = brain.think("security")

    assert isinstance(result, str)
    assert "Python" in result


def test_brain_followup_after_topic_change():
    brain = Brain()

    brain.think("Tell me about Python")
    brain.think("Tell me about Java")

    result = brain.think("advantages")

    assert isinstance(result, str)
    assert "Java" in result


def test_brain_learning_after_topic_change():
    brain = Brain()

    brain.think("Tell me about Python")
    brain.think("Tell me about Java")

    result = brain.think("learn")

    assert isinstance(result, str)
    assert "Java" in result