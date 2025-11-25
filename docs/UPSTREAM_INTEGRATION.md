# Upstream Integration Guide: multi-agent-workflow

This document explains how to maintain parity with the upstream `apolopena/multi-agent-workflow` repository, which provides the observability and hook system for Claude Code agents.

## Overview

The `multi-agent-workflow` directory in this project contains code from [apolopena/multi-agent-workflow](https://github.com/apolopena/multi-agent-workflow), which provides:
- Real-time agent observability dashboard
- Hook system for Claude Code lifecycle events
- Multi-agent coordination and monitoring
- TTS notifications and AI summarization

We maintain this as a subdirectory rather than a submodule to allow easier customization while tracking upstream changes.

## Why We Track Upstream

The apolopena/multi-agent-workflow project receives regular updates including:
- Bug fixes and performance improvements
- New hook types and observability features
- Enhanced TTS and AI summarization capabilities
- Better agent coordination patterns

Staying current with upstream ensures we benefit from these improvements.

## Integration Architecture

```
super_agent_monitor/
├── multi-agent-workflow/           # apolopena/multi-agent-workflow (tracked)
│   ├── .claude/                     # Hooks, agents, status lines
│   ├── apps/                        # Server & client applications
│   ├── scripts/                     # Management scripts
│   └── templates/                   # Configuration templates
├── agent-sandboxes/                 # E2B sandbox integration
├── beyond-mcp/                      # Script-based agent SDK (non-MCP)
├── components/
│   └── skills/agent-sandboxes/     # Sandbox skill integration
└── [other project files]
```

## Update Process

### Step 1: Check for Upstream Updates

```bash
cd multi-agent-workflow
git remote -v  # Verify upstream is configured

# Add upstream if not present
git remote add upstream https://github.com/apolopena/multi-agent-workflow.git

# Fetch latest changes
git fetch upstream

# View recent changes
git log --oneline upstream/main --since="1 month ago"
```

### Step 2: Review Changes

Before merging, understand what changed:

```bash
# View commit history
git log --oneline HEAD..upstream/main

# View detailed changes for a specific commit
git show <commit-hash>

# View file changes summary
git diff --stat HEAD..upstream/main

# View full diff
git diff HEAD..upstream/main
```

### Step 3: Backup Current State

```bash
# From project root
cd /home/user/super_agent_monitor

# Create backup branch
git checkout -b backup/multi-agent-workflow-$(date +%Y%m%d)
git add multi-agent-workflow/
git commit -m "Backup: multi-agent-workflow before upstream merge"

# Return to main
git checkout main
```

### Step 4: Perform Update

Since `multi-agent-workflow` is a directory within our repo (not a submodule), we use a replacement strategy:

```bash
cd /home/user/super_agent_monitor

# Remove old content (keep directory)
rm -rf multi-agent-workflow/*
rm -rf multi-agent-workflow/.*  2>/dev/null

# Clone latest upstream
git clone https://github.com/apolopena/multi-agent-workflow.git multi-agent-workflow-tmp

# Move contents (excluding .git to avoid nested repo)
mv multi-agent-workflow-tmp/* multi-agent-workflow/
rm -rf multi-agent-workflow-tmp

# Stage changes
git add multi-agent-workflow/

# Commit
git commit -m "Upstream: Sync multi-agent-workflow with apolopena/$(git -C multi-agent-workflow log -1 --format=%h)"
```

### Step 5: Verify Integration

```bash
# Check directory structure
ls -la multi-agent-workflow/

# Verify key files exist
test -f multi-agent-workflow/README.md && echo "✓ README exists"
test -d multi-agent-workflow/.claude && echo "✓ .claude directory exists"
test -d multi-agent-workflow/apps && echo "✓ apps directory exists"
test -d multi-agent-workflow/scripts && echo "✓ scripts directory exists"

# Check for breaking changes in configuration
cat multi-agent-workflow/templates/.env.template

# Test scripts are executable
test -x multi-agent-workflow/scripts/observability-start.sh && echo "✓ Scripts are executable"
```

### Step 6: Update Dependencies

```bash
cd multi-agent-workflow

# Update server dependencies
cd apps/server && bun install

# Update client dependencies
cd ../client && bun install

# Return to project root
cd /home/user/super_agent_monitor
```

### Step 7: Update Environment Configuration

```bash
# Compare environment templates
diff .env.example multi-agent-workflow/templates/.env.template

# Add any new required variables to project .env.example
# Update project documentation if new configuration is required
```

### Step 8: Test the Integration

```bash
# Start the observability system
cd multi-agent-workflow
./scripts/observability-start.sh

# In another terminal, verify endpoints
curl http://localhost:4000/events/recent
curl http://localhost:5173  # Should load dashboard

# Stop system
./scripts/observability-stop.sh
```

## Handling Customizations

If you've customized `multi-agent-workflow` files:

1. **Document customizations** in `docs/multi-agent-workflow-customizations.md`
2. **Use git stash** before updating:
   ```bash
   cd multi-agent-workflow
   git stash  # Save local changes
   # Perform update steps
   git stash pop  # Reapply changes
   ```
3. **Maintain patch files** for significant customizations:
   ```bash
   git diff upstream/main > ../patches/multi-agent-workflow-custom.patch
   ```

## Conflict Resolution

If conflicts occur during updates:

1. **Review conflict markers** in affected files
2. **Understand both versions**: what changed upstream vs. our customizations
3. **Prioritize upstream** for bug fixes and improvements
4. **Preserve customizations** that add project-specific functionality
5. **Test thoroughly** after resolution

Example conflict resolution:

```bash
# View conflicts
git status

# Edit conflicted files
nano multi-agent-workflow/path/to/conflicted/file.ts

# Look for conflict markers:
# <<<<<<< HEAD
# Our version
# =======
# Upstream version
# >>>>>>> upstream/main

# Choose appropriate resolution, remove markers, save

# Mark as resolved
git add multi-agent-workflow/path/to/conflicted/file.ts

# Complete merge
git commit
```

## Rollback Procedure

If update causes issues:

```bash
# Find backup commit
git log --oneline | grep "Backup: multi-agent-workflow"

# Checkout backup
git checkout <backup-commit-hash> -- multi-agent-workflow/

# Or restore from backup branch
git checkout backup/multi-agent-workflow-YYYYMMDD -- multi-agent-workflow/

# Commit rollback
git commit -m "Rollback: Restore multi-agent-workflow to working state"
```

## Update Frequency

**Recommended Schedule:**
- **Weekly**: Check for critical bug fixes
- **Monthly**: Review and integrate feature updates
- **Before major releases**: Ensure latest stable version

**Monitoring Upstream:**
```bash
# Watch repository on GitHub for notifications
# Or use RSS feed: https://github.com/apolopena/multi-agent-workflow/commits/main.atom

# Check for updates via CLI
git fetch upstream
git log --oneline HEAD..upstream/main | wc -l  # Shows number of new commits
```

## Troubleshooting

### "unrelated histories" Error

If git complains about unrelated histories:

```bash
# This is expected when merging separate repos
# Use the replacement strategy (Step 4) instead of git merge
```

### Missing Dependencies

```bash
# Reinstall dependencies after update
cd multi-agent-workflow/apps/server && rm -rf node_modules && bun install
cd ../client && rm -rf node_modules && bun install
```

### Broken Scripts

```bash
# Ensure scripts are executable
chmod +x multi-agent-workflow/scripts/*.sh

# Check for missing dependencies
cd multi-agent-workflow
./scripts/observability-start.sh  # Should show clear error messages
```

### Database Migration Issues

```bash
# If observability database schema changed
cd multi-agent-workflow/apps/server
rm data/*.db  # Remove old database (loses history)
bun run dev  # Will recreate with new schema
```

## Integration with Super Agent Monitor

After updating `multi-agent-workflow`, verify integration:

1. **Check hook compatibility** with our agent orchestration
2. **Verify WebSocket events** work with our monitoring dashboard
3. **Test TTS notifications** if enabled
4. **Confirm AI summarization** with our workflows

## Documentation Updates

After upstream sync, update:

1. **README.md**: Note new features or requirements
2. **CHANGELOG.md**: Document what changed from upstream
3. **API documentation**: If endpoints or hooks changed
4. **User guides**: If workflow or setup changed

## Support

- **Upstream Issues**: https://github.com/apolopena/multi-agent-workflow/issues
- **Integration Issues**: Create issue in this repository
- **Breaking Changes**: Check upstream CHANGELOG.md

## Quick Reference Commands

```bash
# Check upstream status
cd multi-agent-workflow && git fetch upstream && git log --oneline HEAD..upstream/main

# Quick update (no customizations)
cd /home/user/super_agent_monitor
rm -rf multi-agent-workflow/* multi-agent-workflow/.* 2>/dev/null
git clone https://github.com/apolopena/multi-agent-workflow.git tmp
mv tmp/* tmp/.github tmp/.gitignore multi-agent-workflow/ 2>/dev/null
rm -rf tmp
git add multi-agent-workflow/ && git commit -m "Upstream: Sync multi-agent-workflow"

# Install dependencies
cd multi-agent-workflow && (cd apps/server && bun install) && (cd apps/client && bun install)

# Test
./scripts/observability-start.sh
```

## Changelog

- **2025-11-25**: Initial documentation created
- **2025-11-25**: Synced with v2.0.2 (major refactor with centralized .env loading)

---

**Last Updated**: 2025-11-25
**Upstream Version**: v2.0.2
**Sync Status**: ✅ Current
