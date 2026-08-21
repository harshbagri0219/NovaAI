from brain.topic_tracker import TopicTracker, extract_topic


def test_extract_tell_me_about():
    assert extract_topic("Tell me about Python") == "Python"


def test_extract_what_is():
    assert extract_topic("What is Java?") == "Java"


def test_extract_explain():
    assert extract_topic("Explain machine learning") == "machine learning"


def test_extract_empty():
    assert extract_topic("") is None


def test_topic_tracker_current():
    tracker = TopicTracker()

    tracker.add("Python")

    assert tracker.current() == "Python"


def test_topic_tracker_previous():
    tracker = TopicTracker()

    tracker.add("Python")
    tracker.add("Java")

    assert tracker.current() == "Java"
    assert tracker.previous() == "Python"


def test_topic_tracker_duplicate():
    tracker = TopicTracker()

    tracker.add("Python")
    tracker.add("Java")
    tracker.add("Python")

    assert tracker.all() == ["Java", "Python"]


def test_topic_tracker_limit():
    tracker = TopicTracker(max_topics=2)

    tracker.add("Python")
    tracker.add("Java")
    tracker.add("Rust")

    assert tracker.all() == ["Java", "Rust"]