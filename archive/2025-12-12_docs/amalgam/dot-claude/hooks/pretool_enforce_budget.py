#!/usr/bin/env python3
# ---
# name: pretool-enforce-budget
# description: Hook to ensure subagents receive required budget parameters. Blocks if missing.
# ---

import sys, json, os
from pathlib import Path

def main():
    # Claude passes hook payload JSON on stdin
    try:
        payload = json.load(sys.stdin)
    except:
        payload = {}

    # Extract agent info
    agent = payload.get("agent") or payload.get("agentName") or "unknown"
    event = payload.get("event") or {}

    # Get manager invocation from various possible locations
    user_meta = event.get("user", {}) if isinstance(event, dict) else {}
    meta = user_meta.get("manager_invocation") or payload.get("manager_invocation") or {}

    # REQUIRED budget fields
    required_fields = {
        "subagent_budget_tokens": 150000,
        "payload_budget_tokens": 40000,
        "payload_utilization_target": 0.75,
        "batch_id": None,
        "model_hint": None
    }

    missing = []
    for field, expected in required_fields.items():
        if field not in meta:
            missing.append(field)
        elif expected is not None and meta[field] != expected:
            # Check if value makes sense
            if field == "subagent_budget_tokens" and meta[field] != 150000:
                missing.append(f"{field} (must be 150000)")

    if missing:
        decision = {
            "decision": "block",
            "permissionDecisionReason": f"Missing/invalid required budget fields for agent {agent}: {', '.join(missing)}. "
                                       f"All subagents MUST receive: subagent_budget_tokens=150000, "
                                       f"payload_budget_tokens=40000, payload_utilization_target=0.75, "
                                       f"batch_id, and model_hint",
            "continue": False
        }
        print(json.dumps(decision, indent=2))
        sys.exit(2)

    # Log successful validation
    os.makedirs(".claude/memory", exist_ok=True)
    log_path = ".claude/memory/hook_validations.log"
    with open(log_path, "a") as f:
        f.write(f"{meta.get('batch_id', 'unknown')}: {agent} - budgets validated\n")

    # Allow the action
    decision = {
        "decision": "allow",
        "continue": True,
        "validated_fields": {
            "subagent_budget_tokens": meta.get("subagent_budget_tokens"),
            "payload_budget_tokens": meta.get("payload_budget_tokens"),
            "model_hint": meta.get("model_hint")
        }
    }
    print(json.dumps(decision))
    sys.exit(0)

if __name__ == "__main__":
    main()
