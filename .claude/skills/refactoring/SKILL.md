---
name: refactoring
displayName: Refactoring Skill
description: Patterns for improving code quality without changing behavior
category: skill
tags: [refactoring, clean-code, improvement, maintenance]
dependencies: []
version: 1.0.0
---

# Refactoring Skill

Guide for safely improving code quality.

## Principles

1. **Preserve Behavior**: Tests must pass before and after
2. **Small Steps**: Make incremental changes
3. **Commit Often**: Each refactor is a commit point
4. **Review Tests**: Ensure adequate coverage first

## Common Refactorings

### Extract Function
Move code block into named function for clarity.

### Rename Variable
Use descriptive names that explain intent.

### Extract Constant
Replace magic values with named constants.

### Inline Function
Remove unnecessary abstractions.

### Extract Class
Split large classes by responsibility.

### Move Method
Place code near the data it operates on.

## Safety Checklist

- [ ] Tests exist for affected code
- [ ] All tests pass before starting
- [ ] Make one change at a time
- [ ] Run tests after each change
- [ ] Review diff before committing

## Red Flags

- No test coverage → Add tests first
- Complex merge conflicts → Smaller changes
- Broken tests → Revert and retry
