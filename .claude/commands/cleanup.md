---
description: Run the Project Gardener cleanup protocol
argument-hint: [target_dir]
---

# Project Cleanup

Runs the **Project Gardener** protocol to archive stale files.

## Steps
1.  **Assess**: Identify clutter in `$TARGET` (default: `.`)
2.  **Plan**: Show what will be moved
3.  **Archive**: Move to `archive/YYYY-MM-DD/`
4.  **Report**: Generate Manifest

## Usage
`/cleanup` - cleanup root
`/cleanup ./docs` - cleanup docs folder
