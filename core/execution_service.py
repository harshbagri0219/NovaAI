from core.tool_executor import ToolExecutor


class ExecutionService:
    """
    Centralized authorized execution boundary for NOVA.

    Owns the authoritative runtime ToolExecutor instance so
    policy and confirmation state have one execution boundary.

    High-level components should use get_execution_service()
    instead of constructing ToolExecutor instances.
    """

    def __init__(self, executor=None):
        self._executor = executor or ToolExecutor()

    def execute(self, tool, context=None):
        return self._executor.execute(
            tool,
            context=context,
        )

    def execute_approved(self, request_id, context=None, registry=None):
        return self._executor.execute_approved(
            request_id,
            context=context,
            registry=registry,
        )


_runtime_service = None


def get_execution_service():
    """
    Return NOVA's authoritative runtime ExecutionService.

    The singleton is intentionally kept inside this module so
    high-level components do not construct their own executors.
    """
    global _runtime_service

    if _runtime_service is None:
        _runtime_service = ExecutionService()

    return _runtime_service
