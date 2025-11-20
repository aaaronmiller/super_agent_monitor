-- Enable pgvector extension for vector similarity search
CREATE EXTENSION IF NOT EXISTS vector;

-- Memory entries table for RAG
CREATE TABLE IF NOT EXISTS memory_entries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id UUID REFERENCES sessions(id) ON DELETE CASCADE,
  workflow_id UUID REFERENCES workflows(id) ON DELETE CASCADE,

  -- Content
  content TEXT NOT NULL,
  content_type VARCHAR(50) NOT NULL, -- 'tool_output', 'error', 'completion', 'user_input'
  metadata JSONB DEFAULT '{}',

  -- Vector embedding (1536 dimensions for OpenAI text-embedding-3-small)
  embedding vector(1536),

  -- Context
  event_id UUID, -- Reference to session_events if applicable
  tool_name VARCHAR(100),
  timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),

  -- Importance scoring (for filtering)
  importance_score FLOAT DEFAULT 0.5,

  -- Tags for categorization
  tags TEXT[] DEFAULT '{}',

  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_memory_entries_session ON memory_entries(session_id);
CREATE INDEX idx_memory_entries_workflow ON memory_entries(workflow_id);
CREATE INDEX idx_memory_entries_timestamp ON memory_entries(timestamp DESC);
CREATE INDEX idx_memory_entries_content_type ON memory_entries(content_type);
CREATE INDEX idx_memory_entries_importance ON memory_entries(importance_score DESC);
CREATE INDEX idx_memory_entries_tags ON memory_entries USING GIN(tags);

-- Vector similarity search index (HNSW for fast approximate search)
CREATE INDEX idx_memory_entries_embedding ON memory_entries
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Memory collections for grouping related memories
CREATE TABLE IF NOT EXISTS memory_collections (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workflow_id UUID REFERENCES workflows(id) ON DELETE CASCADE,

  name VARCHAR(255) NOT NULL,
  description TEXT,

  -- Collection-level metadata
  metadata JSONB DEFAULT '{}',

  -- Stats
  entry_count INTEGER DEFAULT 0,

  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Junction table for memory entries in collections
CREATE TABLE IF NOT EXISTS memory_collection_entries (
  collection_id UUID REFERENCES memory_collections(id) ON DELETE CASCADE,
  entry_id UUID REFERENCES memory_entries(id) ON DELETE CASCADE,

  added_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

  PRIMARY KEY (collection_id, entry_id)
);

CREATE INDEX idx_memory_collection_entries_collection ON memory_collection_entries(collection_id);
CREATE INDEX idx_memory_collection_entries_entry ON memory_collection_entries(entry_id);

-- Function to update collection entry count
CREATE OR REPLACE FUNCTION update_memory_collection_count()
RETURNS TRIGGER AS $$
BEGIN
  IF TG_OP = 'INSERT' THEN
    UPDATE memory_collections
    SET entry_count = entry_count + 1, updated_at = NOW()
    WHERE id = NEW.collection_id;
  ELSIF TG_OP = 'DELETE' THEN
    UPDATE memory_collections
    SET entry_count = entry_count - 1, updated_at = NOW()
    WHERE id = OLD.collection_id;
  END IF;
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Trigger to maintain collection counts
CREATE TRIGGER trigger_update_memory_collection_count
AFTER INSERT OR DELETE ON memory_collection_entries
FOR EACH ROW EXECUTE FUNCTION update_memory_collection_count();

-- Memory access log (for tracking which memories are useful)
CREATE TABLE IF NOT EXISTS memory_access_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  entry_id UUID REFERENCES memory_entries(id) ON DELETE CASCADE,
  session_id UUID REFERENCES sessions(id) ON DELETE CASCADE,

  accessed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  relevance_score FLOAT, -- Cosine similarity score
  used_in_context BOOLEAN DEFAULT FALSE -- Was this memory actually used?
);

CREATE INDEX idx_memory_access_log_entry ON memory_access_log(entry_id);
CREATE INDEX idx_memory_access_log_session ON memory_access_log(session_id);
CREATE INDEX idx_memory_access_log_timestamp ON memory_access_log(accessed_at DESC);

-- View for memory statistics
CREATE OR REPLACE VIEW memory_stats AS
SELECT
  me.workflow_id,
  COUNT(DISTINCT me.id) as total_entries,
  COUNT(DISTINCT me.session_id) as sessions_with_memories,
  AVG(me.importance_score) as avg_importance,
  COUNT(DISTINCT mal.id) as total_accesses,
  AVG(mal.relevance_score) as avg_relevance
FROM memory_entries me
LEFT JOIN memory_access_log mal ON me.id = mal.entry_id
GROUP BY me.workflow_id;

COMMENT ON TABLE memory_entries IS 'Stores session outputs and events as embeddings for RAG retrieval';
COMMENT ON TABLE memory_collections IS 'Groups related memories for better organization';
COMMENT ON TABLE memory_access_log IS 'Tracks memory retrieval and usage for analytics';
COMMENT ON COLUMN memory_entries.embedding IS 'Vector embedding (1536-dim) for semantic search';
COMMENT ON COLUMN memory_entries.importance_score IS 'Score 0-1 for filtering important memories';
