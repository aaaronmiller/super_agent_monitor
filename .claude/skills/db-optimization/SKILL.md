---
name: db-optimization
displayName: Database Optimization Techniques
description: Expert knowledge for optimizing database performance, queries, and schema design
category: skill
tags: [database, postgresql, optimization, performance, indexing]
dependencies: []
version: 1.0.0
---

# Database Optimization Techniques

This skill provides expert guidance for optimizing database performance, with focus on PostgreSQL.

## Indexing Strategies

### When to Add an Index

```sql
-- ✅ Index columns used in WHERE clauses
CREATE INDEX idx_sessions_status ON sessions(status);
SELECT * FROM sessions WHERE status = 'active';

-- ✅ Index foreign keys
CREATE INDEX idx_sessions_workflow_id ON sessions(workflow_id);

-- ✅ Index columns used in ORDER BY
CREATE INDEX idx_sessions_created_at ON sessions(created_at DESC);

-- ✅ Index columns used in JOIN conditions
CREATE INDEX idx_events_session_id ON events(session_id);
```

### Index Types

#### B-Tree Index (Default)
```sql
-- Best for: =, <, <=, >, >=, BETWEEN, IN, IS NULL
CREATE INDEX idx_workflows_name ON workflows(name);
CREATE INDEX idx_sessions_created_at ON sessions(created_at);
```

#### Hash Index
```sql
-- Best for: = only (faster than B-tree for equality)
CREATE INDEX idx_api_keys_hash ON api_keys USING HASH (key_hash);
```

#### GIN Index (Generalized Inverted Index)
```sql
-- Best for: JSONB, arrays, full-text search
CREATE INDEX idx_workflow_metadata ON workflows USING GIN (metadata);
CREATE INDEX idx_workflow_tags ON workflows USING GIN (tags);

-- Query
SELECT * FROM workflows WHERE metadata @> '{"env": "production"}';
SELECT * FROM workflows WHERE tags @> ARRAY['research'];
```

#### BRIN Index (Block Range Index)
```sql
-- Best for: Large tables with natural ordering (timestamps)
-- Much smaller than B-tree, good for time-series data
CREATE INDEX idx_events_timestamp_brin ON events USING BRIN (timestamp);
```

#### Vector Index (for pgvector)
```sql
-- Best for: Similarity search on embeddings
CREATE INDEX idx_memories_embedding ON memories
  USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);
```

### Composite Indexes
```sql
-- Order matters: most selective column first
CREATE INDEX idx_sessions_workflow_status
  ON sessions(workflow_id, status);

-- ✅ Can use this index
SELECT * FROM sessions WHERE workflow_id = '123' AND status = 'active';
SELECT * FROM sessions WHERE workflow_id = '123';

-- ❌ Cannot use this index (doesn't start with workflow_id)
SELECT * FROM sessions WHERE status = 'active';
```

### Partial Indexes
```sql
-- Index only relevant rows (smaller, faster)
CREATE INDEX idx_sessions_active
  ON sessions(workflow_id)
  WHERE status = 'active';

-- Much smaller than indexing all sessions
-- Perfect for: SELECT * FROM sessions WHERE status = 'active' AND workflow_id = '123'
```

### Index Maintenance
```sql
-- Check index usage
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan ASC;

-- Remove unused indexes
DROP INDEX idx_rarely_used;

-- Rebuild bloated indexes
REINDEX INDEX idx_sessions_workflow_id;
REINDEX TABLE sessions;
```

## Query Optimization

### Use EXPLAIN ANALYZE
```sql
EXPLAIN ANALYZE
SELECT * FROM sessions WHERE workflow_id = '123';

-- Look for:
-- ✅ "Index Scan" (good)
-- ❌ "Seq Scan" on large tables (bad)
-- Cost numbers (lower is better)
-- Actual time vs estimated time
```

### Avoid SELECT *
```sql
-- ❌ Bad: Fetches all columns
SELECT * FROM workflows WHERE status = 'active';

-- ✅ Good: Fetch only what you need
SELECT id, name, status FROM workflows WHERE status = 'active';
```

### Use LIMIT for Large Results
```sql
-- ✅ Paginate results
SELECT * FROM sessions
ORDER BY created_at DESC
LIMIT 20 OFFSET 40;

-- Even better: Cursor-based pagination
SELECT * FROM sessions
WHERE created_at < '2025-01-19T10:00:00Z'
ORDER BY created_at DESC
LIMIT 20;
```

### Avoid N+1 Queries
```sql
-- ❌ Bad: N+1 queries (1 + N)
-- Query 1: Fetch workflows
SELECT * FROM workflows LIMIT 10;

-- Queries 2-11: Fetch sessions for each workflow (x10)
SELECT * FROM sessions WHERE workflow_id = '123';
SELECT * FROM sessions WHERE workflow_id = '456';
-- ... 8 more queries

-- ✅ Good: Single query with JOIN
SELECT w.*, s.*
FROM workflows w
LEFT JOIN sessions s ON s.workflow_id = w.id
WHERE w.id IN ('123', '456', ...);
```

### Use CTEs for Readability
```sql
-- Common Table Expressions (WITH clause)
WITH active_workflows AS (
  SELECT id, name FROM workflows WHERE status = 'active'
),
recent_sessions AS (
  SELECT workflow_id, COUNT(*) as session_count
  FROM sessions
  WHERE created_at > NOW() - INTERVAL '7 days'
  GROUP BY workflow_id
)
SELECT w.name, COALESCE(s.session_count, 0) as sessions
FROM active_workflows w
LEFT JOIN recent_sessions s ON s.workflow_id = w.id;
```

### Optimize JOINs
```sql
-- ✅ Join on indexed columns
SELECT * FROM sessions s
JOIN workflows w ON w.id = s.workflow_id;

-- Index: CREATE INDEX idx_sessions_workflow_id ON sessions(workflow_id);

-- ⚠️ Avoid joining on expressions
-- ❌ Bad
SELECT * FROM sessions s
JOIN workflows w ON LOWER(w.name) = LOWER(s.workflow_name);

-- ✅ Good: Store lowercase name in indexed column
ALTER TABLE workflows ADD COLUMN name_lower TEXT;
CREATE INDEX idx_workflows_name_lower ON workflows(name_lower);
```

## Schema Design

### Normalization vs Denormalization

#### Normalized (Less Redundancy)
```sql
-- workflows table
id | name | description
---|------|------------
1  | Res  | Research workflow

-- sessions table
id | workflow_id | status | created_at
---|-------------|--------|------------
10 | 1           | active | 2025-01-19
11 | 1           | done   | 2025-01-18

-- ✅ No duplicate data
-- ❌ Requires JOIN to get workflow name
```

#### Denormalized (Performance)
```sql
-- sessions table (includes workflow name)
id | workflow_id | workflow_name | status | created_at
---|-------------|---------------|--------|------------
10 | 1           | Research      | active | 2025-01-19
11 | 1           | Research      | done   | 2025-01-18

-- ✅ No JOIN needed
-- ❌ Duplicate data (what if workflow name changes?)

-- Trade-off decision:
-- Normalize: Data changes often
-- Denormalize: Read-heavy, data rarely changes
```

### Data Types

```sql
-- ✅ Use smallest appropriate type
-- ❌ Bad: BIGINT for user IDs (8 bytes)
user_id BIGINT

-- ✅ Good: INT for <2 billion users (4 bytes)
user_id INT

-- ✅ Use VARCHAR(n) with reasonable limit
name VARCHAR(255)  -- ✅ Good
name TEXT          -- ⚠️ OK for truly unlimited text
name VARCHAR       -- ❌ Same as TEXT, unclear intent

-- ✅ Use TIMESTAMP WITH TIME ZONE
created_at TIMESTAMPTZ  -- ✅ Good (stores UTC + offset)
created_at TIMESTAMP    -- ❌ No timezone info

-- ✅ Use UUID for public IDs
id UUID PRIMARY KEY DEFAULT gen_random_uuid()

-- ✅ Use JSONB (not JSON) for flexible data
metadata JSONB  -- ✅ Indexed, faster
metadata JSON   -- ❌ Not indexed

-- ✅ Use ENUM for fixed choices
CREATE TYPE session_status AS ENUM ('pending', 'active', 'stalled', 'completed', 'failed');
status session_status NOT NULL DEFAULT 'pending';
```

### Constraints
```sql
-- ✅ Use NOT NULL where appropriate
name VARCHAR(255) NOT NULL

-- ✅ Use CHECK constraints for validation
cost_usd DECIMAL(10,4) CHECK (cost_usd >= 0)

-- ✅ Use UNIQUE constraints
email VARCHAR(255) UNIQUE NOT NULL

-- ✅ Use foreign keys with proper ON DELETE
workflow_id UUID REFERENCES workflows(id) ON DELETE CASCADE
```

## Connection Pooling

### pgBouncer Configuration
```ini
[databases]
super_agent_monitor = host=localhost dbname=super_agent_monitor

[pgbouncer]
pool_mode = transaction
max_client_conn = 100
default_pool_size = 20
reserve_pool_size = 5
reserve_pool_timeout = 3
```

### Application-Level Pooling (Node.js)
```typescript
import { Pool } from 'pg'

const pool = new Pool({
  host: 'localhost',
  database: 'super_agent_monitor',
  max: 20,              // Max connections
  idleTimeoutMillis: 30000,  // Close idle connections after 30s
  connectionTimeoutMillis: 2000,
})

// ✅ Good: Release connection
const client = await pool.connect()
try {
  const result = await client.query('SELECT * FROM workflows')
  return result.rows
} finally {
  client.release()  // CRITICAL: Always release!
}

// ✅ Better: Use pool.query (auto-releases)
const result = await pool.query('SELECT * FROM workflows')
```

## Caching Strategies

### Application-Level Cache (Redis)
```typescript
import Redis from 'ioredis'
const redis = new Redis()

async function getWorkflow(id: string) {
  // 1. Check cache
  const cached = await redis.get(`workflow:${id}`)
  if (cached) return JSON.parse(cached)

  // 2. Query database
  const result = await pool.query('SELECT * FROM workflows WHERE id = $1', [id])
  const workflow = result.rows[0]

  // 3. Cache for 5 minutes
  await redis.setex(`workflow:${id}`, 300, JSON.stringify(workflow))

  return workflow
}
```

### Materialized Views
```sql
-- Pre-compute expensive aggregations
CREATE MATERIALIZED VIEW workflow_stats AS
SELECT
  w.id,
  w.name,
  COUNT(s.id) as total_sessions,
  SUM(s.cost_usd) as total_cost,
  AVG(s.duration_seconds) as avg_duration
FROM workflows w
LEFT JOIN sessions s ON s.workflow_id = w.id
GROUP BY w.id, w.name;

-- Refresh periodically
REFRESH MATERIALIZED VIEW workflow_stats;

-- Add index
CREATE INDEX idx_workflow_stats_name ON workflow_stats(name);

-- Query (fast!)
SELECT * FROM workflow_stats WHERE name LIKE 'Deep%';
```

## Monitoring & Diagnostics

### Slow Query Log
```sql
-- Enable slow query logging (postgresql.conf)
log_min_duration_statement = 1000  -- Log queries taking >1s

-- Check logs
tail -f /var/log/postgresql/postgresql-*.log
```

### Active Queries
```sql
-- See currently running queries
SELECT
  pid,
  now() - query_start as duration,
  state,
  query
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY duration DESC;

-- Kill long-running query
SELECT pg_terminate_backend(12345);
```

### Table Sizes
```sql
-- Largest tables
SELECT
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### Index Usage
```sql
-- Unused indexes (candidates for removal)
SELECT
  schemaname,
  tablename,
  indexname,
  idx_scan as scans
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND indexname NOT LIKE 'pg_%'
ORDER BY pg_relation_size(indexrelid) DESC;
```

### Cache Hit Ratio
```sql
-- Should be >99% for good performance
SELECT
  sum(heap_blks_read) as heap_read,
  sum(heap_blks_hit) as heap_hit,
  sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) as ratio
FROM pg_statio_user_tables;
```

## Performance Checklist

### Schema
- [ ] Use appropriate data types (smallest that fits)
- [ ] Add NOT NULL where applicable
- [ ] Use TIMESTAMPTZ (not TIMESTAMP)
- [ ] Use UUID for public IDs
- [ ] Use JSONB (not JSON) for metadata

### Indexes
- [ ] Index foreign keys
- [ ] Index WHERE clause columns
- [ ] Index ORDER BY columns
- [ ] Use composite indexes for multi-column queries
- [ ] Use partial indexes for filtered queries
- [ ] Remove unused indexes

### Queries
- [ ] Use EXPLAIN ANALYZE to check query plans
- [ ] Avoid SELECT * (fetch only needed columns)
- [ ] Use LIMIT for pagination
- [ ] Avoid N+1 queries (use JOINs or batch queries)
- [ ] Use prepared statements to prevent SQL injection

### Application
- [ ] Use connection pooling
- [ ] Cache frequently accessed data (Redis)
- [ ] Use transactions for multi-step operations
- [ ] Always release database connections
- [ ] Handle errors and retry transient failures

### Monitoring
- [ ] Enable slow query logging
- [ ] Monitor active queries
- [ ] Track table sizes
- [ ] Check index usage
- [ ] Monitor cache hit ratio (>99%)
