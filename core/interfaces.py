from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional, Protocol, runtime_checkable, TYPE_CHECKING

if TYPE_CHECKING:
    from core.confirmation import ConfirmationStatus

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

class ImmutableConfirmationRequest:
    """Immutable fields: request_id, tool_name, capability, expires_at."""
    def __init__(self,
                 request_id: str,
                 tool_name: str,
                 capability: 'Capability',
                 description: str,
                 status: 'ConfirmationStatus' = 'pending',
                 expires_at: Optional[datetime] = None,
                 context: Optional[Any] = None):
        # Set immutable fields
        object.__setattr__(self, '_request_id', request_id)
        object.__setattr__(self, '_tool_name', tool_name)
        object.__setattr__(self, '_capability', capability)
        object.__setattr__(self, '_description', description)
        object.__setattr__(self, '_expires_at', expires_at)
        # Mutable field
        object.__setattr__(self, '_status', status)
        object.__setattr__(self, '_context', context)

    def __setattr__(self, name, value):
        # Prevent modification of immutable fields after init
        immutable = ('_request_id', '_tool_name', '_capability', '_description', '_expires_at')
        if name in immutable:
            raise AttributeError(f"Cannot modify {name} after initialization")
        super().__setattr__(name, value)

    @property
    def request_id(self) -> str:
        return self._request_id

    @property
    def tool_name(self) -> str:
        return self._tool_name

    @property
    def capability(self) -> 'Capability':
        return self._capability

    @property
    def expires_at(self) -> Optional[datetime]:
        return self._expires_at

    @property
    def status(self) -> 'ConfirmationStatus':
        return self._status

    @status.setter
    def status(self, value: 'ConfirmationStatus'):
        object.__setattr__(self, '_status', value)

    @property
    def description(self) -> str:
        return self._description

    @property
    def context(self) -> Optional[Any]:
        return self._context


@dataclass
class ConfirmationRequest(ImmutableConfirmationRequest):
    """Convenient dataclass that inherits immutable behavior."""
    request_id: str
    tool_name: str
    capability: 'Capability'
    description: str
    status: 'ConfirmationStatus' = 'pending'
    expires_at: Optional[datetime] = None
    context: Optional[Any] = None

    def __init__(self,
                 request_id: str,
                 tool_name: str,
                 capability: 'Capability',
                 description: str,
                 status: 'ConfirmationStatus' = 'pending',
                 expires_at: Optional[datetime] = None,
                 context: Optional[Any] = None):
        # Call the immutable base init
        super().__init__(request_id, tool_name, capability, description,
                         status, expires_at, context)