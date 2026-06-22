---
description: Scan project for file lineage and evolution relationships
argument-hint: [command]
---

# File Phylogeny

Track how files evolve and relate to each other.

## Commands

- `/phylogeny scan` - Build `.lineage.json` with all file relationships
- `/phylogeny graph` - Generate mermaid visualization
- `/phylogeny show <file>` - Inspect lineage for one file
- `/phylogeny similar <file>` - Find similar files (by content)

## Usage

```bash
python .claude/scripts/phylogeny.py scan
python .claude/scripts/phylogeny.py graph > lineage.mmd
python .claude/scripts/phylogeny.py show .claude/hooks/tts_service.py
```
