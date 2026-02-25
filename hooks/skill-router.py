import json
import sys

RULES = json.loads(sys.argv[1]) if len(sys.argv) > 1 else []


def main():
    if not RULES:
        return
    lines = [
        "## Skill Routing Rules",
        "When the user's message matches these keywords, invoke the skill BEFORE responding:",
        "",
    ]
    for rule in RULES:
        keywords = ", ".join(f'"{k}"' for k in rule["keywords"])
        lines.append(f"- Keywords [{keywords}] -> invoke skill: **{rule['skill']}**")
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": "\n".join(lines),
            }
        },
        sys.stdout,
    )


if __name__ == "__main__":
    main()
