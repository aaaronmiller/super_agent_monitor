import { Router, Request, Response } from 'express'
import { mcpConverterService } from '../services/McpConverterService'
import path from 'path'
import fs from 'fs/promises'

export const converterRouter = Router()

/**
 * Convert MCP to Skill
 * POST /api/converter/mcp-to-skill
 */
converterRouter.post('/mcp-to-skill', async (req: Request, res: Response) => {
    try {
        const { mcpFilePath, skillName } = req.body

        if (!mcpFilePath || !skillName) {
            res.status(400).json({ error: 'mcpFilePath and skillName are required' })
            return
        }

        // Validate input file
        const isValid = await mcpConverterService.validateFile(mcpFilePath)
        if (!isValid) {
            res.status(400).json({ error: 'Invalid MCP file path' })
            return
        }

        // Define output directory (e.g., in a temporary location or a dedicated skills folder)
        // For now, let's put it in the project's components/skills directory
        const outputDir = path.join(process.cwd(), 'components', 'skills', skillName)

        // Ensure output directory exists
        await fs.mkdir(outputDir, { recursive: true })

        const result = await mcpConverterService.convert(mcpFilePath, outputDir, skillName)

        if (result.success) {
            res.json(result)
        } else {
            res.status(500).json({ error: result.error })
        }
    } catch (error: any) {
        console.error('Error converting MCP:', error)
        res.status(500).json({ error: error.message || 'Failed to convert MCP' })
    }
})
