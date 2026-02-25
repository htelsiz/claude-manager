from __future__ import annotations

from cchooks.types import HookContext, HookOutput


class SessionEndOutput(HookOutput):
    def __init__(self):
        super().__init__("SessionEnd")


class SessionEndContext(HookContext):
    @property
    def reason(self) -> str:
        return self._data.get("reason", "other")

    @property
    def cwd(self) -> str:
        return self._data.get("cwd", "")

    @property
    def output(self) -> SessionEndOutput:
        return SessionEndOutput()
