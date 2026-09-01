from typing import Protocol, runtime_checkable


@runtime_checkable
class VoiceInput(Protocol):
    def listen(self) -> str:
        ...


@runtime_checkable
class VoiceOutput(Protocol):
    def speak(self, text: str) -> None:
        ...
