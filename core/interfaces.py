from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional, Protocol, runtime_checkable


class ResultStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"
    CONFIRMATION_REQUIRED = "confirmation_required"


@dataclass
class StructuredResult:
    status: ResultStatus
    payload: Any = None
    error: Optional[str] = None
    confirmation_request: Optional["ConfirmationRequest"] = None


class Capability(str, Enum):
    READ_ONLY = "read_only"
    STATE_CHANGING = "state_changing"
    DESTRUCTIVE = "destructive"


@dataclass
class PolicyDecision:
    decision: str
    reason: Optional[str] = None
    requires_confirmation: bool = False


@runtime_checkable
class Tool(Protocol):
    name: str
    capability: Capability

    def run(self, context: Any) -> StructuredResult:
        ...


class ConfirmationStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    EXPIRED = "expired"
    CONSUMED = "consumed"


@dataclass
class ConfirmationRequest:
    request_id: str
    tool_name: str
    capability: Capability
    description: str
    status: ConfirmationStatus = ConfirmationStatus.PENDING
    expires_at: Optional[Any] = None
    context: Optional[Any] = None
