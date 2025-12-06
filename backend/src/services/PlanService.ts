import fs from 'fs/promises'
import path from 'path'
import { v4 as uuidv4 } from 'uuid'

export interface Plan {
    id: string
    name: string
    version: string
    description?: string
    orchestrator: string
    workflows: string[]
    customComponents: {
        type: 'mcp' | 'skill' | 'tool' | 'agent'
        path: string
    }[]
    settings: any
    createdAt: string
    updatedAt: string
}

export class PlanService {
    private plansDir: string
    private componentsDir: string

    constructor() {
        this.plansDir = path.join(process.cwd(), 'plans')
        this.componentsDir = path.join(process.cwd(), 'components')
    }

    /**
     * Initialize directories
     */
    async init() {
        try {
            await fs.mkdir(this.plansDir, { recursive: true })
        } catch (error) {
            console.error('Failed to create plans directory:', error)
        }
    }

    /**
     * List available components by scanning the components directory
     */
    async listComponents() {
        const components: any = {
            orchestrators: [],
            agents: [],
            skills: [],
            tools: []
        }

        try {
            // Scan orchestrators
            const orchDir = path.join(this.componentsDir, 'orchestrators', 'templates')
            if (await this.exists(orchDir)) {
                const files = await fs.readdir(orchDir)
                components.orchestrators = files
                    .filter(f => f.endsWith('.md'))
                    .map(f => ({ name: f.replace('.md', ''), path: path.join(orchDir, f) }))
            }

            // Scan agents
            const agentDir = path.join(this.componentsDir, 'agents')
            if (await this.exists(agentDir)) {
                const files = await fs.readdir(agentDir)
                components.agents = files
                    .filter(f => f.endsWith('.md'))
                    .map(f => ({ name: f.replace('.md', ''), path: path.join(agentDir, f) }))
            }

            // Scan skills (assuming they are in a skills dir or similar)
            // For now, we'll just return what we have
        } catch (error) {
            console.error('Error scanning components:', error)
        }

        return components
    }

    /**
     * Save a plan to disk
     */
    async savePlan(planData: Partial<Plan>): Promise<Plan> {
        const id = planData.id || uuidv4()
        const now = new Date().toISOString()

        const plan: Plan = {
            id,
            name: planData.name || 'Untitled Plan',
            version: planData.version || '1.0.0',
            description: planData.description,
            orchestrator: planData.orchestrator || 'default',
            workflows: planData.workflows || [],
            customComponents: planData.customComponents || [],
            settings: planData.settings || {},
            createdAt: planData.createdAt || now,
            updatedAt: now
        }

        const filePath = path.join(this.plansDir, `${id}.json`)
        await fs.writeFile(filePath, JSON.stringify(plan, null, 2))

        return plan
    }

    /**
     * Load a plan by ID
     */
    async loadPlan(id: string): Promise<Plan> {
        const filePath = path.join(this.plansDir, `${id}.json`)
        const content = await fs.readFile(filePath, 'utf-8')
        return JSON.parse(content)
    }

    /**
     * List all plans
     */
    async listPlans(): Promise<Plan[]> {
        try {
            const files = await fs.readdir(this.plansDir)
            const plans: Plan[] = []

            for (const file of files) {
                if (file.endsWith('.json')) {
                    const content = await fs.readFile(path.join(this.plansDir, file), 'utf-8')
                    try {
                        plans.push(JSON.parse(content))
                    } catch (e) {
                        console.error(`Failed to parse plan ${file}`, e)
                    }
                }
            }

            return plans.sort((a, b) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime())
        } catch (error) {
            return []
        }
    }

    /**
     * Hydrate a plan into a target directory (create .claude folder)
     */
    async hydrate(planId: string, targetDir: string) {
        const plan = await this.loadPlan(planId)
        const claudeDir = path.join(targetDir, '.claude')

        // 1. Create .claude directory
        await fs.mkdir(claudeDir, { recursive: true })

        // 2. Copy Orchestrator to CLAUDE.md
        // We assume the orchestrator name matches a file in components/orchestrators/templates
        const orchPath = path.join(this.componentsDir, 'orchestrators', 'templates', `${plan.orchestrator}.md`)

        try {
            const orchContent = await fs.readFile(orchPath, 'utf-8')
            await fs.writeFile(path.join(claudeDir, 'CLAUDE.md'), orchContent)
        } catch (error) {
            console.warn(`Orchestrator ${plan.orchestrator} not found, using default.`)
            await fs.writeFile(path.join(claudeDir, 'CLAUDE.md'), '# Default Agent\n\nYou are a helpful assistant.')
        }

        // 3. Generate config/settings if needed
        if (plan.settings) {
            await fs.writeFile(
                path.join(claudeDir, 'config.json'),
                JSON.stringify(plan.settings, null, 2)
            )
        }

        // 4. Copy custom components (simplified logic)
        // In a real implementation, we would resolve paths and copy files

        return { success: true, path: claudeDir }
    }

    private async exists(path: string): Promise<boolean> {
        try {
            await fs.access(path)
            return true
        } catch {
            return false
        }
    }
}

export const planService = new PlanService()
