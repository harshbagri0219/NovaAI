import ast
import json
from pathlib import Path

import pytest


FORBIDDEN_IMPORTS = {
    "core.tool_executor",
    "core.tool_registry",
    "core.tool_adapter",
    "core.confirmation",
    "core.controlled_router",
    "plugins",
}

FORBIDDEN_SOURCE_TERMS = {
    "tool_executor",
    "tool_registry",
    "tool_adapter",
    "confirmation_manager",
    "execute_approved",
    "execute_confirmed",
}


def _imports_from_source(path):
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imports = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)

        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module)

    return imports


def test_intelligence_has_no_execution_imports():
    path = Path("brain/intelligence.py")
    imports = _imports_from_source(path)

    forbidden = imports & FORBIDDEN_IMPORTS

    assert not forbidden, (
        f"LLM intelligence imports forbidden execution modules: {forbidden}"
    )


def test_llm_provider_has_no_execution_imports():
    path = Path("ai/llm_provider.py")
    imports = _imports_from_source(path)

    forbidden = {
        item
        for item in imports
        if item == "core"
        or item.startswith("core.")
        or item == "plugins"
        or item.startswith("plugins.")
    }

    assert not forbidden, (
        f"LLM provider imports forbidden execution modules: {forbidden}"
    )


def test_intelligence_has_no_forbidden_execution_terms():
    path = Path("brain/intelligence.py")
    source = path.read_text(encoding="utf-8").lower()

    found = {
        term
        for term in FORBIDDEN_SOURCE_TERMS
        if term in source
    }

    assert not found, (
        f"LLM intelligence contains forbidden execution references: {found}"
    )


def test_provider_has_no_forbidden_execution_terms():
    path = Path("ai/llm_provider.py")
    source = path.read_text(encoding="utf-8").lower()

    found = {
        term
        for term in FORBIDDEN_SOURCE_TERMS
        if term in source
    }

    assert not found, (
        f"LLM provider contains forbidden execution references: {found}"
    )


def test_ollama_payload_contains_only_llm_fields(monkeypatch):
    from ai.llm_provider import OllamaProvider

    captured = {}

    class FakeResponse:
        def read(self):
            return json.dumps(
                {"response": "Hello from NOVA."}
            ).encode("utf-8")

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

    def fake_urlopen(request, timeout):
        captured["timeout"] = timeout
        captured["body"] = json.loads(
            request.data.decode("utf-8")
        )
        return FakeResponse()

    monkeypatch.setattr(
        "ai.llm_provider.urlopen",
        fake_urlopen,
    )

    provider = OllamaProvider(
        base_url="http://localhost:11434",
        model="qwen2.5-coder:7b",
    )

    result = provider.generate(
        user="Hello NOVA",
        context="Previous conversation",
        personality="Calm and helpful",
    )

    assert result == "Hello from NOVA."

    assert set(captured["body"]) == {
        "model",
        "prompt",
        "stream",
    }

    assert captured["body"]["model"] == "qwen2.5-coder:7b"
    assert captured["body"]["stream"] is False

    prompt = captured["body"]["prompt"]

    assert "Hello NOVA" in prompt
    assert "Previous conversation" in prompt
    assert "Calm and helpful" in prompt


def test_ollama_failure_returns_none(monkeypatch):
    from ai.llm_provider import OllamaProvider

    def fake_urlopen(*args, **kwargs):
        raise OSError("Ollama unavailable")

    monkeypatch.setattr(
        "ai.llm_provider.urlopen",
        fake_urlopen,
    )

    provider = OllamaProvider()

    result = provider.generate("Hello NOVA")

    assert result is None


def test_intelligence_passes_only_conversational_data(monkeypatch):
    import brain.intelligence as intelligence

    captured = {}

    class FakeProvider:
        def generate(self, user, context=None, personality=None):
            captured["user"] = user
            captured["context"] = context
            captured["personality"] = personality
            return "Safe LLM response"

    monkeypatch.setattr(
        intelligence,
        "OllamaProvider",
        FakeProvider,
    )

    monkeypatch.setattr(
        intelligence,
        "last_conversation",
        lambda: "Previous conversation",
    )

    monkeypatch.setattr(
        intelligence,
        "get_personality",
        lambda: "Calm and helpful",
    )

    result = intelligence.respond("Hello NOVA")

    assert result == "Safe LLM response"

    assert captured["user"] == "Hello NOVA"
    assert captured["context"] == "Previous conversation"
    assert captured["personality"] == "Calm and helpful"


def test_llm_output_is_plain_text(monkeypatch):
    import brain.intelligence as intelligence

    class FakeProvider:
        def generate(self, user, context=None, personality=None):
            return "battery status: 80%"

    monkeypatch.setattr(
        intelligence,
        "OllamaProvider",
        FakeProvider,
    )

    result = intelligence.respond("How are you?")

    assert isinstance(result, str)
    assert result == "battery status: 80%"


def test_brain_keeps_deterministic_identity_before_llm(monkeypatch):
    import brain.brain as brain_module

    called = {"llm": False}

    def fake_llm(user):
        called["llm"] = True
        return "LLM should not replace deterministic identity."

    monkeypatch.setattr(
        brain_module,
        "llm_respond",
        fake_llm,
    )

    brain = brain_module.Brain()

    result = brain.think("What is your name?")

    assert result
    assert "NOVA" in result.upper()
    assert called["llm"] is False


def test_llm_boundary_has_no_execution_objects():
    intelligence_source = Path(
        "brain/intelligence.py"
    ).read_text(encoding="utf-8")

    provider_source = Path(
        "ai/llm_provider.py"
    ).read_text(encoding="utf-8")

    for source_name, source in (
        ("brain/intelligence.py", intelligence_source),
        ("ai/llm_provider.py", provider_source),
    ):
        tree = ast.parse(source)

        names = {
            node.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Name)
        }

        attributes = {
            node.attr
            for node in ast.walk(tree)
            if isinstance(node, ast.Attribute)
        }

        forbidden_names = {
            "ToolExecutor",
            "ToolRegistry",
            "ToolAdapter",
            "ConfirmationManager",
            "ControlledRouter",
        }

        forbidden_attributes = {
            "execute",
            "execute_approved",
            "execute_confirmed",
        }

        assert not (
            names & forbidden_names
        ), f"{source_name} references execution objects"

        assert not (
            attributes & forbidden_attributes
        ), f"{source_name} references execution methods"