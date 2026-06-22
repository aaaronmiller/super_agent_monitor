# Command: /delobotomize.iterate
## Purpose
Generate iteration proposals based on recent Delobotomize runs.

## Usage
```
/delobotomize.iterate [options]
```

## Behavior
1. **Collect recent run data**
2. **Analyze patterns and outcomes**
3. **Generate improvement proposals**
4. **Present as "proposals" (not active rules)**

## Options
- `--runs <N>`: Number of recent runs to analyze (default: 10)
- `--scope <all|scanner|remediation>`: Focus area (default: all)
- `--output <path>`: Save proposals to file (optional)

## Analysis Sources
- Recent memory snapshots
- Scan results trends
- Remediation success/failure
- Verification metrics
- Operator feedback

## Proposal Categories
1. **Detection Rules**
   - New scanner patterns
   - Improved heuristics
   - False positive reduction

2. **Remediation Strategies**
   - Better fix approaches
   - Safer auto-application
   - Improved verification

3. **Workflow Improvements**
   - Phase optimization
   - Hook refinements
   - Performance tuning

4. **Prompt Evolution**
   - Better LLM prompts
   - Context optimization
   - Response formatting

## Example Output
```
Generated 5 iteration proposals:

1. **[Scanner]** Add pattern for TODO:FIXME comments
   - Evidence: Found 12 undocumented fixes
   - Impact: Improve code documentation
   - Risk: Low

2. **[Remediation]** Auto-remove console.log in production
   - Evidence: 5 instances found across runs
   - Impact: Cleaner production code
   - Risk: Medium (verify no debugging needed)

Apply any proposals with: /delobotomize.iterate-apply
```

## Safety
- Generates proposals only
- Requires explicit approval to apply
- Maintains backward compatibility
- Documents expected impact
- Provides rollback plan
