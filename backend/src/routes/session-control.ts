import { Router, Request, Response } from 'express'
import { sessionLauncher } from '../services/SessionLauncher'
import { sessionMonitor } from '../services/SessionMonitor'
import { workflowGenerator } from '../services/WorkflowGenerator'
import { pool } from '../index'

export const sessionControlRouter = Router()

/**
 * Start a session
 * POST /api/sessions/:id/start
 */
sessionControlRouter.post('/:id/start', async (req: Request, res: Response) => {
  try {
    const sessionId = req.params.id

    // Check if session exists and is in pending state
    const sessionResult = await pool.query(
      `SELECT s.*, w.config
       FROM sessions s
       JOIN workflows w ON s.workflow_id = w.id
       WHERE s.id = $1`,
      [sessionId]
    )

    if (sessionResult.rows.length === 0) {
      res.status(404).json({ error: 'Session not found' })
      return
    }

    const session = sessionResult.rows[0]

    if (session.status !== 'pending') {
      res.status(400).json({
        error: 'Session cannot be started',
        currentStatus: session.status
      })
      return
    }

    // Generate .claude folder for the workflow
    const claudeFolderPath = await workflowGenerator.generate(session.workflow_id)

    // Launch the session
    await sessionLauncher.launch({
      workflowId: session.workflow_id,
      claudeFolderPath,
      sessionId
    })

    res.json({
      success: true,
      sessionId,
      message: 'Session started successfully'
    })

  } catch (error) {
    console.error('Error starting session:', error)
    res.status(500).json({
      error: 'Failed to start session',
      details: (error as Error).message
    })
  }
})

/**
 * Stop a session
 * POST /api/sessions/:id/stop
 */
sessionControlRouter.post('/:id/stop', async (req: Request, res: Response) => {
  try {
    const sessionId = req.params.id

    // Check if session exists and is active
    const sessionResult = await pool.query(
      `SELECT status FROM sessions WHERE id = $1`,
      [sessionId]
    )

    if (sessionResult.rows.length === 0) {
      res.status(404).json({ error: 'Session not found' })
      return
    }

    const session = sessionResult.rows[0]

    if (session.status !== 'active') {
      res.status(400).json({
        error: 'Session is not active',
        currentStatus: session.status
      })
      return
    }

    // Stop the session
    await sessionLauncher.stop(sessionId)

    res.json({
      success: true,
      sessionId,
      message: 'Session stopped successfully'
    })

  } catch (error) {
    console.error('Error stopping session:', error)
    res.status(500).json({
      error: 'Failed to stop session',
      details: (error as Error).message
    })
  }
})

/**
 * Restart a session
 * POST /api/sessions/:id/restart
 */
sessionControlRouter.post('/:id/restart', async (req: Request, res: Response) => {
  try {
    const sessionId = req.params.id

    // Check if session exists
    const sessionResult = await pool.query(
      `SELECT status FROM sessions WHERE id = $1`,
      [sessionId]
    )

    if (sessionResult.rows.length === 0) {
      res.status(404).json({ error: 'Session not found' })
      return
    }

    const session = sessionResult.rows[0]

    if (session.status === 'pending') {
      res.status(400).json({
        error: 'Cannot restart pending session. Use /start instead.',
        currentStatus: session.status
      })
      return
    }

    // Restart the session
    const newSessionId = await sessionLauncher.restart(sessionId)

    res.json({
      success: true,
      oldSessionId: sessionId,
      newSessionId,
      message: 'Session restarted successfully'
    })

  } catch (error) {
    console.error('Error restarting session:', error)
    res.status(500).json({
      error: 'Failed to restart session',
      details: (error as Error).message
    })
  }
})

/**
 * Get session status and real-time info
 * GET /api/sessions/:id/status
 */
sessionControlRouter.get('/:id/status', async (req: Request, res: Response) => {
  try {
    const sessionId = req.params.id

    // Get session from database
    const sessionResult = await pool.query(
      `SELECT * FROM sessions WHERE id = $1`,
      [sessionId]
    )

    if (sessionResult.rows.length === 0) {
      res.status(404).json({ error: 'Session not found' })
      return
    }

    const session = sessionResult.rows[0]

    // Get live status from SessionLauncher
    const isActive = sessionLauncher.getActiveSessions().includes(sessionId)
    const lastActivity = sessionLauncher.getLastActivity(sessionId)
    const retryCount = sessionMonitor.getRetryCount(sessionId)

    res.json({
      session,
      live: {
        isActive,
        lastActivity: lastActivity?.toISOString(),
        retryCount,
        timeSinceActivity: lastActivity
          ? Math.floor((Date.now() - lastActivity.getTime()) / 1000)
          : null
      }
    })

  } catch (error) {
    console.error('Error getting session status:', error)
    res.status(500).json({
      error: 'Failed to get session status',
      details: (error as Error).message
    })
  }
})

/**
 * Get monitor statistics
 * GET /api/monitor/stats
 */
sessionControlRouter.get('/monitor/stats', async (req: Request, res: Response) => {
  try {
    const stats = sessionMonitor.getStats()

    res.json({
      monitor: stats,
      launcher: {
        activeSessions: sessionLauncher.getActiveSessions()
      }
    })

  } catch (error) {
    console.error('Error getting monitor stats:', error)
    res.status(500).json({
      error: 'Failed to get monitor stats',
      details: (error as Error).message
    })
  }
})

/**
 * Update monitor configuration
 * PUT /api/monitor/config
 */
sessionControlRouter.put('/monitor/config', async (req: Request, res: Response) => {
  try {
    const { stallDetectionSeconds, checkIntervalSeconds, maxRetries } = req.body

    const config: any = {}
    if (stallDetectionSeconds !== undefined) config.stallDetectionSeconds = stallDetectionSeconds
    if (checkIntervalSeconds !== undefined) config.checkIntervalSeconds = checkIntervalSeconds
    if (maxRetries !== undefined) config.maxRetries = maxRetries

    sessionMonitor.updateConfig(config)

    res.json({
      success: true,
      config: sessionMonitor.getStats().config
    })

  } catch (error) {
    console.error('Error updating monitor config:', error)
    res.status(500).json({
      error: 'Failed to update monitor config',
      details: (error as Error).message
    })
  }
})

/**
 * Start the monitor
 * POST /api/monitor/start
 */
sessionControlRouter.post('/monitor/start', async (req: Request, res: Response) => {
  try {
    sessionMonitor.start()

    res.json({
      success: true,
      message: 'Session monitor started'
    })

  } catch (error) {
    console.error('Error starting monitor:', error)
    res.status(500).json({
      error: 'Failed to start monitor',
      details: (error as Error).message
    })
  }
})

/**
 * Stop the monitor
 * POST /api/monitor/stop
 */
sessionControlRouter.post('/monitor/stop', async (req: Request, res: Response) => {
  try {
    sessionMonitor.stop()

    res.json({
      success: true,
      message: 'Session monitor stopped'
    })

  } catch (error) {
    console.error('Error stopping monitor:', error)
    res.status(500).json({
      error: 'Failed to stop monitor',
      details: (error as Error).message
    })
  }
})
