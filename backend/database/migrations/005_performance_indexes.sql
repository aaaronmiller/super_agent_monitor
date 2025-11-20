-- Performance optimization indexes for analytics and queries

-- Sessions table indexes for analytics queries
CREATE INDEX IF NOT EXISTS idx_sessions_started_at_cost ON sessions(started_at, cost_usd) WHERE cost_usd IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_sessions_workflow_started ON sessions(workflow_id, started_at);
CREATE INDEX IF NOT EXISTS idx_sessions_status_started ON sessions(status, started_at);
CREATE INDEX IF NOT EXISTS idx_sessions_cost_desc ON sessions(cost_usd DESC NULLS LAST);

-- Composite index for cost analytics queries
CREATE INDEX IF NOT EXISTS idx_sessions_analytics ON sessions(workflow_id, status, started_at, cost_usd, input_tokens, output_tokens);

-- Session events indexes for timeline queries
CREATE INDEX IF NOT EXISTS idx_session_events_session_timestamp ON session_events(session_id, timestamp);
CREATE INDEX IF NOT EXISTS idx_session_events_type ON session_events(type);

-- Workflows index for joins
CREATE INDEX IF NOT EXISTS idx_workflows_created ON workflows(created_at DESC);

-- Memory entries indexes for better search performance
CREATE INDEX IF NOT EXISTS idx_memory_entries_workflow_timestamp ON memory_entries(workflow_id, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_memory_entries_session_importance ON memory_entries(session_id, importance_score DESC);
CREATE INDEX IF NOT EXISTS idx_memory_entries_created ON memory_entries(created_at DESC);

-- Partial indexes for active sessions (frequently queried)
CREATE INDEX IF NOT EXISTS idx_sessions_active ON sessions(started_at DESC) WHERE status = 'active';
CREATE INDEX IF NOT EXISTS idx_sessions_failed ON sessions(started_at DESC) WHERE status = 'failed';

-- Expression index for session duration calculations
CREATE INDEX IF NOT EXISTS idx_sessions_duration ON sessions((EXTRACT(EPOCH FROM (completed_at - started_at)))) WHERE completed_at IS NOT NULL;

-- Covering index for session list view (reduces lookups)
CREATE INDEX IF NOT EXISTS idx_sessions_list_view ON sessions(started_at DESC)
  INCLUDE (id, workflow_id, status, cost_usd, input_tokens, output_tokens);

COMMENT ON INDEX idx_sessions_started_at_cost IS 'Optimizes cost analytics time-series queries';
COMMENT ON INDEX idx_sessions_workflow_started IS 'Optimizes per-workflow analytics';
COMMENT ON INDEX idx_sessions_analytics IS 'Composite index for complex analytics queries';
COMMENT ON INDEX idx_session_events_session_timestamp IS 'Optimizes event timeline queries';
COMMENT ON INDEX idx_memory_entries_workflow_timestamp IS 'Optimizes workflow memory retrieval';
COMMENT ON INDEX idx_sessions_active IS 'Partial index for active session monitoring';
COMMENT ON INDEX idx_sessions_duration IS 'Expression index for duration analytics';
COMMENT ON INDEX idx_sessions_list_view IS 'Covering index to reduce table lookups';
