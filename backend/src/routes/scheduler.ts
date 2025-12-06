import { Router, Request, Response } from 'express'
import { schedulerService } from '../services/SchedulerService'

export const schedulerRouter = Router()

/**
 * List all tasks
 * GET /api/scheduler/tasks
 */
schedulerRouter.get('/tasks', async (req: Request, res: Response) => {
    try {
        const tasks = await schedulerService.listTasks()
        res.json(tasks)
    } catch (error) {
        console.error('Error listing tasks:', error)
        res.status(500).json({ error: 'Failed to list tasks' })
    }
})

/**
 * Create a task
 * POST /api/scheduler/tasks
 */
schedulerRouter.post('/tasks', async (req: Request, res: Response) => {
    try {
        const task = await schedulerService.createTask(req.body)
        res.json(task)
    } catch (error: any) {
        console.error('Error creating task:', error)
        res.status(400).json({ error: error.message || 'Failed to create task' })
    }
})

/**
 * Update a task
 * PATCH /api/scheduler/tasks/:id
 */
schedulerRouter.patch('/tasks/:id', async (req: Request, res: Response) => {
    try {
        const task = await schedulerService.updateTask(req.params.id, req.body)
        res.json(task)
    } catch (error: any) {
        console.error('Error updating task:', error)
        res.status(400).json({ error: error.message || 'Failed to update task' })
    }
})

/**
 * Delete a task
 * DELETE /api/scheduler/tasks/:id
 */
schedulerRouter.delete('/tasks/:id', async (req: Request, res: Response) => {
    try {
        await schedulerService.deleteTask(req.params.id)
        res.json({ success: true })
    } catch (error: any) {
        console.error('Error deleting task:', error)
        res.status(500).json({ error: error.message || 'Failed to delete task' })
    }
})

/**
 * Manually trigger a task
 * POST /api/scheduler/tasks/:id/run
 */
schedulerRouter.post('/tasks/:id/run', async (req: Request, res: Response) => {
    try {
        const task = await schedulerService.getTask(req.params.id)
        // Run async to not block response
        schedulerService.executeTask(task).catch(err =>
            console.error(`Manual trigger failed for task ${task.id}:`, err)
        )
        res.json({ success: true, message: 'Task execution started' })
    } catch (error: any) {
        console.error('Error triggering task:', error)
        res.status(500).json({ error: error.message || 'Failed to trigger task' })
    }
})
