from abc import ABC, abstractmethod
from typing import Any, Optional


class MemoryStore(ABC):
    @abstractmethod
    def get(self, category: str, key: str, default: Any = None) -> Any:
        ...

    @abstractmethod
    def set(self, category: str, key: str, value: Any) -> bool:
        ...

    @abstractmethod
    def delete(self, category: str, key: str) -> bool:
        ...
