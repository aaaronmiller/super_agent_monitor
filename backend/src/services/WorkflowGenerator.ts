import fs from 'fs/promises'
import path from 'path'
import yaml from 'js-yaml'
import { componentRegistry } from './ComponentRegistry'

export interface WorkflowConfig {
  id: string
  name: string
  description?: string
  version?: string
  orchestration: {
    pattern: 'ceo-worker' | 'star' | 'round-robin'
    model: string
    systemPrompt?: string
    thinkingBudget?: number
    temperature?: number
  }
  components: {
    agents?: string[]
    skills?: string[]
    hooks?: string[]
    scripts?: string[]
  }
  memory?: {
    enabled: boolean
    persistence?: 'session' | 'permanent'
    rag?: boolean
  }
  lifecycle?: {
    haltDetectionSeconds?: number
    autoRestart?: boolean
    maxRetries?: number
    kickPrompt?: string
  }
  defaults?: {
    maxTokensPerMessage?: number
    toolTimeout?: number
  }
}

export class WorkflowGenerator {
  private workflowsDir: string
  private outputDir: string

  constructor(
    workflowsDir: string = path.join(process.cwd(), '../workflows'),
    outputDir: string = path.join(process.cwd(), '../.super_agent_monitor/workflows')
  ) {
    this.workflowsDir = workflowsDir
    this.outputDir = outputDir
  }

  /**
   * Load workflow configuration from YAML file
   */
  async loadWorkflow(workflowId: string): Promise<WorkflowConfig> {
    const workflowPath = path.join(this.workflowsDir, `${workflowId}.yaml`)
    const content = await fs.readFile(workflowPath, 'utf-8')
    const config = yaml.load(content) as WorkflowConfig

    // Validate workflow config
    if (!config.id || !config.name) {
      throw new Error('Workflow must have id and name')
    }

    if (!config.orchestration?.pattern || !config.orchestration?.model) {
      throw new Error('Workflow must specify orchestration pattern and model')
    }

    return config
  }

  /**
   * Generate .claude folder structure from workflow config
   */
  async generate(workflowId: string): Promise<string> {
    console.log(`🔧 Generating workflow: ${workflowId}`)

    // Load workflow config
    const config = await this.loadWorkflow(workflowId)

    // Create output directory
    const workflowOutputDir = path.join(this.outputDir, config.id, '.claude')
    await fs.mkdir(workflowOutputDir, { recursive: true })

    // Generate CLAUDE.md (main orchestrator prompt)
    await this.generateMainPrompt(workflowOutputDir, config)

    // Generate agents/
    if (config.components.agents?.length) {
      await this.copyComponents(workflowOutputDir, 'agents', config.components.agents)
    }

    // Generate skills/
    if (config.components.skills?.length) {
      await this.copyComponents(workflowOutputDir, 'skills', config.components.skills)
    }

    // Generate hooks/
    if (config.components.hooks?.length) {
      await this.copyComponents(workflowOutputDir, 'hooks', config.components.hooks)
    }

    // Generate scripts/
    if (config.components.scripts?.length) {
      await this.copyComponents(workflowOutputDir, 'scripts', config.components.scripts)
    }

    // Generate settings.json
    await this.generateSettings(workflowOutputDir, config)

    console.log(`✅ Workflow generated: ${workflowOutputDir}`)
    return workflowOutputDir
  }

  /**
   * Generate main CLAUDE.md orchestrator prompt
   */
  private async generateMainPrompt(outputDir: string, config: WorkflowConfig): Promise<void> {
    let content = ''

    // If workflow specifies a custom system prompt (orchestrator), use it
    if (config.orchestration.systemPrompt) {
      const orchestratorComponent = componentRegistry.getById(`orchestrator:${config.orchestration.systemPrompt.replace(/\.md$/, '')}`)
      if (orchestratorComponent) {
        content = orchestratorComponent.content
      } else {
        // Load from file
        const orchestratorPath = path.join(process.cwd(), 'components', config.orchestration.systemPrompt)
        content = await fs.readFile(orchestratorPath, 'utf-8')
      }
    } else {
      // Generate default orchestrator prompt
      content = this.generateDefaultPrompt(config)
    }

    await fs.writeFile(path.join(outputDir, 'CLAUDE.md'), content)
  }

  /**
   * Generate default orchestrator prompt
   */
  private generateDefaultPrompt(config: WorkflowConfig): string {
    return `# ${config.name}

${config.description || 'Autonomous workflow powered by Super Agent Monitor'}

## Workflow Configuration

**Pattern**: ${config.orchestration.pattern}
**Model**: ${config.orchestration.model}

## Available Components

### Agents
${config.components.agents?.map(a => `- @${a}`).join('\n') || 'None'}

### Skills
${config.components.skills?.map(s => `- ${s}`).join('\n') || 'None'}

### Hooks
${config.components.hooks?.map(h => `- ${h}`).join('\n') || 'None'}

### Scripts
${config.components.scripts?.map(s => `- ${s}`).join('\n') || 'None'}

## Memory Configuration
${config.memory?.enabled ? `
- **Persistence**: ${config.memory.persistence || 'session'}
- **RAG**: ${config.memory.rag ? 'Enabled' : 'Disabled'}
` : 'Memory disabled'}

## Lifecycle Management
${config.lifecycle ? `
- **Stall Detection**: ${config.lifecycle.haltDetectionSeconds || 300}s
- **Auto-restart**: ${config.lifecycle.autoRestart ? 'Enabled' : 'Disabled'}
- **Max Retries**: ${config.lifecycle.maxRetries || 3}
` : 'Default lifecycle settings'}

---

**You are now operating in ${config.orchestration.pattern} orchestration mode.**

${config.lifecycle?.kickPrompt ? `\n**Kick Prompt**: ${config.lifecycle.kickPrompt}` : ''}
`
  }

  /**
   * Copy components to workflow .claude directory
   */
  private async copyComponents(
    outputDir: string,
    category: string,
    componentNames: string[]
  ): Promise<void> {
    const categoryDir = path.join(outputDir, category)
    await fs.mkdir(categoryDir, { recursive: true })

    for (const componentName of componentNames) {
      const component = componentRegistry.getById(`${category.replace(/s$/, '')}:${componentName}`)

      if (!component) {
        console.warn(`⚠️  Component not found: ${category}/${componentName}`)
        continue
      }

      // Determine output filename
      let filename: string
      if (component.language === 'markdown') {
        filename = `${componentName}.md`
      } else if (component.language === 'python') {
        filename = `${componentName}.py`
      } else if (component.language === 'shell') {
        filename = `${componentName}.sh`
      } else {
        filename = componentName
      }

      const outputPath = path.join(categoryDir, filename)
      await fs.writeFile(outputPath, component.content)

      // Make scripts/hooks executable
      if (category === 'scripts' || category === 'hooks') {
        await fs.chmod(outputPath, 0o755)
      }

      console.log(`  ✓ Copied: ${category}/${filename}`)
    }
  }

  /**
   * Generate settings.json for Claude Code
   */
  private async generateSettings(outputDir: string, config: WorkflowConfig): Promise<void> {
    const settings = {
      model: config.orchestration.model,
      temperature: config.orchestration.temperature ?? 0.7,
      thinkingBudget: config.orchestration.thinkingBudget ?? 10000,
      maxTokens: config.defaults?.maxTokensPerMessage ?? 4096,
      systemPrompt: './CLAUDE.md',
      hooks: config.components.hooks?.reduce((acc, hook) => {
        acc[`${hook}`] = {
          path: `./hooks/${hook}.py`,
          trigger: 'after_tool_use'
        }
        return acc
      }, {} as Record<string, any>) || {},
      memory: config.memory?.enabled ? {
        enabled: true,
        persistence: config.memory.persistence || 'session',
        rag: config.memory.rag || false
      } : { enabled: false },
      lifecycle: {
        stall_detection_seconds: config.lifecycle?.haltDetectionSeconds || 300,
        auto_restart: config.lifecycle?.autoRestart ?? true,
        max_retries: config.lifecycle?.maxRetries || 3,
        kick_prompt: config.lifecycle?.kickPrompt || 'Continue with your task.'
      }
    }

    await fs.writeFile(
      path.join(outputDir, 'settings.json'),
      JSON.stringify(settings, null, 2)
    )
  }

  /**
   * List all available workflow templates
   */
  async listWorkflows(): Promise<string[]> {
    const files = await fs.readdir(this.workflowsDir)
    return files
      .filter(f => f.endsWith('.yaml') || f.endsWith('.yml'))
      .map(f => f.replace(/\.(yaml|yml)$/, ''))
  }

  /**
   * Validate workflow configuration
   */
  async validate(workflowId: string): Promise<{ valid: boolean; errors: string[] }> {
    const errors: string[] = []

    try {
      const config = await this.loadWorkflow(workflowId)

      // Check required fields
      if (!config.id) errors.push('Missing workflow id')
      if (!config.name) errors.push('Missing workflow name')
      if (!config.orchestration?.pattern) errors.push('Missing orchestration pattern')
      if (!config.orchestration?.model) errors.push('Missing orchestration model')

      // Validate orchestration pattern
      const validPatterns = ['ceo-worker', 'star', 'round-robin']
      if (config.orchestration?.pattern && !validPatterns.includes(config.orchestration.pattern)) {
        errors.push(`Invalid orchestration pattern: ${config.orchestration.pattern}. Must be one of: ${validPatterns.join(', ')}`)
      }

      // Validate component references
      if (config.components.agents) {
        for (const agent of config.components.agents) {
          const component = componentRegistry.getById(`agent:${agent}`)
          if (!component) {
            errors.push(`Agent not found: ${agent}`)
          }
        }
      }

      if (config.components.skills) {
        for (const skill of config.components.skills) {
          const component = componentRegistry.getById(`skill:${skill}`)
          if (!component) {
            errors.push(`Skill not found: ${skill}`)
          }
        }
      }

      return { valid: errors.length === 0, errors }

    } catch (error: any) {
      errors.push(`Failed to load workflow: ${error.message}`)
      return { valid: false, errors }
    }
  }
}

// Singleton instance
export const workflowGenerator = new WorkflowGenerator()
