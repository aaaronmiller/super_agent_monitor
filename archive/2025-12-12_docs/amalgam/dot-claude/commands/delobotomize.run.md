# Command: /delobotomize.run
## Purpose
Run a supervised Delobotomize pass on the current repository.

## Usage
```
/delobotomize.run [options]
```

## Behavior
1. **Invoke delobotomize-orchestrator agent**
2. **Require human confirmation before remediation-apply**
3. **Present remediation plan for review**
4. **Apply only approved changes**
5. **Generate final report**

## Options
- `--project-path <path>`: Target repository (default: current directory)
- `--dry-run`: Preview changes without applying
- `--verify`: Run verification phase (default: true)
- `--memory`: Enable memory snapshots (default: true)
- `--agentic`: Enable UI logging (default: false)

## Process
1. **Scan Phase**: Always runs
2. **Triage Phase**: Always runs
3. **Remediation Plan**: Always generated
4. **Remediation Apply**: **Requires approval**
5. **Verify Phase**: Runs after remediation
6. **Iterate Phase**: Generates proposals only
7. **Memory**: Snapshots stored
8. **Report**: Final summary presented

## Example Interaction
```
User: /delobotomize.run
Agent: "Scanning project... Found 23 issues.
        Remediation plan: 5 safe fixes, 3 require review.
        Apply safe fixes? [y/N]"

User: y
Agent: "Applied 5 safe fixes. Verifying... Health score: 0.75 → 0.82
        Generated 3 iteration proposals."
```

## Output
- Scan results
- Remediation plan
- Applied changes
- Verification report
- Iteration proposals
- Memory snapshot reference

## Safety
- Read-only scan
- Approved remediation only
- Full audit trail
- Rollback available
