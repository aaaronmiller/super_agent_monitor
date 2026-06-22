# 📋 Ironclad Phase 6 - Deployment Reference Card

## Quick Commands

```bash
# Full deployment
./deploy.sh full-deploy

# Status checks
./deploy.sh status && ./deploy.sh health

# Logs monitoring
./deploy.sh logs

# Stop everything
./deploy.sh stop
```

## Endpoints

| Service | URL | Health Check |
|---------|-----|-------------|
| **Frontend** | http://localhost:4173 | `curl localhost:4173` |
| **Backend** | http://localhost:3001 | `curl localhost:3001/health` |
| **WebSocket** | ws://localhost:8080/ws | `curl localhost:3001/api/phase6/ws/test` |
| **PostgreSQL** | localhost:5432 | `docker-compose exec postgres pg_isready` |
| **Redis** | localhost:6379 | `docker-compose exec redis redis-cli PING` |

## Phase 6 Features API Reference

### Real-time Collaboration (WebSocket)
```bash
# Test connection
wscat -c ws://localhost:8080/ws

# Browser test
const ws = new WebSocket('ws://localhost:8080/ws');
ws.onopen = () => ws.send(JSON.stringify({type: 'ping'}));
```

### Team RBAC
```bash
# Get teams (requires JWT)
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:3001/api/phase6/teams

# Create team
curl -X POST http://localhost:3001/api/phase6/teams/create \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Engineering", "description": "Dev team"}'
```

### CI/CD Integration
```bash
# GitHub webhook
curl -X POST http://localhost:3001/api/phase6/webhooks/github \
  -H "X-Hub-Signature-256: sha256=SIGNATURE" \
  -H "Content-Type: application/json" \
  -d '{"action":"push","repository":{"name":"test"}}'
```

### Audit Logs
```bash
# View audit logs
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:3001/api/phase6/audit/logs?limit=50"
```

### Analytics
```bash
# Get analytics summary
curl http://localhost:3001/api/analytics/summary

# Access dashboard
open http://localhost:4173/analytics
```

## Environment Variables

### Required (Generate These)
```bash
# Generate secrets
JWT_SECRET=$(openssl rand -hex 32)
SESSION_SECRET=$(openssl rand -hex 16)
WEBHOOK_SECRET=$(openssl rand -hex 16)
REDIS_PASSWORD=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")

# Add to .env:
OPENAI_API_KEY=sk-your-key
JWT_SECRET=$JWT_SECRET
SESSION_SECRET=$SESSION_SECRET
WEBHOOK_SECRET=$WEBHOOK_SECRET
REDIS_PASSWORD=$REDIS_PASSWORD
```

### Production URLs
```env
PUBLIC_API_URL=https://api.yourdomain.com
PUBLIC_WS_URL=wss://api.yourdomain.com/ws
PUBLIC_FRONTEND_URL=https://yourdomain.com
CORS_ORIGIN=https://yourdomain.com,https://app.yourdomain.com
```

### Feature Flags
```env
ENABLE_REALTIME_COLLABORATION=true
ENABLE_TEAM_RBAC=true
ENABLE_CI_CD_INTEGRATION=true
ENABLE_AUDIT_LOGGING=true
ENABLE_ANALYTICS_DASHBOARD=true
```

## Troubleshooting

### Service won't start
```bash
# Check why
docker-compose ps
docker-compose logs backend

# Restart
docker-compose restart backend
```

### Port conflicts
```bash
# Find what's using ports
lsof -i :3001  # Backend
lsof -i :8080  # WebSocket
lsof -i :4173  # Frontend
lsof -i :5432  # PostgreSQL
lsof -i :6379  # Redis
```

### Database issues
```bash
# Reset everything (WARNING: loses data)
docker-compose down -v
docker-compose up -d

# Check database
docker-compose exec postgres psql -U ironclad -c "SELECT 1"
```

### WebSocket not connecting
```bash
# Check Redis
docker-compose exec redis redis-cli PING

# Check WebSocket service logs
docker-compose logs backend | grep WebSocket

# Verify port
netstat -an | grep 8080
```

## Maintenance

### Backup
```bash
./deploy.sh backup
# Creates: backups/YYYYMMDD_HHMMSS.tar.gz
```

### Restore
```bash
./deploy.sh restore backups/20240107_120000.tar.gz
```

### Update
```bash
git pull origin main
./deploy.sh update
```

### Cleanup
```bash
./deploy.sh cleanup
# Removes all containers, volumes, images
```

## Health Check Script

Save as `health.sh`:
```bash
#!/bin/bash
echo "=== Ironclad Health Check ==="
echo "Backend:  $(curl -s http://localhost:3001/health > /dev/null && echo "✅" || echo "❌")"
echo "Frontend: $(curl -s http://localhost:4173 > /dev/null && echo "✅" || echo "❌")"
echo "WebSocket:$(nc -z localhost 8080 2>/dev/null && echo " ✅" || echo " ❌")"
echo "PostgreSQL: $(docker-compose exec -T postgres pg_isready > /dev/null 2>&1 && echo "✅" || echo "❌")"
echo "Redis: $(docker-compose exec -T redis redis-cli ping > /dev/null 2>&1 && echo "✅" || echo "❌")"
```

Make executable: `chmod +x health.sh`

## Performance Tuning

### Increase limits
```bash
# In .env:
WS_MAX_CONNECTIONS=1000
RATE_LIMIT_MAX_REQUESTS=100
REDIS_MAX_MEMORY=512mb
```

### Scale services
```bash
# Scale backend
docker-compose up -d --scale backend=3

# Scale frontend
docker-compose up -d --scale frontend=2
```

### Database tuning
```bash
docker-compose exec postgres psql -U ironclad -c "VACUUM ANALYZE;"
```

## Security Checklist

- [ ] `.env` file has 600 permissions (`chmod 600 .env`)
- [ ] All secrets generated (not default values)
- [ ] JWT_SECRET ≥ 32 characters
- [ ] CORS_ORIGIN restricted to actual domains
- [ ] Database password strong and unique
- [ ] Redis password strong and unique
- [ ] REQUIRE_2FA=true for production
- [ ] SSL certificates configured (Caddy auto)

## Monitoring

### Real-time stats
```bash
# Container resource usage
docker stats

# Logs with timestamps
docker-compose logs -f --timestamps

# Network connections
docker-compose exec backend netstat -tulpn
```

### External monitoring
```bash
# Health endpoint
curl https://yourdomain.com/health

# Ready endpoint (load balancer)
curl https://yourdomain.com/ready

# Live endpoint (orchestrators)
curl https://yourdomain.com/live
```

## Phase 6 Feature Verification

Run this checklist after deployment:

```bash
# 1. WebSocket
echo "Testing WebSocket..." && \
wscat -c ws://localhost:8080/ws -x '{"type":"ping"}' -w

# 2. Teams API
echo "Testing Teams..." && \
curl -s http://localhost:3001/api/phase6/teams | jq .

# 3. Audit logs
echo "Testing Audit..." && \
curl -s http://localhost:3001/api/phase6/audit/logs?limit=5 | jq .

# 4. Analytics
echo "Testing Analytics..." && \
curl -s http://localhost:3001/api/analytics/summary | jq .

# 5. Webhook endpoint
echo "Testing Webhooks..." && \
curl -s -X POST http://localhost:3001/api/phase6/webhooks/github \
  -H "Content-Type: application/json" \
  -d '{"action":"ping"}' | jq .
```

## File Manifest

```
./deploy.sh                    - Main deployment script
./docker-compose.yml           - Orchestration
./.env                         - Environment variables
./backend/Dockerfile.production - Backend image
./frontend/Dockerfile.production - Frontend image
./caddy/Caddyfile              - Reverse proxy config
./backend/src/index.ts         - API entrypoint
./backend/src/routes/phase6.ts - Phase 6 routes
./frontend/env-check.sh        - Environment validation
./PHASE6_DEPLOYMENT.md         - Full documentation
./QUICKSTART.md                - Quick start guide
```

---

**Status**: ✅ Phase 6 Ready
**Version**: 1.0.0
**Last Updated**: 2024-01-07
**Maintainer**: Ice-ninja