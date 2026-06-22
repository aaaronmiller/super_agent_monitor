#!/bin/bash
# 🚀 Ironclad System - Complete Deployment Script
# Handles setup, deployment, verification, and monitoring

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
RESET='\033[0m'

# Configuration
PROJECT_NAME="ironclad"
COMPOSE_FILE="docker-compose.yml"
ENV_FILE=".env"
ENV_EXAMPLE=".env.example"
ENV_PHASE6=".env.phase6.example"

# Helper functions
log() {
    echo -e "${GREEN}[INFO]${RESET} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${RESET} $1"
}

error() {
    echo -e "${RED}[ERROR]${RESET} $1"
    exit 1
}

section() {
    echo -e "\n${CYAN}=== $1 ===${RESET}"
}

check_command() {
    if ! command -v $1 &> /dev/null; then
        error "Required command '$1' not found. Please install it first."
    fi
    log "✓ Found $1"
}

check_file() {
    if [ ! -f "$1" ]; then
        error "Required file '$1' not found."
    fi
    log "✓ Found $1"
}

# ==================== VALIDATION FUNCTIONS ====================
validate_environment() {
    section "Validating Environment"

    # Check for required commands
    check_command docker
    check_command docker-compose
    check_command curl

    # Check for required files
    check_file "$COMPOSE_FILE"
    check_file "$ENV_FILE"

    # Check Docker daemon
    if ! docker info > /dev/null 2>&1; then
        error "Docker daemon is not running. Please start Docker."
    fi
    log "✓ Docker daemon is running"

    # Validate .env file
    if [ ! -f "$ENV_FILE" ]; then
        warn ".env file not found. Creating from template..."
        if [ -f "$ENV_EXAMPLE" ]; then
            cp "$ENV_EXAMPLE" "$ENV_FILE"
            warn "Please edit $ENV_FILE with your configuration"
        else
            error "No .env template found."
        fi
    fi

    # Check for required variables
    check_required_env_vars
}

check_required_env_vars() {
    section "Checking Required Environment Variables"

    local required_vars=(
        "OPENAI_API_KEY"
        "JWT_SECRET"
        "SESSION_SECRET"
        "WEBHOOK_SECRET"
        "REDIS_PASSWORD"
    )

    local missing=0

    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            error "Required variable $var is not set in $ENV_FILE"
            missing=$((missing + 1))
        else
            log "✓ $var is set"
        fi
    done

    if [ $missing -gt 0 ]; then
        error "Please set all required environment variables in $ENV_FILE"
    fi
}

check_security() {
    section "Security Validation"

    # Check for default/secrets
    if grep -q "change_this" "$ENV_FILE" || grep -q "your-" "$ENV_FILE"; then
        warn "Default placeholder values found in .env"
        warn "Please update all secrets before production deployment"
    fi

    # Check JWT secret length
    JWT_SECRET_LENGTH=$(grep "^JWT_SECRET=" "$ENV_FILE" | cut -d'=' -f2 | wc -c)
    if [ $JWT_SECRET_LENGTH -lt 64 ]; then
        warn "JWT_SECRET should be at least 64 characters"
    fi

    # Check file permissions
    if [ -r "$ENV_FILE" ]; then
        PERMS=$(stat -f "%A" "$ENV_FILE" 2>/dev/null || stat -c "%a" "$ENV_FILE")
        if [ "$PERMS" != "600" ] && [ "$PERMS" != "400" ]; then
            warn "Environment file permissions are $PERMS (recommended: 600)"
        fi
    fi

    log "✓ Basic security checks completed"
}

check_ports() {
    section "Port Availability Check"

    local ports=("3001" "8080" "5173" "5432" "6379" "80" "443")
    local in_use=0

    for port in "${ports[@]}"; do
        if lsof -i ":$port" > /dev/null 2>&1 || netstat -an 2>/dev/null | grep -q ":$port "; then
            warn "Port $port is already in use"
            in_use=$((in_use + 1))
        fi
    done

    if [ $in_use -gt 0 ]; then
        warn "Some ports are in use. This might cause conflicts."
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            error "Deployment cancelled by user"
        fi
    fi

    log "✓ Port check completed"
}

# ==================== DEPLOYMENT FUNCTIONS ====================
setup() {
    section "Setting up Ironclad System"

    # Create necessary directories
    mkdir -p backend/logs
    mkdir -p .checkpoints
    mkdir -p caddy

    # Make scripts executable
    chmod +x backend/health-check.sh 2>/dev/null || true
    chmod +x frontend/env-check.sh 2>/dev/null || true

    log "✓ Created directory structure"

    # Check for .env file
    if [ ! -f "$ENV_FILE" ]; then
        warn "Creating $ENV_FILE from template..."
        if [ -f "$ENV_PHASE6" ]; then
            cp "$ENV_PHASE6" "$ENV_FILE"
            warn "Please configure $ENV_FILE before deploying"
            error "Edit $ENV_FILE and run this script again"
        fi
    fi

    log "✓ Setup completed"
}

build() {
    section "Building Docker Images"

    # Build backend
    log "Building backend (this may take a few minutes)..."
    docker-compose build backend

    # Build frontend
    log "Building frontend..."
    docker-compose build frontend

    # Build optional services if profiles are enabled
    if [ "$ENABLE_DEBUG" = "true" ]; then
        log "Building debug tools..."
        docker-compose --profile debug build
    fi

    log "✓ Build completed"
}

deploy() {
    section "Deploying Ironclad System"

    log "Starting all services..."

    # Start with detached mode
    if docker-compose up -d; then
        log "✓ Services started"
    else
        error "Deployment failed. Check logs above."
    fi

    # Wait for services to be healthy
    wait_for_healthy
}

wait_for_healthy() {
    section "Waiting for Services to be Healthy"

    local services=("backend" "frontend" "redis" "postgres")
    local max_wait=120
    local wait_time=0

    for service in "${services[@]}"; do
        log "Checking $service..."

        while [ $wait_time -lt $max_wait ]; do
            if docker-compose ps $service | grep -q "Up (healthy)"; then
                log "✓ $service is healthy"
                break
            elif docker-compose ps $service | grep -q "Up"; then
                log "... $service is starting..."
            elif docker-compose ps $service | grep -q "Exit"; then
                error "$service failed to start. Check logs: docker-compose logs $service"
            fi

            sleep 5
            wait_time=$((wait_time + 5))

            if [ $wait_time -ge $max_wait ]; then
                warn "$service did not become healthy within $max_wait seconds"
                warn "Check logs: docker-compose logs $service"
            fi
        done

        wait_time=0
    done
}

# ==================== VERIFICATION FUNCTIONS ====================
verify() {
    section "Verifying Deployment"

    # Check running services
    log "Checking service status..."
    docker-compose ps

    # Health checks
    check_service_health "backend" "http://localhost:3001/health"
    check_service_health "frontend" "http://localhost:4173/"
    check_websocket
    check_redis

    echo
    log "✅ Deployment verification completed"
}

check_service_health() {
    local service=$1
    local url=$2

    log "Testing $service health at $url..."

    if curl -f -s --max-time 10 "$url" > /dev/null 2>&1; then
        log "✓ $service is responding"
    else
        warn "⚠ $service health check failed (may still be starting)"
    fi
}

check_websocket() {
    log "Testing WebSocket server..."

    if nc -z localhost 8080 2>/dev/null; then
        log "✓ WebSocket port 8080 is open"
    else
        warn "⚠ WebSocket not reachable on port 8080"
    fi
}

check_redis() {
    log "Testing Redis connection..."

    if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
        log "✓ Redis is responding"
    else
        warn "⚠ Redis health check failed"
    fi
}

# ==================== MONITORING FUNCTIONS ====================
logs() {
    section "Displaying Logs"
    docker-compose logs -f --tail=50
}

monitor() {
    section "Monitoring Services"
    log "Press Ctrl+C to exit monitoring"
    docker-compose ps
    echo
    docker-compose logs -f
}

status() {
    section "System Status"
    docker-compose ps
    echo
    log "For detailed logs: ./deploy.sh logs"
    log "To view metrics: open http://localhost:9090 (if enabled)"
}

stop() {
    section "Stopping Ironclad System"
    docker-compose down
    log "✓ Services stopped"
}

cleanup() {
    section "Cleaning Up"
    warn "This will remove all containers, volumes, and images"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker-compose down -v --rmi all --remove-orphans
        log "✓ Cleanup completed"
    else
        log "Cleanup cancelled"
    fi
}

# ==================== ADVANCED FUNCTIONS ====================
update() {
    section "Updating Ironclad System"

    log "Pulling latest changes..."
    git pull

    log "Rebuilding images..."
    docker-compose build --no-cache

    log "Restarting services..."
    docker-compose up -d

    wait_for_healthy
    verify
}

backup() {
    section "Creating Backup"

    local timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_dir="backups/$timestamp"
    mkdir -p "$backup_dir"

    log "Backing up data to $backup_dir..."

    # Backup PostgreSQL
    if docker-compose ps postgres | grep -q "Up"; then
        docker-compose exec -T postgres pg_dumpall -U postgres > "$backup_dir/postgres_backup.sql"
        log "✓ PostgreSQL backup completed"
    fi

    # Backup Redis
    if docker-compose ps redis | grep -q "Up"; then
        docker-compose exec -T redis redis-cli BGSAVE
        sleep 2
        docker cp $(docker-compose ps -q redis):/data/dump.rdb "$backup_dir/redis_dump.rdb" 2>/dev/null || true
        log "✓ Redis backup completed"
    fi

    # Compress backup
    tar -czf "$backup_dir.tar.gz" "$backup_dir" 2>/dev/null && rm -rf "$backup_dir"
    log "✓ Backup created: $backup_dir.tar.gz"
}

restore() {
    section "Restore from Backup"

    if [ -z "$1" ]; then
        error "Usage: ./deploy.sh restore <backup-file.tar.gz>"
    fi

    local backup_file="$1"
    if [ ! -f "$backup_file" ]; then
        error "Backup file not found: $backup_file"
    fi

    log "Restoring from $backup_file..."

    # Extract
    mkdir -p /tmp/ironclad_restore
    tar -xzf "$backup_file" -C /tmp/ironclad_restore

    # Restore PostgreSQL
    if docker-compose ps postgres | grep -q "Up"; then
        cat /tmp/ironclad_restore/*/postgres_backup.sql | docker-compose exec -T postgres psql -U postgres
        log "✓ PostgreSQL restored"
    fi

    # Restore Redis
    if docker-compose ps redis | grep -q "Up"; then
        docker cp /tmp/ironclad_restore/*/redis_dump.rdb $(docker-compose ps -q redis):/data/dump.rdb
        docker-compose exec -T redis redis-cli SHUTDOWN NOSAVE
        sleep 5
        docker-compose start redis
        log "✓ Redis restored"
    fi

    rm -rf /tmp/ironclad_restore
    log "✓ Restore completed"
}

health_check() {
    section "Comprehensive Health Check"

    local all_healthy=true

    # Service status
    log "Service Status:"
    docker-compose ps

    # Container health
    echo
    log "Container Health:"
    for container in $(docker-compose ps -q); do
        local name=$(docker inspect --format '{{.Name}}' $container | sed 's|/||')
        local health=$(docker inspect --format '{{.State.Health.Status}}' $container 2>/dev/null || echo "no-healthcheck")
        echo "  $name: $health"
    done

    # API health
    echo
    if curl -f -s http://localhost:3001/health > /dev/null 2>&1; then
        log "✓ Backend API is healthy"
    else
        error "✗ Backend API health check failed"
        all_healthy=false
    fi

    # Frontend
    if curl -f -s http://localhost:4173/ > /dev/null 2>&1; then
        log "✓ Frontend is healthy"
    else
        error "✗ Frontend health check failed"
        all_healthy=false
    fi

    # WebSocket
    if nc -z localhost 8080 2>/dev/null; then
        log "✓ WebSocket server is listening"
    else
        warn "⚠ WebSocket not listening"
        all_healthy=false
    fi

    if [ "$all_healthy" = true ]; then
        log "✅ All systems operational"
    else
        warn "⚠ Some systems need attention"
    fi
}

# ==================== MAIN DEPLOYMENT WORKFLOW ====================
full_deploy() {
    section "Full Production Deployment"

    log "Starting complete deployment workflow..."

    validate_environment
    setup
    build
    deploy
    verify

    echo
    log "🎉 Ironclad System deployed successfully!"
    echo
    log "Access Points:"
    log "  Frontend:    http://localhost:5173"
    log "  Backend API: http://localhost:3001"
    log "  WebSocket:   ws://localhost:8080"
    log "  Redis:       localhost:6379"
    log "  PostgreSQL:  localhost:5432"
    echo
    log "Useful Commands:"
    log "  ./deploy.sh status    - Check system status"
    log "  ./deploy.sh logs      - View logs"
    log "  ./deploy.sh monitor   - Monitor in real-time"
    log "  ./deploy.sh health    - Run health checks"
    log "  ./deploy.sh backup    - Create backup"
    echo
    log "Next Steps:"
    log "  1. Configure your domain in Caddyfile"
    log "  2. Set up SSL certificates (auto-configured)"
    log "  3. Test all Phase 6 features"
    log "  4. Monitor logs for any issues"
}

# ==================== USAGE ====================
usage() {
    echo "Ironclad System Deployment Script"
    echo
    echo "Usage: $0 [command]"
    echo
    echo "Commands:"
    echo "  full-deploy    - Complete deployment (setup, build, deploy, verify)"
    echo "  setup          - Setup directories and environment"
    echo "  build          - Build Docker images"
    echo "  deploy         - Deploy services"
    echo "  verify         - Verify deployment"
    echo "  status         - Show service status"
    echo "  logs           - Follow logs"
    echo "  monitor        - Monitor services"
    echo "  health         - Run health checks"
    echo "  stop           - Stop all services"
    echo "  cleanup        - Remove all services and data"
    echo "  update         - Update and redeploy"
    echo "  backup         - Create backup"
    echo "  restore <file> - Restore from backup"
    echo
    echo "Examples:"
    echo "  ./deploy.sh full-deploy    # Complete deployment"
    echo "  ./deploy.sh status         # Check status"
    echo "  ./deploy.sh logs           # View logs"
    echo "  ./deploy.sh backup         # Create backup"
}

# ==================== MAIN ====================
case "${1:-help}" in
    full-deploy)
        full_deploy
        ;;
    setup)
        setup
        ;;
    build)
        build
        ;;
    deploy)
        deploy
        ;;
    verify)
        verify
        ;;
    status)
        status
        ;;
    logs)
        logs
        ;;
    monitor)
        monitor
        ;;
    health)
        health_check
        ;;
    stop)
        stop
        ;;
    cleanup)
        cleanup
        ;;
    update)
        update
        ;;
    backup)
        backup
        ;;
    restore)
        restore "$2"
        ;;
    *)
        usage
        ;;
esac