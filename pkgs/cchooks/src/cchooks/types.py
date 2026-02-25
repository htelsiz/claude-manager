"""Base types for hook contexts and outputs."""

from __future__ import annotations

import json
import sys
from abc import ABC, abstractmethod
from typing import Any


class HookOutput(ABC):
    """Base output handler for all hook events."""

    def __init__(self, hook_event_name: str):
        self._hook_event_name = hook_event_name

    def _emit(self, data: dict[str, Any]) -> None:
        json.dump(data, sys.stdout)
        sys.stdout.flush()

    def exit_success(self) -> None:
        sys.exit(0)

    def exit_non_block(self, message: str = "") -> None:
        if message:
            print(message, file=sys.stderr)
        sys.exit(1)

    def exit_block(self, reason: str = "") -> None:
        if reason:
            self._emit({"decision": "block", "reason": reason})
        sys.exit(2)


class HookContext(ABC):
    """Base context for all hook events."""

    def __init__(self, data: dict[str, Any]):
        self._data = data

    @property
    def session_id(self) -> str:
        return self._data.get("session_id", "")

    @property
    def transcript_path(self) -> str:
        return self._data.get("transcript_path", "")

    @property
    def hook_event_name(self) -> str:
        return self._data.get("hook_event_name", "")

    @property
    def claude_project_dir(self) -> str:
        return self._data.get("claude_project_dir", "")

    @abstractmethod
    def output(self) -> HookOutput:
        pass
