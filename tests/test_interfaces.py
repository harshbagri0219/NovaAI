from core.interfaces import (
    Capability,
    PolicyDecision,
    ResultStatus,
    StructuredResult,
    Tool,
)


def test_structured_result_success():
    result = StructuredResult(
        status=ResultStatus.SUCCESS,
        payload={"key": "value"},
    )
    assert result.status == ResultStatus.SUCCESS
    assert result.payload == {"key": "value"}
    assert result.error is None


def test_structured_result_error():
    result = StructuredResult(
        status=ResultStatus.ERROR,
        error="something failed",
    )
    assert result.status == ResultStatus.ERROR
    assert result.error == "something failed"
    assert result.payload is None


def test_policy_decision_allow():
    decision = PolicyDecision(decision="allow")
    assert decision.decision == "allow"
    assert decision.requires_confirmation is False
    assert decision.reason is None


def test_policy_decision_deny():
    decision = PolicyDecision(decision="deny", reason="not permitted")
    assert decision.decision == "deny"
    assert decision.reason == "not permitted"
    assert decision.requires_confirmation is False


def test_policy_decision_confirm():
    decision = PolicyDecision(
        decision="confirm",
        requires_confirmation=True,
    )
    assert decision.decision == "confirm"
    assert decision.requires_confirmation is True


def test_tool_protocol_accepts_compatible_class():
    class MyTool:
        name = "test_tool"
        capability = Capability.READ_ONLY

        def run(self, context):
            return StructuredResult(
                status=ResultStatus.SUCCESS,
                payload=context,
            )

    tool = MyTool()
    assert isinstance(tool, Tool)
    assert tool.name == "test_tool"
    assert tool.capability == Capability.READ_ONLY


def test_tool_protocol_rejects_incompatible():
    class NotATool:
        pass

    assert not isinstance(NotATool(), Tool)


def test_capability_enum_values():
    assert Capability.READ_ONLY == "read_only"
    assert Capability.STATE_CHANGING == "state_changing"
    assert Capability.DESTRUCTIVE == "destructive"


def test_result_status_enum_values():
    assert ResultStatus.SUCCESS == "success"
    assert ResultStatus.ERROR == "error"
