from core.execution_service import ExecutionService, get_execution_service
from core.tool_executor import ToolExecutor


def test_execution_service_creates_authoritative_executor():
    service = ExecutionService()

    result = service.execute(None)

    assert result.error == "invalid tool"


def test_execution_service_can_accept_injected_executor():
    executor = ToolExecutor()
    service = ExecutionService(executor=executor)

    assert service._executor is executor


def test_execution_service_execute_delegates():
    executor = ToolExecutor()
    service = ExecutionService(executor=executor)

    assert callable(service.execute)


def test_execution_service_execute_approved_delegates():
    executor = ToolExecutor()
    service = ExecutionService(executor=executor)

    assert callable(service.execute_approved)


def test_runtime_execution_service_is_singleton():
    first = get_execution_service()
    second = get_execution_service()

    assert first is second
