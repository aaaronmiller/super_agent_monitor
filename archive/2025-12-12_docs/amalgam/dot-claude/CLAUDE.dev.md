# Delobotomize Dev Claude Code Configuration

This root `.claude/` directory is **for development and experiments only**.

- Production orchestration lives in `production/.claude` and `production/CLAUDE.md`.
- Local Claude Code instances may load from this directory while iterating.
- Do not treat agents/skills/hooks here as stable API for CI/CD or external users.
- For authoritative behavior, always reference the `production/` configuration.
