import { Router, Request, Response } from 'express'
import { memoryIngestion } from '../services/MemoryIngestion'
import { ragRetrieval } from '../services/RAGRetrieval'
import { pool } from '../index'

export const memoryRouter = Router()

/**
 * Ingest a memory entry
 * POST /api/memory/ingest
 */
memoryRouter.post('/ingest', async (req: Request, res: Response) => {
  try {
    const { sessionId, workflowId, content, contentType, metadata, toolName, importanceScore, tags } = req.body

    if (!sessionId || !workflowId || !content || !contentType) {
      res.status(400).json({ error: 'Missing required fields' })
      return
    }

    const result = await memoryIngestion.ingest({
      sessionId,
      workflowId,
      content,
      contentType,
      metadata,
      toolName,
      importanceScore,
      tags
    })

    res.json({
      success: true,
      ...result
    })
  } catch (error) {
    console.error('Memory ingestion error:', error)
    res.status(500).json({
      error: 'Failed to ingest memory',
      details: (error as Error).message
    })
  }
})

/**
 * Retrieve memories using RAG
 * POST /api/memory/retrieve
 */
memoryRouter.post('/retrieve', async (req: Request, res: Response) => {
  try {
    const {
      query,
      workflowId,
      sessionId,
      contentTypes,
      tags,
      limit,
      minSimilarity,
      minImportance,
      timeRange,
      keywords
    } = req.body

    if (!query) {
      res.status(400).json({ error: 'Query is required' })
      return
    }

    const retrievalQuery = {
      query,
      workflowId,
      sessionId,
      contentTypes,
      tags,
      limit,
      minSimilarity,
      minImportance,
      timeRange
    }

    // Use hybrid retrieval if keywords provided
    const result = keywords && keywords.length > 0
      ? await ragRetrieval.hybridRetrieve(retrievalQuery, keywords)
      : await ragRetrieval.retrieve(retrievalQuery)

    res.json(result)
  } catch (error) {
    console.error('Memory retrieval error:', error)
    res.status(500).json({
      error: 'Failed to retrieve memories',
      details: (error as Error).message
    })
  }
})

/**
 * Get session context
 * GET /api/memory/session/:sessionId/context
 */
memoryRouter.get('/session/:sessionId/context', async (req: Request, res: Response) => {
  try {
    const { sessionId } = req.params
    const limit = parseInt(req.query.limit as string) || 20

    const memories = await ragRetrieval.getSessionContext(sessionId, limit)

    res.json({ memories, count: memories.length })
  } catch (error) {
    console.error('Error getting session context:', error)
    res.status(500).json({
      error: 'Failed to get session context',
      details: (error as Error).message
    })
  }
})

/**
 * Get workflow history
 * GET /api/memory/workflow/:workflowId/history
 */
memoryRouter.get('/workflow/:workflowId/history', async (req: Request, res: Response) => {
  try {
    const { workflowId } = req.params
    const sessionId = req.query.currentSessionId as string
    const limit = parseInt(req.query.limit as string) || 10

    if (!sessionId) {
      res.status(400).json({ error: 'currentSessionId is required' })
      return
    }

    const memories = await ragRetrieval.getWorkflowHistory(workflowId, sessionId, limit)

    res.json({ memories, count: memories.length })
  } catch (error) {
    console.error('Error getting workflow history:', error)
    res.status(500).json({
      error: 'Failed to get workflow history',
      details: (error as Error).message
    })
  }
})

/**
 * Find similar memories
 * GET /api/memory/:entryId/similar
 */
memoryRouter.get('/:entryId/similar', async (req: Request, res: Response) => {
  try {
    const { entryId } = req.params
    const limit = parseInt(req.query.limit as string) || 5

    const memories = await ragRetrieval.findSimilar(entryId, limit)

    res.json({ memories, count: memories.length })
  } catch (error) {
    console.error('Error finding similar memories:', error)
    res.status(500).json({
      error: 'Failed to find similar memories',
      details: (error as Error).message
    })
  }
})

/**
 * Create a memory collection
 * POST /api/memory/collections
 */
memoryRouter.post('/collections', async (req: Request, res: Response) => {
  try {
    const { workflowId, name, description, metadata } = req.body

    if (!workflowId || !name) {
      res.status(400).json({ error: 'workflowId and name are required' })
      return
    }

    const collectionId = await memoryIngestion.createCollection({
      workflowId,
      name,
      description,
      metadata
    })

    res.json({ success: true, collectionId })
  } catch (error) {
    console.error('Error creating collection:', error)
    res.status(500).json({
      error: 'Failed to create collection',
      details: (error as Error).message
    })
  }
})

/**
 * Add entries to a collection
 * POST /api/memory/collections/:collectionId/entries
 */
memoryRouter.post('/collections/:collectionId/entries', async (req: Request, res: Response) => {
  try {
    const { collectionId } = req.params
    const { entryIds } = req.body

    if (!entryIds || !Array.isArray(entryIds)) {
      res.status(400).json({ error: 'entryIds array is required' })
      return
    }

    await memoryIngestion.addToCollection(collectionId, entryIds)

    res.json({ success: true, added: entryIds.length })
  } catch (error) {
    console.error('Error adding to collection:', error)
    res.status(500).json({
      error: 'Failed to add entries to collection',
      details: (error as Error).message
    })
  }
})

/**
 * Get collection statistics
 * GET /api/memory/collections/:collectionId/stats
 */
memoryRouter.get('/collections/:collectionId/stats', async (req: Request, res: Response) => {
  try {
    const { collectionId } = req.params

    const stats = await memoryIngestion.getCollectionStats(collectionId)

    if (!stats) {
      res.status(404).json({ error: 'Collection not found' })
      return
    }

    res.json(stats)
  } catch (error) {
    console.error('Error getting collection stats:', error)
    res.status(500).json({
      error: 'Failed to get collection stats',
      details: (error as Error).message
    })
  }
})

/**
 * Get workflow memory statistics
 * GET /api/memory/workflow/:workflowId/stats
 */
memoryRouter.get('/workflow/:workflowId/stats', async (req: Request, res: Response) => {
  try {
    const { workflowId } = req.params

    const stats = await ragRetrieval.getWorkflowStats(workflowId)

    res.json(stats || {})
  } catch (error) {
    console.error('Error getting workflow stats:', error)
    res.status(500).json({
      error: 'Failed to get workflow stats',
      details: (error as Error).message
    })
  }
})

/**
 * Get memory entry details
 * GET /api/memory/:entryId
 */
memoryRouter.get('/:entryId', async (req: Request, res: Response) => {
  try {
    const { entryId } = req.params

    const result = await pool.query(
      `SELECT
        id,
        session_id,
        workflow_id,
        content,
        content_type,
        metadata,
        tool_name,
        timestamp,
        importance_score,
        tags,
        created_at
       FROM memory_entries
       WHERE id = $1`,
      [entryId]
    )

    if (result.rows.length === 0) {
      res.status(404).json({ error: 'Memory entry not found' })
      return
    }

    const entry = result.rows[0]

    // Get access stats
    const accessStats = await ragRetrieval.getAccessStats(entryId)

    res.json({
      ...entry,
      accessStats
    })
  } catch (error) {
    console.error('Error getting memory entry:', error)
    res.status(500).json({
      error: 'Failed to get memory entry',
      details: (error as Error).message
    })
  }
})

/**
 * Log memory access
 * POST /api/memory/:entryId/access
 */
memoryRouter.post('/:entryId/access', async (req: Request, res: Response) => {
  try {
    const { entryId } = req.params
    const { sessionId, relevanceScore, usedInContext } = req.body

    if (!sessionId) {
      res.status(400).json({ error: 'sessionId is required' })
      return
    }

    await ragRetrieval.logAccess(entryId, sessionId, relevanceScore || 0, usedInContext || false)

    res.json({ success: true })
  } catch (error) {
    console.error('Error logging access:', error)
    res.status(500).json({
      error: 'Failed to log access',
      details: (error as Error).message
    })
  }
})

/**
 * Prune old memories
 * POST /api/memory/prune
 */
memoryRouter.post('/prune', async (req: Request, res: Response) => {
  try {
    const { retentionDays, minImportance } = req.body

    const deletedCount = await memoryIngestion.pruneOldMemories(
      retentionDays || 30,
      minImportance || 0.3
    )

    res.json({
      success: true,
      deletedCount,
      retentionDays: retentionDays || 30,
      minImportance: minImportance || 0.3
    })
  } catch (error) {
    console.error('Error pruning memories:', error)
    res.status(500).json({
      error: 'Failed to prune memories',
      details: (error as Error).message
    })
  }
})
