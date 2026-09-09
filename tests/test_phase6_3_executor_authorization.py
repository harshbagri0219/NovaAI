import ast
from pathlib import Path

import pytest

from core.execution_service import (
    ExecutionService,
    get_execution_service,
)
from core.tool_catalog import get_registry


PROJECT_ROOT = Path(__file__).resolve().parents[1]


PRODUCTION_FILES = [
    PROJECT_ROOT / "main.py",
    PROJECT_ROOT / "ai" / "decision.py",
    PROJECT_ROOT / "ai" / "task_executor.py",
    PROJECT_ROOT / "core" / "controlled_router.py",
]


def _imports_tool_executor(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module == "core.tool_executor":
                return True

        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "core.tool_executor":
                    return True

    return False


def _constructs_tool_executor(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            function = node.func

            if isinstance(function, ast.Name):
                if function.id == "ToolExecutor":
                    return True

            if isinstance(function, ast.Attribute):
                if function.attr == "ToolExecutor":
                    return True

    return False


def test_production_modules_do_not_import_tool_executor():
    violations = [
        str(path)
        for path in PRODUCTION_FILES
        if _imports_tool_executor(path)
    ]

    assert violations == []


def test_production_modules_do_not_construct_tool_executor():
    violations = [
        str(path)
        for path in PRODUCTION_FILES
        if _constructs_tool_executor(path)
    ]

    assert violations == []


def test_execution_service_is_authoritative_runtime_owner():
    service = get_execution_service()

    assert isinstance(service, ExecutionService)
    assert service._executor.__class__.__name__ == "ToolExecutor"


def test_runtime_execution_service_is_singleton():
    first = get_execution_service()
    second = get_execution_service()

    assert first is second


def test_execution_service_does_not_expose_raw_executor_property():
    service = get_execution_service()

    assert not hasattr(service, "executor")


def test_tool_catalog_is_explicit_and_nonempty():
    registry = get_registry()

    assert registry is not None
    assert registry.get("battery") is not None
    assert registry.get("storage") is not None
    assert registry.get("device") is not None


def test_llm_provider_has_no_tool_executor_import():
    path = PROJECT_ROOT / "ai" / "llm_provider.py"

    assert not _imports_tool_executor(path)


def test_brain_intelligence_has_no_tool_executor_import():
    path = PROJECT_ROOT / "brain" / "intelligence.py"

    assert not _imports_tool_executor(path)


def test_execution_service_exposes_only_authorized_execution_methods():
    service = get_execution_service()

    assert callable(service.execute)
    assert callable(service.execute_approved)

    assert not hasattr(service, "execute_confirmed")