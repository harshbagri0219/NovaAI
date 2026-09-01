import pytest

from core.interfaces import Capability, ResultStatus, StructuredResult, Tool
from core.tool_adapter import ToolAdapter


def test_adapter_exposes_tool_protocol():
    def my_run():
        return "hello"

    adapter = ToolAdapter(name="hello", runnable=my_run)
    assert isinstance(adapter, Tool)
    assert adapter.name == "hello"
    assert adapter.capability == Capability.STATE_CHANGING


def test_adapter_exposes_read_only_capability():
    adapter = ToolAdapter(name="time", runnable=lambda: "now", capability=Capability.READ_ONLY)
    assert adapter.capability == Capability.READ_ONLY


def test_adapter_run_returns_structured_result_success():
    adapter = ToolAdapter(name="hello", runnable=lambda: "hello")
    result = adapter.run()
    assert isinstance(result, StructuredResult)
    assert result.status == ResultStatus.SUCCESS
    assert result.payload == "hello"
    assert result.error is None


def test_adapter_run_returns_structured_result_on_exception():
    def bad():
        raise RuntimeError("boom")

    adapter = ToolAdapter(name="bad", runnable=bad)
    result = adapter.run()
    assert isinstance(result, StructuredResult)
    assert result.status == ResultStatus.ERROR
    assert "boom" in (result.error or "")


def test_adapter_passthrough_structured_result():
    existing = StructuredResult(status=ResultStatus.SUCCESS, payload={"x": 1})
    adapter = ToolAdapter(name="passthrough", runnable=lambda: existing)
    result = adapter.run()
    assert result is existing


def test_adapter_default_capability_is_state_changing():
    adapter = ToolAdapter(name="unknown", runnable=lambda: None)
    assert adapter.capability == Capability.STATE_CHANGING


def test_adapter_name_is_readonly():
    adapter = ToolAdapter(name="hello", runnable=lambda: None)
    try:
        adapter.name = "changed"
    except AttributeError:
        pass
    assert adapter.name == "hello"


def test_registry_register_and_get():
    from core.tool_registry import ToolRegistry
    adapter = ToolAdapter(name="time", runnable=lambda: "12:00")
    registry = ToolRegistry()
    registry.register(adapter)
    assert registry.get("time") is adapter
    assert registry.get("missing") is None


def test_registry_rejects_non_adapter():
    from core.tool_registry import ToolRegistry
    registry = ToolRegistry()
    with pytest.raises(TypeError):
        registry.register("not an adapter")


def test_registry_from_plugin_map():
    from core.tool_registry import ToolRegistry
    plugin_map = {
        "time": lambda: "12:00",
        "help": lambda: "help text",
        "battery": lambda: {"percentage": 50},
    }
    registry = ToolRegistry.from_plugin_map(plugin_map)
    assert registry.get("time").capability == Capability.READ_ONLY
    assert registry.get("help").capability == Capability.READ_ONLY
    assert registry.get("battery").capability == Capability.STATE_CHANGING
    result = registry.get("time").run()
    assert result.payload == "12:00"


def test_registry_from_plugin_map_error_safety():
    from core.tool_registry import ToolRegistry

    def bad():
        raise ValueError("fail")

    plugin_map = {"bad": bad}
    registry = ToolRegistry.from_plugin_map(plugin_map)
    result = registry.get("bad").run()
    assert result.status == ResultStatus.ERROR
    assert "fail" in (result.error or "")
