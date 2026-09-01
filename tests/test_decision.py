import ast
import os

import pytest

from ai.decision import decide
from core.interfaces import Capability, ResultStatus, StructuredResult
from core.tool_adapter import ToolAdapter
from core.tool_registry import ToolRegistry
from core.tool_executor import ToolExecutor


def test_decision_does_not_import_legacy_router():
    filepath = os.path.join(os.path.dirname(__file__), "..", "ai", "decision.py")
    with open(filepath, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=filepath)

    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)

    assert "core.router" not in imports
    assert "handle_command" not in [n.id for n in ast.walk(tree) if isinstance(n, ast.Name)]


def test_decision_allows_read_only_tool():
    registry = ToolRegistry.from_plugin_map({
        "time": lambda: "12:00",
    })
    executor = ToolExecutor()
    response = decide("What time is it?", {}, registry=registry, executor=executor)
    assert response == "12:00"


def test_decision_confirm_never_executes():
    call_count = 0

    def stateful():
        nonlocal call_count
        call_count += 1
        return "executed"

    adapter = ToolAdapter(name="time", runnable=stateful, capability=Capability.STATE_CHANGING)
    registry = ToolRegistry()
    registry.register(adapter)
    executor = ToolExecutor()
    response = decide("What time is it?", {}, registry=registry, executor=executor)
    assert isinstance(response, StructuredResult)
    assert response.status == ResultStatus.CONFIRMATION_REQUIRED
    assert call_count == 0


def test_decision_deny_never_executes():
    call_count = 0

    def destructive():
        nonlocal call_count
        call_count += 1
        return "wiped"

    adapter = ToolAdapter(name="time", runnable=destructive, capability=Capability.DESTRUCTIVE)
    registry = ToolRegistry()
    registry.register(adapter)
    executor = ToolExecutor()
    response = decide("What time is it?", {}, registry=registry, executor=executor)
    assert isinstance(response, str)
    assert "not permitted" in response
    assert call_count == 0


def test_decision_unknown_intent_falls_back_to_brain():
    registry = ToolRegistry()
    executor = ToolExecutor()
    response = decide("Tell me something completely random", {}, registry=registry, executor=executor)
    assert isinstance(response, str)
    assert response


def test_decision_plugin_exception_becomes_error():
    def bad():
        raise RuntimeError("boom")

    registry = ToolRegistry.from_plugin_map({
        "time": bad,
    })
    executor = ToolExecutor()
    response = decide("What time is it?", {}, registry=registry, executor=executor)
    assert isinstance(response, str)
    assert "boom" in response


def test_decision_unregistered_tool_falls_back_to_brain():
    registry = ToolRegistry()
    executor = ToolExecutor()
    response = decide("battery", {}, registry=registry, executor=executor)
    assert isinstance(response, str)
    assert response


def test_decision_no_fallback_to_legacy_router():
    registry = ToolRegistry()
    executor = ToolExecutor()
    response = decide("battery", {}, registry=registry, executor=executor)
    assert isinstance(response, str)
    assert response


def test_decision_learning_still_works():
    response = decide("my name is Nova", {})
    assert isinstance(response, str)
    assert response


def test_decision_task_coordination_still_works():
    response = decide("battery and storage", {})
    assert isinstance(response, str)
    assert response


def test_decision_uses_controlled_execution():
    call_count = 0

    def counting():
        nonlocal call_count
        call_count += 1
        return "ok"

    registry = ToolRegistry.from_plugin_map({
        "time": counting,
    })
    executor = ToolExecutor()
    response = decide("What time is it?", {}, registry=registry, executor=executor)
    assert response == "ok"
    assert call_count == 1
