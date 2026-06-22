#!/bin/bash
#
# 🚀 Super Agent Monitor - Mac Native Startup
# Pure macOS dev environment launcher
#
# Usage:
#   ./dev.sh           # Start everything + open browser
#   ./dev.sh --no-open # Don't open browser
#

# Strict mode
set -e

# Configuration
readonly BACKEND_DIR="./backend"
readonly FRONTEND_DIR="./frontend"
readonly BACKEND_URL="http://localhost:3001"
readonly FRONTEND_URL="http://localhost:5173"
readonly WEBSOCKET_URL="ws://localhost:3001/ws"

# macOS Colors (Terminal.app supports these)
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[0;33m'
readonly BLUE='\033[0;34m'
readonly MAGENTA='\033[0;35m'
readonly CYAN='\033[0;36m'
readonly BOLD='\033[1m'
readonly DIM='\033[2m'
readonly RESET='\033[0m'

# Parse args
OPEN_BROWSER=true
if [[ "$1" == "--no-open" ]]; then
    OPEN_BROWSER=false
fi

# Utility: Print with timestamp and color
print_status() {
    local color=$1
    local prefix=$2
    local message=$3
    local time=$(date "+%H:%M:%S")
    echo -e "${DIM}[${time}]${RESET} ${color}${prefix}${RESET} ${message}"
}

# Utility: Check port
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        print_status "$RED" "❌" "Port ${port} is in use"
        print_status "$YELLOW" "⚠️" "Running: lsof -i :${port} | grep LISTEN"
        lsof -Pi :$port -sTCP:LISTEN
        return 1
    fi
    return 0
}

# Utility: Wait for service
wait_for_service() {
    local url=$1
    local name=$2
    local max_attempts=20

    print_status "$CYAN" "⏳" "Waiting for ${name}..."

    for ((i=1; i<=max_attempts; i++)); do
        if curl -s "$url" >/dev/null 2>&1; then
            print_status "$GREEN" "✅" "${name} is ready"
            return 0
        fi
        sleep 1
    done

    print_status "$RED" "❌" "${name} failed to start"
    return 1
}

# Utility: Send macOS notification
notify() {
    local title=$1
    local message=$2
    osascript -e "display notification \"$message\" with title \"$title\" sound name \"default\"" 2>/dev/null || true
}

# Utility: Open URL in default browser
open_browser() {
    local url=$1
    open "$url" 2>/dev/null || {
        print_status "$YELLOW" "⚠️" "Could not auto-open browser"
        print_status "$CYAN" "ℹ️" "Open manually: $url"
    }
}

# Cleanup handler
cleanup() {
    echo ""
    print_status "$YELLOW" "🛑" "Shutting down all services..."

    [[ -n "$BACKEND_PID" ]] && kill -- -"$BACKEND_PID" 2>/dev/null && \
        print_status "$GREEN" "✅" "Backend stopped (PID: $BACKEND_PID)"

    [[ -n "$FRONTEND_PID" ]] && kill -- -"$FRONTEND_PID" 2>/dev/null && \
        print_status "$GREEN" "✅" "Frontend stopped (PID: $FRONTEND_PID)"

    rm -f .dev-status.json .backend.log .frontend.log 2>/dev/null

    print_status "$GREEN" "👋" "Clean exit. Goodbye!"
    exit 0
}

# Main startup
main() {
    print_status "$CYAN" "🚀" "Super Agent Monitor - Mac Dev Startup"
    echo ""

    # Check bun
    if ! command -v bun &> /dev/null; then
        print_status "$RED" "❌" "bun not installed"
        print_status "$YELLOW" "ℹ️" "Run: curl -fsSL https://bun.sh/install | bash"
        exit 1
    fi

    # Check ports
    if ! check_port 3001 || ! check_port 5173; then
        print_status "$RED" "❌" "Port conflicts detected"
        print_status "$YELLOW" "ℹ️" "Kill conflicting processes: sudo lsof -i :3001 -i :5173"
        exit 1
    fi

    # Set cleanup trap
    trap cleanup INT TERM

    # Start Backend
    print_status "$CYAN" "🔥" "Starting Backend on port 3001..."
    cd "$BACKEND_DIR" || exit 1
    bun run dev > ../.backend.log 2>&1 &
    BACKEND_PID=$!
    cd ..

    # Wait for backend
    wait_for_service "$BACKEND_URL/health" "Backend"

    # Start Frontend
    print_status "$CYAN" "🔥" "Starting Frontend on port 5173..."
    cd "$FRONTEND_DIR" || exit 1
    bun run dev > ../.frontend.log 2>&1 &
    FRONTEND_PID=$!
    cd ..

    # Wait for frontend
    wait_for_service "$FRONTEND_URL" "Frontend"

    # Final startup delay
    sleep 2

    # Open browser
    if [[ "$OPEN_BROWSER" == true ]]; then
        print_status "$CYAN" "🌐" "Opening browser..."
        open_browser "$FRONTEND_URL"
    fi

    # Send macOS notification
    notify "Super Agent Monitor" "✅ Dev environment ready!"

    # Write status file
    cat > .dev-status.json << EOF
{
    "status": "running",
    "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "backend": {
        "pid": $BACKEND_PID,
        "url": "$BACKEND_URL",
        "port": 3001
    },
    "frontend": {
        "pid": $FRONTEND_PID,
        "url": "$FRONTEND_URL",
        "port": 5173
    },
    "websocket": "$WEBSOCKET_URL",
    "logs": {
        "backend": ".backend.log",
        "frontend": ".frontend.log"
    }
}
EOF

    # Final status
    echo ""
    echo -e "${BOLD}${GREEN}🎉 Super Agent Monitor is READY!${RESET}"
    echo ""
    echo -e "  ${CYAN}Backend:   ${RESET}$BACKEND_URL"
    echo -e "  ${CYAN}Frontend:  ${RESET}$FRONTEND_URL"
    echo -e "  ${CYAN}WebSocket: ${RESET}$WEBSOCKET_URL"
    echo ""
    echo -e "${DIM}Logs available in: .backend.log, .frontend.log${RESET}"
    echo -e "${DIM}Status file: .dev-status.json${RESET}"
    echo ""
    echo -e "${YELLOW}Press Ctrl+C to stop everything${RESET}"
    echo ""

    # Tail logs with colors
    print_status "$MAGENTA" "📡" "Live logs:"
    echo -e "${DIM}(Use Ctrl+C to stop)${RESET}\n"

    # Colorize logs by service
    tail -f .backend.log .frontend.log | \
    while IFS= read -r line; do
        if [[ "$line" == *"backend"* ]] || [[ "$line" == *"Backend"* ]]; then
            echo -e "${BLUE}Backend:${RESET} $line"
        elif [[ "$line" == *"frontend"* ]] || [[ "$line" == *"Frontend"* ]]; then
            echo -e "${GREEN}Frontend:${RESET} $line"
        else
            echo -e "${DIM}$line${RESET}"
        fi
    done
}

# Run
main