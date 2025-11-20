#!/usr/bin/env python3
"""
Stall Detector Hook
Monitors session activity and detects stalls (no progress for X seconds)

Triggers: After tool use
Purpose: Detect when session is stuck and needs restart
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Stall detection threshold (seconds)
STALL_THRESHOLD_SECONDS = 300  # 5 minutes

def parse_timestamp(ts_str: str) -> datetime:
    """Parse ISO timestamp to datetime"""
    try:
        return datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
    except:
        return datetime.now(timezone.utc)

def check_stall(event: dict):
    """
    Check if session has stalled

    Event structure:
    {
        "type": "tool_use",
        "tool": "Read",
        "timestamp": "2025-01-19T10:30:00Z",
        "session_id": "sess-123"
    }
    """
    session_id = event.get("session_id", "unknown")
    current_time = parse_timestamp(event.get("timestamp", datetime.now(timezone.utc).isoformat()))

    # Load activity log
    activity_log_path = Path(f".super_agent_monitor/session_activity.json")
    activity_log_path.parent.mkdir(parents=True, exist_ok=True)

    if activity_log_path.exists():
        with open(activity_log_path, "r") as f:
            activity_log = json.load(f)
    else:
        activity_log = {
            "session_id": session_id,
            "last_activity": current_time.isoformat(),
            "activity_count": 0,
            "stalls_detected": 0
        }

    # Calculate time since last activity
    last_activity = parse_timestamp(activity_log["last_activity"])
    time_since_last = (current_time - last_activity).total_seconds()

    # Update activity log
    activity_log["last_activity"] = current_time.isoformat()
    activity_log["activity_count"] += 1

    # Check for stall
    is_stalled = time_since_last > STALL_THRESHOLD_SECONDS

    if is_stalled:
        activity_log["stalls_detected"] += 1
        print(f"\\n⚠️  Stall Detected!")
        print(f"   Last activity: {int(time_since_last)}s ago")
        print(f"   Threshold: {STALL_THRESHOLD_SECONDS}s")
        print(f"   Total stalls this session: {activity_log['stalls_detected']}")
        print(f"   Recommendation: Check session logs and consider restart")

        # Save stall event
        stalls_log_path = Path(f".super_agent_monitor/stalls.json")
        if stalls_log_path.exists():
            with open(stalls_log_path, "r") as f:
                stalls = json.load(f)
        else:
            stalls = []

        stalls.append({
            "session_id": session_id,
            "detected_at": current_time.isoformat(),
            "stall_duration_seconds": time_since_last,
            "activity_count_at_detection": activity_log["activity_count"]
        })

        with open(stalls_log_path, "w") as f:
            json.dump(stalls, f, indent=2)

    else:
        # Normal activity
        if activity_log["activity_count"] % 10 == 0:
            # Print status every 10 activities
            print(f"\\n✅ Session Active")
            print(f"   Activities: {activity_log['activity_count']}")
            print(f"   Last activity: {int(time_since_last)}s ago")

    # Save updated activity log
    with open(activity_log_path, "w") as f:
        json.dump(activity_log, f, indent=2)

    # Exit with error code if stalled (can be used to trigger restart)
    if is_stalled and activity_log["stalls_detected"] >= 3:
        print(f"\\n🚨 CRITICAL: 3+ stalls detected. Auto-restart recommended.")
        # Don't actually exit with error - let orchestrator decide
        # sys.exit(1)

def main():
    """Hook entrypoint"""
    # Read event from stdin
    try:
        event = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        print("Error: Invalid JSON input", file=sys.stderr)
        sys.exit(1)

    # Track any event as activity
    if event.get("type") in ["tool_use", "api_request", "api_response"]:
        check_stall(event)

    # Allow execution to continue
    sys.exit(0)

if __name__ == "__main__":
    main()
