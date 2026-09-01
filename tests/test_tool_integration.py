from core.interfaces import Capability, ResultStatus, StructuredResult
from core.tool_adapter import ToolAdapter
from core.tool_registry import ToolRegistry
from policy.engine import PolicyEngine


def test_adapter_does_not_execute_policy():
    adapter = ToolAdapter(name="destructive", runnable=lambda: "done", capability=Capability.DESTRUCTIVE)
    decision = PolicyEngine().evaluate(adapter)
    assert decision.decision == "deny"
    result = adapter.run()
    assert result.status == ResultStatus.SUCCESS


def test_read_only_adapter_with_policy():
    adapter = ToolAdapter(name="time", runnable=lambda: "12:00", capability=Capability.READ_ONLY)
    decision = PolicyEngine().evaluate(adapter)
    assert decision.decision == "allow"
    result = adapter.run()
    assert result.payload == "12:00"


def test_state_changing_adapter_with_policy():
    adapter = ToolAdapter(name="memory", runnable=lambda: "saved", capability=Capability.STATE_CHANGING)
    decision = PolicyEngine().evaluate(adapter)
    assert decision.decision == "confirm"
    assert decision.requires_confirmation is True


def test_destructive_adapter_never_auto_allowed():
    adapter = ToolAdapter(name="wipe", runnable=lambda: "wiped", capability=Capability.DESTRUCTIVE)
    decision = PolicyEngine().evaluate(adapter)
    assert decision.decision == "deny"
    assert decision.requires_confirmation is False


def test_unknown_capability_adapter_fails_closed():
    adapter = ToolAdapter(name="mystery", runnable=lambda: "data", capability="unknown")
    decision = PolicyEngine().evaluate(adapter)
    assert decision.decision == "deny"


def test_existing_plugin_battery_wrapped():
    from plugins import battery
    adapter = ToolAdapter(name="battery", runnable=battery.run, capability=Capability.READ_ONLY)
    assert adapter.name == "battery"
    result = adapter.run()
    assert isinstance(result, StructuredResult)


def test_existing_plugin_storage_wrapped():
    from plugins import storage
    adapter = ToolAdapter(name="storage", runnable=storage.run, capability=Capability.READ_ONLY)
    assert adapter.name == "storage"
    result = adapter.run()
    assert isinstance(result, StructuredResult)


def test_existing_plugin_time_wrapped():
    from plugins import time
    adapter = ToolAdapter(name="time", runnable=time.run, capability=Capability.READ_ONLY)
    assert adapter.name == "time"
    result = adapter.run()
    assert isinstance(result, StructuredResult)


def test_existing_plugin_help_wrapped():
    from plugins import help as help_plugin
    adapter = ToolAdapter(name="help", runnable=help_plugin.run, capability=Capability.READ_ONLY)
    assert adapter.name == "help"
    result = adapter.run()
    assert isinstance(result, StructuredResult)
    assert "Available Commands" in (result.payload or "")


def test_existing_plugin_device_wrapped():
    from plugins import device
    adapter = ToolAdapter(name="device", runnable=device.run, capability=Capability.READ_ONLY)
    assert adapter.name == "device"
    result = adapter.run()
    assert isinstance(result, StructuredResult)


def test_existing_plugin_status_wrapped():
    from plugins import status
    adapter = ToolAdapter(name="status", runnable=status.run, capability=Capability.READ_ONLY)
    assert adapter.name == "status"
    result = adapter.run()
    assert isinstance(result, StructuredResult)


def test_existing_plugin_hello_wrapped():
    from plugins import hello
    adapter = ToolAdapter(name="hello", runnable=hello.run, capability=Capability.READ_ONLY)
    assert adapter.name == "hello"
    result = adapter.run()
    assert isinstance(result, StructuredResult)
    assert result.payload == "Hello! I am a new plugin."
