import fs from 'fs/promises'
import path from 'path'
import { v4 as uuidv4 } from 'uuid'

export interface PlanFile {
    name: string
    content: string
}

export interface PlanDefinition {
    name: string
    description?: string
    prompt?: string
    files?: PlanFile[]
    orchestrator_config?: any
}

export class PlanDeployerService {
    private baseDir: string

    constructor() {
        // Default to .claude directory in the project root
        this.baseDir = path.resolve(process.cwd(), '../.claude')
    }

    /**
     * Deploy a plan to the .claude directory
     */
    async deployPlan(plan: PlanDefinition): Promise<string> {
        const planId = plan.name.toLowerCase().replace(/[^a-z0-9-_]/g, '-')
        const planDir = path.join(this.baseDir, planId)

        try {
            // Create directory
            await fs.mkdir(planDir, { recursive: true })

            // Create CLAUDE.md (Instructions)
            const claudeMdContent = `# ${plan.name}\n\n${plan.description || ''}\n\n## Instructions\n${plan.prompt || 'No specific instructions provided.'}`
            await fs.writeFile(path.join(planDir, 'CLAUDE.md'), claudeMdContent)

            // Create config.json (Orchestrator Config)
            const configContent = JSON.stringify(plan.orchestrator_config || {}, null, 2)
            await fs.writeFile(path.join(planDir, 'config.json'), configContent)

            // Create additional files
            if (plan.files) {
                for (const file of plan.files) {
                    const filePath = path.join(planDir, file.name)
                    // Ensure subdirectory exists if file has path
                    await fs.mkdir(path.dirname(filePath), { recursive: true })
                    await fs.writeFile(filePath, file.content)
                }
            }

            console.log(`✅ Deployed plan '${plan.name}' to ${planDir}`)
            return planDir
        } catch (error) {
            console.error(`❌ Failed to deploy plan '${plan.name}':`, error)
            throw error
        }
    }

    /**
     * List deployed plans
     */
    async listPlans(): Promise<string[]> {
        try {
            await fs.mkdir(this.baseDir, { recursive: true })
            const entries = await fs.readdir(this.baseDir, { withFileTypes: true })
            return entries.filter(e => e.isDirectory()).map(e => e.name)
        } catch (error) {
            return []
        }
    }
}

export const planDeployerService = new PlanDeployerService()
