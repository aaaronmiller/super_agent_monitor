#!/bin/bash
# Dev Launch Script - Start backend, frontend, and open browser
# Usage: ./dev.sh [--no-browser] [--frontend-only]

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
FRONTEND_URL="http://localhost:5173"
BACKEND_URL="http://localhost:3001"

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   🚀 Super Agent Monitor Dev Launcher  ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# Parse arguments
OPEN_BROWSER=true
FRONTEND_ONLY=false
for arg in "$@"; do
    case $arg in
        --no-browser) OPEN_BROWSER=false ;;
        --frontend-only) FRONTEND_ONLY=true ;;
    esac
done

# Check PostgreSQL
check_postgres() {
    if pg_isready -q 2>/dev/null; then
        echo -e "${GREEN}✓ PostgreSQL is running${NC}"
        return 0
    elif pgrep -x "postgres" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PostgreSQL process detected${NC}"
        return 0
    else
        echo -e "${RED}✗ PostgreSQL is not running${NC}"
        echo -e "${YELLOW}  Try: brew services start postgresql@16${NC}"
        echo -e "${YELLOW}  Or:  postgres -D /opt/homebrew/var/postgresql@16 &${NC}"
        return 1
    fi
}

# Kill any existing processes on our ports
echo -e "${YELLOW}Cleaning up existing processes...${NC}"
lsof -ti:3001 | xargs kill -9 2>/dev/null || true
lsof -ti:5173 | xargs kill -9 2>/dev/null || true
lsof -ti:3000 | xargs kill -9 2>/dev/null || true

BACKEND_PID=""
FRONTEND_PID=""

# Start backend if not frontend-only
if [ "$FRONTEND_ONLY" = false ]; then
    echo ""
    if ! check_postgres; then
        echo ""
        echo -e "${YELLOW}Starting in frontend-only mode (no database)${NC}"
        FRONTEND_ONLY=true
    else
        echo -e "${GREEN}Starting backend on port 3001...${NC}"
        cd "$PROJECT_ROOT/backend"
        bun run dev > /tmp/backend.log 2>&1 &
        BACKEND_PID=$!
    fi
fi

# Start frontend
echo -e "${GREEN}Starting frontend...${NC}"
cd "$PROJECT_ROOT/frontend"
bun run dev > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!

# Wait for servers to be ready
echo -e "${YELLOW}Waiting for servers to start...${NC}"

wait_for_service() {
    local url=$1
    local name=$2
    local max_attempts=20
    local attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        if curl -s "$url" > /dev/null 2>&1; then
            echo -e "${GREEN}✓ $name is ready${NC}"
            return 0
        fi
        attempt=$((attempt + 1))
        sleep 1
    done
    
    echo -e "${YELLOW}⚠ $name may not be ready${NC}"
    return 1
}

# Give processes time to start
sleep 3

# Detect frontend port from log
DETECTED_PORT=$(grep -oE 'localhost:[0-9]+' /tmp/frontend.log 2>/dev/null | head -1 | cut -d: -f2 || echo "5173")
if [ -n "$DETECTED_PORT" ]; then
    FRONTEND_URL="http://localhost:$DETECTED_PORT"
fi

if [ "$FRONTEND_ONLY" = false ] && [ -n "$BACKEND_PID" ]; then
    wait_for_service "$BACKEND_URL/health" "Backend"
fi
wait_for_service "$FRONTEND_URL" "Frontend"

# Open browser
if [ "$OPEN_BROWSER" = true ]; then
    echo -e "${GREEN}Opening browser...${NC}"
    sleep 1
    open -a "Google Chrome" "$FRONTEND_URL" 2>/dev/null || open "$FRONTEND_URL" 2>/dev/null || echo "Could not open browser"
fi

echo ""
echo -e "${GREEN}═══════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Dev environment is running!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════${NC}"
echo ""
echo -e "  Frontend: ${BLUE}$FRONTEND_URL${NC}"
if [ "$FRONTEND_ONLY" = false ]; then
    echo -e "  Backend:  ${BLUE}$BACKEND_URL${NC}"
    echo -e "  Health:   ${BLUE}$BACKEND_URL/health${NC}"
fi
echo ""
echo -e "  Logs: ${YELLOW}/tmp/frontend.log${NC}, ${YELLOW}/tmp/backend.log${NC}"
echo -e "  Press ${YELLOW}Ctrl+C${NC} to stop all services"
echo ""

# Trap to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}Shutting down services...${NC}"
    [ -n "$BACKEND_PID" ] && kill $BACKEND_PID 2>/dev/null || true
    [ -n "$FRONTEND_PID" ] && kill $FRONTEND_PID 2>/dev/null || true
    lsof -ti:3001 | xargs kill -9 2>/dev/null || true
    lsof -ti:5173 | xargs kill -9 2>/dev/null || true
    lsof -ti:3000 | xargs kill -9 2>/dev/null || true
    echo -e "${GREEN}✓ All services stopped${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Tail logs in foreground
echo -e "${BLUE}=== Live Logs ===${NC}"
tail -f /tmp/frontend.log /tmp/backend.log 2>/dev/null || wait

