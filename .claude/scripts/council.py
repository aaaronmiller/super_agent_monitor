#!/usr/bin/env python3
"""
Council Voting System

Implements Byzantine Fault Tolerance via peer voting.
Agents in a council vote on completion quality; lowest-voted agent
terminated after two consecutive failures.

Usage:
    python scripts/council.py spawn --size 5 --task "Review PR #123"
    python scripts/council.py vote --council-id abc123 --target agent-1 --score 0.8
    python scripts/council.py status --council-id abc123
"""

import argparse
import json
import os
import sys
import uuid
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict
from enum import Enum


class VoteScore(float, Enum):
    """Valid vote scores."""
    REJECT = 0.0
    PARTIAL = 0.5
    APPROVE = 1.0


@dataclass
class Vote:
    """A single vote from one agent about another."""
    voter_id: str
    target_id: str
    score: float  # 0.0, 0.5, or 1.0
    rationale: str
    encrypted: bool = False
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def validate(self) -> bool:
        """Validate vote is in correct format."""
        return self.score in [0.0, 0.5, 1.0] and self.voter_id != self.target_id


@dataclass
class CouncilRound:
    """A single voting round in a council."""
    round_number: int
    votes: List[Vote]
    started_at: str
    completed_at: Optional[str] = None
    consensus_reached: bool = False
    terminated_agent: Optional[str] = None


@dataclass
class Council:
    """A council of agents for Byzantine fault tolerance."""
    council_id: str
    task: str
    size: int
    agents: List[str]
    consensus_threshold: float = 0.8
    quorum: int = 3  # ceil(size/2) + 1
    rounds: List[CouncilRound] = field(default_factory=list)
    status: str = "active"  # active, completed, failed
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    consecutive_failures: Dict[str, int] = field(default_factory=dict)


class CouncilService:
    """Service for managing council voting."""
    
    COUNCIL_DIR = Path(".super_agent_monitor/councils")
    
    def __init__(self):
        self.COUNCIL_DIR.mkdir(parents=True, exist_ok=True)
    
    def _get_council_path(self, council_id: str) -> Path:
        return self.COUNCIL_DIR / f"{council_id}.json"
    
    def spawn_council(
        self,
        task: str,
        size: int = 5,
        agents: Optional[List[str]] = None,
        consensus_threshold: float = 0.8
    ) -> Council:
        """Spawn a new council for a task."""
        council_id = f"council-{uuid.uuid4().hex[:8]}"
        
        # Generate agent IDs if not provided
        if agents is None:
            agents = [f"agent-{i+1}" for i in range(size)]
        
        quorum = (size // 2) + 1  # ceil(n/2)
        
        council = Council(
            council_id=council_id,
            task=task,
            size=size,
            agents=agents,
            consensus_threshold=consensus_threshold,
            quorum=quorum,
            consecutive_failures={agent: 0 for agent in agents}
        )
        
        self._save_council(council)
        return council
    
    def _save_council(self, council: Council):
        """Save council state to disk."""
        path = self._get_council_path(council.council_id)
        
        # Convert to JSON-serializable dict
        data = asdict(council)
        
        # Handle rounds serialization
        serialized_rounds = []
        for r in council.rounds:
            round_dict = {
                'round_number': r.round_number,
                'started_at': r.started_at,
                'completed_at': r.completed_at,
                'consensus_reached': r.consensus_reached,
                'terminated_agent': r.terminated_agent,
                'votes': [asdict(v) for v in r.votes]
            }
            serialized_rounds.append(round_dict)
        data['rounds'] = serialized_rounds
        
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_council(self, council_id: str) -> Optional[Council]:
        """Load council from disk."""
        path = self._get_council_path(council_id)
        if not path.exists():
            return None
        
        with open(path) as f:
            data = json.load(f)
        
        # Reconstruct dataclasses
        rounds = []
        for r in data.get('rounds', []):
            votes = [Vote(**v) for v in r.get('votes', [])]
            rounds.append(CouncilRound(
                round_number=r['round_number'],
                votes=votes,
                started_at=r['started_at'],
                completed_at=r.get('completed_at'),
                consensus_reached=r.get('consensus_reached', False),
                terminated_agent=r.get('terminated_agent')
            ))
        
        return Council(
            council_id=data['council_id'],
            task=data['task'],
            size=data['size'],
            agents=data['agents'],
            consensus_threshold=data.get('consensus_threshold', 0.8),
            quorum=data.get('quorum', 3),
            rounds=rounds,
            status=data.get('status', 'active'),
            created_at=data['created_at'],
            consecutive_failures=data.get('consecutive_failures', {})
        )
    
    def start_round(self, council_id: str) -> CouncilRound:
        """Start a new voting round."""
        council = self.load_council(council_id)
        if not council:
            raise ValueError(f"Council not found: {council_id}")
        
        round_number = len(council.rounds) + 1
        new_round = CouncilRound(
            round_number=round_number,
            votes=[],
            started_at=datetime.utcnow().isoformat()
        )
        
        council.rounds.append(new_round)
        self._save_council(council)
        return new_round
    
    def cast_vote(
        self,
        council_id: str,
        voter_id: str,
        target_id: str,
        score: float,
        rationale: str
    ) -> Vote:
        """Cast a vote in the current round."""
        council = self.load_council(council_id)
        if not council:
            raise ValueError(f"Council not found: {council_id}")
        
        if not council.rounds:
            raise ValueError("No active round. Call start_round first.")
        
        current_round = council.rounds[-1]
        if current_round.completed_at:
            raise ValueError("Current round is completed.")
        
        vote = Vote(
            voter_id=voter_id,
            target_id=target_id,
            score=score,
            rationale=rationale
        )
        
        if not vote.validate():
            raise ValueError("Invalid vote: score must be 0.0, 0.5, or 1.0 and voter != target")
        
        current_round.votes.append(vote)
        self._save_council(council)
        return vote
    
    def complete_round(self, council_id: str) -> Dict:
        """Complete the current round and check for termination."""
        council = self.load_council(council_id)
        if not council:
            raise ValueError(f"Council not found: {council_id}")
        
        if not council.rounds:
            raise ValueError("No active round.")
        
        current_round = council.rounds[-1]
        current_round.completed_at = datetime.utcnow().isoformat()
        
        # Aggregate votes by target
        agent_scores: Dict[str, List[float]] = {a: [] for a in council.agents}
        for vote in current_round.votes:
            if vote.target_id in agent_scores:
                agent_scores[vote.target_id].append(vote.score)
        
        # Calculate average scores
        avg_scores = {}
        for agent, scores in agent_scores.items():
            if scores:
                avg_scores[agent] = sum(scores) / len(scores)
            else:
                avg_scores[agent] = 1.0  # Default to approved if no votes
        
        # Check consensus
        lowest_agent = min(avg_scores, key=avg_scores.get)
        lowest_score = avg_scores[lowest_agent]
        
        consensus_reached = lowest_score >= council.consensus_threshold
        current_round.consensus_reached = consensus_reached
        
        result = {
            "round": current_round.round_number,
            "consensus_reached": consensus_reached,
            "scores": avg_scores,
            "lowest_agent": lowest_agent,
            "lowest_score": lowest_score,
            "terminated": None
        }
        
        if not consensus_reached:
            # Increment failure count for lowest agent
            council.consecutive_failures[lowest_agent] = \
                council.consecutive_failures.get(lowest_agent, 0) + 1
            
            # Two-strike rule: terminate after 2 consecutive failures
            if council.consecutive_failures[lowest_agent] >= 2:
                current_round.terminated_agent = lowest_agent
                council.agents.remove(lowest_agent)
                result["terminated"] = lowest_agent
                print(f"⚠️ Agent {lowest_agent} terminated after 2 consecutive failures")
        else:
            # Reset all failure counts on consensus
            council.consecutive_failures = {a: 0 for a in council.agents}
        
        self._save_council(council)
        return result
    
    def get_status(self, council_id: str) -> Dict:
        """Get council status."""
        council = self.load_council(council_id)
        if not council:
            return {"error": f"Council not found: {council_id}"}
        
        return {
            "council_id": council.council_id,
            "task": council.task,
            "status": council.status,
            "agents": council.agents,
            "rounds_completed": len([r for r in council.rounds if r.completed_at]),
            "consecutive_failures": council.consecutive_failures
        }


def main():
    parser = argparse.ArgumentParser(
        description='Council Voting System',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # Spawn command
    spawn_parser = subparsers.add_parser('spawn', help='Spawn a new council')
    spawn_parser.add_argument('--size', '-s', type=int, default=5, help='Council size')
    spawn_parser.add_argument('--task', '-t', required=True, help='Task description')
    spawn_parser.add_argument('--threshold', type=float, default=0.8, help='Consensus threshold')
    spawn_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Vote command
    vote_parser = subparsers.add_parser('vote', help='Cast a vote')
    vote_parser.add_argument('--council-id', '-c', required=True, help='Council ID')
    vote_parser.add_argument('--voter', '-v', required=True, help='Voter agent ID')
    vote_parser.add_argument('--target', '-t', required=True, help='Target agent ID')
    vote_parser.add_argument('--score', '-s', type=float, required=True, choices=[0.0, 0.5, 1.0],
                            help='Vote score')
    vote_parser.add_argument('--rationale', '-r', default='', help='Vote rationale')
    vote_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Start round command
    round_parser = subparsers.add_parser('start-round', help='Start a voting round')
    round_parser.add_argument('--council-id', '-c', required=True, help='Council ID')
    round_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Complete round command  
    complete_parser = subparsers.add_parser('complete-round', help='Complete current round')
    complete_parser.add_argument('--council-id', '-c', required=True, help='Council ID')
    complete_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Get council status')
    status_parser.add_argument('--council-id', '-c', required=True, help='Council ID')
    status_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    service = CouncilService()
    
    try:
        if args.command == 'spawn':
            council = service.spawn_council(
                task=args.task,
                size=args.size,
                consensus_threshold=args.threshold
            )
            result = {
                "success": True,
                "council_id": council.council_id,
                "agents": council.agents,
                "task": council.task
            }
            
        elif args.command == 'vote':
            vote = service.cast_vote(
                council_id=args.council_id,
                voter_id=args.voter,
                target_id=args.target,
                score=args.score,
                rationale=args.rationale
            )
            result = {"success": True, "vote": asdict(vote)}
            
        elif args.command == 'start-round':
            round_obj = service.start_round(args.council_id)
            result = {"success": True, "round": round_obj.round_number}
            
        elif args.command == 'complete-round':
            result = service.complete_round(args.council_id)
            result["success"] = True
            
        elif args.command == 'status':
            result = service.get_status(args.council_id)
            result["success"] = True
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"✅ {args.command}: {json.dumps(result, indent=2)}")
            
    except Exception as e:
        result = {"success": False, "error": str(e)}
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
