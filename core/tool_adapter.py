import inspect

from core.interfaces import Capability, StructuredResult, Tool
from core.interfaces import ResultStatus


class ToolAdapter:
    """Wraps an existing plugin callable so it participates in the Tool interface.

    This adapter is intentionally conservative:
    - It does NOT execute policy.
    - It does NOT bypass capability evaluation.
    - It safely captures plugin errors into StructuredResult.
    """

    def __init__(self, name, runnable, capability=None):
        self._name = name
        self._runnable = runnable
        self._capability = capability or Capability.STATE_CHANGING

    @property
    def name(self):
        return self._name

    @property
    def capability(self):
        return self._capability

    def run(self, context=None):
        try:
            if context is not None and _accepts_context(self._runnable):
                result = self._runnable(context)
            else:
                result = self._runnable()
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


def _accepts_context(runnable):
    try:
        sig = inspect.signature(runnable)
    except (ValueError, TypeError):
        return True

    for param in sig.parameters.values():
        if param.kind in (
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            inspect.Parameter.VAR_POSITIONAL,
        ):
            return True

    return False
