-- Super Agent Monitor Database Schema
-- PostgreSQL 16+ with pgvector extension

-- Enable vector extension for RAG
CREATE EXTENSION IF NOT EXISTS vector;

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ language 'plpgsql';

-- Workflows table
CREATE TABLE workflows (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  description TEXT,
  version VARCHAR(20),
  author VARCHAR(255),
  tags TEXT[],
  config JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  last_used_at TIMESTAMP,
  is_template BOOLEAN DEFAULT FALSE,
  is_permanent BOOLEAN DEFAULT FALSE,
  storage_bytes BIGINT DEFAULT 0,
  template_id VARCHAR(255),
  status VARCHAR(50) DEFAULT 'pending'
);

CREATE INDEX idx_workflows_last_used ON workflows(last_used_at);
CREATE INDEX idx_workflows_tags ON workflows USING GIN(tags);
CREATE INDEX idx_workflows_template ON workflows(is_template);

-- Apply trigger to workflows
CREATE TRIGGER update_workflows_updated_at BEFORE UPDATE ON workflows
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Sessions table
CREATE TABLE sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workflow_id UUID REFERENCES workflows(id) ON DELETE CASCADE,
  status VARCHAR(20) DEFAULT 'starting',
  started_at TIMESTAMP DEFAULT NOW(),
  ended_at TIMESTAMP,
  last_activity_at TIMESTAMP DEFAULT NOW(),
  stall_count INTEGER DEFAULT 0,
  retry_count INTEGER DEFAULT 0,
  total_tokens INTEGER DEFAULT 0,
  total_cost_usd DECIMAL(10,4) DEFAULT 0,
  config_snapshot JSONB,
  output_path VARCHAR(500),
  error_message TEXT
);

CREATE INDEX idx_sessions_status ON sessions(status, started_at DESC);
CREATE INDEX idx_sessions_workflow ON sessions(workflow_id);
CREATE INDEX idx_sessions_activity ON sessions(last_activity_at DESC);

-- Components table
CREATE TABLE components (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) UNIQUE NOT NULL,
  display_name VARCHAR(255),
  category VARCHAR(50) NOT NULL,
  description TEXT,
  tags TEXT[],
  dependencies TEXT[],
  incompatibilities TEXT[],
  content TEXT NOT NULL,
  metadata JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  usage_count INTEGER DEFAULT 0
);

CREATE INDEX idx_components_category ON components(category);
CREATE INDEX idx_components_tags ON components USING GIN(tags);
CREATE INDEX idx_components_usage ON components(usage_count DESC);
CREATE INDEX idx_components_name ON components(name);

-- Apply trigger to components
CREATE TRIGGER update_components_updated_at BEFORE UPDATE ON components
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Memories table (RAG)
CREATE TABLE memory_entries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id UUID REFERENCES sessions(id) ON DELETE CASCADE,
  workflow_id UUID REFERENCES workflows(id) ON DELETE CASCADE,
  content_type VARCHAR(50) NOT NULL,
  content TEXT NOT NULL,
  embedding vector(1536),
  metadata JSONB,
  timestamp TIMESTAMP DEFAULT NOW(),
  tool_name VARCHAR(255),
  importance_score FLOAT DEFAULT 0.5,
  tags TEXT[],
  event_id UUID,
  retrieval_score FLOAT DEFAULT 1.0
);

CREATE INDEX idx_memory_entries_embedding ON memory_entries
  USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);
CREATE INDEX idx_memory_entries_workflow ON memory_entries(workflow_id, timestamp DESC);
CREATE INDEX idx_memory_entries_session ON memory_entries(session_id);
CREATE INDEX idx_memory_entries_type ON memory_entries(content_type);

-- Events table (for monitoring)
CREATE TABLE events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id UUID REFERENCES sessions(id) ON DELETE CASCADE,
  event_type VARCHAR(50) NOT NULL,
  agent_id VARCHAR(255),
  tool_name VARCHAR(255),
  timestamp TIMESTAMP DEFAULT NOW(),
  data JSONB,
  duration_ms INTEGER
);

CREATE INDEX idx_events_session ON events(session_id, timestamp);
CREATE INDEX idx_events_type ON events(event_type);
CREATE INDEX idx_events_agent ON events(agent_id);

-- Scheduled Tasks table
CREATE TABLE scheduled_tasks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  cron_expression VARCHAR(100) NOT NULL,
  workflow_id UUID REFERENCES workflows(id) ON DELETE CASCADE,
  config JSONB DEFAULT '{}',
  is_active BOOLEAN DEFAULT TRUE,
  last_run_at TIMESTAMP,
  next_run_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_scheduled_tasks_active ON scheduled_tasks(is_active);
CREATE INDEX idx_scheduled_tasks_next_run ON scheduled_tasks(next_run_at);

-- Apply trigger to scheduled_tasks
CREATE TRIGGER update_scheduled_tasks_updated_at BEFORE UPDATE ON scheduled_tasks
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
