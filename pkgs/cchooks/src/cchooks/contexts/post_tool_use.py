from __future__ import annotations

from typing import Any

from cchooks.types import HookContext, HookOutput


class PostToolUseOutput(HookOutput):
    def __init__(self):
        super().__init__("PostToolUse")

    def add_context(self, context: str) -> None:
        self._emit(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PostToolUse",
                    "additionalContext": context,
                }
            }
        )

    def challenge(self, reason: str = "") -> None:
        data: dict[str, Any] = {
            "hookSpecificOutput": {"hookEventName": "PostToolUse"}
        }
        if reason:
            data["hookSpecificOutput"]["challengeReason"] = reason
        self._emit(data)


class PostToolUseContext(HookContext):
    @property
    def tool_name(self) -> str:
        return self._data.get("tool_name", "")

    @property
    def tool_input(self) -> dict[str, Any]:
        return self._data.get("tool_input", {})

    @property
    def tool_response(self) -> dict[str, Any]:
        return self._data.get("tool_response", {})

    @property
    def cwd(self) -> str:
        return self._data.get("cwd", "")

    @property
    def output(self) -> PostToolUseOutput:
        return PostToolUseOutput()
