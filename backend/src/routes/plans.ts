import { Router, Request, Response } from 'express'
import { planDeployerService } from '../services/PlanDeployerService'

export const plansRouter = Router()

plansRouter.post('/deploy', async (req: Request, res: Response) => {
    try {
        const plan = req.body

        if (!plan.name) {
            return res.status(400).json({ error: 'Plan name is required' })
        }

        const planPath = await planDeployerService.deployPlan(plan)
        res.json({ success: true, path: planPath })
    } catch (error: any) {
        console.error('Deploy error:', error)
        res.status(500).json({ error: error.message })
    }
})

plansRouter.get('/', async (req: Request, res: Response) => {
    try {
        const plans = await planDeployerService.listPlans()
        res.json({ plans })
    } catch (error: any) {
        res.status(500).json({ error: error.message })
    }
})
