#!/usr/bin/env python3
"""
Approval Gate Hook
Requires user approval before executing dangerous operations.
"""

import json
import sys
import os

DANGEROUS_TOOLS = ["Bash", "Write", "Delete", "Execute"]
DANGEROUS_PATTERNS = ["rm -rf", "sudo", "chmod 777", "DROP TABLE"]

def main():
    event_data = json.loads(sys.stdin.read())
    
    payload = event_data.get("payload", {})
    tool_name = payload.get("tool_name", "")
    tool_input = str(payload.get("tool_input", {}))
    
    requires_approval = False
    reason = ""
    
    # Check for dangerous tools
    if tool_name in DANGEROUS_TOOLS:
        requires_approval = True
        reason = f"Tool '{tool_name}' requires approval"
    
    # Check for dangerous patterns
    for pattern in DANGEROUS_PATTERNS:
        if pattern.lower() in tool_input.lower():
            requires_approval = True
            reason = f"Command contains '{pattern}'"
            break
    
    if requires_approval:
        event_data["humanInTheLoop"] = True
        event_data["humanInTheLoopQuestion"] = f"⚠️ Approval Required: {reason}"
        event_data["humanInTheLoopType"] = "permission"
    
    print(json.dumps(event_data))

if __name__ == "__main__":
    main()
