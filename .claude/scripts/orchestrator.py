#!/usr/bin/env python3
"""
Master Orchestrator - Prime Layer Agent Coordination

The "brain" that coordinates all Super Agent Monitor components.
Implements the Prime/Orchestrator pattern from MACS architecture.

Methods:
- Batch processing of agent tasks
- Context-aware delegation
- Cross-swarm coordination
- Budget-aware spawning

Usage:
    python scripts/orchestrator.py plan --goal "Build authentication system"
    python scripts/orchestrator.py execute --plan /path/to/plan.json
    python scripts/orchestrator.py delegate --task "Review security" --to security-swarm
"""

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


@dataclass
class Task:
    """A task in the execution plan."""
    id: str
    description: str
    agent_type: str  # single, swarm, council
    agent: str
    priority: int = 1
    dependencies: List[str] = None
    status: str = "pending"
    result: Optional[Dict] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


@dataclass
class ExecutionPlan:
    """An execution plan with ordered tasks."""
    plan_id: str
    goal: str
    tasks: List[Task]
    created_at: str = None
    status: str = "pending"
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow().isoformat()


class MasterOrchestrator:
    """
    Prime Layer orchestration.
    
    Responsibilities:
    1. PLAN: Break goals into delegatable tasks
    2. DELEGATE: Assign tasks to appropriate agents/swarms
    3. COORDINATE: Handle dependencies and sequencing
    4. SYNTHESIZE: Aggregate results from multiple agents
    """
    
    SCRIPTS_DIR = Path(__file__).parent
    PLANS_DIR = Path(".super_agent_monitor/plans")
    
    def __init__(self):
        self.PLANS_DIR.mkdir(parents=True, exist_ok=True)
    
    def create_plan(self, goal: str) -> ExecutionPlan:
        """
        Create an execution plan for a goal.
        
        This is a simplified planner - in production would use
        LLM to decompose complex goals.
        """
        import uuid
        plan_id = str(uuid.uuid4())[:8]
        
        # Simple heuristic-based task decomposition
        tasks = []
        
        # Always start with analysis
        tasks.append(Task(
            id=f"{plan_id}-1",
            description=f"Analyze requirements for: {goal}",
            agent_type="single",
            agent="analyzer",
            priority=1
        ))
        
        # Add planning phase
        tasks.append(Task(
            id=f"{plan_id}-2",
            description=f"Create implementation plan for: {goal}",
            agent_type="single",
            agent="product-manager",
            priority=2,
            dependencies=[f"{plan_id}-1"]
        ))
        
        # Keyword-based swarm selection
        goal_lower = goal.lower()
        
        if any(kw in goal_lower for kw in ["security", "audit", "vulnerability"]):
            tasks.append(Task(
                id=f"{plan_id}-3",
                description=f"Security review for: {goal}",
                agent_type="swarm",
                agent="security-swarm",
                priority=3,
                dependencies=[f"{plan_id}-2"]
            ))
        
        if any(kw in goal_lower for kw in ["test", "coverage", "qa"]):
            tasks.append(Task(
                id=f"{plan_id}-4",
                description=f"Test generation for: {goal}",
                agent_type="swarm",
                agent="test-swarm",
                priority=3,
                dependencies=[f"{plan_id}-2"]
            ))
        
        if any(kw in goal_lower for kw in ["api", "endpoint", "route"]):
            tasks.append(Task(
                id=f"{plan_id}-5",
                description=f"API development for: {goal}",
                agent_type="swarm",
                agent="api-swarm",
                priority=3,
                dependencies=[f"{plan_id}-2"]
            ))
        
        if any(kw in goal_lower for kw in ["performance", "optimize", "speed"]):
            tasks.append(Task(
                id=f"{plan_id}-6",
                description=f"Performance optimization for: {goal}",
                agent_type="swarm",
                agent="performance-swarm",
                priority=4,
                dependencies=[f"{plan_id}-3"] if f"{plan_id}-3" in [t.id for t in tasks] else [f"{plan_id}-2"]
            ))
        
        # Final review via council
        tasks.append(Task(
            id=f"{plan_id}-final",
            description=f"Final review and decision for: {goal}",
            agent_type="council",
            agent="review-council",
            priority=5,
            dependencies=[t.id for t in tasks if t.priority == max(t.priority for t in tasks)]
        ))
        
        plan = ExecutionPlan(
            plan_id=plan_id,
            goal=goal,
            tasks=tasks
        )
        
        # Save plan
        self._save_plan(plan)
        
        return plan
    
    def _save_plan(self, plan: ExecutionPlan):
        """Save plan to disk."""
        plan_path = self.PLANS_DIR / f"{plan.plan_id}.json"
        with open(plan_path, 'w') as f:
            json.dump(asdict(plan), f, indent=2)
    
    def _load_plan(self, plan_id: str) -> Optional[ExecutionPlan]:
        """Load plan from disk."""
        plan_path = self.PLANS_DIR / f"{plan_id}.json"
        if not plan_path.exists():
            return None
        
        with open(plan_path) as f:
            data = json.load(f)
        
        tasks = [Task(**t) for t in data.pop('tasks')]
        return ExecutionPlan(tasks=tasks, **data)
    
    def execute_plan(self, plan_id: str, dry_run: bool = False) -> Dict:
        """Execute all tasks in a plan."""
        plan = self._load_plan(plan_id)
        if not plan:
            return {"success": False, "error": f"Plan not found: {plan_id}"}
        
        plan.status = "running"
        results = []
        
        # Sort by priority and dependencies
        sorted_tasks = sorted(plan.tasks, key=lambda t: t.priority)
        completed = set()
        
        for task in sorted_tasks:
            # Check dependencies
            deps_met = all(d in completed for d in task.dependencies)
            if not deps_met:
                task.status = "blocked"
                continue
            
            if dry_run:
                task.status = "would_run"
                task.result = {"dry_run": True}
            else:
                task.status = "running"
                result = self._execute_task(task)
                task.status = "completed" if result.get("success") else "failed"
                task.result = result
            
            completed.add(task.id)
            results.append({
                "task_id": task.id,
                "status": task.status,
                "result": task.result
            })
        
        plan.status = "completed"
        self._save_plan(plan)
        
        return {
            "success": True,
            "plan_id": plan_id,
            "tasks_executed": len([r for r in results if r["status"] in ["completed", "would_run"]]),
            "results": results
        }
    
    def _execute_task(self, task: Task) -> Dict:
        """Execute a single task."""
        spawner_cmd = [
            sys.executable,
            str(self.SCRIPTS_DIR / "agent_spawner.py"),
        ]
        
        if task.agent_type == "single":
            spawner_cmd.extend([
                "spawn",
                "--agent", task.agent,
                "--prompt", task.description,
                "--json"
            ])
        elif task.agent_type == "swarm":
            spawner_cmd.extend([
                "swarm",
                "--swarm", task.agent,
                "--prompt", task.description,
                "--json"
            ])
        elif task.agent_type == "council":
            spawner_cmd.extend([
                "council",
                "--topic", task.description,
                "--json"
            ])
        
        try:
            result = subprocess.run(spawner_cmd, capture_output=True, text=True, timeout=600)
            if result.returncode == 0:
                return json.loads(result.stdout)
            return {"success": False, "error": result.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def delegate(self, task: str, to: str) -> Dict:
        """Delegate a single task to an agent or swarm."""
        # Determine if 'to' is a swarm or agent
        if to.endswith("-swarm"):
            return self._execute_task(Task(
                id="delegate-1",
                description=task,
                agent_type="swarm",
                agent=to
            ))
        else:
            return self._execute_task(Task(
                id="delegate-1",
                description=task,
                agent_type="single",
                agent=to
            ))
    
    def list_plans(self) -> List[Dict]:
        """List all saved plans."""
        plans = []
        for plan_file in self.PLANS_DIR.glob("*.json"):
            with open(plan_file) as f:
                data = json.load(f)
            plans.append({
                "plan_id": data["plan_id"],
                "goal": data["goal"][:50],
                "tasks": len(data["tasks"]),
                "status": data["status"]
            })
        return plans


def main():
    parser = argparse.ArgumentParser(
        description='Master Orchestrator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # Plan command
    plan_parser = subparsers.add_parser('plan', help='Create execution plan')
    plan_parser.add_argument('--goal', '-g', required=True, help='Goal to plan')
    plan_parser.add_argument('--json', action='store_true', help='JSON output')
    
    # Execute command
    exec_parser = subparsers.add_parser('execute', help='Execute a plan')
    exec_parser.add_argument('--plan', '-p', required=True, help='Plan ID or path')
    exec_parser.add_argument('--dry-run', '-n', action='store_true', help="Don't execute")
    exec_parser.add_argument('--json', action='store_true', help='JSON output')
    
    # Delegate command
    delegate_parser = subparsers.add_parser('delegate', help='Delegate task')
    delegate_parser.add_argument('--task', '-t', required=True, help='Task to delegate')
    delegate_parser.add_argument('--to', required=True, help='Agent or swarm')
    delegate_parser.add_argument('--json', action='store_true', help='JSON output')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List plans')
    list_parser.add_argument('--json', action='store_true', help='JSON output')
    
    args = parser.parse_args()
    orchestrator = MasterOrchestrator()
    
    if args.command == 'plan':
        plan = orchestrator.create_plan(args.goal)
        
        if args.json:
            print(json.dumps(asdict(plan), indent=2))
        else:
            print(f"📋 Plan created: {plan.plan_id}")
            print(f"   Goal: {plan.goal}")
            print(f"   Tasks: {len(plan.tasks)}")
            for task in plan.tasks:
                print(f"   • [{task.priority}] {task.agent_type}/{task.agent}: {task.description[:40]}...")
    
    elif args.command == 'execute':
        result = orchestrator.execute_plan(args.plan, args.dry_run)
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if result["success"]:
                action = "Would execute" if args.dry_run else "Executed"
                print(f"✅ {action} {result['tasks_executed']} tasks")
            else:
                print(f"❌ {result['error']}")
    
    elif args.command == 'delegate':
        result = orchestrator.delegate(args.task, args.to)
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if result.get("success"):
                print(f"✅ Delegated to {args.to}")
            else:
                print(f"❌ {result.get('error', 'Failed')}")
    
    elif args.command == 'list':
        plans = orchestrator.list_plans()
        
        if args.json:
            print(json.dumps({"plans": plans}, indent=2))
        else:
            print(f"📋 {len(plans)} plans:")
            for p in plans:
                print(f"   • {p['plan_id']}: {p['goal']} ({p['tasks']} tasks, {p['status']})")


if __name__ == "__main__":
    main()
