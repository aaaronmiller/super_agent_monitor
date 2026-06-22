#!/usr/bin/env python3
"""Session Start Hook"""
import json
from datetime import datetime
from pathlib import Path

def init_memory_bank():
    """Initialize Memory Bank"""
    root = Path(__file__).parent.parent.parent
    memory_dir = root / "memory"
    memory_dir.mkdir(exist_ok=True)
    
    memory_bank = {
        "session_id": datetime.now().isoformat(),
        "status": "initialized",
        "metadata": {},
        "data": {}
    }
    
    (memory_dir / "memory-bank.json").write_text(json.dumps(memory_bank, indent=2))
    print(f"[Swarm] Memory Bank initialized")

if __name__ == "__main__":
    init_memory_bank()
