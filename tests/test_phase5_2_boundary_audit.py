import ast
import os

import pytest

from core.controlled_router import handle_controlled_command
from core.router import handle_command
from core.tool_catalog import get_registry
from core.tool_executor import ToolExecutor
from core.tool_registry import ToolRegistry


RUNTIME_FILES = [
    "main.py",
    "ai/decision.py",
    "ai/task_coordinator.py",
    "ai/task_executor.py",
    "ai/task_planner.py",
    "core/router.py",
    "core/controlled_router.py",
    "core/tool_catalog.py",
    "core/tool_registry.py",
    "core/tool_adapter.py",
    "core/tool_executor.py",
    "policy/engine.py",
    "brain/brain.py",
    "brain/followup.py",
    "brain/reasoning.py",
    "brain/context.py",
    "brain/context_builder.py",
    "brain/context_resolver.py",
    "brain/topic_tracker.py",
    "knowledge/profile.py",
    "memory/memory.py",
    "memory/manager.py",
    "monitor/system_monitor.py",
    "plugins/__init__.py",
    "plugins/battery.py",
    "plugins/storage.py",
    "plugins/device.py",
    "plugins/time.py",
    "plugins/status.py",
    "plugins/help.py",
    "plugins/memory.py",
    "plugins/check_phone.py",
    "plugins/hello.py",
    "voice/speak.py",
    "voice/listen.py",
    "system/device.py",
    "state/system_state.py",
    "utils/logger.py",
    "startup.py",
    "config.py",
]


def _get_imports(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=filepath)
    except Exception:
        return set()

    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
    return imports


def test_legacy_router_has_no_active_runtime_callers():
    legacy_callers = []
    for rel_path in RUNTIME_FILES:
        filepath = os.path.join(os.path.dirname(__file__), "..", rel_path)
        if not os.path.isfile(filepath):
            continue
        imports = _get_imports(filepath)
        if "core.router" in imports:
            legacy_callers.append(rel_path)

    assert legacy_callers == [], (
        f"Expected no active runtime callers of core.router, found: {legacy_callers}"
    )


def test_controlled_router_does_not_fallback_to_legacy_router():
    imports = _get_imports(
        os.path.join(os.path.dirname(__file__), "..", "core", "controlled_router.py")
    )
    assert "core.router" not in imports, (
        "controlled_router must not import core.router to avoid fallback"
    )


def test_tool_catalog_is_single_source_of_truth():
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


def test_legacy_router_still_works():
    response = handle_command("What is my favorite language?", {})
    assert isinstance(response, str)


def test_controlled_router_read_only_allows_execution():
    registry = ToolRegistry.from_plugin_map({
        "time": lambda: "12:00",
    })
    executor = ToolExecutor()
    response = handle_controlled_command("What time is it?", {}, registry=registry, executor=executor)
    assert response == "12:00"


def test_controlled_router_state_changing_blocks_execution():
    registry = ToolRegistry.from_plugin_map({
        "battery": lambda: "50%",
    })
    executor = ToolExecutor()
    response = handle_controlled_command("battery", {}, registry=registry, executor=executor)
    from core.interfaces import ResultStatus, StructuredResult
    assert isinstance(response, StructuredResult)
    assert response.status == ResultStatus.CONFIRMATION_REQUIRED


def test_controlled_router_destructive_denies_execution():
    from core.tool_adapter import ToolAdapter
    from core.interfaces import Capability
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
    response = handle_controlled_command("totally unknown", {}, registry=registry, executor=executor)
    assert response is None


def test_unregistered_tool_fails_closed():
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


def test_task_executor_still_uses_controlled_path():
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


def test_no_fallback_after_deny():
    registry = ToolRegistry()
    executor = ToolExecutor()
    response = handle_controlled_command("battery", {}, registry=registry, executor=executor)
    assert response is None


def test_no_fallback_after_confirm():
    registry = ToolRegistry.from_plugin_map({
        "battery": lambda: "50%",
    })
    executor = ToolExecutor()
    response = handle_controlled_command("battery", {}, registry=registry, executor=executor)
    from core.interfaces import ResultStatus, StructuredResult
    assert isinstance(response, StructuredResult)
    assert response.status == ResultStatus.CONFIRMATION_REQUIRED


def test_no_fallback_after_error():
    def bad():
        raise RuntimeError("boom")

    registry = ToolRegistry.from_plugin_map({
        "time": bad,
    })
    executor = ToolExecutor()
    response = handle_controlled_command("What time is it?", {}, registry=registry, executor=executor)
    assert isinstance(response, str)
    assert "boom" in response
