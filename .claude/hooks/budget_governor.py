#!/usr/bin/env python3
"""
Budget Governor Hook

Pre-Tool-Use hook that blocks expensive operations when budget is exhausted.
Implements the "Metabolic Constraints" pattern from MACS architecture.

This hook runs before spawn_mission, spawn_sub_orchestrator, or similar operations.

Usage:
    # Check budget before operation
    python .claude/hooks/budget_governor.py --operation spawn --estimated-cost 0.50
    
    # Update budget state
    python .claude/hooks/budget_governor.py --update --spent 0.25
    
    # Show current budget
    python .claude/hooks/budget_governor.py --status
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional


class BudgetGovernor:
    """
    Budget Governor for metabolic constraints.
    
    Key principles from MACS:
    - Hooks are "Autonomic Regulation"
    - Cost > Budget = Pain Signal (block the action)
    - Budget limits force evolution of smarter heuristics
    """
    
    STATE_FILE = Path(".super_agent_monitor/budget.json")
    
    # Default budget configuration
    DEFAULT_CONFIG = {
        "daily_budget": 10.00,      # USD per day
        "hourly_limit": 2.00,       # Max per hour
        "operation_limit": 1.00,    # Max per operation
        "warning_threshold": 0.20,  # Warn when 20% remaining
        "critical_threshold": 0.05  # Block when 5% remaining
    }
    
    # Estimated costs per operation type
    OPERATION_COSTS = {
        "spawn_mission": 0.15,
        "spawn_sub_orchestrator": 0.50,
        "spawn_swarm": 1.00,
        "council_vote": 0.25,
        "rag_query": 0.02,
        "tts_generate": 0.01,
        "default": 0.10
    }
    
    def __init__(self):
        self._load_state()
    
    def _load_state(self):
        """Load or initialize budget state."""
        if self.STATE_FILE.exists():
            try:
                with open(self.STATE_FILE) as f:
                    self.state = json.load(f)
            except Exception:
                self.state = self._init_state()
        else:
            self.state = self._init_state()
        
        # Reset if new day
        last_reset = datetime.fromisoformat(self.state.get("last_reset", "2000-01-01"))
        if datetime.utcnow().date() > last_reset.date():
            self._reset_daily()
    
    def _init_state(self) -> Dict:
        """Initialize fresh budget state."""
        return {
            "config": self.DEFAULT_CONFIG.copy(),
            "spent_today": 0.0,
            "spent_this_hour": 0.0,
            "last_reset": datetime.utcnow().isoformat(),
            "last_hour_reset": datetime.utcnow().isoformat(),
            "operations": []
        }
    
    def _reset_daily(self):
        """Reset daily budget."""
        self.state["spent_today"] = 0.0
        self.state["last_reset"] = datetime.utcnow().isoformat()
        self.state["operations"] = []
        self._save_state()
    
    def _reset_hourly(self):
        """Reset hourly limit."""
        self.state["spent_this_hour"] = 0.0
        self.state["last_hour_reset"] = datetime.utcnow().isoformat()
    
    def _save_state(self):
        """Save budget state to disk."""
        self.STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(self.STATE_FILE, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def check_budget(
        self,
        operation: str,
        estimated_cost: Optional[float] = None
    ) -> Dict:
        """
        Check if operation is within budget.
        
        Returns:
            {
                "allowed": bool,
                "reason": str,
                "remaining_daily": float,
                "remaining_hourly": float,
                "estimated_cost": float
            }
        """
        config = self.state["config"]
        
        # Check hourly reset
        last_hour = datetime.fromisoformat(self.state.get("last_hour_reset", datetime.utcnow().isoformat()))
        if datetime.utcnow() - last_hour > timedelta(hours=1):
            self._reset_hourly()
        
        # Get estimated cost
        if estimated_cost is None:
            estimated_cost = self.OPERATION_COSTS.get(operation, self.OPERATION_COSTS["default"])
        
        # Calculate remaining
        remaining_daily = config["daily_budget"] - self.state["spent_today"]
        remaining_hourly = config["hourly_limit"] - self.state["spent_this_hour"]
        
        result = {
            "allowed": True,
            "reason": "OK",
            "remaining_daily": remaining_daily,
            "remaining_hourly": remaining_hourly,
            "estimated_cost": estimated_cost,
            "warning": None
        }
        
        # Check operation limit
        if estimated_cost > config["operation_limit"]:
            result["allowed"] = False
            result["reason"] = f"Operation cost ${estimated_cost:.2f} exceeds limit ${config['operation_limit']:.2f}"
            return result
        
        # Check hourly limit
        if estimated_cost > remaining_hourly:
            result["allowed"] = False
            result["reason"] = f"Hourly limit reached. Remaining: ${remaining_hourly:.2f}"
            return result
        
        # Check daily budget
        if estimated_cost > remaining_daily:
            result["allowed"] = False
            result["reason"] = f"Daily budget exhausted. Remaining: ${remaining_daily:.2f}"
            return result
        
        # Check warning threshold
        remaining_pct = remaining_daily / config["daily_budget"]
        if remaining_pct <= config["warning_threshold"]:
            result["warning"] = f"Budget low: {remaining_pct*100:.0f}% remaining"
        
        # Check critical threshold
        if remaining_pct <= config["critical_threshold"]:
            result["allowed"] = False
            result["reason"] = f"CRITICAL: Only {remaining_pct*100:.0f}% budget remaining"
            return result
        
        return result
    
    def record_spend(self, operation: str, amount: float):
        """Record an expenditure."""
        self.state["spent_today"] += amount
        self.state["spent_this_hour"] += amount
        self.state["operations"].append({
            "operation": operation,
            "amount": amount,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Keep only last 100 operations
        self.state["operations"] = self.state["operations"][-100:]
        self._save_state()
    
    def get_status(self) -> Dict:
        """Get current budget status."""
        config = self.state["config"]
        remaining_daily = config["daily_budget"] - self.state["spent_today"]
        remaining_hourly = config["hourly_limit"] - self.state["spent_this_hour"]
        
        return {
            "daily_budget": config["daily_budget"],
            "spent_today": self.state["spent_today"],
            "remaining_daily": remaining_daily,
            "remaining_pct": (remaining_daily / config["daily_budget"]) * 100,
            "hourly_limit": config["hourly_limit"],
            "spent_this_hour": self.state["spent_this_hour"],
            "remaining_hourly": remaining_hourly,
            "operation_count": len(self.state["operations"]),
            "last_reset": self.state["last_reset"]
        }
    
    def set_budget(self, daily: Optional[float] = None, hourly: Optional[float] = None):
        """Update budget limits."""
        if daily is not None:
            self.state["config"]["daily_budget"] = daily
        if hourly is not None:
            self.state["config"]["hourly_limit"] = hourly
        self._save_state()


def main():
    parser = argparse.ArgumentParser(
        description='Budget Governor Hook',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument('--operation', '-o', help='Operation type to check')
    parser.add_argument('--estimated-cost', '-c', type=float, help='Estimated cost')
    parser.add_argument('--update', action='store_true', help='Record spend')
    parser.add_argument('--spent', type=float, help='Amount spent (with --update)')
    parser.add_argument('--status', action='store_true', help='Show budget status')
    parser.add_argument('--set-daily', type=float, help='Set daily budget')
    parser.add_argument('--set-hourly', type=float, help='Set hourly limit')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    governor = BudgetGovernor()
    
    try:
        if args.status:
            status = governor.get_status()
            
            if args.json:
                print(json.dumps(status, indent=2))
            else:
                print("💰 Budget Status:")
                print(f"  📅 Daily: ${status['spent_today']:.2f} / ${status['daily_budget']:.2f} ({status['remaining_pct']:.0f}% remaining)")
                print(f"  ⏰ Hourly: ${status['spent_this_hour']:.2f} / ${status['hourly_limit']:.2f}")
                print(f"  📊 Operations today: {status['operation_count']}")
        
        elif args.update and args.spent is not None:
            operation = args.operation or "manual"
            governor.record_spend(operation, args.spent)
            
            if args.json:
                print(json.dumps({"success": True, "spent": args.spent}))
            else:
                print(f"✅ Recorded ${args.spent:.2f} for {operation}")
        
        elif args.operation:
            result = governor.check_budget(args.operation, args.estimated_cost)
            
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                if result["allowed"]:
                    icon = "⚠️" if result.get("warning") else "✅"
                    print(f"{icon} ALLOWED: {args.operation} (${result['estimated_cost']:.2f})")
                    if result.get("warning"):
                        print(f"  {result['warning']}")
                else:
                    print(f"❌ BLOCKED: {result['reason']}")
                    sys.exit(2)  # Exit code 2 = blocked by governor
        
        elif args.set_daily or args.set_hourly:
            governor.set_budget(daily=args.set_daily, hourly=args.set_hourly)
            print("✅ Budget limits updated")
        
        else:
            parser.print_help()
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
