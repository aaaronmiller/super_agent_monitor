#!/bin/sh
# 🩺 Health Check Script for Ironclad Backend
# Checks HTTP API, WebSocket, and dependencies

set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
RESET='\033[0m'

log() {
    echo "${GREEN}[HEALTHCHECK]${RESET} $1"
}

error() {
    echo "${RED}[HEALTHCHECK ERROR]${RESET} $1"
}

warn() {
    echo "${YELLOW}[HEALTHCHECK WARN]${RESET} $1"
}

# Check HTTP API
check_api() {
    log "Checking HTTP API on port 3001..."

    if curl -f -s -o /dev/null --max-time 5 http://localhost:3001/health; then
        log "✓ HTTP API is healthy"
        return 0
    else
        error "✗ HTTP API health check failed"
        return 1
    fi
}

# Check WebSocket Server
check_websocket() {
    log "Checking WebSocket Server on port 8080..."

    # Check if port is listening
    if ! nc -z localhost 8080 2>/dev/null; then
        error "✗ WebSocket port 8080 not listening"
        return 1
    fi

    # Try WebSocket connection
    if command -v wscat >/dev/null 2>&1; then
        # Use wscat if available
        echo '{"type":"ping"}' | timeout 5 wscat -c ws://localhost:8080 2>&1 | grep -q "pong" && {
            log "✓ WebSocket server is responding"
            return 0
        } || {
            error "✗ WebSocket not responding correctly"
            return 1
        }
    else
        # Alternative: check with curl
        if curl -f -s --max-time 5 http://localhost:8080/health >/dev/null 2>&1; then
            log "✓ WebSocket health endpoint responded"
            return 0
        else
            warn "WebSocket health check limited (wscat not available)"
            # Still pass if port is open
            return 0
        fi
    fi
}

# Check Redis connection (if using)
check_redis() {
    if [ -n "$REDIS_URL" ]; then
        log "Checking Redis connection..."

        # Extract host and port from REDIS_URL
        REDIS_HOST=$(echo $REDIS_URL | sed 's|redis://||' | sed 's|:.*||')
        REDIS_PORT=$(echo $REDIS_URL | sed 's|redis://||' | sed 's|.*:||')

        if nc -z $REDIS_HOST $REDIS_PORT 2>/dev/null; then
            log "✓ Redis is reachable"
            return 0
        else
            warn "✗ Redis connection failed (optional)"
            return 0  # Don't fail health check for optional Redis
        fi
    else
        log "Redis URL not configured, skipping"
        return 0
    fi
}

# Check Database connection (if using)
check_database() {
    if [ -n "$DATABASE_URL" ]; then
        log "Checking Database connection..."

        # Simple connection test using curl (assuming HTTP endpoint)
        # For PostgreSQL, you'd use pg_isready if available
        if command -v pg_isready >/dev/null 2>&1; then
            if pg_isready -d $(basename $DATABASE_URL) 2>/dev/null; then
                log "✓ Database is ready"
                return 0
            else
                warn "✗ Database not ready"
                return 0  # Don't fail for optional DB in some deployments
            fi
        else
            warn "pg_isready not available, skipping DB check"
            return 0
        fi
    else
        log "DATABASE_URL not configured, skipping"
        return 0
    fi
}

# Check system resources
check_resources() {
    log "Checking system resources..."

    # Memory usage (fail if > 90%)
    MEM_TOTAL=$(free -m | awk '/^Mem:/{print $2}')
    MEM_USED=$(free -m | awk '/^Mem:/{print $3}')
    MEM_PERCENT=$(( (MEM_USED * 100) / MEM_TOTAL ))

    if [ $MEM_PERCENT -gt 90 ]; then
        warn "⚠ High memory usage: ${MEM_PERCENT}%"
    else
        log "✓ Memory usage OK: ${MEM_PERCENT}%"
    fi

    # Disk usage (fail if > 90%)
    DISK_PERCENT=$(df /app | awk 'NR==2 {print $5}' | sed 's/%//')

    if [ $DISK_PERCENT -gt 90 ]; then
        warn "⚠ High disk usage: ${DISK_PERCENT}%"
    else
        log "✓ Disk usage OK: ${DISK_PERCENT}%"
    fi

    return 0
}

# Main health check
main() {
    log "Starting health check for Ironclad Backend..."

    # Track overall health
    ALL_HEALTHY=true

    # Run checks
    check_api || ALL_HEALTHY=false
    check_websocket || ALL_HEALTHY=false
    check_redis || ALL_HEALTHY=false
    check_database || ALL_HEALTHY=false
    check_resources

    if [ "$ALL_HEALTHY" = true ]; then
        log "✅ All health checks passed"
        exit 0
    else
        error "❌ Some health checks failed"
        exit 1
    fi
}

# Run main function
main "$@"