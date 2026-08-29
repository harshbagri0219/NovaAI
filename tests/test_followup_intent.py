from brain.followup import detect_followup_intent


def test_speed_intent():
    assert detect_followup_intent("speed") == "performance"


def test_performance_intent():
    assert detect_followup_intent("performance") == "performance"


def test_learning_intent():
    assert detect_followup_intent("learn") == "learning"


def test_learning_question():
    assert detect_followup_intent("how to learn it") == "learning"


def test_advantages_intent():
    assert detect_followup_intent("advantages") == "advantages"


def test_disadvantages_intent():
    assert detect_followup_intent("disadvantages") == "disadvantages"


def test_use_cases_intent():
    assert detect_followup_intent("uses") == "use_cases"


def test_examples_intent():
    assert detect_followup_intent("examples") == "examples"


def test_career_intent():
    assert detect_followup_intent("career") == "career"


def test_jobs_intent():
    assert detect_followup_intent("jobs") == "career"


def test_unknown_intent():
    assert detect_followup_intent("hello") is None