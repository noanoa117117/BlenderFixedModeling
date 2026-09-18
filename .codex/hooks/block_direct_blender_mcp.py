"""Deny direct Blender MCP calls; the repository bridge is tools/hairflow.py."""

from __future__ import annotations

import json
import sys


def main() -> int:
    json.load(sys.stdin)
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                "Direct Blender MCP is disabled for this repository. "
                "Use python tools/hairflow.py or add a versioned operation first."
            ),
        }
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
