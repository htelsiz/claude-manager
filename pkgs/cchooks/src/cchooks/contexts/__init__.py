"""Context classes for each hook event type."""

from cchooks.contexts.pre_tool_use import PreToolUseContext, PreToolUseOutput
from cchooks.contexts.post_tool_use import PostToolUseContext, PostToolUseOutput
from cchooks.contexts.notification import NotificationContext, NotificationOutput
from cchooks.contexts.user_prompt_submit import (
    UserPromptSubmitContext,
    UserPromptSubmitOutput,
)
from cchooks.contexts.stop import StopContext, StopOutput
from cchooks.contexts.subagent_stop import SubagentStopContext, SubagentStopOutput
from cchooks.contexts.pre_compact import PreCompactContext, PreCompactOutput
from cchooks.contexts.session_start import SessionStartContext, SessionStartOutput
from cchooks.contexts.session_end import SessionEndContext, SessionEndOutput

__all__ = [
    "PreToolUseContext",
    "PreToolUseOutput",
    "PostToolUseContext",
    "PostToolUseOutput",
    "NotificationContext",
    "NotificationOutput",
    "UserPromptSubmitContext",
    "UserPromptSubmitOutput",
    "StopContext",
    "StopOutput",
    "SubagentStopContext",
    "SubagentStopOutput",
    "PreCompactContext",
    "PreCompactOutput",
    "SessionStartContext",
    "SessionStartOutput",
    "SessionEndContext",
    "SessionEndOutput",
]
