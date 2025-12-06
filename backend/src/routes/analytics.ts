import { Router, Request, Response } from 'express'
import { pool } from '../db/pool'

export const analyticsRouter = Router()

/**
 * Get cost analytics over time
 * GET /api/analytics/costs
 */
analyticsRouter.get('/costs', async (req: Request, res: Response) => {
  try {
    const { timeRange = '7d', granularity = 'day', workflowId } = req.query

    // Parse time range
    const days = parseInt(timeRange as string) || 7
    const startDate = new Date()
    startDate.setDate(startDate.getDate() - days)

    // Build query with optional workflow filter
    let query = `
      SELECT
        DATE_TRUNC($1, started_at) as time_bucket,
        COUNT(*) as session_count,
        SUM(cost_usd) as total_cost,
        SUM(input_tokens) as total_input_tokens,
        SUM(output_tokens) as total_output_tokens,
        AVG(cost_usd) as avg_cost_per_session
      FROM sessions
      WHERE started_at >= $2
        AND cost_usd IS NOT NULL
    `

    const params: any[] = [granularity, startDate]

    if (workflowId) {
      query += ` AND workflow_id = $3`
      params.push(workflowId)
    }

    query += `
      GROUP BY time_bucket
      ORDER BY time_bucket ASC
    `

    const result = await pool.query(query, params)

    // Calculate totals
    const totals = await pool.query(
      `SELECT
        COUNT(*) as total_sessions,
        COALESCE(SUM(cost_usd), 0) as total_cost,
        COALESCE(SUM(input_tokens), 0) as total_input_tokens,
        COALESCE(SUM(output_tokens), 0) as total_output_tokens,
        COALESCE(AVG(cost_usd), 0) as avg_cost
       FROM sessions
       WHERE started_at >= $1
         ${workflowId ? 'AND workflow_id = $2' : ''}
         AND cost_usd IS NOT NULL`,
      workflowId ? [startDate, workflowId] : [startDate]
    )

    res.json({
      timeRange: {
        start: startDate.toISOString(),
        end: new Date().toISOString(),
        days
      },
      timeSeries: result.rows,
      totals: totals.rows[0]
    })
  } catch (error) {
    console.error('Cost analytics error:', error)
    res.status(500).json({
      error: 'Failed to fetch cost analytics',
      details: (error as Error).message
    })
  }
})

/**
 * Get workflow performance analytics
 * GET /api/analytics/workflows
 */
analyticsRouter.get('/workflows', async (req: Request, res: Response) => {
  try {
    const { timeRange = '30d' } = req.query
    const days = parseInt(timeRange as string) || 30
    const startDate = new Date()
    startDate.setDate(startDate.getDate() - days)

    const result = await pool.query(
      `SELECT
        w.id,
        w.name,
        w.description,
        COUNT(s.id) as total_sessions,
        COUNT(CASE WHEN s.status = 'completed' THEN 1 END) as completed_sessions,
        COUNT(CASE WHEN s.status = 'failed' THEN 1 END) as failed_sessions,
        COUNT(CASE WHEN s.status = 'stalled' THEN 1 END) as stalled_sessions,
        COALESCE(SUM(s.cost_usd), 0) as total_cost,
        COALESCE(AVG(s.cost_usd), 0) as avg_cost,
        COALESCE(SUM(s.input_tokens + s.output_tokens), 0) as total_tokens,
        AVG(EXTRACT(EPOCH FROM (s.completed_at - s.started_at))) as avg_duration_seconds,
        ROUND(
          100.0 * COUNT(CASE WHEN s.status = 'completed' THEN 1 END) /
          NULLIF(COUNT(s.id), 0),
          2
        ) as success_rate
       FROM workflows w
       LEFT JOIN sessions s ON w.id = s.workflow_id
         AND s.started_at >= $1
       GROUP BY w.id, w.name, w.description
       HAVING COUNT(s.id) > 0
       ORDER BY total_sessions DESC`,
      [startDate]
    )

    res.json({
      workflows: result.rows,
      timeRange: {
        start: startDate.toISOString(),
        end: new Date().toISOString(),
        days
      }
    })
  } catch (error) {
    console.error('Workflow analytics error:', error)
    res.status(500).json({
      error: 'Failed to fetch workflow analytics',
      details: (error as Error).message
    })
  }
})

/**
 * Get session status distribution
 * GET /api/analytics/status-distribution
 */
analyticsRouter.get('/status-distribution', async (req: Request, res: Response) => {
  try {
    const { timeRange = '7d', workflowId } = req.query
    const days = parseInt(timeRange as string) || 7
    const startDate = new Date()
    startDate.setDate(startDate.getDate() - days)

    let query = `
      SELECT
        status,
        COUNT(*) as count,
        ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as percentage
      FROM sessions
      WHERE started_at >= $1
    `

    const params: any[] = [startDate]

    if (workflowId) {
      query += ` AND workflow_id = $2`
      params.push(workflowId)
    }

    query += `
      GROUP BY status
      ORDER BY count DESC
    `

    const result = await pool.query(query, params)

    res.json({
      distribution: result.rows,
      timeRange: {
        start: startDate.toISOString(),
        end: new Date().toISOString(),
        days
      }
    })
  } catch (error) {
    console.error('Status distribution error:', error)
    res.status(500).json({
      error: 'Failed to fetch status distribution',
      details: (error as Error).message
    })
  }
})

/**
 * Get token usage breakdown
 * GET /api/analytics/token-usage
 */
analyticsRouter.get('/token-usage', async (req: Request, res: Response) => {
  try {
    const { timeRange = '7d', workflowId } = req.query
    const days = parseInt(timeRange as string) || 7
    const startDate = new Date()
    startDate.setDate(startDate.getDate() - days)

    let query = `
      SELECT
        DATE_TRUNC('day', started_at) as date,
        SUM(input_tokens) as input_tokens,
        SUM(output_tokens) as output_tokens,
        SUM(input_tokens + output_tokens) as total_tokens
      FROM sessions
      WHERE started_at >= $1
        AND input_tokens IS NOT NULL
    `

    const params: any[] = [startDate]

    if (workflowId) {
      query += ` AND workflow_id = $2`
      params.push(workflowId)
    }

    query += `
      GROUP BY date
      ORDER BY date ASC
    `

    const result = await pool.query(query, params)

    // Get totals
    const totalsResult = await pool.query(
      `SELECT
        SUM(input_tokens) as total_input,
        SUM(output_tokens) as total_output,
        SUM(input_tokens + output_tokens) as total_tokens
       FROM sessions
       WHERE started_at >= $1
         ${workflowId ? 'AND workflow_id = $2' : ''}
         AND input_tokens IS NOT NULL`,
      workflowId ? [startDate, workflowId] : [startDate]
    )

    res.json({
      timeSeries: result.rows,
      totals: totalsResult.rows[0],
      timeRange: {
        start: startDate.toISOString(),
        end: new Date().toISOString(),
        days
      }
    })
  } catch (error) {
    console.error('Token usage error:', error)
    res.status(500).json({
      error: 'Failed to fetch token usage',
      details: (error as Error).message
    })
  }
})

/**
 * Get top costly sessions
 * GET /api/analytics/top-costs
 */
analyticsRouter.get('/top-costs', async (req: Request, res: Response) => {
  try {
    const { limit = 10, timeRange = '30d', workflowId } = req.query
    const days = parseInt(timeRange as string) || 30
    const startDate = new Date()
    startDate.setDate(startDate.getDate() - days)

    let query = `
      SELECT
        s.id,
        s.workflow_id,
        w.name as workflow_name,
        s.status,
        s.cost_usd,
        s.input_tokens,
        s.output_tokens,
        s.started_at,
        s.completed_at,
        EXTRACT(EPOCH FROM (s.completed_at - s.started_at)) as duration_seconds
      FROM sessions s
      JOIN workflows w ON s.workflow_id = w.id
      WHERE s.started_at >= $1
        AND s.cost_usd IS NOT NULL
    `

    const params: any[] = [startDate]

    if (workflowId) {
      query += ` AND s.workflow_id = $2`
      params.push(workflowId)
    }

    query += `
      ORDER BY s.cost_usd DESC
      LIMIT $${params.length + 1}
    `
    params.push(limit)

    const result = await pool.query(query, params)

    res.json({
      sessions: result.rows,
      timeRange: {
        start: startDate.toISOString(),
        end: new Date().toISOString(),
        days
      }
    })
  } catch (error) {
    console.error('Top costs error:', error)
    res.status(500).json({
      error: 'Failed to fetch top costs',
      details: (error as Error).message
    })
  }
})

/**
 * Get hourly activity heatmap
 * GET /api/analytics/activity-heatmap
 */
analyticsRouter.get('/activity-heatmap', async (req: Request, res: Response) => {
  try {
    const { timeRange = '30d', workflowId } = req.query
    const days = parseInt(timeRange as string) || 30
    const startDate = new Date()
    startDate.setDate(startDate.getDate() - days)

    let query = `
      SELECT
        EXTRACT(DOW FROM started_at) as day_of_week,
        EXTRACT(HOUR FROM started_at) as hour_of_day,
        COUNT(*) as session_count,
        AVG(cost_usd) as avg_cost
      FROM sessions
      WHERE started_at >= $1
    `

    const params: any[] = [startDate]

    if (workflowId) {
      query += ` AND workflow_id = $2`
      params.push(workflowId)
    }

    query += `
      GROUP BY day_of_week, hour_of_day
      ORDER BY day_of_week, hour_of_day
    `

    const result = await pool.query(query, params)

    res.json({
      heatmap: result.rows,
      timeRange: {
        start: startDate.toISOString(),
        end: new Date().toISOString(),
        days
      }
    })
  } catch (error) {
    console.error('Activity heatmap error:', error)
    res.status(500).json({
      error: 'Failed to fetch activity heatmap',
      details: (error as Error).message
    })
  }
})

/**
 * Get dashboard summary
 * GET /api/analytics/summary
 */
analyticsRouter.get('/summary', async (req: Request, res: Response) => {
  try {
    const { timeRange = '7d' } = req.query
    const days = parseInt(timeRange as string) || 7
    const startDate = new Date()
    startDate.setDate(startDate.getDate() - days)

    // Get overall stats
    const statsResult = await pool.query(
      `SELECT
        COUNT(*) as total_sessions,
        COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_count,
        COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed_count,
        COUNT(CASE WHEN status = 'active' THEN 1 END) as active_count,
        COUNT(CASE WHEN status = 'stalled' THEN 1 END) as stalled_count,
        COALESCE(SUM(cost_usd), 0) as total_cost,
        COALESCE(SUM(input_tokens + output_tokens), 0) as total_tokens,
        COUNT(DISTINCT workflow_id) as unique_workflows,
        ROUND(
          100.0 * COUNT(CASE WHEN status = 'completed' THEN 1 END) /
          NULLIF(COUNT(*), 0),
          2
        ) as success_rate
       FROM sessions
       WHERE started_at >= $1`,
      [startDate]
    )

    // Get cost trend (compare to previous period)
    const previousStartDate = new Date(startDate)
    previousStartDate.setDate(previousStartDate.getDate() - days)

    const trendResult = await pool.query(
      `SELECT
        CASE
          WHEN started_at >= $1 THEN 'current'
          ELSE 'previous'
        END as period,
        COALESCE(SUM(cost_usd), 0) as total_cost,
        COUNT(*) as session_count
       FROM sessions
       WHERE started_at >= $2
       GROUP BY period`,
      [startDate, previousStartDate]
    )

    const currentPeriod = trendResult.rows.find((r: any) => r.period === 'current') || { total_cost: 0, session_count: 0 }
    const previousPeriod = trendResult.rows.find((r: any) => r.period === 'previous') || { total_cost: 0, session_count: 0 }

    const costTrend = previousPeriod.total_cost > 0
      ? ((currentPeriod.total_cost - previousPeriod.total_cost) / previousPeriod.total_cost * 100).toFixed(2)
      : null

    const sessionTrend = previousPeriod.session_count > 0
      ? ((currentPeriod.session_count - previousPeriod.session_count) / previousPeriod.session_count * 100).toFixed(2)
      : null

    res.json({
      summary: statsResult.rows[0],
      trends: {
        cost: {
          current: parseFloat(currentPeriod.total_cost),
          previous: parseFloat(previousPeriod.total_cost),
          change_percent: costTrend ? parseFloat(costTrend) : null
        },
        sessions: {
          current: currentPeriod.session_count,
          previous: previousPeriod.session_count,
          change_percent: sessionTrend ? parseFloat(sessionTrend) : null
        }
      },
      timeRange: {
        start: startDate.toISOString(),
        end: new Date().toISOString(),
        days
      }
    })
  } catch (error) {
    console.error('Summary error:', error)
    res.status(500).json({
      error: 'Failed to fetch summary',
      details: (error as Error).message
    })
  }
})
