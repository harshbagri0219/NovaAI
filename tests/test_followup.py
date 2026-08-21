from brain.followup import is_followup, extract_followup_question


def test_tell_me_more():
    assert is_followup("Tell me more")


def test_what_about_speed():
    assert is_followup("What about its speed?")


def test_is_it_difficult():
    assert is_followup("Is it difficult?")


def test_which_one():
    assert is_followup("Which one?")


def test_normal_question_is_not_followup():
    assert not is_followup("What is Python?")


def test_extract_speed():
    assert extract_followup_question("What about its speed?") == "speed"


def test_extract_advantages():
    assert extract_followup_question("What are its advantages?") == "advantages"


def test_extract_difficult():
    assert extract_followup_question("Is it difficult?") == "difficult"


def test_extract_empty():
    assert extract_followup_question("") is None