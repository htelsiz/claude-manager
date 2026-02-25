from __future__ import annotations

from cchooks.types import HookContext, HookOutput


class NotificationOutput(HookOutput):
    def __init__(self):
        super().__init__("Notification")

    def acknowledge(self, message: str = "") -> None:
        if message:
            self._emit({"message": message})


class NotificationContext(HookContext):
    @property
    def message(self) -> str:
        return self._data.get("message", "")

    @property
    def cwd(self) -> str:
        return self._data.get("cwd", "")

    @property
    def output(self) -> NotificationOutput:
        return NotificationOutput()
