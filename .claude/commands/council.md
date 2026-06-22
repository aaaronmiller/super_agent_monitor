---
description: View current council votes and agent standings
---

# Council

Manage the Byzantine Fault Tolerant council voting system.

## List Active Councils

```bash
python scripts/council.py list
```

## Show Council Status

```bash
python scripts/council.py status --council-id $1
```

## Cast a Vote

```bash
python scripts/council.py vote --council-id $1 --agent $2 --score $3 --rationale "$4"
```

## View Agent Strikes

```bash
python scripts/council.py strikes
```

## Two-Strike Rule

Agents with 2+ consecutive low scores (<0.5) are terminated.
