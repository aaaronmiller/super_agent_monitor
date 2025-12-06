import { Router, Request, Response } from 'express'
import { localModelService } from '../services/LocalModelService'

const router = Router()

/**
 * GET /api/local-models/status
 * Check if LM Studio is available and list models
 */
router.get('/status', async (req: Request, res: Response) => {
    try {
        const status = await localModelService.getStatus()
        res.json(status)
    } catch (error) {
        res.status(500).json({
            available: false,
            error: (error as Error).message
        })
    }
})

/**
 * GET /api/local-models
 * List available models from LM Studio
 */
router.get('/', async (req: Request, res: Response) => {
    try {
        const models = await localModelService.listModels()
        res.json({ models })
    } catch (error) {
        res.status(503).json({
            error: 'LM Studio not available',
            message: (error as Error).message
        })
    }
})

/**
 * GET /api/local-models/recommended
 * Get recommended model configurations
 */
router.get('/recommended', (req: Request, res: Response) => {
    const configs = localModelService.getRecommendedConfigs()
    const specConfigs = localModelService.getSpeculativeConfigs()
    res.json({
        models: configs,
        speculativeDecoding: specConfigs
    })
})

/**
 * POST /api/local-models/chat
 * Proxy chat completion to LM Studio
 */
router.post('/chat', async (req: Request, res: Response) => {
    try {
        const { model, messages, temperature, max_tokens } = req.body

        if (!model || !messages) {
            return res.status(400).json({
                error: 'Missing required fields: model, messages'
            })
        }

        const response = await localModelService.chat({
            model,
            messages,
            temperature: temperature ?? 0.7,
            max_tokens: max_tokens ?? 4096
        })

        res.json(response)
    } catch (error) {
        res.status(503).json({
            error: 'Local model chat failed',
            message: (error as Error).message
        })
    }
})

export default router
