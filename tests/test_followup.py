from brain.followup import detect_followup, is_followup


def test_topic_followup():
    assert detect_followup("What about its speed?") == "topic_followup"


def test_reference_followup():
    assert detect_followup("Is it difficult?") == "reference"


def test_continuation_followup():
    assert detect_followup("Tell me more") == "continuation"


def test_comparison_followup():
    assert detect_followup("Which one?") == "comparison"


def test_which_is_better():
    assert detect_followup("Which is better?") == "comparison"


def test_non_followup():
    assert detect_followup("Tell me about Python") is None


def test_empty_input():
    assert detect_followup("") is None


def test_is_followup_true():
    assert is_followup("What about its speed?")


def test_is_followup_false():
    assert not is_followup("Tell me about Python")