import secrets
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timedelta, UTC
from enum import Enum

from core.interfaces import Capability, ConfirmationRequest

class ConfirmationError(Exception):
    pass

class ConfirmationStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    EXPIRED = "expired"
    CONSUMED = "consumed"


@dataclass
class _AuthorizationRecord:
    tool: object
    tool_name: str
    capability: Capability
    description: str
    status: ConfirmationStatus
    expires_at: datetime
    context: object


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

        record = _AuthorizationRecord(
            tool=tool,
            tool_name=getattr(tool, "name", "unknown"),
            capability=getattr(tool, "capability", Capability.STATE_CHANGING),
            description=description or f"Tool '{getattr(tool, 'name', 'unknown')}' requires confirmation",
            status=ConfirmationStatus.PENDING,
            expires_at=expires_at,
            context=self._snapshot_context(context),
        )

        self._requests[request_id] = record
        return self._snapshot(request_id, record)

    def get_request(self, request_id):
        record = self._requests.get(request_id)
        if record is None:
            return None

        if (
            record.status in (ConfirmationStatus.PENDING, ConfirmationStatus.APPROVED)
            and self._is_expired(record)
        ):
            record.status = ConfirmationStatus.EXPIRED

        return self._snapshot(request_id, record)

    def approve(self, request_id):
        record = self._get_valid_request(request_id)
        if record.status != ConfirmationStatus.PENDING:
            raise ConfirmationError(
                f"cannot approve request in status {record.status.value}"
            )
        record.status = ConfirmationStatus.APPROVED
        return self._snapshot(request_id, record)

    def deny(self, request_id):
        record = self._get_valid_request(request_id)
        if record.status != ConfirmationStatus.PENDING:
            raise ConfirmationError(
                f"cannot deny request in status {record.status.value}"
            )
        record.status = ConfirmationStatus.DENIED
        return self._snapshot(request_id, record)

    def consume(self, request_id, tool):
        record = self._get_valid_request(request_id)
        if record.status != ConfirmationStatus.APPROVED:
            raise ConfirmationError(
                f"cannot consume request in status {record.status.value}"
            )

        expected_name = record.tool_name
        actual_name = getattr(tool, "name", None)

        if actual_name != expected_name:
            raise ConfirmationError(
                f"tool mismatch: expected {expected_name}, got {actual_name}"
            )

        expected_capability = record.capability
        actual_capability = getattr(tool, "capability", None)

        if actual_capability != expected_capability:
            raise ConfirmationError(
                "tool capability mismatch"
            )

        if tool is not record.tool:
            raise ConfirmationError("tool identity mismatch")

        record.status = ConfirmationStatus.CONSUMED
        return self._snapshot(request_id, record)

    def _get_valid_request(self, request_id):
        record = self._requests.get(request_id)
        if record is None:
            raise ConfirmationError("request not found")
        if (
            record.status in (ConfirmationStatus.PENDING, ConfirmationStatus.APPROVED)
            and self._is_expired(record)
        ):
            record.status = ConfirmationStatus.EXPIRED
            raise ConfirmationError("request expired")
        return record

    def _snapshot(self, request_id, record):
        return ConfirmationRequest(
            request_id=request_id,
            tool_name=record.tool_name,
            capability=record.capability,
            description=record.description,
            status=record.status,
            expires_at=record.expires_at,
            context=self._snapshot_context(record.context),
        )

    def _snapshot_context(self, context):
        if context is None:
            return None
        try:
            return deepcopy(context)
        except Exception as exc:
            raise ConfirmationError("context cannot be safely copied") from exc

    def _is_expired(self, request):
        if request.expires_at is None:
            return False
        return datetime.now(UTC) > request.expires_at
