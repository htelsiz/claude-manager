from __future__ import annotations

from typing import Any

from cchooks.types import HookContext, HookOutput


class UserPromptSubmitOutput(HookOutput):
    def __init__(self):
        super().__init__("UserPromptSubmit")

    def allow(self, reason: str = "") -> None:
        data: dict[str, Any] = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "decision": "allow",
            }
        }
        if reason:
            data["hookSpecificOutput"]["reason"] = reason
        self._emit(data)

    def block(self, reason: str = "") -> None:
        data: dict[str, Any] = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "decision": "block",
            }
        }
        if reason:
            data["hookSpecificOutput"]["reason"] = reason
        self._emit(data)

    def add_context(self, context: str) -> None:
        self._emit(
            {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": context,
                }
            }
        )


class UserPromptSubmitContext(HookContext):
    @property
    def prompt(self) -> str:
        return self._data.get("prompt", "")

    @property
    def cwd(self) -> str:
        return self._data.get("cwd", "")

    @property
    def output(self) -> UserPromptSubmitOutput:
        return UserPromptSubmitOutput()
