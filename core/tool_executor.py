from core.interfaces import (
    Capability,
    ConfirmationRequest,
    ConfirmationStatus,
    ResultStatus,
    StructuredResult,
    Tool,
)
from core.confirmation import ConfirmationError, ConfirmationManager
from policy.engine import PolicyEngine


class ToolExecutor:

    def __init__(self, policy_engine=None, confirmation_manager=None):
        self._policy = policy_engine or PolicyEngine()
        self._confirmations = confirmation_manager or ConfirmationManager()

    def execute(self, tool, context=None):
        if tool is None or not isinstance(tool, Tool):
            return StructuredResult(
                status=ResultStatus.ERROR,
                error="invalid tool",
            )

        decision = self._policy.evaluate(tool, context)

        if decision.decision == "deny":
            return StructuredResult(
                status=ResultStatus.ERROR,
                error=decision.reason or "tool execution denied",
            )

        if decision.decision == "confirm":
            request = self._confirmations.create_request(
                tool=tool,
                description=decision.reason or "confirmation required",
                context=context,
            )
            return StructuredResult(
                status=ResultStatus.CONFIRMATION_REQUIRED,
                error=decision.reason or "confirmation required",
                confirmation_request=request,
            )

        if decision.decision != "allow":
            return StructuredResult(
                status=ResultStatus.ERROR,
                error="unsupported policy decision",
            )

        try:
            result = tool.run(context)
        except Exception as exc:
            return StructuredResult(
                status=ResultStatus.ERROR,
                error=str(exc),
            )

        if isinstance(result, StructuredResult):
            return result

        return StructuredResult(
            status=ResultStatus.SUCCESS,
            payload=result,
        )

    def execute_approved(self, request_id, context=None, registry=None):
        request = self._confirmations.get_request(request_id)
        if request is None:
            return StructuredResult(
                status=ResultStatus.ERROR,
                error="request not found",
            )

        if request.status != ConfirmationStatus.APPROVED:
            return StructuredResult(
                status=ResultStatus.ERROR,
                error=f"request is not approved (status: {request.status.value})",
            )

        if self._confirmations._is_expired(request):
            return StructuredResult(
                status=ResultStatus.ERROR,
                error="request expired",
            )

        tool = None
        if registry is not None:
            tool = registry.get(request.tool_name)
            if tool is None:
                return StructuredResult(
                    status=ResultStatus.ERROR,
                    error="tool not registered",
                )

        if tool is None or getattr(tool, "name", None) != request.tool_name:
            return StructuredResult(
                status=ResultStatus.ERROR,
                error="tool identity mismatch",
            )

        try:
            consumed = self._confirmations.consume(request_id, tool)
        except ConfirmationError as exc:
            return StructuredResult(
                status=ResultStatus.ERROR,
                error=str(exc),
            )

        effective_context = request.context if request.context is not None else context

        try:
            result = tool.run(effective_context)
        except Exception as exc:
            return StructuredResult(
                status=ResultStatus.ERROR,
                error=str(exc),
            )

        if isinstance(result, StructuredResult):
            return result

        return StructuredResult(
            status=ResultStatus.SUCCESS,
            payload=result,
        )

    def execute_confirmed(self, request_id, tool, context=None, registry=None):
        request = self._confirmations.get_request(request_id)

        if request is None:
            return StructuredResult(
                status=ResultStatus.ERROR,
                error="request not found",
            )

        if request.status != ConfirmationStatus.APPROVED:
            return StructuredResult(
                status=ResultStatus.ERROR,
                error=f"request is not approved (status: {request.status.value})",
            )

        if self._confirmations._is_expired(request):
            return StructuredResult(
                status=ResultStatus.ERROR,
                error="request expired",
            )

        if registry is not None:
            registered = registry.get(request.tool_name)

            if registered is None:
                return StructuredResult(
                    status=ResultStatus.ERROR,
                    error="tool not registered",
                )

            if registered is not tool:
                return StructuredResult(
                    status=ResultStatus.ERROR,
                    error="tool identity mismatch",
                )

        try:
            self._confirmations.consume(request_id, tool)
        except ConfirmationError as exc:
            return StructuredResult(
                status=ResultStatus.ERROR,
                error=str(exc),
            )

        effective_context = (
            request.context if request.context is not None else context
        )

        try:
            result = tool.run(effective_context)
        except Exception as exc:
            return StructuredResult(
                status=ResultStatus.ERROR,
                error=str(exc),
            )

        if isinstance(result, StructuredResult):
            return result

        return StructuredResult(
            status=ResultStatus.SUCCESS,
            payload=result,
        )