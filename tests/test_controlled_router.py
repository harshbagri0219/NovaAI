import pytest

from core.interfaces import Capability, ResultStatus, StructuredResult
from core.controlled_router import handle_controlled_command
from core.tool_adapter import ToolAdapter
from core.tool_catalog import get_registry
from core.tool_registry import ToolRegistry
from core.tool_executor import ToolExecutor
from core.router import handle_command


def test_centralized_catalog_contains_only_explicit_tools():
    registry = get_registry()
    names = set(registry.all().keys())
    assert names == {
        "battery",
        "storage",
        "device",
        "time",
        "status",
        "help",
        "memory",
        "check_phone",
        "hello",
    }


def test_battery_is_explicitly_registered():
    registry = get_registry()
    tool = registry.get("battery")
    assert tool is not None
    assert tool.name == "battery"
    assert tool.capability == Capability.READ_ONLY


def test_storage_is_explicitly_registered():
    registry = get_registry()
    tool = registry.get("storage")
    assert tool is not None
    assert tool.name == "storage"
    assert tool.capability == Capability.READ_ONLY


def test_arbitrary_plugin_is_not_automatically_executable():
    registry = get_registry()
    assert registry.get("totally_random_plugin") is None


def test_read_only_tool_allowed_and_executes():
    registry = ToolRegistry.from_plugin_map({
        "time": lambda: "12:00",
    })
    executor = ToolExecutor()
    response = handle_controlled_command("What time is it?", {}, registry=registry, executor=executor)
    assert response == "12:00"


def test_state_changing_tool_returns_confirmation_required():
    registry = ToolRegistry.from_plugin_map({
        "battery": lambda: "50%",
    })
    executor = ToolExecutor()
    response = handle_controlled_command("battery", {}, registry=registry, executor=executor)
    assert isinstance(response, StructuredResult)
    assert response.status == ResultStatus.CONFIRMATION_REQUIRED


def test_destructive_tool_returns_error():
    adapter = ToolAdapter(name="battery", runnable=lambda: "wiped", capability=Capability.DESTRUCTIVE)
    registry = ToolRegistry()
    registry.register(adapter)
    executor = ToolExecutor()
    response = handle_controlled_command("battery", {}, registry=registry, executor=executor)
    assert isinstance(response, str)
    assert "not permitted" in response


def test_unknown_intent_fails_closed():
    registry = ToolRegistry()
    executor = ToolExecutor()
    response = handle_controlled_command("completely unknown intent", {}, registry=registry, executor=executor)
    assert response is None


def test_unregistered_callable_cannot_execute():
    registry = ToolRegistry()
    executor = ToolExecutor()
    response = handle_controlled_command("What time is it?", {}, registry=registry, executor=executor)
    assert response is None


def test_plugin_exception_becomes_structured_error():
    def bad():
        raise RuntimeError("boom")

    registry = ToolRegistry.from_plugin_map({
        "time": bad,
    })
    executor = ToolExecutor()
    response = handle_controlled_command("What time is it?", {}, registry=registry, executor=executor)
    assert isinstance(response, str)
    assert "boom" in response


def test_legacy_router_still_works():
    response = handle_command("What is my favorite language?", {})
    assert isinstance(response, str)


def test_allow_executes_exactly_once():
    call_count = 0

    def counting():
        nonlocal call_count
        call_count += 1
        return "ok"

    registry = ToolRegistry.from_plugin_map({
        "time": counting,
    })
    executor = ToolExecutor()
    response = handle_controlled_command("What time is it?", {}, registry=registry, executor=executor)
    assert response == "ok"
    assert call_count == 1


def test_confirm_never_executes():
    call_count = 0

    def stateful():
        nonlocal call_count
        call_count += 1
        return "executed"

    registry = ToolRegistry.from_plugin_map({
        "battery": stateful,
    })
    executor = ToolExecutor()
    response = handle_controlled_command("battery", {}, registry=registry, executor=executor)
    assert isinstance(response, StructuredResult)
    assert response.status == ResultStatus.CONFIRMATION_REQUIRED
    assert call_count == 0


def test_deny_never_executes():
    call_count = 0

    def destructive():
        nonlocal call_count
        call_count += 1
        return "wiped"

    adapter = ToolAdapter(name="battery", runnable=destructive, capability=Capability.DESTRUCTIVE)
    registry = ToolRegistry()
    registry.register(adapter)
    executor = ToolExecutor()
    response = handle_controlled_command("battery", {}, registry=registry, executor=executor)
    assert isinstance(response, str)
    assert call_count == 0


def test_task_executor_uses_controlled_path():
    from ai.task_executor import execute_plan

    plan = [
        {"task": "battery", "description": "Check battery"},
        {"task": "storage", "description": "Check storage"},
    ]

    results = execute_plan(plan, {})
    assert len(results) == 2
    assert results[0]["task"] == "battery"
    assert results[1]["task"] == "storage"
    for item in results:
        assert item["result"] is not None


def test_no_duplicate_execution():
    call_count = 0

    def counting():
        nonlocal call_count
        call_count += 1
        return "ok"

    registry = ToolRegistry.from_plugin_map({
        "time": counting,
    })
    executor = ToolExecutor()
    for _ in range(5):
        response = handle_controlled_command("What time is it?", {}, registry=registry, executor=executor)
        assert response == "ok"
    assert call_count == 5


def test_controlled_router_normalizes_non_string_payload():
    registry = ToolRegistry.from_plugin_map({
        "time": lambda: {"key": "value"},
    })
    executor = ToolExecutor()
    response = handle_controlled_command("What time is it?", {}, registry=registry, executor=executor)
    assert response == "{'key': 'value'}"


def test_context_reaches_intended_tool():
    received = {}

    def context_tool(ctx):
        received["ctx"] = ctx
        return "ok"

    adapter = ToolAdapter(name="memory", runnable=context_tool, capability=Capability.READ_ONLY)
    registry = ToolRegistry()
    registry.register(adapter)
    executor = ToolExecutor()
    memory = {"owner": "Harshvardhan"}
    result = executor.execute(adapter, context=memory)
    assert result.status == ResultStatus.SUCCESS
    assert result.payload == "ok"
    assert received["ctx"] == memory


def test_no_fallback_to_legacy_router_after_deny():
    registry = ToolRegistry()
    executor = ToolExecutor()
    response = handle_controlled_command("battery", {}, registry=registry, executor=executor)
    assert response is None


def test_no_fallback_to_legacy_router_after_confirm():
    registry = ToolRegistry.from_plugin_map({
        "battery": lambda: "50%",
    })
    executor = ToolExecutor()
    response = handle_controlled_command("battery", {}, registry=registry, executor=executor)
    assert isinstance(response, StructuredResult)
    assert response.status == ResultStatus.CONFIRMATION_REQUIRED


def test_no_fallback_to_legacy_router_after_error():
    def bad():
        raise RuntimeError("boom")

    registry = ToolRegistry.from_plugin_map({
        "time": bad,
    })
    executor = ToolExecutor()
    response = handle_controlled_command("What time is it?", {}, registry=registry, executor=executor)
    assert isinstance(response, str)
    assert "boom" in response
