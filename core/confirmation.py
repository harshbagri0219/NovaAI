import secrets
from datetime import datetime, timedelta, UTC

from core.interfaces import Capability, ConfirmationRequest, ConfirmationStatus


class ConfirmationError(Exception):
    pass


class ConfirmationManager:

    def __init__(self, ttl_seconds=300):
        self._requests = {}
        self._ttl = timedelta(seconds=ttl_seconds)

    def create_request(self, tool, description="", ttl_seconds=None, context=None):
        if tool is None:
            raise ConfirmationError("tool is required")

        request_id = secrets.token_urlsafe(16)
        ttl = ttl_seconds if ttl_seconds is not None else self._ttl.total_seconds()
        expires_at = datetime.now(UTC) + timedelta(seconds=ttl)

        request = ConfirmationRequest(
            request_id=request_id,
            tool_name=getattr(tool, "name", "unknown"),
            capability=getattr(tool, "capability", Capability.STATE_CHANGING),
            description=description or f"Tool '{getattr(tool, 'name', 'unknown')}' requires confirmation",
            status=ConfirmationStatus.PENDING,
            expires_at=expires_at,
            context=context,
        )

        self._requests[request_id] = request
        return request

    def get_request(self, request_id):
        request = self._requests.get(request_id)
        if request is None:
            return None

        if self._is_expired(request):
            request.status = ConfirmationStatus.EXPIRED

        return request

    def approve(self, request_id):
        request = self._get_valid_request(request_id)
        if request.status != ConfirmationStatus.PENDING:
            raise ConfirmationError(
                f"cannot approve request in status {request.status.value}"
            )
        request.status = ConfirmationStatus.APPROVED
        return request

    def deny(self, request_id):
        request = self._get_valid_request(request_id)
        if request.status != ConfirmationStatus.PENDING:
            raise ConfirmationError(
                f"cannot deny request in status {request.status.value}"
            )
        request.status = ConfirmationStatus.DENIED
        return request

    def consume(self, request_id, tool):
        request = self._get_valid_request(request_id)
        if request.status != ConfirmationStatus.APPROVED:
            raise ConfirmationError(
                f"cannot consume request in status {request.status.value}"
            )

        expected_name = request.tool_name
        actual_name = getattr(tool, "name", None)

        if actual_name != expected_name:
            raise ConfirmationError(
                f"tool mismatch: expected {expected_name}, got {actual_name}"
            )

        expected_capability = request.capability
        actual_capability = getattr(tool, "capability", None)

        if actual_capability != expected_capability:
            raise ConfirmationError(
                "tool capability mismatch"
            )

        request.status = ConfirmationStatus.CONSUMED
        return request

    def _get_valid_request(self, request_id):
        request = self._requests.get(request_id)
        if request is None:
            raise ConfirmationError("request not found")
        if self._is_expired(request):
            request.status = ConfirmationStatus.EXPIRED
            raise ConfirmationError("request expired")
        return request

    def _is_expired(self, request):
        if request.expires_at is None:
            return False
        return datetime.now(UTC) > request.expires_at
