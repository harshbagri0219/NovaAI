import re


class TopicTracker:

    def __init__(self, max_topics=5):
        self.topics = []
        self.max_topics = max_topics

    def add(self, topic):
        if not isinstance(topic, str):
            return

        topic = topic.strip()

        if not topic:
            return

        # Remove duplicate topic
        self.topics = [
            item for item in self.topics
            if item.lower() != topic.lower()
        ]

        # Add newest topic
        self.topics.append(topic)

        # Keep only recent topics
        if len(self.topics) > self.max_topics:
            self.topics.pop(0)

    def current(self):
        if not self.topics:
            return None

        return self.topics[-1]

    def previous(self):
        if len(self.topics) < 2:
            return None

        return self.topics[-2]

    def all(self):
        return list(self.topics)


def extract_topic(text):
    """
    Extract a simple topic from common conversational patterns.
    """

    if not isinstance(text, str):
        return None

    text = text.strip()

    if not text:
        return None

    patterns = [
        r"tell me about (.+)",
        r"what is (.+)",
        r"what are (.+)",
        r"explain (.+)",
        r"how does (.+) work",
        r"how do i use (.+)",
    ]

    for pattern in patterns:

        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            topic = match.group(1).strip()
            topic = topic.rstrip(".,!?;:")

            if topic:
                return topic

    return None