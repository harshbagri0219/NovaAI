import pytest

from datetime import datetime, timedelta, UTC

from core.confirmation import ConfirmationError, ConfirmationManager
from core.interfaces import Capability, ConfirmationStatus
from core.tool_adapter import ToolAdapter
from core.tool_executor import ToolExecutor
from core.tool_registry import ToolRegistry


def make_tool(name="test", capability=Capability.STATE_CHANGING):
    return ToolAdapter(
        name=name,
        runnable=lambda: "ok",
        capability=capability,
    )


class TestConfirmationManagerLifecycle:

    def test_create_request_returns_pending(self):
        manager = ConfirmationManager()
        tool = make_tool()

        request = manager.create_request(tool, "do something")

        assert request.status == ConfirmationStatus.PENDING
        assert request.tool_name == "test"
        assert request.capability == Capability.STATE_CHANGING
        assert request.description == "do something"
        assert request.request_id

    def test_get_request_returns_none_for_unknown(self):
        manager = ConfirmationManager()

        assert manager.get_request("missing") is None

    def test_get_request_returns_request(self):
        manager = ConfirmationManager()
        tool = make_tool()

        request = manager.create_request(tool)
        fetched = manager.get_request(request.request_id)

        assert fetched is request
        assert fetched.status == ConfirmationStatus.PENDING

    def test_approve_pending_request(self):
        manager = ConfirmationManager()
        tool = make_tool()

        request = manager.create_request(tool)
        approved = manager.approve(request.request_id)

        assert approved.status == ConfirmationStatus.APPROVED

    def test_deny_pending_request(self):
        manager = ConfirmationManager()
        tool = make_tool()

        request = manager.create_request(tool)
        denied = manager.deny(request.request_id)

        assert denied.status == ConfirmationStatus.DENIED

    def test_consume_approved_request(self):
        manager = ConfirmationManager()
        tool = make_tool()

        request = manager.create_request(tool)
        manager.approve(request.request_id)

        consumed = manager.consume(request.request_id, tool)

        assert consumed.status == ConfirmationStatus.CONSUMED

    def test_pending_to_expired_via_get(self):
        manager = ConfirmationManager(ttl_seconds=-1)
        tool = make_tool()

        request = manager.create_request(tool, ttl_seconds=-1)
        fetched = manager.get_request(request.request_id)

        assert fetched.status == ConfirmationStatus.EXPIRED

    def test_approve_denied_request_raises(self):
        manager = ConfirmationManager()
        tool = make_tool()

        request = manager.create_request(tool)
        manager.deny(request.request_id)

        with pytest.raises(ConfirmationError, match="denied"):
            manager.approve(request.request_id)

    def test_approve_consumed_request_raises(self):
        manager = ConfirmationManager()
        tool = make_tool()

        request = manager.create_request(tool)
        manager.approve(request.request_id)
        manager.consume(request.request_id, tool)

        with pytest.raises(ConfirmationError, match="consumed"):
            manager.approve(request.request_id)

    def test_deny_approved_request_raises(self):
        manager = ConfirmationManager()
        tool = make_tool()

        request = manager.create_request(tool)
        manager.approve(request.request_id)

        with pytest.raises(ConfirmationError, match="approved"):
            manager.deny(request.request_id)

    def test_consume_pending_request_raises(self):
        manager = ConfirmationManager()
        tool = make_tool()

        request = manager.create_request(tool)

        with pytest.raises(ConfirmationError, match="pending"):
            manager.consume(request.request_id, tool)

    def test_consume_denied_request_raises(self):
        manager = ConfirmationManager()
        tool = make_tool()

        request = manager.create_request(tool)
        manager.deny(request.request_id)

        with pytest.raises(ConfirmationError, match="denied"):
            manager.consume(request.request_id, tool)

    def test_consume_expired_request_raises(self):
        manager = ConfirmationManager(ttl_seconds=-1)
        tool = make_tool()

        request = manager.create_request(tool, ttl_seconds=-1)

        with pytest.raises(ConfirmationError, match="expired"):
            manager.consume(request.request_id, tool)

    def test_approve_missing_request_raises(self):
        manager = ConfirmationManager()

        with pytest.raises(ConfirmationError, match="not found"):
            manager.approve("missing")

    def test_consume_missing_request_raises(self):
        manager = ConfirmationManager()

        with pytest.raises(ConfirmationError, match="not found"):
            manager.consume("missing", make_tool())


class TestToolExecutorConfirmation:

    def test_confirm_creates_confirmation_request(self):
        executor = ToolExecutor()
        tool = make_tool(capability=Capability.STATE_CHANGING)

        result = executor.execute(tool)

        assert result.status.value == "confirmation_required"
        assert result.confirmation_request is not None
        assert result.confirmation_request.tool_name == "test"
        assert result.confirmation_request.status == ConfirmationStatus.PENDING

    def test_confirm_never_executes(self):
        call_count = 0

        def stateful():
            nonlocal call_count
            call_count += 1
            return "executed"

        executor = ToolExecutor()

        tool = ToolAdapter(
            name="stateful",
            runnable=stateful,
            capability=Capability.STATE_CHANGING,
        )

        result = executor.execute(tool)

        assert result.status.value == "confirmation_required"
        assert call_count == 0

    def test_approved_request_executes_exactly_once(self):
        manager = ConfirmationManager()
        executor = ToolExecutor(confirmation_manager=manager)
        tool = make_tool(capability=Capability.STATE_CHANGING)

        result = executor.execute(tool)
        request = result.confirmation_request

        manager.approve(request.request_id)

        executed = executor.execute_confirmed(
            request.request_id,
            tool,
        )

        assert executed.status.value == "success"
        assert executed.payload == "ok"

    def test_approved_request_cannot_execute_twice(self):
        manager = ConfirmationManager()
        executor = ToolExecutor(confirmation_manager=manager)
        tool = make_tool(capability=Capability.STATE_CHANGING)

        result = executor.execute(tool)
        request = result.confirmation_request

        manager.approve(request.request_id)

        executor.execute_confirmed(request.request_id, tool)
        second = executor.execute_confirmed(request.request_id, tool)

        assert second.status.value == "error"

    def test_tool_substitution_rejected(self):
        manager = ConfirmationManager()
        executor = ToolExecutor(confirmation_manager=manager)

        tool_a = make_tool(
            name="tool_a",
            capability=Capability.STATE_CHANGING,
        )

        tool_b = make_tool(
            name="tool_b",
            capability=Capability.STATE_CHANGING,
        )

        result = executor.execute(tool_a)
        request = result.confirmation_request

        manager.approve(request.request_id)

        bad = executor.execute_confirmed(
            request.request_id,
            tool_b,
        )

        assert bad.status.value == "error"
        assert "mismatch" in (bad.error or "")

    def test_invalid_request_id_fails_closed(self):
        executor = ToolExecutor()
        tool = make_tool()

        result = executor.execute_confirmed("missing", tool)

        assert result.status.value == "error"

    def test_denied_request_cannot_execute(self):
        manager = ConfirmationManager()
        executor = ToolExecutor(confirmation_manager=manager)
        tool = make_tool(capability=Capability.STATE_CHANGING)

        result = executor.execute(tool)
        request = result.confirmation_request

        manager.deny(request.request_id)

        executed = executor.execute_confirmed(
            request.request_id,
            tool,
        )

        assert executed.status.value == "error"

    def test_expired_request_cannot_execute(self):
        manager = ConfirmationManager(ttl_seconds=300)
        executor = ToolExecutor(confirmation_manager=manager)
        tool = make_tool(capability=Capability.STATE_CHANGING)

        result = executor.execute(tool)
        request = result.confirmation_request

        manager.approve(request.request_id)

        request.expires_at = datetime.now(UTC) - timedelta(seconds=1)

        executed = executor.execute_confirmed(
            request.request_id,
            tool,
        )

        assert executed.status.value == "error"

    def test_registry_verification_rejects_unregistered_tool(self):
        registry = ToolRegistry.from_plugin_map({
            "time": lambda: "12:00",
        })

        manager = ConfirmationManager()
        executor = ToolExecutor(confirmation_manager=manager)

        tool = make_tool(
            name="unknown_tool",
            capability=Capability.STATE_CHANGING,
        )

        result = executor.execute(tool)
        request = result.confirmation_request

        manager.approve(request.request_id)

        executed = executor.execute_confirmed(
            request.request_id,
            tool,
            registry=registry,
        )

        assert executed.status.value == "error"
        assert "not registered" in (executed.error or "")

    def test_registry_verification_accepts_registered_tool(self):
        tool = make_tool(
            name="time",
            capability=Capability.STATE_CHANGING,
        )

        registry = ToolRegistry()
        registry.register(tool)

        manager = ConfirmationManager()
        executor = ToolExecutor(confirmation_manager=manager)

        result = executor.execute(tool)
        request = result.confirmation_request

        manager.approve(request.request_id)

        executed = executor.execute_confirmed(
            request.request_id,
            tool,
            registry=registry,
        )

        assert executed.status.value == "success"

    def test_plugin_exception_during_confirmed_execution(self):
        manager = ConfirmationManager()
        executor = ToolExecutor(confirmation_manager=manager)

        def bad():
            raise RuntimeError("boom")

        tool = ToolAdapter(
            name="bad",
            runnable=bad,
            capability=Capability.STATE_CHANGING,
        )

        result = executor.execute(tool)
        request = result.confirmation_request

        manager.approve(request.request_id)

        executed = executor.execute_confirmed(
            request.request_id,
            tool,
        )

        assert executed.status.value == "error"
        assert "boom" in (executed.error or "")


class TestRegression:

    def test_read_only_executes(self):
        executor = ToolExecutor()
        tool = make_tool(capability=Capability.READ_ONLY)

        result = executor.execute(tool)

        assert result.status.value == "success"
        assert result.payload == "ok"

    def test_destructive_denied(self):
        executor = ToolExecutor()
        tool = make_tool(capability=Capability.DESTRUCTIVE)

        result = executor.execute(tool)

        assert result.status.value == "error"

    def test_unknown_tool_fails_closed(self):
        executor = ToolExecutor()

        result = executor.execute(None)

        assert result.status.value == "error"

    def test_plugin_exception_becomes_error(self):
        executor = ToolExecutor()

        def bad():
            raise RuntimeError("boom")

        tool = make_tool(capability=Capability.READ_ONLY)
        tool._runnable = bad

        result = executor.execute(tool)

        assert result.status.value == "error"
        assert "boom" in (result.error or "")


class TestConfirmationIntegrity:

    def test_request_ids_are_unique(self):
        manager = ConfirmationManager()
        tool = make_tool()

        request_a = manager.create_request(tool, "first")
        request_b = manager.create_request(tool, "second")
        request_c = manager.create_request(tool, "third")

        assert request_a.request_id != request_b.request_id
        assert request_b.request_id != request_c.request_id
        assert request_a.request_id != request_c.request_id

    def test_approved_request_cannot_be_approved_again(self):
        manager = ConfirmationManager()
        tool = make_tool()

        request = manager.create_request(tool)
        manager.approve(request.request_id)

        with pytest.raises(ConfirmationError, match="approved"):
            manager.approve(request.request_id)

    def test_expired_request_cannot_be_approved(self):
        manager = ConfirmationManager(ttl_seconds=-1)
        tool = make_tool()

        request = manager.create_request(tool, ttl_seconds=-1)

        with pytest.raises(ConfirmationError, match="expired"):
            manager.approve(request.request_id)

    def test_expired_request_cannot_be_denied(self):
        manager = ConfirmationManager(ttl_seconds=-1)
        tool = make_tool()

        request = manager.create_request(tool, ttl_seconds=-1)

        with pytest.raises(ConfirmationError, match="expired"):
            manager.deny(request.request_id)

    def test_destructive_capability_cannot_become_approved(self):
        manager = ConfirmationManager()
        tool = make_tool(capability=Capability.DESTRUCTIVE)

        request = manager.create_request(tool)

        assert request.capability == Capability.DESTRUCTIVE
        assert request.status == ConfirmationStatus.PENDING

        manager.approve(request.request_id)

        assert request.status == ConfirmationStatus.APPROVED

    def test_confirmation_request_preserves_tool_name_and_capability(self):
        manager = ConfirmationManager()
        tool = make_tool(name="custom_tool", capability=Capability.STATE_CHANGING)

        request = manager.create_request(tool, "test description")

        assert request.tool_name == "custom_tool"
        assert request.capability == Capability.STATE_CHANGING
        assert request.description == "test description"


class TestContextIntegrity:

    def test_execute_approved_uses_stored_context_when_caller_does_not_supply(self):
        manager = ConfirmationManager()
        executor = ToolExecutor(confirmation_manager=manager)

        captured = {}

        def stateful(context=None):
            captured["context"] = context
            return "ok"

        tool = ToolAdapter(
            name="stateful",
            runnable=stateful,
            capability=Capability.STATE_CHANGING,
        )

        registry = ToolRegistry()
        registry.register(tool)

        stored_context = {"key": "stored_value"}

        result = executor.execute(tool, context=stored_context)
        request = result.confirmation_request

        manager.approve(request.request_id)

        executed = executor.execute_approved(
            request.request_id,
            registry=registry,
        )

        assert executed.status.value == "success"
        assert captured["context"] == stored_context

    def test_execute_approved_stored_context_wins_over_caller_context(self):
        manager = ConfirmationManager()
        executor = ToolExecutor(confirmation_manager=manager)

        captured = {}

        def stateful(context=None):
            captured["context"] = context
            return "ok"

        tool = ToolAdapter(
            name="stateful",
            runnable=stateful,
            capability=Capability.STATE_CHANGING,
        )

        registry = ToolRegistry()
        registry.register(tool)

        stored_context = {"key": "stored_value"}
        caller_context = {"key": "caller_value"}

        result = executor.execute(tool, context=stored_context)
        request = result.confirmation_request

        manager.approve(request.request_id)

        executed = executor.execute_approved(
            request.request_id,
            context=caller_context,
            registry=registry,
        )

        assert executed.status.value == "success"
        assert captured["context"] == stored_context

    def test_execute_confirmed_uses_stored_context_when_caller_does_not_supply(self):
        manager = ConfirmationManager()
        executor = ToolExecutor(confirmation_manager=manager)

        captured = {}

        def stateful(context=None):
            captured["context"] = context
            return "ok"

        tool = ToolAdapter(
            name="stateful",
            runnable=stateful,
            capability=Capability.STATE_CHANGING,
        )

        stored_context = {"key": "stored_value"}

        result = executor.execute(tool, context=stored_context)
        request = result.confirmation_request

        manager.approve(request.request_id)

        executed = executor.execute_confirmed(
            request.request_id,
            tool,
        )

        assert executed.status.value == "success"
        assert captured["context"] == stored_context

    def test_execute_confirmed_stored_context_wins_over_caller_context(self):
        manager = ConfirmationManager()
        executor = ToolExecutor(confirmation_manager=manager)

        captured = {}

        def stateful(context=None):
            captured["context"] = context
            return "ok"

        tool = ToolAdapter(
            name="stateful",
            runnable=stateful,
            capability=Capability.STATE_CHANGING,
        )

        stored_context = {"key": "stored_value"}
        caller_context = {"key": "caller_value"}

        result = executor.execute(tool, context=stored_context)
        request = result.confirmation_request

        manager.approve(request.request_id)

        executed = executor.execute_confirmed(
            request.request_id,
            tool,
            context=caller_context,
        )

        assert executed.status.value == "success"
        assert captured["context"] == stored_context

    def test_context_tampering_is_rejected(self):
        manager = ConfirmationManager()
        executor = ToolExecutor(confirmation_manager=manager)

        captured = {}

        def stateful(context=None):
            captured["context"] = context
            return "ok"

        tool = ToolAdapter(
            name="stateful",
            runnable=stateful,
            capability=Capability.STATE_CHANGING,
        )

        registry = ToolRegistry()
        registry.register(tool)

        stored_context = {"key": "authorized"}

        result = executor.execute(tool, context=stored_context)
        request = result.confirmation_request

        manager.approve(request.request_id)

        tampered_context = {"key": "tampered"}

        executed = executor.execute_approved(
            request.request_id,
            context=tampered_context,
            registry=registry,
        )

        assert executed.status.value == "success"
        assert captured["context"] == stored_context
        assert captured["context"] != tampered_context

    def test_execute_confirmed_context_tampering_is_rejected(self):
        manager = ConfirmationManager()
        executor = ToolExecutor(confirmation_manager=manager)

        captured = {}

        def stateful(context=None):
            captured["context"] = context
            return "ok"

        tool = ToolAdapter(
            name="stateful",
            runnable=stateful,
            capability=Capability.STATE_CHANGING,
        )

        stored_context = {"key": "authorized"}

        result = executor.execute(tool, context=stored_context)
        request = result.confirmation_request

        manager.approve(request.request_id)

        tampered_context = {"key": "tampered"}

        executed = executor.execute_confirmed(
            request.request_id,
            tool,
            context=tampered_context,
        )

        assert executed.status.value == "success"
        assert captured["context"] == stored_context
        assert captured["context"] != tampered_context

    def test_execute_approved_caller_context_used_when_no_stored_context(self):
        manager = ConfirmationManager()
        executor = ToolExecutor(confirmation_manager=manager)

        captured = {}

        def stateful(context=None):
            captured["context"] = context
            return "ok"

        tool = ToolAdapter(
            name="stateful",
            runnable=stateful,
            capability=Capability.STATE_CHANGING,
        )

        registry = ToolRegistry()
        registry.register(tool)

        result = executor.execute(tool)
        request = result.confirmation_request

        assert request.context is None

        manager.approve(request.request_id)

        caller_context = {"key": "caller_value"}

        executed = executor.execute_approved(
            request.request_id,
            context=caller_context,
            registry=registry,
        )

        assert executed.status.value == "success"
        assert captured["context"] == caller_context

    def test_execute_confirmed_caller_context_used_when_no_stored_context(self):
        manager = ConfirmationManager()
        executor = ToolExecutor(confirmation_manager=manager)

        captured = {}

        def stateful(context=None):
            captured["context"] = context
            return "ok"

        tool = ToolAdapter(
            name="stateful",
            runnable=stateful,
            capability=Capability.STATE_CHANGING,
        )

        result = executor.execute(tool)
        request = result.confirmation_request

        assert request.context is None

        manager.approve(request.request_id)

        caller_context = {"key": "caller_value"}

        executed = executor.execute_confirmed(
            request.request_id,
            tool,
            context=caller_context,
        )

        assert executed.status.value == "success"
        assert captured["context"] == caller_context
