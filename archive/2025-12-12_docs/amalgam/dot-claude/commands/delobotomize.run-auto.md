# Command: /delobotomize.run-auto
## Purpose
Run an automated Delobotomize pass with auto-application of low-risk fixes.

## Usage
```
/delobotomize.run-auto [options]
```

## Behavior
1. **Invoke delobotomize-orchestrator agent**
2. **Auto-apply LOW-RISK changes**:
   - Documentation updates
   - Comment fixes
   - Unused imports
   - Whitespace/formatting
3. **Present MEDIUM/HIGH-RISK for approval**
4. **Run full verification**
5. **Generate report with audit**

## Options
- `--project-path <path>`: Target repository
- `--risk-threshold <low|medium>`: Max risk level to auto-apply (default: low)
- `--verify`: Run verification phase (default: true)
- `--rollback`: Keep rollback snapshots (default: true)

## Auto-Apply Categories
### Low Risk (Auto-Applied)
- Documentation errors
- Comment typos
- Unused imports
- Whitespace issues
- Dead code removal

### Medium Risk (Requires Approval)
- Refactoring existing functions
- Code style improvements
- Test additions
- Configuration updates

### High Risk (Never Auto-Applied)
- API changes
- Logic modifications
- Data model changes
- Breaking changes

## Example Interaction
```
User: /delobotomize.run-auto
Agent: "Auto-applying 5 low-risk fixes...
        Applied: Removed 3 unused imports, fixed 2 doc typos.
        Approval needed: 3 medium-risk refactorings.
        Review and approve? [y/N]"
```

## Safety
- Governed by pre-remediation-apply hook
- Auto-applies only pre-approved categories
- Keeps full rollback snapshots
- Verification required
- Complete audit trail

## Output
- List of auto-applied changes
- Changes requiring approval
- Verification results
- Rollback availability
- Full audit log
