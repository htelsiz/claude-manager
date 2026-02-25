from __future__ import annotations

from cchooks.types import HookContext, HookOutput


class StopOutput(HookOutput):
    def __init__(self):
        super().__init__("Stop")

    def prevent(self, reason: str = "") -> None:
        data = {"hookSpecificOutput": {"hookEventName": "Stop", "decision": "prevent"}}
        if reason:
            data["hookSpecificOutput"]["reason"] = reason
        self._emit(data)

    def allow(self, reason: str = "") -> None:
        data = {"hookSpecificOutput": {"hookEventName": "Stop", "decision": "allow"}}
        if reason:
            data["hookSpecificOutput"]["reason"] = reason
        self._emit(data)


class StopContext(HookContext):
    @property
    def stop_hook_active(self) -> bool:
        return self._data.get("stop_hook_active", False)

    @property
    def output(self) -> StopOutput:
        return StopOutput()
