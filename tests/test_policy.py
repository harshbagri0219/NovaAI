from policy.engine import PolicyEngine


def test_read_only_is_allowed():
    engine = PolicyEngine()

    class Tool:
        name = "time"
        capability = "read_only"

    decision = engine.evaluate(Tool())
    assert decision.decision == "allow"
    assert decision.requires_confirmation is False


def test_state_changing_requires_confirmation():
    engine = PolicyEngine()

    class Tool:
        name = "memory"
        capability = "state_changing"

    decision = engine.evaluate(Tool())
    assert decision.decision == "confirm"
    assert decision.requires_confirmation is True


def test_destructive_is_denied():
    engine = PolicyEngine()

    class Tool:
        name = "wipe"
        capability = "destructive"

    decision = engine.evaluate(Tool())
    assert decision.decision == "deny"
    assert decision.requires_confirmation is False


def test_unknown_capability_is_denied():
    engine = PolicyEngine()

    class Tool:
        name = "mystery"
        capability = "unknown"

    decision = engine.evaluate(Tool())
    assert decision.decision == "deny"
    assert decision.reason == "unknown capability"


def test_missing_capability_is_denied():
    engine = PolicyEngine()

    class Tool:
        name = "broken"
        capability = None

    decision = engine.evaluate(Tool())
    assert decision.decision == "deny"


def test_capability_enum_accepted():
    engine = PolicyEngine()

    from core.interfaces import Capability

    class Tool:
        name = "time"
        capability = Capability.READ_ONLY

    decision = engine.evaluate(Tool())
    assert decision.decision == "allow"


def test_evaluate_is_side_effect_free():
    engine = PolicyEngine()

    class Tool:
        name = "time"
        capability = "read_only"

        def run(self, context):
            return "executed"

    tool = Tool()
    decision = engine.evaluate(tool)
    assert decision.decision == "allow"
    assert not hasattr(tool, "executed")
