import pytest

from core.interfaces import Capability, ResultStatus, StructuredResult, Tool

from core.tool_adapter import ToolAdapter


def test_adapter_exposes_tool_protocol():
    def my_run():
        return "hello"

    adapter = ToolAdapter(
        name="hello",
        runnable=my_run,
        capability=Capability.READ_ONLY,
    )

    assert isinstance(adapter, Tool)
    assert adapter.name == "hello"
    assert adapter.capability == Capability.READ_ONLY


def test_adapter_exposes_read_only_capability():
    adapter = ToolAdapter(
        name="time",
        runnable=lambda: "now",
        capability=Capability.READ_ONLY,
    )

    assert adapter.capability == Capability.READ_ONLY


def test_adapter_run_returns_structured_result_success():
    adapter = ToolAdapter(
        name="hello",
        runnable=lambda: "hello",
        capability=Capability.READ_ONLY,
    )

    result = adapter.run()

    assert isinstance(result, StructuredResult)
    assert result.status == ResultStatus.SUCCESS
    assert result.payload == "hello"
    assert result.error is None


def test_adapter_run_returns_structured_result_on_exception():
    def bad(ctx):
        raise RuntimeError("boom")

    adapter = ToolAdapter(
        name="bad",
        runnable=bad,
        capability=Capability.STATE_CHANGING,
    )

    result = adapter.run(context={})

    assert isinstance(result, StructuredResult)
    assert result.status == ResultStatus.ERROR
    assert "boom" in (result.error or "")


def test_adapter_passthrough_structured_result():
    existing = StructuredResult(
        status=ResultStatus.SUCCESS,
        payload={"x": 1},
    )

    adapter = ToolAdapter(
        name="passthrough",
        runnable=lambda: existing,
        capability=Capability.READ_ONLY,
    )

    result = adapter.run()

    assert result is existing


def test_adapter_missing_capability_raises():
    with pytest.raises(ValueError):
        ToolAdapter(
            name="unknown",
            runnable=lambda: None,
            capability=None,
        )


def test_adapter_name_is_readonly():
    adapter = ToolAdapter(
        name="hello",
        runnable=lambda: None,
        capability=Capability.READ_ONLY,
    )

    try:
        adapter.name = "changed"
    except AttributeError:
        pass

    assert adapter.name == "hello"


def test_registry_register_and_get():
    from core.tool_registry import ToolRegistry

    adapter = ToolAdapter(
        name="time",
        runnable=lambda: "12:00",
        capability=Capability.READ_ONLY,
    )

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
        "time": (
            lambda: "12:00",
            Capability.READ_ONLY,
        ),
        "help": (
            lambda: "help text",
            Capability.READ_ONLY,
        ),
        "battery": (
            lambda: {"percentage": 50},
            Capability.STATE_CHANGING,
        ),
    }

    registry = ToolRegistry.from_plugin_map(plugin_map)

    assert registry.get("time").capability == Capability.READ_ONLY
    assert registry.get("help").capability == Capability.READ_ONLY
    assert registry.get("battery").capability == Capability.STATE_CHANGING

    result = registry.get("time").run()

    assert result.payload == "12:00"


def test_registry_from_plugin_map_error_safety():
    from core.tool_registry import ToolRegistry

    def bad(ctx):
        raise ValueError("fail")

    plugin_map = {
        "bad": (
            bad,
            Capability.STATE_CHANGING,
        ),
    }

    registry = ToolRegistry.from_plugin_map(plugin_map)

    result = registry.get("bad").run(context={})

    assert result.status == ResultStatus.ERROR
    assert "fail" in (result.error or "")


def test_registry_rejects_missing_explicit_capability():
    from core.tool_registry import ToolRegistry

    plugin_map = {
        "battery": lambda: "50%",
    }

    with pytest.raises(TypeError):
        ToolRegistry.from_plugin_map(plugin_map)


def test_tool_name_does_not_determine_capability():
    from core.tool_registry import ToolRegistry

    plugin_map = {
        "time": (
            lambda: "12:00",
            Capability.STATE_CHANGING,
        ),
    }

    registry = ToolRegistry.from_plugin_map(plugin_map)

    assert registry.get("time").capability == Capability.STATE_CHANGING


def test_adapter_run_passes_context_to_callable():
    received = {}

    def context_tool(ctx):
        received["ctx"] = ctx
        return "ok"

    adapter = ToolAdapter(
        name="ctx",
        runnable=context_tool,
        capability=Capability.STATE_CHANGING,
    )

    result = adapter.run(context={"key": "value"})

    assert result.status == ResultStatus.SUCCESS
    assert result.payload == "ok"
    assert received["ctx"] == {"key": "value"}


def test_adapter_run_no_arg_callable_executes_without_context():
    call_count = 0

    def no_arg_tool():
        nonlocal call_count
        call_count += 1
        return "ok"

    adapter = ToolAdapter(
        name="noarg",
        runnable=no_arg_tool,
        capability=Capability.READ_ONLY,
    )

    result = adapter.run(context={"ignored": True})

    assert result.status == ResultStatus.SUCCESS
    assert result.payload == "ok"
    assert call_count == 1


def test_adapter_internal_type_error_is_not_retried():
    call_count = 0

    def bad(ctx):
        nonlocal call_count
        call_count += 1
        raise TypeError("internal type error")

    adapter = ToolAdapter(
        name="bad",
        runnable=bad,
        capability=Capability.STATE_CHANGING,
    )

    result = adapter.run(context={})

    assert result.status == ResultStatus.ERROR
    assert "internal type error" in (result.error or "")
    assert call_count == 1


def test_adapter_runs_exactly_once():
    call_count = 0

    def counting():
        nonlocal call_count

    def counting():
        nonlocal call_count
        call_count += 1
        return "ok"

    adapter = ToolAdapter(
        name="count",
        runnable=counting,
        capability=Capability.READ_ONLY,
    )

    result = adapter.run()

    assert result.status == ResultStatus.SUCCESS
    assert result.payload == "ok"
    assert call_count == 1


# New regression tests for Phase 6.1

def test_adapter_capability_mutation_after_init_raises():
    adapter = ToolAdapter(
        name="test",
        runnable=lambda: None,
        capability=Capability.READ_ONLY,
    )
    with pytest.raises(AttributeError):
        adapter.capability = Capability.STATE_CHANGING

def test_adapter_capability_attr_mutation_after_init_raises():
    adapter = ToolAdapter(
        name="test",
        runnable=lambda: None,
        capability=Capability.READ_ONLY,
    )
    with pytest.raises(AttributeError):
        adapter._capability = Capability.STATE_CHANGING

def test_adapter_capability_name_mangled_mutation_after_init_raises():
    adapter = ToolAdapter(
        name="test",
        runnable=lambda: None,
        capability=Capability.READ_ONLY,
    )
    with pytest.raises(AttributeError):
        adapter.__capability = Capability.STATE_CHANGING

def test_registered_readonly_adapter_cannot_be_mutated():
    from core.tool_registry import ToolRegistry
    adapter = ToolAdapter(
        name="readonly",
        runnable=lambda: "ok",
        capability=Capability.READ_ONLY,
    )
    registry = ToolRegistry()
    registry.register(adapter)
    with pytest.raises(AttributeError):
        adapter.capability = Capability.STATE_CHANGING

def test_registered_destructive_adapter_cannot_be_mutated():
    from core.tool_registry import ToolRegistry
    adapter = ToolAdapter(
        name="destructive",
        runnable=lambda: "ok",
        capability=Capability.DESTRUCTIVE,
    )
    registry = ToolRegistry()
    registry.register(adapter)
    with pytest.raises(AttributeError):
        adapter.capability = Capability.READ_ONLY