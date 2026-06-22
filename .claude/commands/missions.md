---
description: List and manage running missions
---

# Missions

Manage headless agent missions.

## List Running Missions

```bash
python scripts/mission_launcher.py list
```

## Show Mission Details

```bash
python scripts/mission_launcher.py status --mission-id $1
```

## Stop a Mission

```bash
python scripts/mission_launcher.py stop --mission-id $1
```

## Clean Up Completed Missions

```bash
python scripts/mission_launcher.py cleanup
```

## Emergency Stop All

```bash
python scripts/mission_launcher.py nuke
```
