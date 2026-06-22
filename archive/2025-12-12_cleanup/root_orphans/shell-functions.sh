#!/usr/bin/env bash
# Shell functions and aliases for Super Agent Monitor
# Source this in your .zshrc/.bashrc:
#   source ~/git/super_agent_monitor/shell-functions.sh

# Toggle Claude Code proxy on/off
cproxy() {
  if [[ -n "$ANTHROPIC_BASE_URL" ]]; then
    unset ANTHROPIC_BASE_URL ANTHROPIC_CUSTOM_HEADERS
    export PROXY_AUTH_KEY="${CLAUDE_REAL_KEY:-$PROXY_AUTH_KEY}"
    echo "🎯 Direct to Anthropic"
  else
    export CLAUDE_REAL_KEY="${PROXY_AUTH_KEY}"
    export ANTHROPIC_BASE_URL="${CLAUDE_PROXY_URL:-http://localhost:8082}"
    echo "🔀 Proxy: $ANTHROPIC_BASE_URL"
  fi
}

# Start proxy server (uses local copy in this project)
ccproxy() {
  local SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  ANTHROPIC_BASE_URL=http://localhost:8082 \
  ANTHROPIC_API_KEY=pass \
  python "$SCRIPT_DIR/claude-code-proxy/start_proxy.py"
}

# Claude via proxy with max tokens
cproxy-init() {
  ANTHROPIC_BASE_URL=http://localhost:8082 \
  ANTHROPIC_API_KEY=pass \
  CLAUDE_CODE_MAX_OUTPUT_TOKENS=128768 \
  claude --dangerously-skip-permissions --verbose "$@"
}

# Continue Claude session via proxy
cproxy-continue() {
  ANTHROPIC_BASE_URL=http://localhost:8082 \
  ANTHROPIC_API_KEY=pass \
  CLAUDE_CODE_MAX_OUTPUT_TOKENS=128768 \
  claude --continue --dangerously-skip-permissions --verbose "$@"
}

# Direct Anthropic
claude-init() {
  claude --dangerously-skip-permissions --verbose "$@"
}

claude-continue() {
  claude --continue --dangerously-skip-permissions --verbose "$@"
}

echo "✓ Super Agent Monitor shell functions loaded"
echo "  cproxy         - Toggle proxy/direct"
echo "  ccproxy        - Start proxy server"
echo "  cproxy-init    - Claude via proxy"
echo "  cproxy-continue - Continue via proxy"
