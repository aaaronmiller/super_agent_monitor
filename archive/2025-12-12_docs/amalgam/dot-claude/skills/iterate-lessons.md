# Skill: iterate-lessons
## Purpose
Generate iteration candidates based on recent runs using real iteration-manager and symptom-detector.

## Implementation
- Use:
  - `src/iteration/iteration-manager.ts`
  - `src/core/symptom-detector.ts`
- Output:
  - Proposed rules/patterns/prompts to adjust
- Mark as "proposals", not auto-applied

## Input
- `recent_runs` (from memory snapshots)
- `iteration_config` (optional)
- `learning_scope` (optional)

## Output
- List of proposed iteration candidates
- Rationale for each proposal
- Expected impact assessment

## Safety
- Read-only on project files
- Only writes to `.delobotomize/iterations/proposals/`
- Marked as proposals, not active rules
