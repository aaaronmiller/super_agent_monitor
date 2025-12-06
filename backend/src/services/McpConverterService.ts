import { spawn } from 'child_process'
import path from 'path'
import fs from 'fs/promises'

export interface ConversionResult {
    success: boolean
    tools: string[]
    outputDir: string
    error?: string
}

export class McpConverterService {
    private pythonScriptPath: string

    constructor() {
        this.pythonScriptPath = path.join(__dirname, '../python/mcp_converter.py')
    }

    /**
     * Convert an MCP server file to a Skill (scripts + SKILL.md)
     * @param mcpFilePath Absolute path to the server.py file
     * @param outputDir Directory to save the generated skill
     * @param skillName Name of the skill
     */
    async convert(mcpFilePath: string, outputDir: string, skillName: string): Promise<ConversionResult> {
        return new Promise((resolve, reject) => {
            const pythonProcess = spawn('python3', [
                this.pythonScriptPath,
                mcpFilePath,
                outputDir,
                '--name',
                skillName
            ])

            let output = ''
            let errorOutput = ''

            pythonProcess.stdout.on('data', (data) => {
                output += data.toString()
            })

            pythonProcess.stderr.on('data', (data) => {
                errorOutput += data.toString()
            })

            pythonProcess.on('close', (code) => {
                if (code !== 0) {
                    console.error('MCP Conversion failed:', errorOutput)
                    resolve({
                        success: false,
                        tools: [],
                        outputDir,
                        error: errorOutput || 'Unknown error during conversion'
                    })
                    return
                }

                try {
                    // The script prints log messages, but the last line should be the JSON result
                    const lines = output.trim().split('\n')
                    const jsonLine = lines[lines.length - 1]
                    const result = JSON.parse(jsonLine)
                    resolve({
                        success: true,
                        tools: result.tools,
                        outputDir: result.output_dir
                    })
                } catch (e) {
                    console.error('Failed to parse conversion output:', e)
                    resolve({
                        success: false,
                        tools: [],
                        outputDir,
                        error: 'Failed to parse conversion output'
                    })
                }
            })
        })
    }

    /**
     * Validate if a file is a valid python file
     */
    async validateFile(filePath: string): Promise<boolean> {
        try {
            await fs.access(filePath)
            return filePath.endsWith('.py')
        } catch {
            return false
        }
    }
}

export const mcpConverterService = new McpConverterService()
