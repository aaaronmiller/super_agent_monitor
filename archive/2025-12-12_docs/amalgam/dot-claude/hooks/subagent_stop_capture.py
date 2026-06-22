#!/usr/bin/env python3
# ---
# name: subagent-stop-capture
# description: Capture subagent outputs and log performance for mutagen system.
# ---

import sys, json, os, hashlib, time
from datetime import datetime
from pathlib import Path

def main():
    try:
        payload = json.load(sys.stdin)
    except:
        payload = {}

    agent = payload.get("agent") or payload.get("agentName") or "unknown-agent"
    text = payload.get("text", "")
    agent_id = payload.get("agentId") or payload.get("id") or f"exec_{int(time.time())}"
    batch_id = payload.get("batch_id", "unknown_batch")

    # Create directories
    outdir = Path(".claude/subagent_reports")
    outdir.mkdir(parents=True, exist_ok=True)

    memory_dir = Path(".claude/memory")
    memory_dir.mkdir(parents=True, exist_ok=True)

    # Save subagent output
    fname = f"{agent}-{agent_id}.md"
    path = outdir / fname
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

    # Extract metrics from output if available
    quality_score = None
    tokens_used = None
    errors = []

    # Try to parse metrics from output
    try:
        if "```json" in text:
            json_start = text.find("```json") + 7
            json_end = text.find("```", json_start)
            if json_end > json_start:
                metrics_json = json.loads(text[json_start:json_end])
                quality_score = metrics_json.get("metrics", {}).get("quality_score")
                tokens_used = metrics_json.get("metrics", {}).get("context_tokens_used")
    except:
        pass

    # Create performance log entry
    exec_id = f"exec_{int(time.time())}_{agent_id}"
    entry = {
        "agent_type": agent,
        "execution_id": exec_id,
        "timestamp": datetime.now().isoformat(),
        "batch_id": batch_id,
        "metrics": {
            "context_tokens_used": tokens_used or "unknown",
            "payload_tokens_used": tokens_used or "unknown",  # approximation
            "quality_score": quality_score,
            "success": quality_score is not None if quality_score is not None else True,
            "errors": errors,
            "files_processed": "unknown",
            "time_seconds": "unknown"
        },
        "output_file": str(path),
        "output_hash": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "lessons_learned": "",
        "next_run_adjustments": {}
    }

    # Append to global performance index
    index_path = memory_dir / "agent_performance.json"
    try:
        if index_path.exists():
            with open(index_path, "r", encoding="utf-8") as idxf:
                idx = json.load(idxf)
        else:
            idx = []
        idx.append(entry)

        # Keep only last 100 executions (mutagen memory depth)
        if len(idx) > 100:
            idx = idx[-100:]

        with open(index_path, "w", encoding="utf-8") as idxf:
            json.dump(idx, idxf, indent=2)
    except Exception as e:
        print(f"Failed to update performance index: {e}", file=sys.stderr)

    print(f"Saved subagent output to {path}")
    print(f"Performance logged to {index_path}")
    sys.exit(0)

if __name__ == "__main__":
    main()
