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

    def __init__(self, name, runnable, capability):
        # Validate capability
        if capability is None:
            raise ValueError("Capability cannot be None")
        if not isinstance(capability, Capability):
            raise TypeError("Capability must be a Capability instance")
        # Store attributes immutably
        object.__setattr__(self, '_name', name)
        object.__setattr__(self, '_runnable', runnable)
        object.__setattr__(self, '_capability', capability)

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

    def __setattr__(self, name, value):
        # Prevent mutation of capability after construction
        if name in ('capability', '_capability', '__capability'):
            raise AttributeError("capability is immutable")
        super().__setattr__(name, value)

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