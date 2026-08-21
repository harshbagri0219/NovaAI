from brain.context import remember, clear_context
from brain.context_resolver import resolve_reference


def setup_function():
    clear_context()


def test_resolve_it():
    remember("Tell me about Python", "Python is a programming language.")

    result = resolve_reference("Is it difficult?")

    assert result is not None
    assert result["reference"] == "it"
    assert result["previous_message"] == "Tell me about Python"


def test_resolve_that():
    remember("Tell me about Java", "Java is a programming language.")

    result = resolve_reference("What about that?")

    assert result is not None
    assert result["reference"] == "that"
    assert result["previous_message"] == "Tell me about Java"


def test_resolve_which_one():
    remember("Python or Java?", "Both are useful.")

    result = resolve_reference("Which one is easier?")

    assert result is not None
    assert result["reference"] == "which one"
    assert result["previous_message"] == "Python or Java?"


def test_it_inside_word_is_not_reference():
    remember("Tell me about GitHub", "GitHub is a code hosting platform.")

    result = resolve_reference("Tell me about GitHub")

    assert result is None


def test_no_reference():
    remember("Tell me about Python", "Python is a programming language.")

    result = resolve_reference("What is programming?")

    assert result is None