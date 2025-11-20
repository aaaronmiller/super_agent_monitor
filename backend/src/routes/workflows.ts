import { Router } from 'express'
import { workflowGenerator } from '../services/WorkflowGenerator'
import { pool } from '../index'

export const workflowsRouter = Router()

/**
 * GET /api/workflows
 * List all workflow templates
 */
workflowsRouter.get('/', async (req, res) => {
  try {
    const templates = await workflowGenerator.listWorkflows()

    // Load details for each template
    const workflows = await Promise.all(
      templates.map(async (id) => {
        try {
          const config = await workflowGenerator.loadWorkflow(id)
          return {
            id: config.id,
            name: config.name,
            description: config.description,
            version: config.version,
            pattern: config.orchestration.pattern,
            model: config.orchestration.model,
            components: {
              agents: config.components.agents?.length || 0,
              skills: config.components.skills?.length || 0,
              hooks: config.components.hooks?.length || 0,
              scripts: config.components.scripts?.length || 0
            }
          }
        } catch (error) {
          console.error(`Error loading workflow ${id}:`, error)
          return null
        }
      })
    )

    res.json({
      workflows: workflows.filter(Boolean),
      total: workflows.filter(Boolean).length
    })
  } catch (error: any) {
    res.status(500).json({ error: { code: 'LIST_ERROR', message: error.message } })
  }
})

/**
 * GET /api/workflows/:id
 * Get workflow template details
 */
workflowsRouter.get('/:id', async (req, res) => {
  try {
    const config = await workflowGenerator.loadWorkflow(req.params.id)

    res.json({ workflow: config })
  } catch (error: any) {
    if (error.code === 'ENOENT') {
      return res.status(404).json({
        error: { code: 'NOT_FOUND', message: 'Workflow template not found' }
      })
    }
    res.status(500).json({ error: { code: 'LOAD_ERROR', message: error.message } })
  }
})

/**
 * POST /api/workflows/:id/validate
 * Validate workflow configuration
 */
workflowsRouter.post('/:id/validate', async (req, res) => {
  try {
    const result = await workflowGenerator.validate(req.params.id)

    if (result.valid) {
      res.json({ valid: true, message: 'Workflow configuration is valid' })
    } else {
      res.status(400).json({
        valid: false,
        errors: result.errors
      })
    }
  } catch (error: any) {
    res.status(500).json({ error: { code: 'VALIDATION_ERROR', message: error.message } })
  }
})

/**
 * POST /api/workflows/:id/generate
 * Generate .claude folder structure from workflow template
 */
workflowsRouter.post('/:id/generate', async (req, res) => {
  try {
    // Validate first
    const validation = await workflowGenerator.validate(req.params.id)
    if (!validation.valid) {
      return res.status(400).json({
        error: {
          code: 'INVALID_WORKFLOW',
          message: 'Workflow validation failed',
          details: validation.errors
        }
      })
    }

    // Generate workflow
    const outputPath = await workflowGenerator.generate(req.params.id)

    res.json({
      success: true,
      workflowId: req.params.id,
      outputPath,
      message: 'Workflow generated successfully'
    })
  } catch (error: any) {
    res.status(500).json({ error: { code: 'GENERATE_ERROR', message: error.message } })
  }
})

/**
 * GET /api/workflows/instances
 * Get all workflow instances (from database)
 */
workflowsRouter.get('/instances/list', async (req, res) => {
  try {
    const result = await pool.query(`
      SELECT
        id,
        name,
        template_id,
        status,
        created_at,
        updated_at
      FROM workflows
      ORDER BY created_at DESC
      LIMIT 50
    `)

    res.json({
      instances: result.rows,
      total: result.rowCount
    })
  } catch (error: any) {
    res.status(500).json({ error: { code: 'DB_ERROR', message: error.message } })
  }
})

/**
 * POST /api/workflows/instances
 * Create a new workflow instance
 * Body: { templateId: string, name?: string, config?: object }
 */
workflowsRouter.post('/instances', async (req, res) => {
  try {
    const { templateId, name, config } = req.body

    if (!templateId) {
      return res.status(400).json({
        error: { code: 'MISSING_TEMPLATE', message: 'templateId is required' }
      })
    }

    // Load template
    const template = await workflowGenerator.loadWorkflow(templateId)

    // Generate .claude folder
    const outputPath = await workflowGenerator.generate(templateId)

    // Save to database
    const result = await pool.query(`
      INSERT INTO workflows (
        name,
        template_id,
        config,
        status,
        created_at,
        updated_at
      ) VALUES ($1, $2, $3, 'pending', NOW(), NOW())
      RETURNING id, name, template_id, status, created_at
    `, [
      name || template.name,
      templateId,
      JSON.stringify(config || template)
    ])

    const instance = result.rows[0]

    res.status(201).json({
      instance,
      outputPath,
      message: 'Workflow instance created successfully'
    })
  } catch (error: any) {
    res.status(500).json({ error: { code: 'CREATE_ERROR', message: error.message } })
  }
})

/**
 * GET /api/workflows/instances/:id
 * Get workflow instance details
 */
workflowsRouter.get('/instances/:id', async (req, res) => {
  try {
    const result = await pool.query(`
      SELECT
        w.*,
        (
          SELECT json_agg(json_build_object(
            'id', s.id,
            'status', s.status,
            'started_at', s.started_at,
            'completed_at', s.completed_at
          ))
          FROM sessions s
          WHERE s.workflow_id = w.id
          ORDER BY s.started_at DESC
          LIMIT 10
        ) as recent_sessions
      FROM workflows w
      WHERE w.id = $1
    `, [req.params.id])

    if (result.rowCount === 0) {
      return res.status(404).json({
        error: { code: 'NOT_FOUND', message: 'Workflow instance not found' }
      })
    }

    res.json({ instance: result.rows[0] })
  } catch (error: any) {
    res.status(500).json({ error: { code: 'DB_ERROR', message: error.message } })
  }
})

/**
 * DELETE /api/workflows/instances/:id
 * Delete workflow instance
 */
workflowsRouter.delete('/instances/:id', async (req, res) => {
  try {
    const result = await pool.query(`
      DELETE FROM workflows
      WHERE id = $1
      RETURNING id
    `, [req.params.id])

    if (result.rowCount === 0) {
      return res.status(404).json({
        error: { code: 'NOT_FOUND', message: 'Workflow instance not found' }
      })
    }

    res.json({
      success: true,
      message: 'Workflow instance deleted'
    })
  } catch (error: any) {
    res.status(500).json({ error: { code: 'DELETE_ERROR', message: error.message } })
  }
})
