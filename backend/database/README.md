# Database Migrations

This directory contains database migration files for the Super Agent Monitor.

## Migration Files

Migrations are numbered SQL files that run in order:

- `001_initial_schema.sql` - Core tables (workflows, sessions, events)
- `002_session_metrics.sql` - Session metrics and analytics
- `003_workflow_lifecycle.sql` - Workflow lifecycle management
- `004_memory_system.sql` - RAG memory system with pgvector

## Running Migrations

### Apply all pending migrations
```bash
cd backend
bun run db:migrate
```

### Check migration status
```bash
bun run db:migrate:status
```

### Rollback last migration
```bash
bun run db:migrate:rollback
```

## Database Setup

### Prerequisites
- PostgreSQL 14+ with pgvector extension
- Database created: `super_agent_monitor`

### Environment Variables
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/super_agent_monitor
OPENAI_API_KEY=sk-...  # Required for RAG memory embeddings
```

### First-Time Setup
```bash
# 1. Create database
createdb super_agent_monitor

# 2. Run migrations
cd backend
bun run db:migrate

# 3. (Optional) Run seed data
bun run db:seed
```

## Migration System

The migration system:
- Tracks applied migrations in `schema_migrations` table
- Runs migrations in alphabetical order
- Each migration runs in a transaction (atomic)
- Supports rollback via `*.rollback.sql` files (optional)

## Creating New Migrations

1. Create a numbered SQL file: `005_my_feature.sql`
2. (Optional) Create rollback: `005_my_feature.rollback.sql`
3. Run: `bun run db:migrate`

## Schema Overview

### Core Tables
- `workflows` - Workflow configurations
- `sessions` - Session instances
- `session_events` - Event log
- `session_metrics` - Performance metrics

### RAG Memory Tables
- `memory_entries` - Embeddings and content
- `memory_collections` - Grouped memories
- `memory_access_log` - Usage analytics

### pgvector
The memory system uses pgvector for semantic search:
- 1536-dimensional embeddings (OpenAI text-embedding-3-small)
- HNSW index for fast similarity search
- Cosine distance operator for relevance ranking
