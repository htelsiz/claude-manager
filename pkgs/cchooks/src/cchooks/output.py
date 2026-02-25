"""Standalone output utilities for simple hooks that don't need full context."""

from __future__ import annotations

import json
import sys
from typing import Any


def output_json(data: dict[str, Any]) -> None:
    """Print JSON to stdout."""
    json.dump(data, sys.stdout)
    sys.stdout.flush()


def exit_success(message: str = "") -> None:
    """Exit with code 0 (success, continue normally)."""
    if message:
        print(message, file=sys.stderr)
    sys.exit(0)


def exit_non_block(message: str = "", exit_code: int = 1) -> None:
    """Exit with code 1 (non-blocking error, continue)."""
    if message:
        print(message, file=sys.stderr)
    sys.exit(exit_code)


def exit_block(reason: str = "") -> None:
    """Exit with code 2 (blocking error, halt)."""
    if reason:
        output_json({"decision": "block", "reason": reason})
    sys.exit(2)
