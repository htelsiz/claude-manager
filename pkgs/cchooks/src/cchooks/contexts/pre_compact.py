from __future__ import annotations

from cchooks.types import HookContext, HookOutput


class PreCompactOutput(HookOutput):
    def __init__(self):
        super().__init__("PreCompact")

    def acknowledge(self, message: str = "") -> None:
        if message:
            self._emit({"message": message})


class PreCompactContext(HookContext):
    @property
    def trigger(self) -> str:
        return self._data.get("trigger", "auto")

    @property
    def custom_instructions(self) -> str:
        return self._data.get("custom_instructions", "")

    @property
    def output(self) -> PreCompactOutput:
        return PreCompactOutput()
