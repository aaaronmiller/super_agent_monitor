#!/bin/sh
# 🔍 Environment Check Script for Ironclad Frontend
# Validates required environment variables before starting

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
RESET='\033[0m'

log() {
    echo "${GREEN}[ENV CHECK]${RESET} $1"
}

warn() {
    echo "${YELLOW}[ENV CHECK WARN]${RESET} $1"
}

error() {
    echo "${RED}[ENV CHECK ERROR]${RESET} $1"
}

# Required variables
REQUIRED_VARS=(
    "VITE_API_BASE_URL"
    "VITE_WS_URL"
)

# Optional variables
OPTIONAL_VARS=(
    "VITE_ENABLE_ANALYTICS"
    "VITE_ENABLE_REALTIME"
    "VITE_ENABLE_RBAC"
    "VITE_ENABLE_CI"
    "VITE_JWT_EXPIRY"
)

check_required() {
    local missing=0

    for var in "${REQUIRED_VARS[@]}"; do
        if [ -z "${!var}" ]; then
            error "❌ Required variable $var is not set"
            missing=$((missing + 1))
        else
            log "✓ $var = ${!var}"
        fi
    done

    return $missing
}

check_optional() {
    for var in "${OPTIONAL_VARS[@]}"; do
        if [ -n "${!var}" ]; then
            log "✓ $var = ${!var}"
        else
            warn "⚠ $var not set (using default)"
        fi
    done
}

check_api_reachable() {
    log "Testing API endpoint..."

    if [ -n "$VITE_API_BASE_URL" ]; then
        # Remove trailing slash if present
        API_URL=${VITE_API_BASE_URL%/}

        # Test health endpoint
        if wget --quiet --tries=1 --timeout=5 --spider "${API_URL}/health" 2>/dev/null; then
            log "✓ API is reachable at $API_URL"
            return 0
        else
            warn "⚠ API not reachable at $API_URL (may need to wait for backend)"
            return 0  # Don't fail, backend may still be starting
        fi
    fi
}

check_websocket_reachable() {
    log "Testing WebSocket endpoint..."

    if [ -n "$VITE_WS_URL" ]; then
        # Test if WebSocket URL is formatted correctly
        if echo "$VITE_WS_URL" | grep -qE "^(ws|wss)://"; then
            log "✓ WebSocket URL format is correct"
            return 0
        else
            warn "⚠ WebSocket URL doesn't start with ws:// or wss://"
            return 0
        fi
    fi
}

main() {
    log "Starting environment validation for Ironclad Frontend..."
    echo

    if check_required; then
        echo
        check_optional
        echo
        check_api_reachable
        check_websocket_reachable
        echo
        log "✅ Environment validation passed"
        exit 0
    else
        echo
        error "❌ Environment validation failed"
        exit 1
    fi
}

main "$@"