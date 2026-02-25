"""Factory function to create typed hook contexts from stdin."""

from __future__ import annotations

import json
import sys
from typing import TextIO

from cchooks.types import HookContext
from cchooks.contexts import (
    NotificationContext,
    PostToolUseContext,
    PreCompactContext,
    PreToolUseContext,
    SessionEndContext,
    SessionStartContext,
    StopContext,
    SubagentStopContext,
    UserPromptSubmitContext,
)

_CONTEXT_MAP: dict[str, type[HookContext]] = {
    "PreToolUse": PreToolUseContext,
    "PostToolUse": PostToolUseContext,
    "PostToolUseFailure": PostToolUseContext,
    "Notification": NotificationContext,
    "UserPromptSubmit": UserPromptSubmitContext,
    "Stop": StopContext,
    "SubagentStop": SubagentStopContext,
    "PreCompact": PreCompactContext,
    "SessionStart": SessionStartContext,
    "SessionEnd": SessionEndContext,
}


def create_context(stdin: TextIO = sys.stdin) -> HookContext:
    """Read JSON from stdin, auto-detect event type, return typed context."""
    data = json.loads(stdin.read())
    event = data.get("hook_event_name", "")
    ctx_cls = _CONTEXT_MAP.get(event)
    if ctx_cls is None:
        raise ValueError(f"Unknown hook event: {event!r}")
    return ctx_cls(data)
