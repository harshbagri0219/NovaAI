from core.interfaces import ResultStatus, StructuredResult, Tool
from policy.engine import PolicyEngine


class ToolExecutor:

    def __init__(self, policy_engine=None):
        self._policy = policy_engine or PolicyEngine()

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
            return StructuredResult(
                status=ResultStatus.CONFIRMATION_REQUIRED,
                error=decision.reason or "confirmation required",
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
