#!/usr/bin/env bash
# update_deps.sh - Refresh upstream dependencies
#
# Usage: ./update_deps.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROXY_SOURCE="$HOME/git/claude-code-proxy"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${BLUE}[update]${NC} $1"; }
success() { echo -e "${GREEN}[update]${NC} $1"; }

# 1. Update Claude Code Proxy
if [[ -d "$PROXY_SOURCE" ]]; then
  log "Refreshing claude-code-proxy from $PROXY_SOURCE..."
  rm -rf "$SCRIPT_DIR/claude-code-proxy"
  cp -r "$PROXY_SOURCE" "$SCRIPT_DIR/claude-code-proxy"
  # Cleanup git metadata from the copy to keep it clean
  rm -rf "$SCRIPT_DIR/claude-code-proxy/.git"
  success "claude-code-proxy updated"
else
  log "Skipping proxy update (source $PROXY_SOURCE not found)"
fi

# 2. Update Disler (if it were a git subtree/submodule, we'd pull here)
# Since it's currently a folder check-in, we assume the user manages it manually
# or we could add logic here if there was a known upstream repo URL.
# For now, just logging status.
log "Disler is integrated verbatim. To update:"
log "  cd disler && git pull origin main"

# 3. Apply Patches
if [[ -f "$SCRIPT_DIR/apply_patches.sh" ]]; then
  "$SCRIPT_DIR/apply_patches.sh"
fi

success "Dependencies refreshed"
