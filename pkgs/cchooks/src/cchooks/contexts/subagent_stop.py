from __future__ import annotations

from cchooks.types import HookContext, HookOutput


class SubagentStopOutput(HookOutput):
    def __init__(self):
        super().__init__("SubagentStop")

    def prevent(self, reason: str = "") -> None:
        data = {
            "hookSpecificOutput": {
                "hookEventName": "SubagentStop",
                "decision": "prevent",
            }
        }
        if reason:
            data["hookSpecificOutput"]["reason"] = reason
        self._emit(data)

    def allow(self, reason: str = "") -> None:
        data = {
            "hookSpecificOutput": {
                "hookEventName": "SubagentStop",
                "decision": "allow",
            }
        }
        if reason:
            data["hookSpecificOutput"]["reason"] = reason
        self._emit(data)


class SubagentStopContext(HookContext):
    @property
    def stop_hook_active(self) -> bool:
        return self._data.get("stop_hook_active", False)

    @property
    def output(self) -> SubagentStopOutput:
        return SubagentStopOutput()
