# 🚀 Ironclad Phase 6 - Production Deployment Guide

## Overview

This guide provides complete instructions for deploying the Ironclad Phase 6 system with full Phase 6 features including:
- **Real-time Collaboration** (WebSocket)
- **Team RBAC** (Role-Based Access Control)
- **CI/CD Integration** (GitHub/GitLab)
- **Audit Logging**
- **Analytics Dashboard**
- **Live Session Management**

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│                 Load Balancer / Caddy                │
│                    (SSL/TLS Termination)             │
└────────────────┬────────────────────────────────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
┌───▼────┐  ┌────▼────┐  ┌────▼────┐
│Frontend│  │ Backend │  │  Redis  │
│ (Port  │  │ (Port   │  │ (Port   │
│  4173) │  │  3001)  │  │  6379)  │
└────────┘  └─────────┘  └─────────┘
                  │
            ┌─────▼──────┐
            │ PostgreSQL │
            │ (Port      │
            │  5432)     │
            └────────────┘
```

## Prerequisites

### Required Tools
```bash
# Install Docker Desktop
# https://www.docker.com/products/docker-desktop/

# Install Docker Compose (usually included with Docker Desktop)
docker-compose --version

# Install git
git --version

# Install curl for health checks
curl --version
```

### System Requirements
- **CPU**: 4+ cores recommended
- **RAM**: 8GB minimum, 16GB recommended
- **Disk**: 20GB free space
- **OS**: macOS 12+, Linux, or Windows 10/11 with WSL2

## Step 1: Environment Setup

### 1.1 Generate Secure Secrets

```bash
# Generate JWT Secret (64 characters)
openssl rand -hex 32

# Generate Session Secret (32 characters)
openssl rand -hex 16

# Generate Webhook Secret (32 characters)
openssl rand -hex 16

# Generate strong Redis password
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 1.2 Create Environment File

```bash
# Copy the example template
cp .env.phase6.example .env

# Or for production use:
cp .env.phase6.example .env.production
```

### 1.3 Configure Environment Variables

Edit `.env` file with your configuration:

```env
# REQUIRED: Replace all placeholders with actual values

# Core Secrets
OPENAI_API_KEY=sk-your-openai-api-key
JWT_SECRET=your-generated-jwt-secret-here
SESSION_SECRET=your-generated-session-secret-here
WEBHOOK_SECRET=your-generated-webhook-secret-here
REDIS_PASSWORD=your-generated-redis-password-here

# Database (if using external)
DATABASE_URL=postgresql://user:password@host:5432/ironclad

# URLs for production
PUBLIC_API_URL=https://api.yourdomain.com
PUBLIC_WS_URL=wss://api.yourdomain.com/ws
PUBLIC_FRONTEND_URL=https://yourdomain.com
CORS_ORIGIN=https://yourdomain.com,https://app.yourdomain.com

# GitHub Integration (Optional)
GITHUB_TOKEN=ghp_your_github_token_here

# Feature Flags
ENABLE_REALTIME_COLLABORATION=true
ENABLE_TEAM_RBAC=true
ENABLE_CI_CD_INTEGRATION=true
ENABLE_AUDIT_LOGGING=true
ENABLE_ANALYTICS_DASHBOARD=true
```

## Step 2: Quick Deployment

### 2.1 One-Command Deployment

```bash
# Make deploy script executable
chmod +x deploy.sh

# Full deployment with validation
./deploy.sh full-deploy
```

This will:
1. ✅ Validate environment and requirements
2. ✅ Setup directories and permissions
3. ✅ Build Docker images
4. ✅ Deploy all services
5. ✅ Verify deployment health

### 2.2 Manual Step-by-Step

If you prefer manual control:

```bash
# 1. Validate environment
./deploy.sh validate_environment

# 2. Setup directories
./deploy.sh setup

# 3. Build images
./deploy.sh build

# 4. Deploy services
./deploy.sh deploy

# 5. Verify everything works
./deploy.sh verify
```

## Step 3: Docker Compose Deep Dive

### Service Configuration

```yaml
# docker-compose.yml
services:
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ironclad
      POSTGRES_USER: ironclad
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ironclad"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis for caching & WebSocket pub/sub
  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD} --maxmemory 256mb --maxmemory-policy allkeys-lru
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  # Backend API
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.production
    environment:
      <<: *common-env
      DATABASE_URL: postgresql://ironclad:${POSTGRES_PASSWORD}@postgres:5432/ironclad
      REDIS_URL: redis://:${REDIS_PASSWORD}@redis:6379
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3001/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.production
    environment:
      VITE_API_BASE_URL: ${PUBLIC_API_URL:-http://localhost:3001}
      VITE_WS_URL: ${PUBLIC_WS_URL:-ws://localhost:8080}
    depends_on:
      - backend
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:4173/"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Caddy Reverse Proxy (Optional but recommended)
  caddy:
    image: caddy:2-alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./caddy/Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data
      - caddy_config:/config
    depends_on:
      - backend
      - frontend
```

## Step 4: Security Hardening

### 4.1 Network Security

```bash
# Create custom Docker network
docker network create --driver bridge ironclad-net

# Update docker-compose.yml to use custom network
networks:
  default:
    name: ironclad-net
    driver: bridge
```

### 4.2 File Permissions

```bash
# Restrict .env file access
chmod 600 .env
chown root:root .env

# Secure sensitive directories
chmod 750 backend/src/services/GitCheckpointService.ts
chmod 600 .checkpoints/*
```

### 4.3 SSL/TLS Configuration

Caddy automatically handles SSL certificates. For custom domains:

```bash
# Update Caddyfile
yourdomain.com {
    reverse_proxy frontend:4173

    @api {
        path /api/*
    }
    reverse_proxy @api backend:3001

    @ws {
        path /ws*
    }
    reverse_proxy @ws backend:8080
}

api.yourdomain.com {
    reverse_proxy backend:3001
}
```

## Step 5: Monitoring & Observability

### 5.1 Health Checks

```bash
# Check all services
./deploy.sh health

# Manual checks:
curl http://localhost:3001/health
curl http://localhost:3001/ready
curl http://localhost:3001/live
curl http://localhost:4173/
```

### 5.2 Logs

```bash
# View all logs in real-time
./deploy.sh logs

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres

# View last 100 lines
docker-compose logs --tail=100 backend
```

### 5.3 System Status

```bash
# Check service status
./deploy.sh status
docker-compose ps

# Check container health
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Health}}"

# Resource usage
docker stats
```

### 5.4 Metrics Dashboard

If enabled in `.env`:
```
ENABLE_METRICS=true
METRICS_PORT=9090
```

Access at: `http://localhost:9090/metrics`

## Step 6: Phase 6 Features Verification

### 6.1 Real-Time Collaboration

```bash
# Test WebSocket connection
wscat -c ws://localhost:8080/ws

# Or use browser console:
const ws = new WebSocket('ws://localhost:8080/ws');
ws.onopen = () => console.log('Connected!');
ws.onmessage = (e) => console.log('Message:', e.data);
```

### 6.2 Team RBAC

```bash
# Check RBAC endpoints
curl -X GET http://localhost:3001/api/phase6/teams \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

curl -X POST http://localhost:3001/api/phase6/teams/create \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Engineering", "description": "Core dev team"}'
```

### 6.3 CI/CD Integration

```bash
# Test webhook endpoint
curl -X POST http://localhost:3001/api/phase6/webhooks/github \
  -H "X-Hub-Signature-256: your-signature" \
  -H "Content-Type: application/json" \
  -d '{"action": "push", "repository": {"name": "test"}}'
```

### 6.4 Audit Logging

```bash
# Query audit logs
curl -X GET "http://localhost:3001/api/phase6/audit/logs?limit=50" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 6.5 Analytics Dashboard

Access at: `http://localhost:4173/analytics`

Verify data collection:
```bash
# Check analytics endpoint
curl http://localhost:3001/api/analytics/summary
```

## Step 7: Production Deployment

### 7.1 Domain Configuration

```bash
# Update DNS records
# A record: yourdomain.com -> YOUR_SERVER_IP
# A record: api.yourdomain.com -> YOUR_SERVER_IP
# CNAME: www -> yourdomain.com
```

### 7.2 Environment Variables for Production

Create `.env.production`:

```bash
# Production-specific settings
NODE_ENV=production
DEV_MODE=false

# Production URLs
PUBLIC_API_URL=https://api.yourdomain.com
PUBLIC_WS_URL=wss://api.yourdomain.com/ws
PUBLIC_FRONTEND_URL=https://yourdomain.com
CORS_ORIGIN=https://yourdomain.com,https://app.yourdomain.com

# Security
REQUIRE_2FA=true
JWT_EXPIRY=2h
SESSION_INACTIVITY_TIMEOUT=1800  # 30 minutes

# Performance
WS_MAX_CONNECTIONS=1000
REDIS_MAX_MEMORY=512mb
RATE_LIMIT_MAX_REQUESTS=100
```

### 7.3 Deploy to Production

```bash
# Use production environment
docker-compose --env-file .env.production up -d

# Or use the deployment script
DEPLOY_ENV=production ./deploy.sh full-deploy
```

### 7.4 SSL Certificates

Caddy automatically obtains Let's Encrypt certificates. For manual setup:

```bash
# Generate SSL certificates (alternative)
certbot certonly --standalone -d yourdomain.com -d api.yourdomain.com

# Update Caddyfile with custom certs
yourdomain.com {
    tls /etc/ssl/certs/yourdomain.com.crt /etc/ssl/private/yourdomain.com.key
    reverse_proxy frontend:4173
}
```

## Step 8: Maintenance & Operations

### 8.1 Backup Strategy

```bash
# Create backup
./deploy.sh backup

# Restore backup
./deploy.sh restore backups/20240107_120000.tar.gz

# Manual backup
docker-compose exec postgres pg_dumpall -U postgres > backup.sql
docker-compose exec redis redis-cli BGSAVE
```

### 8.2 Updates & Upgrades

```bash
# Update code and redeploy
./deploy.sh update

# Or manual process:
git pull origin main
./deploy.sh build
./deploy.sh deploy
```

### 8.3 Scaling

#### Vertical Scaling
```bash
# Update docker-compose.yml
backend:
  deploy:
    resources:
      limits:
        cpus: '4'
        memory: 4G
```

#### Horizontal Scaling (Backend)
```bash
# Scale backend instances
docker-compose up -d --scale backend=3
```

#### Database Scaling
Consider managed PostgreSQL (RDS, Cloud SQL) for production.

### 8.4 Troubleshooting

#### Service won't start
```bash
# Check logs
docker-compose logs backend

# Restart specific service
docker-compose restart backend

# Rebuild and restart
docker-compose up -d --build backend
```

#### Database connection issues
```bash
# Check database health
docker-compose exec postgres psql -U ironclad -c "SELECT 1"

# Reset database (WARNING: loses data)
docker-compose down -v
docker-compose up -d
```

#### WebSocket connection issues
```bash
# Check Redis connectivity
docker-compose exec redis redis-cli PING

# Verify WebSocket service logs
docker-compose logs backend | grep WebSocket
```

#### Disk space issues
```bash
# Clean up old containers/images
docker system prune -a --volumes

# Check disk usage
docker system df
```

### 8.5 Monitoring Alerts

Set up external monitoring:

```bash
# Uptime monitoring (UptimeRobot, Pingdom)
# Monitor: https://yourdomain.com/health
# Monitor: https://yourdomain.com/ready

# Error tracking (Sentry)
# Set SENTRY_DSN in .env

# Performance monitoring
# Enable ENABLE_METRICS=true
# Scrape metrics at :9090/metrics
```

## Step 9: Advanced Configuration

### 9.1 Custom Components

Add custom components to `backend/src/components/`:

```typescript
// backend/src/components/custom.ts
export const customComponent = {
  name: 'custom',
  description: 'My custom component',
  inputs: { /* ... */ },
  outputs: { /* ... */ },
  execute: async (inputs) => { /* ... */ }
}
```

### 9.2 Custom Workflows

Add workflow definitions to `backend/src/workflows/`:

```yaml
# backend/src/workflows/custom.yml
name: My Workflow
steps:
  - component: custom
    config:
      param: value
```

### 9.3 External Integrations

Configure in `.env`:

```env
# Slack notifications
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK

# Email service (SendGrid)
SENDGRID_API_KEY=your-sendgrid-key
SENDGRID_FROM=alerts@yourdomain.com

# Monitoring (Datadog)
DD_API_KEY=your-datadog-key
DD_APP_KEY=your-datadog-app-key
```

## Step 10: Performance Optimization

### 10.1 Database Optimization

```sql
-- Connect to database
docker-compose exec postgres psql -U ironclad

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_logs(created_at);

-- Analyze tables
ANALYZE;
```

### 10.2 Redis Optimization

```bash
# Configure Redis for performance
docker-compose exec redis redis-cli CONFIG SET maxmemory-policy allkeys-lru
docker-compose exec redis redis-cli CONFIG SET save 60 1000
```

### 10.3 Caddy Optimization

```bash
# Enable caching in Caddyfile
yourdomain.com {
    route /static/* {
        header Cache-Control "public, max-age=31536000"
        reverse_proxy frontend:4173
    }
}
```

## Common Commands Reference

```bash
# Deployment
./deploy.sh full-deploy    # Complete deployment
./deploy.sh status         # Check status
./deploy.sh logs           # View logs
./deploy.sh stop           # Stop services
./deploy.sh cleanup        # Remove everything

# Maintenance
./deploy.sh backup         # Create backup
./deploy.sh restore <file> # Restore backup
./deploy.sh update         # Update & redeploy
./deploy.sh health         # Health checks

# Docker Commands
docker-compose ps          # List services
docker-compose logs -f     # Follow all logs
docker-compose restart <service>
docker-compose up -d --build <service>

# Database
docker-compose exec postgres psql -U ironclad
docker-compose exec redis redis-cli
```

## Troubleshooting Checklist

If deployment fails:

- [ ] Docker daemon is running
- [ ] All required ports are available (3001, 8080, 4173, 5432, 6379)
- [ ] .env file exists with all required variables
- [ ] API keys are valid and have permissions
- [ ] Disk space is sufficient (>5GB)
- [ ] System meets minimum requirements (4GB RAM)
- [ ] Firewall allows required ports
- [ ] DNS records point to correct server
- [ ] SSL certificates are valid (if using HTTPS)

## Support & Resources

- **Documentation**: Check `/docs` directory
- **Logs**: Use `./deploy.sh logs`
- **Health**: `curl http://localhost:3001/health`
- **Community**: [GitHub Issues](https://github.com/your-org/ironclad/issues)

## Quick Start Checklist

1. ✅ Install Docker & Docker Compose
2. ✅ Generate secure secrets
3. ✅ Configure `.env` file
4. ✅ Run `./deploy.sh full-deploy`
5. ✅ Verify at `http://localhost:4173`
6. ✅ Test WebSocket at `http://localhost:3001/api/phase6/ws/test`
7. ✅ Check logs: `./deploy.sh logs`

---

**Deployment Status**: 🚀 Ready for Phase 6 Production

**Last Updated**: 2024-01-07
**Version**: 1.0.0
**Maintainer**: Ice-ninja