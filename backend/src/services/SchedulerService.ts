import * as cron from 'node-cron'
import { pool } from '../db/pool'
import { sessionLauncher } from './SessionLauncher'

export interface ScheduledTask {
    id: string
    name: string
    cronExpression: string
    workflowId: string
    config: any
    isActive: boolean
    lastRunAt?: Date
    nextRunAt?: Date
    createdAt: Date
    updatedAt: Date
}

export class SchedulerService {
    private jobs: Map<string, cron.ScheduledTask> = new Map()

    /**
     * Initialize the scheduler by loading active tasks from DB
     */
    async init() {
        console.log('🕰️  Initializing Scheduler...')
        const result = await pool.query(
            'SELECT * FROM scheduled_tasks WHERE is_active = true'
        )

        for (const row of result.rows) {
            const task = this.mapRowToTask(row)
            this.scheduleJob(task)
        }
        console.log(`✅ Scheduler initialized with ${this.jobs.size} active tasks.`)
    }

    /**
     * Schedule a cron job for a task
     */
    private scheduleJob(task: ScheduledTask) {
        // Cancel existing job if any
        if (this.jobs.has(task.id)) {
            this.jobs.get(task.id)?.stop()
        }

        if (!cron.validate(task.cronExpression)) {
            console.error(`❌ Invalid cron expression for task ${task.id}: ${task.cronExpression}`)
            return
        }

        const job = cron.schedule(task.cronExpression, async () => {
            console.log(`⏰ Executing scheduled task: ${task.name} (${task.id})`)
            try {
                await this.executeTask(task)
            } catch (error) {
                console.error(`❌ Failed to execute scheduled task ${task.id}:`, error)
            }
        })

        this.jobs.set(task.id, job)
        console.log(`📅 Scheduled job for task: ${task.name} (${task.cronExpression})`)
    }

    /**
     * Execute a task (Launch Session)
     */
    async executeTask(task: ScheduledTask) {
        // Update last run time
        await pool.query(
            'UPDATE scheduled_tasks SET last_run_at = NOW() WHERE id = $1',
            [task.id]
        )

        // Launch session
        // Note: We need to adapt SessionLauncher to work without req/res if needed,
        // but here we assume we can call the internal method if we refactor or use a mock.
        // For now, we'll use the public launch method but we need to construct a config.

        try {
            // Fetch workflow to ensure it exists
            const wfResult = await pool.query('SELECT * FROM workflows WHERE id = $1', [task.workflowId])
            if (wfResult.rows.length === 0) {
                throw new Error(`Workflow ${task.workflowId} not found`)
            }

            const sessionConfig = {
                workflowId: task.workflowId,
                ...task.config
            }

            // Launch session
            const sessionId = await sessionLauncher.launch(sessionConfig)
            console.log(`🚀 Scheduled session started: ${sessionId}`)
        } catch (error) {
            console.error('Error launching scheduled session:', error)
            throw error
        }
    }

    /**
     * Create a new scheduled task
     */
    async createTask(data: Partial<ScheduledTask>): Promise<ScheduledTask> {
        const { name, cronExpression, workflowId, config, isActive } = data

        if (!name || !cronExpression || !workflowId) {
            throw new Error('Missing required fields')
        }

        if (!cron.validate(cronExpression)) {
            throw new Error('Invalid cron expression')
        }

        const result = await pool.query(
            `INSERT INTO scheduled_tasks 
       (name, cron_expression, workflow_id, config, is_active)
       VALUES ($1, $2, $3, $4, $5)
       RETURNING *`,
            [name, cronExpression, workflowId, config || {}, isActive ?? true]
        )

        const task = this.mapRowToTask(result.rows[0])

        if (task.isActive) {
            this.scheduleJob(task)
        }

        return task
    }

    /**
     * Update a scheduled task
     */
    async updateTask(id: string, data: Partial<ScheduledTask>): Promise<ScheduledTask> {
        const updates: string[] = []
        const values: any[] = []
        let idx = 1

        if (data.name !== undefined) {
            updates.push(`name = $${idx++}`)
            values.push(data.name)
        }
        if (data.cronExpression !== undefined) {
            if (!cron.validate(data.cronExpression)) throw new Error('Invalid cron expression')
            updates.push(`cron_expression = $${idx++}`)
            values.push(data.cronExpression)
        }
        if (data.workflowId !== undefined) {
            updates.push(`workflow_id = $${idx++}`)
            values.push(data.workflowId)
        }
        if (data.config !== undefined) {
            updates.push(`config = $${idx++}`)
            values.push(data.config)
        }
        if (data.isActive !== undefined) {
            updates.push(`is_active = $${idx++}`)
            values.push(data.isActive)
        }

        if (updates.length === 0) return this.getTask(id)

        values.push(id)
        const result = await pool.query(
            `UPDATE scheduled_tasks SET ${updates.join(', ')} WHERE id = $${idx} RETURNING *`,
            values
        )

        if (result.rows.length === 0) throw new Error('Task not found')

        const task = this.mapRowToTask(result.rows[0])

        // Refresh job
        if (task.isActive) {
            this.scheduleJob(task)
        } else {
            this.jobs.get(task.id)?.stop()
            this.jobs.delete(task.id)
        }

        return task
    }

    /**
     * Delete a task
     */
    async deleteTask(id: string) {
        await pool.query('DELETE FROM scheduled_tasks WHERE id = $1', [id])
        this.jobs.get(id)?.stop()
        this.jobs.delete(id)
    }

    /**
     * Get a single task
     */
    async getTask(id: string): Promise<ScheduledTask> {
        const result = await pool.query('SELECT * FROM scheduled_tasks WHERE id = $1', [id])
        if (result.rows.length === 0) throw new Error('Task not found')
        return this.mapRowToTask(result.rows[0])
    }

    /**
     * List all tasks
     */
    async listTasks(): Promise<ScheduledTask[]> {
        const result = await pool.query('SELECT * FROM scheduled_tasks ORDER BY created_at DESC')
        return result.rows.map(this.mapRowToTask)
    }

    /**
     * Helper to map DB row to object
     */
    private mapRowToTask(row: any): ScheduledTask {
        return {
            id: row.id,
            name: row.name,
            cronExpression: row.cron_expression,
            workflowId: row.workflow_id,
            config: row.config,
            isActive: row.is_active,
            lastRunAt: row.last_run_at,
            nextRunAt: row.next_run_at,
            createdAt: row.created_at,
            updatedAt: row.updated_at
        }
    }

    /**
     * Send webhook notification
     */
    private async sendWebhook(url: string, payload: any) {
        try {
            // Use dynamic import for axios to avoid top-level await issues if any
            const axios = (await import('axios')).default
            await axios.post(url, payload)
            console.log(`🔔 Webhook sent to ${url}`)
        } catch (error) {
            console.error(`❌ Failed to send webhook to ${url}:`, error)
        }
    }
}

export const schedulerService = new SchedulerService()

// Listen for session events to trigger webhooks
sessionLauncher.on('session:exit', async (data) => {
    const { sessionId, status } = data
    // We need to check if this session was triggered by a scheduled task
    // Since we don't have easy access to session config here without querying DB or cache,
    // we'll query the sessions table to get the metadata we (will) store.

    // Wait, SessionLauncher doesn't store metadata in DB yet.
    // But we passed it to launch().
    // We should probably store it in the sessions table or just check if we can retrieve it.
    // For now, let's assume we can get it from sessionConfigs in SessionLauncher if it's still active?
    // But session is exiting, so it might be gone.

    // Better approach: When launching, we can store the mapping in SchedulerService if we want,
    // OR we can update SessionLauncher to persist metadata to DB.
    // Given the constraints, let's try to fetch it from the in-memory map in SessionLauncher BEFORE it's deleted.
    // But handleExit deletes it.
    // session:exit is emitted AFTER handleExit.

    // So we need to persist metadata to DB.
    // I'll skip this for now and just implement the trigger logic assuming we can get it.
    // Actually, I can just use a simple map in SchedulerService to track sessionIds it launched.
})

// Better approach: Track sessions launched by scheduler
const schedulerSessionMap = new Map<string, { taskId: string, webhookUrl: string }>()

const originalLaunch = sessionLauncher.launch.bind(sessionLauncher)
sessionLauncher.launch = async (config) => {
    const sessionId = await originalLaunch(config)
    if (config.metadata?.taskId && config.metadata?.webhookUrl) {
        schedulerSessionMap.set(sessionId, {
            taskId: config.metadata.taskId,
            webhookUrl: config.metadata.webhookUrl
        })
    }
    return sessionId
}

sessionLauncher.on('session:exit', async (data) => {
    const { sessionId, status } = data
    const taskInfo = schedulerSessionMap.get(sessionId)

    if (taskInfo) {
        console.log(`🔔 Task ${taskInfo.taskId} session ${sessionId} finished with status ${status}`)

        // Send webhook
        try {
            const axios = (await import('axios')).default
            await axios.post(taskInfo.webhookUrl, {
                taskId: taskInfo.taskId,
                sessionId,
                status,
                timestamp: new Date().toISOString()
            })
            console.log(`🔔 Webhook sent to ${taskInfo.webhookUrl}`)
        } catch (error) {
            console.error(`❌ Failed to send webhook:`, error)
        }

        schedulerSessionMap.delete(sessionId)
    }
})
