import pytest

from core.interfaces import Capability, ResultStatus, StructuredResult, Tool
from core.tool_adapter import ToolAdapter
from core.tool_executor import ToolExecutor
from policy.engine import PolicyEngine


class DummyReadTool:
    name = "time"
    capability = Capability.READ_ONLY

    def run(self, context):
        return "12:00"


class DummyStateTool:
    name = "memory"
    capability = Capability.STATE_CHANGING

    def run(self, context):
        return "saved"


class DummyDestructiveTool:
    name = "wipe"
    capability = Capability.DESTRUCTIVE

    def run(self, context):
        return "wiped"


class DummyUnknownTool:
    name = "mystery"
    capability = "unknown"

    def run(self, context):
        return "data"


class DummyNoCapTool:
    name = "broken"
    capability = None

    def run(self, context):
        return "done"


class DummyExceptionTool:
    name = "bad"
    capability = Capability.READ_ONLY

    def run(self, context):
        raise RuntimeError("boom")


def test_read_only_tool_allowed_and_executes():
    executor = ToolExecutor()
    tool = DummyReadTool()
    result = executor.execute(tool)
    assert result.status == ResultStatus.SUCCESS
    assert result.payload == "12:00"
    assert result.error is None


def test_state_changing_tool_does_not_execute():
    executor = ToolExecutor()
    tool = DummyStateTool()
    result = executor.execute(tool)
    assert result.status == ResultStatus.CONFIRMATION_REQUIRED
    assert result.error is not None
    assert result.payload is None


def test_destructive_tool_does_not_execute():
    executor = ToolExecutor()
    tool = DummyDestructiveTool()
    result = executor.execute(tool)
    assert result.status == ResultStatus.ERROR
    assert result.payload is None
    assert result.error is not None


def test_unknown_capability_fails_closed():
    executor = ToolExecutor()
    tool = DummyUnknownTool()
    result = executor.execute(tool)
    assert result.status == ResultStatus.ERROR
    assert result.payload is None


def test_missing_capability_fails_closed():
    executor = ToolExecutor()
    tool = DummyNoCapTool()
    result = executor.execute(tool)
    assert result.status == ResultStatus.ERROR
    assert result.payload is None


def test_none_tool_fails_closed():
    executor = ToolExecutor()
    result = executor.execute(None)
    assert result.status == ResultStatus.ERROR
    assert result.payload is None


def test_non_tool_object_fails_closed():
    executor = ToolExecutor()
    result = executor.execute("not a tool")
    assert result.status == ResultStatus.ERROR
    assert result.payload is None


def test_plugin_exception_becomes_structured_error():
    executor = ToolExecutor()
    tool = DummyExceptionTool()
    result = executor.execute(tool)
    assert result.status == ResultStatus.ERROR
    assert "boom" in (result.error or "")
    assert result.payload is None


def test_confirmation_cannot_accidentally_execute():
    executor = ToolExecutor()

    class ConfirmingTool:
        name = "stateful"
        capability = Capability.STATE_CHANGING
        executed = False

        def run(self, context):
            ConfirmingTool.executed = True
            return "executed"

    tool = ConfirmingTool()
    result = executor.execute(tool)
    assert result.status == ResultStatus.CONFIRMATION_REQUIRED
    assert ConfirmingTool.executed is False


def test_deny_never_executes():
    executor = ToolExecutor()

    class DeniedTool:
        name = "destructive"
        capability = Capability.DESTRUCTIVE
        executed = False

        def run(self, context):
            DeniedTool.executed = True
            return "executed"

    tool = DeniedTool()
    result = executor.execute(tool)
    assert result.status == ResultStatus.ERROR
    assert DeniedTool.executed is False


def test_allow_executes_exact_registered_tool():
    executor = ToolExecutor()

    class CountingTool:
        name = "counter"
        capability = Capability.READ_ONLY
        count = 0

        def run(self, context):
            CountingTool.count += 1
            return CountingTool.count

    tool = CountingTool()
    result1 = executor.execute(tool)
    result2 = executor.execute(tool)
    assert result1.payload == 1
    assert result2.payload == 2
    assert CountingTool.count == 2


def test_executor_does_not_bypass_policy():
    class NoPolicyEngine:
        def evaluate(self, tool, context):
            return PolicyEngine().evaluate(tool, context)

    executor = ToolExecutor(policy_engine=NoPolicyEngine())
    tool = DummyStateTool()
    result = executor.execute(tool)
    assert result.status == ResultStatus.CONFIRMATION_REQUIRED


def test_tool_adapter_works_with_executor():
    adapter = ToolAdapter(
        name="adapter_time",
        runnable=lambda: "now",
        capability=Capability.READ_ONLY,
    )
    executor = ToolExecutor()
    result = executor.execute(adapter)
    assert result.status == ResultStatus.SUCCESS
    assert result.payload == "now"
