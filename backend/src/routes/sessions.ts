import { Router } from 'express'
import { pool } from '../db/pool'

export const sessionsRouter = Router()

/**
 * GET /api/sessions
 * List all sessions
 */
sessionsRouter.get('/', async (req, res) => {
  try {
    const { workflowId, status, limit = 50 } = req.query

    let query = `
      SELECT
        s.*,
        w.name as workflow_name,
        w.template_id
      FROM sessions s
      JOIN workflows w ON w.id = s.workflow_id
      WHERE 1=1
    `
    const params: any[] = []

    if (workflowId) {
      params.push(workflowId)
      query += ` AND s.workflow_id = $${params.length}`
    }

    if (status) {
      params.push(status)
      query += ` AND s.status = $${params.length}`
    }

    params.push(limit)
    query += ` ORDER BY s.started_at DESC LIMIT $${params.length}`

    const result = await pool.query(query, params)

    res.json({
      sessions: result.rows,
      total: result.rowCount
    })
  } catch (error: any) {
    res.status(500).json({ error: { code: 'DB_ERROR', message: error.message } })
  }
})

/**
 * GET /api/sessions/:id
 * Get session details
 */
sessionsRouter.get('/:id', async (req, res) => {
  try {
    const result = await pool.query(`
      SELECT
        s.*,
        w.name as workflow_name,
        w.template_id,
        w.config as workflow_config,
        (
          SELECT json_agg(json_build_object(
            'id', e.id,
            'type', e.event_type,
            'timestamp', e.timestamp,
            'data', e.data
          ) ORDER BY e.timestamp DESC)
          FROM events e
          WHERE e.session_id = s.id
          LIMIT 100
        ) as recent_events
      FROM sessions s
      JOIN workflows w ON w.id = s.workflow_id
      WHERE s.id = $1
    `, [req.params.id])

    if (result.rowCount === 0) {
      return res.status(404).json({
        error: { code: 'NOT_FOUND', message: 'Session not found' }
      })
    }

    res.json({ session: result.rows[0] })
  } catch (error: any) {
    res.status(500).json({ error: { code: 'DB_ERROR', message: error.message } })
  }
})

/**
 * GET /api/sessions/:id/events
 * Get session events with pagination
 */
sessionsRouter.get('/:id/events', async (req, res) => {
  try {
    const { limit = 50, offset = 0, type } = req.query

    let query = `
      SELECT *
      FROM events
      WHERE session_id = $1
    `
    const params: any[] = [req.params.id]

    if (type) {
      params.push(type)
      query += ` AND type = $${params.length}`
    }

    query += ` ORDER BY timestamp DESC`

    params.push(limit, offset)
    query += ` LIMIT $${params.length - 1} OFFSET $${params.length}`

    const result = await pool.query(query, params)

    // Get total count
    const countResult = await pool.query(
      `SELECT COUNT(*) FROM events WHERE session_id = $1`,
      [req.params.id]
    )

    res.json({
      events: result.rows,
      total: parseInt(countResult.rows[0].count),
      limit: parseInt(limit as string),
      offset: parseInt(offset as string)
    })
  } catch (error: any) {
    res.status(500).json({ error: { code: 'DB_ERROR', message: error.message } })
  }
})

/**
 * GET /api/sessions/:id/metrics
 * Get session metrics and statistics
 */
sessionsRouter.get('/:id/metrics', async (req, res) => {
  try {
    const result = await pool.query(`
      SELECT
        s.id,
        s.status,
        s.started_at,
        s.completed_at,
        EXTRACT(EPOCH FROM (COALESCE(s.completed_at, NOW()) - s.started_at)) as duration_seconds,
        s.cost_usd,
        s.input_tokens,
        s.output_tokens,
        (s.input_tokens + s.output_tokens) as total_tokens,
        (
          SELECT COUNT(*)
          FROM events e
          WHERE e.session_id = s.id AND e.type = 'tool_use'
        ) as tool_calls,
        (
          SELECT COUNT(*)
          FROM events e
          WHERE e.session_id = s.id AND e.type = 'error'
        ) as errors
      FROM sessions s
      WHERE s.id = $1
    `, [req.params.id])

    if (result.rowCount === 0) {
      return res.status(404).json({
        error: { code: 'NOT_FOUND', message: 'Session not found' }
      })
    }

    res.json({ metrics: result.rows[0] })
  } catch (error: any) {
    res.status(500).json({ error: { code: 'DB_ERROR', message: error.message } })
  }
})

/**
 * POST /api/sessions
 * Create a new session
 * Body: { workflowId: string }
 */
sessionsRouter.post('/', async (req, res) => {
  try {
    console.log('Creating session:', req.body)
    const { workflowId, config, runtime } = req.body

    if (!workflowId) {
      return res.status(400).json({
        error: { code: 'MISSING_WORKFLOW', message: 'workflowId is required' }
      })
    }

    // Verify workflow exists and resolve UUID if needed
    let targetWorkflowId = workflowId
    const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i

    if (!uuidRegex.test(workflowId)) {
      console.log(`Resolving non-UUID workflow ID: ${workflowId}`)
      try {
        // Import dynamically to avoid circular dependencies if any
        const { workflowGenerator } = await import('../services/WorkflowGenerator')
        const config = await workflowGenerator.loadWorkflow(workflowId)

        const nameCheck = await pool.query(
          'SELECT id FROM workflows WHERE name = $1',
          [config.name]
        )

        if (nameCheck.rowCount && nameCheck.rowCount > 0) {
          targetWorkflowId = nameCheck.rows[0].id
          console.log(`Resolved to UUID: ${targetWorkflowId}`)
        } else {
          console.warn(`Workflow with name "${config.name}" not found in DB`)
        }
      } catch (err) {
        console.error('Failed to resolve workflow ID:', err)
        // Fall through to let the UUID check fail naturally or handle gracefully
      }
    }

    const workflowCheck = await pool.query(
      'SELECT id FROM workflows WHERE id = $1',
      [targetWorkflowId]
    )

    if (workflowCheck.rowCount === 0) {
      return res.status(404).json({
        error: { code: 'WORKFLOW_NOT_FOUND', message: 'Workflow not found' }
      })
    }

    // Create session
    const result = await pool.query(`
      INSERT INTO sessions (
        workflow_id,
        status,
        started_at,
        config_snapshot
      ) VALUES ($1, 'pending', NOW(), $2)
      RETURNING id, workflow_id, status, started_at
    `, [targetWorkflowId, { runtime, ...config }])

    const session = result.rows[0]

    // Launch session
    const { sessionLauncher } = await import('../services/SessionLauncher')
    // We need to construct SessionConfig
    // The sessionLauncher.launch expects SessionConfig
    // We should pass the ID we just created
    sessionLauncher.launch({
      sessionId: session.id,
      workflowId: targetWorkflowId,
      claudeFolderPath: '', // Will be generated or ignored for E2B
      runtime: runtime as 'local' | 'e2b',
      initialPrompt: config.initialPrompt,
      orchestratorId: config.orchestratorId,
      contextInjection: config.contextInjection,
      metadata: config.metadata
    }).catch(err => console.error(`Failed to launch session ${session.id}:`, err))

    res.status(201).json({
      session,
      message: 'Session created and launched successfully'
    })
  } catch (error: any) {
    res.status(500).json({ error: { code: 'CREATE_ERROR', message: error.message } })
  }
})

/**
 * POST /api/sessions/:id/clone
 * Clone a session (start new one with same config)
 */
sessionsRouter.post('/:id/clone', async (req, res) => {
  try {
    const { sessionLauncher } = await import('../services/SessionLauncher')
    const newSessionId = await sessionLauncher.clone(req.params.id)

    res.status(201).json({
      newSessionId,
      message: 'Session cloned successfully'
    })
  } catch (error: any) {
    res.status(500).json({ error: { code: 'CLONE_ERROR', message: error.message } })
  }
})

/**
 * PATCH /api/sessions/:id
 * Update session status
 * Body: { status: 'active' | 'completed' | 'failed' | 'stalled' }
 */
sessionsRouter.patch('/:id', async (req, res) => {
  try {
    const { status, cost_usd, input_tokens, output_tokens, error } = req.body

    if (!status) {
      return res.status(400).json({
        error: { code: 'MISSING_STATUS', message: 'status is required' }
      })
    }

    const validStatuses = ['pending', 'active', 'completed', 'failed', 'stalled']
    if (!validStatuses.includes(status)) {
      return res.status(400).json({
        error: {
          code: 'INVALID_STATUS',
          message: `Status must be one of: ${validStatuses.join(', ')}`
        }
      })
    }

    // Build update query dynamically
    const updates: string[] = ['status = $1', 'updated_at = NOW()']
    const params: any[] = [status]

    if (status === 'completed' || status === 'failed') {
      updates.push('completed_at = NOW()')
    }

    if (cost_usd !== undefined) {
      params.push(cost_usd)
      updates.push(`cost_usd = $${params.length}`)
    }

    if (input_tokens !== undefined) {
      params.push(input_tokens)
      updates.push(`input_tokens = $${params.length}`)
    }

    if (output_tokens !== undefined) {
      params.push(output_tokens)
      updates.push(`output_tokens = $${params.length}`)
    }

    if (error !== undefined) {
      params.push(error)
      updates.push(`error = $${params.length}`)
    }

    params.push(req.params.id)
    const result = await pool.query(`
      UPDATE sessions
      SET ${updates.join(', ')}
      WHERE id = $${params.length}
      RETURNING *
    `, params)

    if (result.rowCount === 0) {
      return res.status(404).json({
        error: { code: 'NOT_FOUND', message: 'Session not found' }
      })
    }

    res.json({
      session: result.rows[0],
      message: 'Session updated successfully'
    })
  } catch (error: any) {
    res.status(500).json({ error: { code: 'UPDATE_ERROR', message: error.message } })
  }
})

/**
 * DELETE /api/sessions/:id
 * Delete session
 */
sessionsRouter.delete('/:id', async (req, res) => {
  try {
    const result = await pool.query(`
      DELETE FROM sessions
      WHERE id = $1
      RETURNING id
    `, [req.params.id])

    if (result.rowCount === 0) {
      return res.status(404).json({
        error: { code: 'NOT_FOUND', message: 'Session not found' }
      })
    }

    res.json({
      success: true,
      message: 'Session deleted'
    })
  } catch (error: any) {
    res.status(500).json({ error: { code: 'DELETE_ERROR', message: error.message } })
  }
})
