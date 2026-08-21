from ai.planner import choose_action


def test_planner_battery():
    assert choose_action("check my battery") == "battery"


def test_planner_storage():
    assert choose_action("how much storage do I have") == "storage"


def test_planner_greeting():
    assert choose_action("hello NOVA") == "greeting"


def test_planner_identity():
    assert choose_action("who are you") == "identity"