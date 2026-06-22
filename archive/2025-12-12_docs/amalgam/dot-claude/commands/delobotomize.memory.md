# Command: /delobotomize.memory
## Purpose
Manage and query project memory snapshots and knowledge base.

## Usage
```
/delobotomize.memory <action> [options]
```

## Actions

### view
View memory snapshots and statistics.
```
/delobotomize.memory view [--limit <N>] [--format json|summary]
```

### search
Search across all memory snapshots.
```
/delobotomize.memory search <query> [--type issue|fix|pattern] [--limit <N>]
```

### cleanup
Optimize memory storage and remove old entries.
```
/delobotomize.memory cleanup [--older-than <days>] [--dry-run]
```

### export
Export memory to external format.
```
/delobotomize.memory export [--format json|yaml] [--output <path>]
```

### import
Import external memory data.
```
/delobotomize.memory import <path> [--merge|replace]
```

## Options
- `--session <id>`: Specific session to query
- `--phase <name>`: Filter by phase
- `--since <date>`: Only show entries after date
- `--format`: Output format (json|summary|table)

## Example Interactions

### View Recent Runs
```
/delobotomize.memory view --limit 5
→ Shows last 5 run summaries with metrics
```

### Search for Issues
```
/delobotomize.memory search "unused import" --type issue
→ Returns all instances of unused import issues
```

### Cleanup Old Data
```
/delobotomize.memory cleanup --older-than 90 --dry-run
→ Previews what would be cleaned (doesn't delete)
```

## Memory Structure
```
.delobotomize/memory/
  snapshots/          # Individual run snapshots
  index/              # Search indexes
  archives/           # Compressed old data
  knowledge/          # Curated knowledge base
```

## Safety
- Read operations: Safe
- Write operations: Atomic
- Deletions: Require --confirm flag
- Import: Validates format and structure
- Export: Read-only operation
