import { pool } from '../index'
import { embeddingService } from './EmbeddingService'

export interface RetrievalQuery {
  query: string
  workflowId?: string
  sessionId?: string
  contentTypes?: string[]
  tags?: string[]
  limit?: number
  minSimilarity?: number
  minImportance?: number
  timeRange?: {
    start?: Date
    end?: Date
  }
}

export interface RetrievedMemory {
  id: string
  content: string
  contentType: string
  metadata: Record<string, any>
  toolName?: string
  timestamp: string
  importanceScore: number
  tags: string[]
  similarityScore: number
  sessionId: string
  workflowId: string
}

export interface RetrievalResult {
  memories: RetrievedMemory[]
  totalFound: number
  queryTokens: number
}

/**
 * Service for retrieving relevant memories using RAG
 */
export class RAGRetrievalService {
  /**
   * Retrieve memories relevant to a query
   */
  async retrieve(query: RetrievalQuery): Promise<RetrievalResult> {
    // Generate query embedding
    const { embedding, tokens } = await embeddingService.embed(query.query)

    // Build SQL query with filters
    const conditions: string[] = ['1=1']
    const params: any[] = []
    let paramIndex = 1

    // Workflow filter
    if (query.workflowId) {
      conditions.push(`workflow_id = $${paramIndex}`)
      params.push(query.workflowId)
      paramIndex++
    }

    // Session filter
    if (query.sessionId) {
      conditions.push(`session_id = $${paramIndex}`)
      params.push(query.sessionId)
      paramIndex++
    }

    // Content type filter
    if (query.contentTypes && query.contentTypes.length > 0) {
      conditions.push(`content_type = ANY($${paramIndex})`)
      params.push(query.contentTypes)
      paramIndex++
    }

    // Tags filter
    if (query.tags && query.tags.length > 0) {
      conditions.push(`tags && $${paramIndex}`) // Array overlap operator
      params.push(query.tags)
      paramIndex++
    }

    // Importance filter
    if (query.minImportance !== undefined) {
      conditions.push(`importance_score >= $${paramIndex}`)
      params.push(query.minImportance)
      paramIndex++
    }

    // Time range filter
    if (query.timeRange?.start) {
      conditions.push(`timestamp >= $${paramIndex}`)
      params.push(query.timeRange.start)
      paramIndex++
    }
    if (query.timeRange?.end) {
      conditions.push(`timestamp <= $${paramIndex}`)
      params.push(query.timeRange.end)
      paramIndex++
    }

    const limit = query.limit || 10
    const minSimilarity = query.minSimilarity || 0.5

    // Vector similarity search using cosine distance
    // Note: <=> is cosine distance operator (1 - cosine similarity)
    const sql = `
      SELECT
        id,
        content,
        content_type,
        metadata,
        tool_name,
        timestamp,
        importance_score,
        tags,
        session_id,
        workflow_id,
        1 - (embedding <=> $${paramIndex}) as similarity_score
      FROM memory_entries
      WHERE ${conditions.join(' AND ')}
        AND 1 - (embedding <=> $${paramIndex}) >= $${paramIndex + 1}
      ORDER BY embedding <=> $${paramIndex} ASC
      LIMIT $${paramIndex + 2}
    `

    params.push(
      `[${embedding.join(',')}]`, // Query embedding
      minSimilarity,
      limit
    )

    const result = await pool.query(sql, params)

    const memories: RetrievedMemory[] = result.rows.map(row => ({
      id: row.id,
      content: row.content,
      contentType: row.content_type,
      metadata: row.metadata,
      toolName: row.tool_name,
      timestamp: row.timestamp,
      importanceScore: row.importance_score,
      tags: row.tags,
      similarityScore: row.similarity_score,
      sessionId: row.session_id,
      workflowId: row.workflow_id
    }))

    return {
      memories,
      totalFound: memories.length,
      queryTokens: tokens
    }
  }

  /**
   * Retrieve memories from a specific session for context continuation
   */
  async getSessionContext(sessionId: string, limit: number = 20): Promise<RetrievedMemory[]> {
    const result = await pool.query(
      `SELECT
        id,
        content,
        content_type,
        metadata,
        tool_name,
        timestamp,
        importance_score,
        tags,
        session_id,
        workflow_id,
        0 as similarity_score
       FROM memory_entries
       WHERE session_id = $1
       ORDER BY importance_score DESC, timestamp DESC
       LIMIT $2`,
      [sessionId, limit]
    )

    return result.rows.map(row => ({
      id: row.id,
      content: row.content,
      contentType: row.content_type,
      metadata: row.metadata,
      toolName: row.tool_name,
      timestamp: row.timestamp,
      importanceScore: row.importance_score,
      tags: row.tags,
      similarityScore: 0,
      sessionId: row.session_id,
      workflowId: row.workflow_id
    }))
  }

  /**
   * Retrieve memories from previous sessions of the same workflow
   */
  async getWorkflowHistory(workflowId: string, currentSessionId: string, limit: number = 10): Promise<RetrievedMemory[]> {
    const result = await pool.query(
      `SELECT
        id,
        content,
        content_type,
        metadata,
        tool_name,
        timestamp,
        importance_score,
        tags,
        session_id,
        workflow_id,
        0 as similarity_score
       FROM memory_entries
       WHERE workflow_id = $1
         AND session_id != $2
         AND importance_score >= 0.6
       ORDER BY importance_score DESC, timestamp DESC
       LIMIT $3`,
      [workflowId, currentSessionId, limit]
    )

    return result.rows.map(row => ({
      id: row.id,
      content: row.content,
      contentType: row.content_type,
      metadata: row.metadata,
      toolName: row.tool_name,
      timestamp: row.timestamp,
      importanceScore: row.importance_score,
      tags: row.tags,
      similarityScore: 0,
      sessionId: row.session_id,
      workflowId: row.workflow_id
    }))
  }

  /**
   * Hybrid retrieval: combine semantic search with keyword matching
   */
  async hybridRetrieve(query: RetrievalQuery, keywords?: string[]): Promise<RetrievalResult> {
    // Get semantic search results
    const semanticResults = await this.retrieve(query)

    // If no keywords, return semantic results
    if (!keywords || keywords.length === 0) {
      return semanticResults
    }

    // Get keyword search results
    const conditions: string[] = []
    const params: any[] = []
    let paramIndex = 1

    // Workflow filter
    if (query.workflowId) {
      conditions.push(`workflow_id = $${paramIndex}`)
      params.push(query.workflowId)
      paramIndex++
    }

    // Build keyword search
    const keywordConditions = keywords.map(kw => {
      const condition = `content ILIKE $${paramIndex}`
      params.push(`%${kw}%`)
      paramIndex++
      return condition
    }).join(' OR ')

    conditions.push(`(${keywordConditions})`)

    const sql = `
      SELECT
        id,
        content,
        content_type,
        metadata,
        tool_name,
        timestamp,
        importance_score,
        tags,
        session_id,
        workflow_id,
        0.5 as similarity_score
      FROM memory_entries
      WHERE ${conditions.join(' AND ')}
      ORDER BY importance_score DESC, timestamp DESC
      LIMIT $${paramIndex}
    `

    params.push(query.limit || 10)

    const keywordResult = await pool.query(sql, params)

    const keywordMemories: RetrievedMemory[] = keywordResult.rows.map(row => ({
      id: row.id,
      content: row.content,
      contentType: row.content_type,
      metadata: row.metadata,
      toolName: row.tool_name,
      timestamp: row.timestamp,
      importanceScore: row.importance_score,
      tags: row.tags,
      similarityScore: 0.5,
      sessionId: row.session_id,
      workflowId: row.workflow_id
    }))

    // Merge and deduplicate results
    const memoryMap = new Map<string, RetrievedMemory>()

    semanticResults.memories.forEach(mem => {
      memoryMap.set(mem.id, mem)
    })

    keywordMemories.forEach(mem => {
      if (!memoryMap.has(mem.id)) {
        memoryMap.set(mem.id, mem)
      }
    })

    // Sort by similarity score
    const mergedMemories = Array.from(memoryMap.values()).sort((a, b) =>
      b.similarityScore - a.similarityScore
    ).slice(0, query.limit || 10)

    return {
      memories: mergedMemories,
      totalFound: mergedMemories.length,
      queryTokens: semanticResults.queryTokens
    }
  }

  /**
   * Log memory access for analytics
   */
  async logAccess(entryId: string, sessionId: string, relevanceScore: number, usedInContext: boolean = false): Promise<void> {
    await pool.query(
      `INSERT INTO memory_access_log (entry_id, session_id, relevance_score, used_in_context)
       VALUES ($1, $2, $3, $4)`,
      [entryId, sessionId, relevanceScore, usedInContext]
    )
  }

  /**
   * Get memory access statistics
   */
  async getAccessStats(entryId: string): Promise<any> {
    const result = await pool.query(
      `SELECT
        COUNT(*) as access_count,
        AVG(relevance_score) as avg_relevance,
        SUM(CASE WHEN used_in_context THEN 1 ELSE 0 END) as usage_count,
        MAX(accessed_at) as last_accessed
       FROM memory_access_log
       WHERE entry_id = $1`,
      [entryId]
    )

    return result.rows[0]
  }

  /**
   * Get workflow-level memory statistics
   */
  async getWorkflowStats(workflowId: string): Promise<any> {
    const result = await pool.query(
      `SELECT * FROM memory_stats WHERE workflow_id = $1`,
      [workflowId]
    )

    return result.rows[0]
  }

  /**
   * Find similar memories to a given memory
   */
  async findSimilar(entryId: string, limit: number = 5): Promise<RetrievedMemory[]> {
    const result = await pool.query(
      `SELECT
        m2.id,
        m2.content,
        m2.content_type,
        m2.metadata,
        m2.tool_name,
        m2.timestamp,
        m2.importance_score,
        m2.tags,
        m2.session_id,
        m2.workflow_id,
        1 - (m1.embedding <=> m2.embedding) as similarity_score
       FROM memory_entries m1
       CROSS JOIN memory_entries m2
       WHERE m1.id = $1
         AND m2.id != $1
       ORDER BY m1.embedding <=> m2.embedding ASC
       LIMIT $2`,
      [entryId, limit]
    )

    return result.rows.map(row => ({
      id: row.id,
      content: row.content,
      contentType: row.content_type,
      metadata: row.metadata,
      toolName: row.tool_name,
      timestamp: row.timestamp,
      importanceScore: row.importance_score,
      tags: row.tags,
      similarityScore: row.similarity_score,
      sessionId: row.session_id,
      workflowId: row.workflow_id
    }))
  }
}

// Singleton instance
export const ragRetrieval = new RAGRetrievalService()
