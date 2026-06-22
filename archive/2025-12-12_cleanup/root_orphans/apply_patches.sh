#!/usr/bin/env bash
# apply_patches.sh - Apply Custom Patches to Upstream Components
#
# Usage: ./apply_patches.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PATCHES_DIR="$SCRIPT_DIR/patches"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log() { echo -e "${BLUE}[patch]${NC} $1"; }
success() { echo -e "${GREEN}[patch]${NC} $1"; }
warn() { echo -e "${YELLOW}[patch]${NC} $1"; }
error() { echo -e "${RED}[patch]${NC} $1"; }

if [[ ! -d "$PATCHES_DIR" ]]; then
  log "No patches directory found. Skipping."
  exit 0
fi

# Find all .patch files
PATCHES=$(find "$PATCHES_DIR" -name "*.patch" | sort)

if [[ -z "$PATCHES" ]]; then
  log "No .patch files found in $PATCHES_DIR."
  exit 0
fi

log "Applying patches..."

for patch_file in $PATCHES; do
  patch_name=$(basename "$patch_file")
  log "Applying $patch_name..."
  
  # Try applying patch (p1 usually works for git patches applied from root)
  if patch -p1 --forward --reject-file=- --no-backup-if-mismatch -r - < "$patch_file" >/dev/null 2>&1; then
    success "✓ $patch_name applied"
  elif patch -p1 --reverse --dry-run --reject-file=- --no-backup-if-mismatch -r - < "$patch_file" >/dev/null 2>&1; then
    warn "⚠ $patch_name already applied (skipping)"
  else
    error "✗ Failed to apply $patch_name"
    # Don't exit on failure, try others, but maybe we should warn louder?
    # exit 1 
  fi
done

success "Patching complete"
