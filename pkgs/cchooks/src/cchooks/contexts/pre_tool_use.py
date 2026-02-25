from __future__ import annotations

from typing import Any

from cchooks.types import HookContext, HookOutput


class PreToolUseOutput(HookOutput):
    def __init__(self):
        super().__init__("PreToolUse")

    def allow(self, reason: str = "") -> None:
        data: dict[str, Any] = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
            }
        }
        if reason:
            data["hookSpecificOutput"]["permissionDecisionReason"] = reason
        self._emit(data)

    def deny(self, reason: str = "") -> None:
        data: dict[str, Any] = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
            }
        }
        if reason:
            data["hookSpecificOutput"]["permissionDecisionReason"] = reason
        self._emit(data)

    def ask(self, reason: str = "") -> None:
        data: dict[str, Any] = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "ask",
            }
        }
        if reason:
            data["hookSpecificOutput"]["permissionDecisionReason"] = reason
        self._emit(data)


class PreToolUseContext(HookContext):
    @property
    def tool_name(self) -> str:
        return self._data.get("tool_name", "")

    @property
    def tool_input(self) -> dict[str, Any]:
        return self._data.get("tool_input", {})

    @property
    def cwd(self) -> str:
        return self._data.get("cwd", "")

    @property
    def output(self) -> PreToolUseOutput:
        return PreToolUseOutput()
