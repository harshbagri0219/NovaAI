import ast
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MAIN_FILE = PROJECT_ROOT / "main.py"


def _tree():
    return ast.parse(MAIN_FILE.read_text(encoding="utf-8"))


def _imports_module(module_name):
    tree = _tree()

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module == module_name:
                return True

        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == module_name:
                    return True

    return False


def _imports_symbol(module_name, symbol_name):
    tree = _tree()

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module == module_name:
                if any(
                    alias.name == symbol_name
                    for alias in node.names
                ):
                    return True

        elif isinstance(node, ast.Import):
            for alias in node.names:
                if (
                    alias.name == module_name
                    and alias.asname == symbol_name
                ):
                    return True

    return False


def _calls_symbol(symbol_name):
    tree = _tree()

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            function = node.func

            if isinstance(function, ast.Name):
                if function.id == symbol_name:
                    return True

    return False


def _calls_attribute(attribute_name):
    tree = _tree()

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            function = node.func

            if isinstance(function, ast.Attribute):
                if function.attr == attribute_name:
                    return True

    return False


def _constructs_tool_executor():
    tree = _tree()

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


def test_main_imports_voice_input():
    assert _imports_symbol(
        "voice.listen",
        "listen",
    )


def test_main_imports_voice_output():
    assert _imports_symbol(
        "voice.speak",
        "speak",
    )


def test_main_imports_decision_engine():
    assert _imports_symbol(
        "ai.decision",
        "decide",
    )


def test_main_imports_execution_service_factory():
    assert _imports_symbol(
        "core.execution_service",
        "get_execution_service",
    )


def test_main_imports_explicit_tool_catalog():
    assert _imports_symbol(
        "core.tool_catalog",
        "get_registry",
    )


def test_main_calls_voice_input():
    assert _calls_symbol("listen")


def test_main_calls_voice_output():
    assert _calls_symbol("speak")


def test_main_calls_decision_engine():
    assert _calls_symbol("decide")


def test_main_does_not_import_tool_executor():
    assert not _imports_module("core.tool_executor")


def test_main_does_not_construct_tool_executor():
    assert not _constructs_tool_executor()


def test_main_does_not_directly_call_tool_run():
    assert not _calls_attribute("run")


def test_main_does_not_directly_call_executor_execute():
    tree = _tree()

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            function = node.func

            if isinstance(function, ast.Attribute):
                if function.attr in (
                    "execute",
                    "execute_confirmed",
                ):
                    source = ast.unparse(function.value)

                    assert source != "executor"
                    assert source != "tool"

                    # Main/UI may only approve a pending
                    # confirmation through the execution service.
                    assert function.attr != "execute"

    assert True


def test_main_uses_authorized_approval_method():
    tree = _tree()

    found = False

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            function = node.func

            if isinstance(function, ast.Attribute):
                if function.attr == "execute_approved":
                    source = ast.unparse(function.value)

                    assert source == "execution_service"
                    found = True

    assert found


def test_main_does_not_import_controlled_router():
    assert not _imports_module("core.controlled_router")


def test_main_does_not_import_legacy_router():
    assert not _imports_module("core.router")


def test_main_does_not_import_plugin_modules():
    tree = _tree()

    violations = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module and node.module.startswith("plugins"):
                violations.append(node.module)

        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("plugins"):
                    violations.append(alias.name)

    assert violations == []


def test_main_has_single_execution_service_acquisition():
    tree = _tree()

    count = 0

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            function = node.func

            if isinstance(function, ast.Name):
                if function.id == "get_execution_service":
                    count += 1

    assert count == 1


def test_main_passes_execution_service_into_decision_engine():
    tree = _tree()

    found = False

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            function = node.func

            if isinstance(function, ast.Name):
                if function.id != "decide":
                    continue

                keyword_names = {
                    keyword.arg
                    for keyword in node.keywords
                    if keyword.arg is not None
                }

                assert "execution_service" in keyword_names
                found = True

    assert found


def test_main_confirmation_flow_requires_human_response():
    source = MAIN_FILE.read_text(encoding="utf-8")

    assert "CONFIRMATION_REQUIRED" in source
    assert "answer = listen()" in source


def test_main_confirmation_acceptance_is_explicit():
    source = MAIN_FILE.read_text(encoding="utf-8")

    assert '"yes"' in source
    assert '"approve"' in source
    assert "execute_approved" in source


def test_main_confirmation_rejection_does_not_execute():
    source = MAIN_FILE.read_text(encoding="utf-8")

    assert 'response = "Action cancelled."' in source


def test_main_handles_structured_tool_errors():
    source = MAIN_FILE.read_text(encoding="utf-8")

    assert "ResultStatus.ERROR" in source
    assert "Tool execution failed." in source


def test_main_does_not_give_ui_direct_registry_execution_capability():
    tree = _tree()

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            function = node.func

            if isinstance(function, ast.Attribute):
                if function.attr == "get":
                    source = ast.unparse(function.value)

                    assert source != "registry"

    assert True