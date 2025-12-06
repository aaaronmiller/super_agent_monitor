import { Router, Request, Response } from 'express'
import { sandboxService } from '../services/SandboxService'

export const sandboxTestRouter = Router()

sandboxTestRouter.post('/test', async (req: Request, res: Response) => {
    try {
        const result = await sandboxService.runCommand('echo "Hello from E2B!"')
        res.json(result)
    } catch (error: any) {
        res.status(500).json({ error: error.message })
    }
})
