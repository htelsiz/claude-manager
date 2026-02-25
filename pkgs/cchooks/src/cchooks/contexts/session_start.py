from __future__ import annotations

from cchooks.types import HookContext, HookOutput


class SessionStartOutput(HookOutput):
    def __init__(self):
        super().__init__("SessionStart")

    def add_context(self, context: str) -> None:
        self._emit(
            {
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": context,
                }
            }
        )


class SessionStartContext(HookContext):
    @property
    def source(self) -> str:
        return self._data.get("source", "startup")

    @property
    def output(self) -> SessionStartOutput:
        return SessionStartOutput()
