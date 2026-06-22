# Skill: scan-project
## Purpose
Run the real delobotomize scanner over the current repository.

## Implementation
- If built:
  - Run: `node dist/cli/delobotomize.js scan --format json`
- Else (dev):
  - Run: `npx tsx src/cli/delobotomize.ts scan --format json`
- Return parsed JSON with findings and health scores.
- Do not modify any files.

## Input
- `project_path` (optional, defaults to current directory)
- `options` (optional, passed to scanner)

## Output
- Parsed JSON with scan results
- Health scores
- List of flagged issues
- File paths and categories

## Safety
- Read-only operation
- No file modifications
