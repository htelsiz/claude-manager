set -euo pipefail
SESSION_ID=$(jq -r '.session_id // "unknown"')
FLAG="/tmp/claude-manager/compact-$SESSION_ID"
mkdir -p /tmp/claude-manager
find /tmp/claude-manager -maxdepth 1 -name 'compact-*' -mmin +1440 -delete 2>/dev/null || true
[ -f "$FLAG" ] && exit 0
touch "$FLAG"
MESSAGE="$1"
jq -n --arg msg "$MESSAGE" '{decision:"block",reason:$msg}'
