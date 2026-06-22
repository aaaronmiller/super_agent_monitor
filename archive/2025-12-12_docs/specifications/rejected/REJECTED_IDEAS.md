# Rejected Ideas

This file tracks ideas that were considered but explicitly rejected, along with the reasoning.

## Multi-Accent Voice Synthesis
- **Status**: Rejected
- **Reasoning**: Deemed out of scope for the core orchestration platform. Focus should remain on agent control and monitoring, not media generation.

## Skills-Based Ecosystem Lock-in
- **Status**: Postponed / Rejected
- **Reasoning**: "Clawed ecosystem lock-in" is an anti-goal. We will implement skills as portable directories but **do not** integrate with Claude Code's native skill system until v2.0, and only if portability is maintained.

## Automated Degradation Recovery (Auto-Rewrite)
- **Status**: Postponed / Rejected
- **Reasoning**: Auto-rewriting agent docs is risky without a massive training set. We will implement a linter for manual fixing instead of autonomous rewriting.
