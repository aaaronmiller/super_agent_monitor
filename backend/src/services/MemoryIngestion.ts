import { pool } from '../db/pool'
import { embeddingService } from './EmbeddingService'
import { EventEmitter } from 'events'

export interface MemoryEntry {
  id?: string
  sessionId: string
  workflowId: string
  content: string
  contentType: 'tool_output' | 'error' | 'completion' | 'user_input' | 'system_message'
  metadata?: Record<string, any>
  eventId?: string
  toolName?: string
  importanceScore?: number
  tags?: string[]
}

export interface IngestionResult {
  entryId: string
  tokens: number
  importanceScore: number
}

/**
 * Service for ingesting session data into memory system
 */
export class MemoryIngestionService extends EventEmitter {
  private batchQueue: MemoryEntry[] = []
  private batchTimeout: NodeJS.Timeout | null = null
  private batchSize: number = 10
  private batchWaitMs: number = 5000

  /**
   * Ingest a single memory entry
   */
  async ingest(entry: MemoryEntry): Promise<IngestionResult> {
    // Calculate importance score if not provided
    const importanceScore = entry.importanceScore ?? this.calculateImportance(entry)

    // Generate embedding
    const { embedding, tokens } = await embeddingService.embed(entry.content)

    // Extract tags if not provided
    const tags = entry.tags ?? this.extractTags(entry)

    // Store in database
    const result = await pool.query(
      `INSERT INTO memory_entries (
        session_id, workflow_id, content, content_type, metadata,
        embedding, event_id, tool_name, importance_score, tags
      ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
      RETURNING id`,
      [
        entry.sessionId,
        entry.workflowId,
        entry.content,
        entry.contentType,
        JSON.stringify(entry.metadata || {}),
        `[${embedding.join(',')}]`, // PostgreSQL vector format
        entry.eventId,
        entry.toolName,
        importanceScore,
        tags
      ]
    )

    const entryId = result.rows[0].id

    // Emit event
    this.emit('memory:ingested', {
      entryId,
      sessionId: entry.sessionId,
      contentType: entry.contentType,
      importanceScore,
      tokens
    })

    return {
      entryId,
      tokens,
      importanceScore
    }
  }

  /**
   * Ingest multiple entries in batch
   */
  async ingestBatch(entries: MemoryEntry[]): Promise<IngestionResult[]> {
    if (entries.length === 0) {
      return []
    }

    // Calculate importance scores
    const entriesWithScores = entries.map(entry => ({
      ...entry,
      importanceScore: entry.importanceScore ?? this.calculateImportance(entry),
      tags: entry.tags ?? this.extractTags(entry)
    }))

    // Generate embeddings in batch
    const texts = entries.map(e => e.content)
    const embeddings = await embeddingService.embedBatch(texts)

    // Prepare batch insert
    const values: any[] = []
    const placeholders: string[] = []
    let paramIndex = 1

    entriesWithScores.forEach((entry, idx) => {
      const embedding = embeddings[idx].embedding

      placeholders.push(
        `($${paramIndex}, $${paramIndex + 1}, $${paramIndex + 2}, $${paramIndex + 3}, $${paramIndex + 4}, $${paramIndex + 5}, $${paramIndex + 6}, $${paramIndex + 7}, $${paramIndex + 8}, $${paramIndex + 9})`
      )

      values.push(
        entry.sessionId,
        entry.workflowId,
        entry.content,
        entry.contentType,
        JSON.stringify(entry.metadata || {}),
        `[${embedding.join(',')}]`,
        entry.eventId,
        entry.toolName,
        entry.importanceScore,
        entry.tags
      )

      paramIndex += 10
    })

    // Execute batch insert
    const result = await pool.query(
      `INSERT INTO memory_entries (
        session_id, workflow_id, content, content_type, metadata,
        embedding, event_id, tool_name, importance_score, tags
      ) VALUES ${placeholders.join(', ')}
      RETURNING id`,
      values
    )

    const results: IngestionResult[] = result.rows.map((row, idx) => ({
      entryId: row.id,
      tokens: embeddings[idx].tokens,
      importanceScore: entriesWithScores[idx].importanceScore!
    }))

    // Emit event
    this.emit('memory:batch_ingested', {
      count: results.length,
      totalTokens: results.reduce((sum, r) => sum + r.tokens, 0)
    })

    return results
  }

  /**
   * Queue entry for batch processing
   */
  queueForBatch(entry: MemoryEntry): void {
    this.batchQueue.push(entry)

    // Process batch if size threshold reached
    if (this.batchQueue.length >= this.batchSize) {
      this.processBatch()
    } else if (!this.batchTimeout) {
      // Set timeout to process batch after delay
      this.batchTimeout = setTimeout(() => {
        this.processBatch()
      }, this.batchWaitMs)
    }
  }

  /**
   * Process queued batch
   */
  private async processBatch(): Promise<void> {
    if (this.batchTimeout) {
      clearTimeout(this.batchTimeout)
      this.batchTimeout = null
    }

    if (this.batchQueue.length === 0) {
      return
    }

    const batch = [...this.batchQueue]
    this.batchQueue = []

    try {
      await this.ingestBatch(batch)
    } catch (error) {
      console.error('Batch ingestion failed:', error)
      // Re-queue failed entries
      this.batchQueue.unshift(...batch)
    }
  }

  /**
   * Calculate importance score based on content characteristics
   */
  private calculateImportance(entry: MemoryEntry): number {
    let score = 0.5 // Base score

    // Boost errors (important to remember failures)
    if (entry.contentType === 'error') {
      score += 0.3
    }

    // Boost completions (successful outputs)
    if (entry.contentType === 'completion') {
      score += 0.2
    }

    // Boost based on content length (longer = more detailed)
    const lengthScore = Math.min(entry.content.length / 5000, 0.2)
    score += lengthScore

    // Boost if contains code blocks
    if (entry.content.includes('```') || entry.content.includes('function ')) {
      score += 0.1
    }

    // Boost if contains specific keywords
    const importantKeywords = [
      'error', 'failed', 'success', 'completed', 'important',
      'critical', 'warning', 'resolved', 'implemented'
    ]
    const hasImportantKeyword = importantKeywords.some(kw =>
      entry.content.toLowerCase().includes(kw)
    )
    if (hasImportantKeyword) {
      score += 0.1
    }

    // Normalize to 0-1 range
    return Math.min(Math.max(score, 0), 1)
  }

  /**
   * Extract tags from entry content and metadata
   */
  private extractTags(entry: MemoryEntry): string[] {
    const tags: Set<string> = new Set()

    // Add content type as tag
    tags.add(entry.contentType)

    // Add tool name if present
    if (entry.toolName) {
      tags.add(`tool:${entry.toolName}`)
    }

    // Extract technology keywords
    const techKeywords = [
      'typescript', 'javascript', 'python', 'react', 'vue',
      'nodejs', 'express', 'postgresql', 'docker', 'api',
      'database', 'frontend', 'backend', 'testing'
    ]

    const contentLower = entry.content.toLowerCase()
    techKeywords.forEach(tech => {
      if (contentLower.includes(tech)) {
        tags.add(tech)
      }
    })

    // Extract from metadata
    if (entry.metadata?.tags) {
      entry.metadata.tags.forEach((tag: string) => tags.add(tag))
    }

    return Array.from(tags)
  }

  /**
   * Create a memory collection
   */
  async createCollection(data: {
    workflowId: string
    name: string
    description?: string
    metadata?: Record<string, any>
  }): Promise<string> {
    const result = await pool.query(
      `INSERT INTO memory_collections (workflow_id, name, description, metadata)
       VALUES ($1, $2, $3, $4)
       RETURNING id`,
      [data.workflowId, data.name, data.description, JSON.stringify(data.metadata || {})]
    )

    return result.rows[0].id
  }

  /**
   * Add entries to a collection
   */
  async addToCollection(collectionId: string, entryIds: string[]): Promise<void> {
    if (entryIds.length === 0) return

    const values = entryIds.map((entryId, idx) =>
      `($1, $${idx + 2})`
    ).join(', ')

    await pool.query(
      `INSERT INTO memory_collection_entries (collection_id, entry_id)
       VALUES ${values}
       ON CONFLICT DO NOTHING`,
      [collectionId, ...entryIds]
    )
  }

  /**
   * Get collection statistics
   */
  async getCollectionStats(collectionId: string): Promise<any> {
    const result = await pool.query(
      `SELECT
        mc.id,
        mc.name,
        mc.description,
        mc.entry_count,
        mc.created_at,
        mc.updated_at,
        AVG(me.importance_score) as avg_importance,
        COUNT(DISTINCT me.session_id) as sessions_count
       FROM memory_collections mc
       LEFT JOIN memory_collection_entries mce ON mc.id = mce.collection_id
       LEFT JOIN memory_entries me ON mce.entry_id = me.id
       WHERE mc.id = $1
       GROUP BY mc.id`,
      [collectionId]
    )

    return result.rows[0]
  }

  /**
   * Delete old memories based on retention policy
   */
  async pruneOldMemories(retentionDays: number = 30, minImportance: number = 0.3): Promise<number> {
    const result = await pool.query(
      `DELETE FROM memory_entries
       WHERE created_at < NOW() - INTERVAL '${retentionDays} days'
       AND importance_score < $1
       RETURNING id`,
      [minImportance]
    )

    const deletedCount = result.rows.length

    if (deletedCount > 0) {
      this.emit('memory:pruned', { count: deletedCount, retentionDays, minImportance })
    }

    return deletedCount
  }
}

// Singleton instance
export const memoryIngestion = new MemoryIngestionService()
