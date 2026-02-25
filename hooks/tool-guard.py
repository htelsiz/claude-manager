import json
import re
import sys

DENY_PATTERNS = json.loads(sys.argv[1]) if len(sys.argv) > 1 else []


def main():
    data = json.loads(sys.stdin.read())
    if data.get("tool_name") != "Bash":
        return
    cmd = data.get("tool_input", {}).get("command", "")
    for pattern in DENY_PATTERNS:
        if re.search(pattern, cmd):
            json.dump(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": f"Blocked: matches pattern '{pattern}'",
                    }
                },
                sys.stdout,
            )
            return


if __name__ == "__main__":
    main()
