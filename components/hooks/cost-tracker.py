#!/usr/bin/env python3
"""
Cost Tracker Hook
Monitors API usage and calculates costs in real-time

Triggers: After tool use (API calls)
Purpose: Track token usage and costs per session
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Pricing per 1M tokens (as of 2025-01-19)
PRICING = {
    "claude-sonnet-4": {"input": 3.00, "output": 15.00},
    "claude-opus-4": {"input": 15.00, "output": 75.00},
    "claude-haiku-3": {"input": 0.25, "output": 1.25},
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
}

def get_model_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """Calculate cost for given model and token usage"""
    # Normalize model name (handle versions)
    model_key = model.lower()
    for key in PRICING:
        if key in model_key:
            pricing = PRICING[key]
            input_cost = (input_tokens / 1_000_000) * pricing["input"]
            output_cost = (output_tokens / 1_000_000) * pricing["output"]
            return round(input_cost + output_cost, 6)

    # Default pricing if model not found
    return round((input_tokens / 1_000_000) * 3.0 + (output_tokens / 1_000_000) * 15.0, 6)

def format_currency(amount: float) -> str:
    """Format cost as currency"""
    if amount < 0.01:
        return f"${amount:.6f}"
    return f"${amount:.4f}"

def track_cost(event: dict):
    """
    Track cost from API event

    Event structure:
    {
        "type": "api_response",
        "model": "claude-sonnet-4",
        "usage": {
            "input_tokens": 1234,
            "output_tokens": 567
        },
        "timestamp": "2025-01-19T10:30:00Z"
    }
    """
    model = event.get("model", "unknown")
    usage = event.get("usage", {})
    input_tokens = usage.get("input_tokens", 0)
    output_tokens = usage.get("output_tokens", 0)

    # Calculate cost
    cost = get_model_cost(model, input_tokens, output_tokens)

    # Load session cost log
    cost_log_path = Path(".super_agent_monitor/session_costs.json")
    cost_log_path.parent.mkdir(parents=True, exist_ok=True)

    if cost_log_path.exists():
        with open(cost_log_path, "r") as f:
            cost_log = json.load(f)
    else:
        cost_log = {
            "session_id": event.get("session_id", "unknown"),
            "total_cost": 0.0,
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "events": []
        }

    # Update totals
    cost_log["total_cost"] += cost
    cost_log["total_input_tokens"] += input_tokens
    cost_log["total_output_tokens"] += output_tokens
    cost_log["events"].append({
        "timestamp": event.get("timestamp", datetime.utcnow().isoformat()),
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cost": cost
    })

    # Save updated log
    with open(cost_log_path, "w") as f:
        json.dump(cost_log, f, indent=2)

    # Print cost summary
    print(f"\\n💰 Cost Tracker")
    print(f"   Model: {model}")
    print(f"   Tokens: {input_tokens:,} in / {output_tokens:,} out")
    print(f"   This call: {format_currency(cost)}")
    print(f"   Session total: {format_currency(cost_log['total_cost'])}")

    # Warn if costs are high
    if cost_log["total_cost"] > 1.0:
        print(f"   ⚠️  Session cost exceeds $1.00")
    if cost_log["total_cost"] > 10.0:
        print(f"   🚨 SESSION COST EXCEEDS $10.00 - Consider halting!")

def main():
    """Hook entrypoint"""
    # Read event from stdin
    try:
        event = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        print("Error: Invalid JSON input", file=sys.stderr)
        sys.exit(1)

    # Only track API response events
    if event.get("type") == "api_response" and "usage" in event:
        track_cost(event)

    # Allow execution to continue
    sys.exit(0)

if __name__ == "__main__":
    main()
