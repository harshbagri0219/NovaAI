import pytest

from ai.decision import decide
from core.confirmation import ConfirmationManager
from core.interfaces import Capability, ConfirmationStatus, ResultStatus, StructuredResult
from core.tool_adapter import ToolAdapter
from core.tool_executor import ToolExecutor
from core.tool_registry import ToolRegistry


def test_read_only_executes_end_to_end():
    registry = ToolRegistry.from_plugin_map({
        "time": lambda: "12:00",
    })
    executor = ToolExecutor()
    response = decide("What time is it?", {}, registry=registry, executor=executor)
    assert response == "12:00"


def test_state_changing_creates_confirmation_end_to_end():
    registry = ToolRegistry.from_plugin_map({
        "device": lambda: "50%",
    })
    executor = ToolExecutor()
    response = decide("device", {}, registry=registry, executor=executor)
    assert isinstance(response, StructuredResult)
    assert response.status == ResultStatus.CONFIRMATION_REQUIRED
    assert response.confirmation_request is not None
    assert response.confirmation_request.tool_name == "device"
    assert response.confirmation_request.status == ConfirmationStatus.PENDING


def test_confirmation_does_not_execute_end_to_end():
    call_count = 0

    def stateful():
        nonlocal call_count
        call_count += 1
        return "executed"

    registry = ToolRegistry.from_plugin_map({
        "device": stateful,
    })
    executor = ToolExecutor()
    response = decide("device", {}, registry=registry, executor=executor)
    assert isinstance(response, StructuredResult)
    assert response.status == ResultStatus.CONFIRMATION_REQUIRED
    assert call_count == 0


def test_approved_execution_end_to_end():
    manager = ConfirmationManager()
    executor = ToolExecutor(confirmation_manager=manager)

    tool = ToolAdapter(name="battery", runnable=lambda: "50%", capability=Capability.STATE_CHANGING)
    registry = ToolRegistry()
    registry.register(tool)

    result = executor.execute(tool)
    request = result.confirmation_request
    manager.approve(request.request_id)

    executed = executor.execute_approved(request.request_id, registry=registry)
    assert executed.status == ResultStatus.SUCCESS
    assert executed.payload == "50%"


def test_denial_does_not_execute_end_to_end():
    manager = ConfirmationManager()
    executor = ToolExecutor(confirmation_manager=manager)

    tool = ToolAdapter(name="battery", runnable=lambda: "50%", capability=Capability.STATE_CHANGING)
    result = executor.execute(tool)
    request = result.confirmation_request
    manager.deny(request.request_id)

    executed = executor.execute_approved(request.request_id, registry=ToolRegistry())
    assert executed.status == ResultStatus.ERROR


def test_expiration_does_not_execute_end_to_end():
    manager = ConfirmationManager(ttl_seconds=300)
    executor = ToolExecutor(confirmation_manager=manager)

    tool = ToolAdapter(name="battery", runnable=lambda: "50%", capability=Capability.STATE_CHANGING)
    result = executor.execute(tool)
    request = result.confirmation_request
    manager.approve(request.request_id)
    request.expires_at = __import__("datetime").datetime.utcnow() - __import__("datetime").timedelta(seconds=1)

    executed = executor.execute_approved(request.request_id, registry=ToolRegistry())
    assert executed.status == ResultStatus.ERROR


def test_replay_blocked_end_to_end():
    manager = ConfirmationManager()
    executor = ToolExecutor(confirmation_manager=manager)

    tool = ToolAdapter(name="battery", runnable=lambda: "50%", capability=Capability.STATE_CHANGING)
    registry = ToolRegistry()
    registry.register(tool)

    result = executor.execute(tool)
    request = result.confirmation_request
    manager.approve(request.request_id)

    executor.execute_approved(request.request_id, registry=registry)
    second = executor.execute_approved(request.request_id, registry=registry)
    assert second.status == ResultStatus.ERROR


def test_wrong_tool_blocked_end_to_end():
    manager = ConfirmationManager()
    executor = ToolExecutor(confirmation_manager=manager)

    tool_a = ToolAdapter(name="tool_a", runnable=lambda: "a", capability=Capability.STATE_CHANGING)
    tool_b = ToolAdapter(name="tool_b", runnable=lambda: "b", capability=Capability.STATE_CHANGING)
    registry = ToolRegistry()
    registry.register(tool_a)
    registry.register(tool_b)

    result = executor.execute(tool_a)
    request = result.confirmation_request
    manager.approve(request.request_id)

    executed = executor.execute_approved(request.request_id, registry=registry)
    assert executed.status == ResultStatus.SUCCESS
    assert executed.payload == "a"

    unregistered = ToolRegistry()
    bad = executor.execute_approved(request.request_id, registry=unregistered)
    assert bad.status == ResultStatus.ERROR


def test_unknown_request_id_fails_closed_end_to_end():
    executor = ToolExecutor()
    executed = executor.execute_approved("missing", registry=ToolRegistry())
    assert executed.status == ResultStatus.ERROR


def test_policy_denial_cannot_be_overridden_end_to_end():
    manager = ConfirmationManager()
    executor = ToolExecutor(confirmation_manager=manager)

    tool = ToolAdapter(name="battery", runnable=lambda: "wiped", capability=Capability.DESTRUCTIVE)
    result = executor.execute(tool)
    assert result.status == ResultStatus.ERROR

    executed = executor.execute_approved("missing", registry=ToolRegistry())
    assert executed.status == ResultStatus.ERROR


def test_ai_cannot_self_approve_end_to_end():
    registry = ToolRegistry.from_plugin_map({
        "device": lambda: "50%",
    })
    executor = ToolExecutor()
    response = decide("device", {}, registry=registry, executor=executor)
    assert isinstance(response, StructuredResult)
    assert response.status == ResultStatus.CONFIRMATION_REQUIRED
    assert response.confirmation_request is not None
    assert response.confirmation_request.status == ConfirmationStatus.PENDING


def test_complete_decision_authorization_execution_flow():
    manager = ConfirmationManager()
    executor = ToolExecutor(confirmation_manager=manager)

    tool = ToolAdapter(name="device", runnable=lambda: "50%", capability=Capability.STATE_CHANGING)
    registry = ToolRegistry()
    registry.register(tool)

    response = decide("device", {}, registry=registry, executor=executor)
    assert isinstance(response, StructuredResult)
    assert response.status == ResultStatus.CONFIRMATION_REQUIRED
    request = response.confirmation_request
    assert request is not None
    assert request.tool_name == "device"
    assert request.status == ConfirmationStatus.PENDING

    manager.approve(request.request_id)
    executed = executor.execute_approved(request.request_id, registry=registry)
    assert executed.status == ResultStatus.SUCCESS
    assert executed.payload == "50%"
