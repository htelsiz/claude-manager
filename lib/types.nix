{ lib }:
{
  hookEventType = lib.types.enum [
    "PreToolUse"
    "PostToolUse"
    "PostToolUseFailure"
    "UserPromptSubmit"
    "SessionStart"
    "SessionEnd"
    "PreCompact"
    "Stop"
    "SubagentStop"
    "Notification"
    "PermissionRequest"
    "SubagentStart"
    "TaskCompleted"
    "ConfigChange"
    "WorktreeCreate"
    "WorktreeRemove"
    "TeammateIdle"
  ];

  mcpServerType = lib.types.submodule {
    options = {
      command = lib.mkOption { type = lib.types.str; };
      args = lib.mkOption {
        type = lib.types.listOf lib.types.str;
        default = [ ];
      };
      env = lib.mkOption {
        type = lib.types.attrsOf lib.types.str;
        default = { };
      };
    };
  };
}
