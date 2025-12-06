import { spawn, ChildProcess } from 'child_process'
import { EventEmitter } from 'events'
import path from 'path'
import { pool } from '../db/pool'
import { v4 as uuidv4 } from 'uuid'
import { memoryIngestion } from './MemoryIngestion'
import { componentRegistry } from './ComponentRegistry'
import { proxyService } from './ProxyService'
import fs from 'fs/promises'

import { sandboxService } from './SandboxService'

export interface SessionConfig {
  workflowId: string
  claudeFolderPath: string
  model?: string
  temperature?: number
  maxTokens?: number
  orchestratorId?: string
  sessionId?: string
  contextInjection?: boolean
  initialPrompt?: string
  runtime?: 'local' | 'e2b'
  metadata?: any
}

export interface SessionEvent {
  type: 'start' | 'output' | 'error' | 'tool_use' | 'api_request' | 'api_response' | 'complete' | 'failed' | 'system_context'
  timestamp: string
  data?: any
}

export class SessionLauncher extends EventEmitter {
  private sessions: Map<string, ChildProcess> = new Map()
  private sessionConfigs: Map<string, SessionConfig> = new Map()
  private lastActivity: Map<string, Date> = new Map()

  constructor() {
    super()
  }

  /**
   * Launch a new Claude Code session
   */
  async launch(config: SessionConfig): Promise<string> {
    const sessionId = config.sessionId || uuidv4()

    try {
      // Create session record in database if it doesn't exist (or update if provided)
      // If sessionId was provided, we assume the record exists (e.g. pending) or we upsert.
      // For safety, we'll use ON CONFLICT DO NOTHING or just update status if it exists.

      if (config.sessionId) {
        await pool.query(`
            UPDATE sessions 
            SET status = 'pending', started_at = NOW() 
            WHERE id = $1
          `, [sessionId])
      } else {
        await pool.query(`
            INSERT INTO sessions (id, workflow_id, status, started_at)
            VALUES ($1, $2, 'pending', NOW())
          `, [sessionId, config.workflowId])
      }

      // Ensure proxy is running
      let proxyPort = proxyService.getPort()
      if (proxyPort === 0) {
        proxyPort = await proxyService.start()
      }
      proxyService.registerSession(sessionId)

      // Handle Orchestrator Injection & Context Injection
      let finalConfigPath = config.claudeFolderPath
      let isTempConfig = false
      let injectedContent = ''

      // 1. Get Orchestrator Template
      if (config.orchestratorId) {
        try {
          console.log(`🔍 Loading orchestrator template for: ${config.orchestratorId}`)
          injectedContent = await componentRegistry.getOrchestratorTemplate(config.orchestratorId)
          console.log(`✅ Loaded orchestrator template (length: ${injectedContent.length})`)
        } catch (error) {
          console.warn(`⚠️ Failed to load orchestrator ${config.orchestratorId}:`, error)
        }
      }

      // 2. Perform RAG Context Injection (if enabled and prompt provided)
      if (config.contextInjection && config.initialPrompt) {
        try {
          const { ragRetrieval } = await import('./RAGRetrieval')
          const results = await ragRetrieval.retrieve({
            query: config.initialPrompt,
            workflowId: config.workflowId,
            limit: 5,
            minImportance: 0.4
          })

          if (results.memories.length > 0) {
            const contextStr = results.memories.map(m =>
              `- [${m.timestamp}] ${m.content.substring(0, 200)}...`
            ).join('\n')

            injectedContent += `\n\n## 🧠 Context from Memory\n${contextStr}\n`
            console.log(`🧠 Injected ${results.memories.length} memories into context`)

            // Log system context event
            await this.logEvent(sessionId, {
              type: 'system_context',
              timestamp: new Date().toISOString(),
              data: {
                count: results.memories.length,
                memories: results.memories.map(m => ({
                  timestamp: m.timestamp,
                  content: m.content,
                  score: m.similarityScore
                }))
              }
            })
          }
        } catch (error) {
          console.warn(`⚠️ Failed to inject context:`, error)
        }
      }

      // 3. Write Temp Config if we have injected content
      if (injectedContent) {
        // If we didn't load an orchestrator, we need to read the original config first
        if (!config.orchestratorId) {
          try {
            const originalContent = await fs.readFile(config.claudeFolderPath, 'utf-8')
            injectedContent = originalContent + injectedContent
          } catch (e) {
            // If original doesn't exist, just use injected (rare)
          }
        }

        const dir = path.dirname(config.claudeFolderPath)
        const tempPath = path.join(dir, `CLAUDE.${sessionId}.md`)

        await fs.writeFile(tempPath, injectedContent, 'utf-8')

        finalConfigPath = tempPath
        isTempConfig = true
        console.log(`🎭 Created temp config at ${tempPath}`)
      }

      // Check runtime
      if (config.runtime === 'e2b') {
        console.log(`🚀 Launching E2B Sandbox Agent for session ${sessionId}`)

        const repoUrl = config.metadata?.repoUrl || 'https://github.com/disler/claude-code-hooks-multi-agent-observability'
        let prompt = config.initialPrompt || 'Check health'

        if (injectedContent) {
          prompt = injectedContent + "\n\nUser Task:\n" + prompt
          console.log(`🧠 Injected context and orchestrator into E2B prompt (length: ${prompt.length})`)
        }

        // Path to sandbox_workflows app
        const sandboxWorkflowsDir = path.resolve(process.cwd(), '../agent-sandboxes/apps/sandbox_workflows')

        console.log(`   Repo: ${repoUrl}`)
        console.log(`   Prompt: ${prompt}`)
        console.log(`   CWD: ${sandboxWorkflowsDir}`)

        const args = [
          'run',
          'python',
          '-m',
          'src.main',
          repoUrl,
          '--prompt',
          prompt,
          '--forks',
          '1'
        ]

        console.log('Spawning agent with args:', args)

        if (config.model) {
          args.push('--model', config.model)
        }

        const agentProcess = spawn('uv', args, {
          cwd: sandboxWorkflowsDir,
          env: {
            ...process.env,
            SESSION_ID: sessionId
          }
        })

        // Store session
        this.sessions.set(sessionId, agentProcess)
        this.sessionConfigs.set(sessionId, config)
        this.lastActivity.set(sessionId, new Date())

        // Setup event handlers (reuse existing setupProcessHandlers logic if compatible, or custom)
        // sandbox-fork outputs logs to files, but also streams to stdout?
        // Let's use setupProcessHandlers which handles stdout/stderr
        this.setupProcessHandlers(sessionId, agentProcess)

        // Update status to active
        await this.updateSessionStatus(sessionId, 'active')

        return sessionId
      }

      // Spawn Claude Code process (Local)
      const claudeProcess = this.spawnClaudeProcess(sessionId, { ...config, claudeFolderPath: finalConfigPath })

      // Store session metadata
      if (isTempConfig) {
        (claudeProcess as any).tempConfigPath = finalConfigPath
      }

      // Store session
      this.sessions.set(sessionId, claudeProcess)
      this.sessionConfigs.set(sessionId, config)
      this.lastActivity.set(sessionId, new Date())

      // Setup event handlers
      this.setupProcessHandlers(sessionId, claudeProcess)

      // Update status to active
      await this.updateSessionStatus(sessionId, 'active')

      // Emit launch event
      this.emit('session:launched', { sessionId, config })

      // Increment usage count for orchestrator
      if (config.orchestratorId) {
        await this.incrementUsage(config.orchestratorId)
      }

      return sessionId
    } catch (error) {
      console.error(`Failed to launch session ${sessionId}:`, error)

      // Update status to failed
      await pool.query(`
        UPDATE sessions
        SET status = 'failed', error = $1, completed_at = NOW()
        WHERE id = $2
      `, [(error as Error).message, sessionId])

      throw error
    }
  }

  /**
   * Spawn Claude Code process
   */
  private spawnClaudeProcess(sessionId: string, config: SessionConfig): ChildProcess {
    const args = [
      '--headless',
      `--config=${config.claudeFolderPath}`,
      `--session-id=${sessionId}`
    ]

    // Add optional parameters
    if (config.model) {
      args.push(`--model=${config.model}`)
    }

    if (config.temperature !== undefined) {
      args.push(`--temperature=${config.temperature}`)
    }

    if (config.maxTokens) {
      args.push(`--max-tokens=${config.maxTokens}`)
    }

    console.log(`🚀 Launching Claude Code for session ${sessionId}`)
    console.log(`   Command: claude ${args.join(' ')}`)

    const claudeProcess = spawn('claude', args, {
      cwd: path.dirname(config.claudeFolderPath),
      env: {
        ...process.env,
        ANTHROPIC_BASE_URL: process.env.CLAUDE_CODE_PROXY_URL || process.env.ANTHROPIC_BASE_URL,
        SESSION_ID: sessionId,
        HTTP_PROXY: `http://127.0.0.1:${proxyService.getPort()}`,
        HTTPS_PROXY: `http://127.0.0.1:${proxyService.getPort()}`
      }
    })

    return claudeProcess
  }

  /**
   * Setup process event handlers
   */
  private setupProcessHandlers(sessionId: string, claudeProcess: ChildProcess) {
    // Track stdout for events
    claudeProcess.stdout?.on('data', (data: Buffer) => {
      const output = data.toString()
      this.handleOutput(sessionId, output)
      this.updateLastActivity(sessionId)
    })

    // Track stderr for errors
    claudeProcess.stderr?.on('data', (data: Buffer) => {
      const error = data.toString()
      console.error(`[${sessionId}] Error: ${error}`)
      this.handleError(sessionId, error)
      this.updateLastActivity(sessionId)
    })

    // Handle process exit
    claudeProcess.on('exit', (code, signal) => {
      console.log(`[${sessionId}] Process exited with code ${code}, signal ${signal}`)
      this.handleExit(sessionId, code, signal)
    })

    // Handle process errors
    claudeProcess.on('error', (error) => {
      console.error(`[${sessionId}] Process error:`, error)
      this.handleProcessError(sessionId, error)
    })
  }

  /**
   * Handle stdout output
   */
  private async handleOutput(sessionId: string, output: string) {
    // Log raw output for debugging
    console.log(`[${sessionId}] Output: ${output.substring(0, 200)}...`)

    // Update last activity
    this.lastActivity.set(sessionId, new Date())

    // Get workflow ID for memory ingestion
    const config = this.sessionConfigs.get(sessionId)
    if (!config) return

    // Parse for structured events (JSON lines)
    const lines = output.split('\n').filter(line => line.trim())

    for (const line of lines) {
      try {
        // Try to parse as JSON (Claude Code outputs events as JSON)
        if (line.startsWith('{')) {
          const event = JSON.parse(line)
          const eventId = uuidv4()

          await this.logEvent(sessionId, {
            type: event.type || 'output',
            timestamp: new Date().toISOString(),
            data: event
          })

          // Ingest into memory system for significant events
          if (event.type === 'tool_use' && event.output) {
            // Queue tool outputs for memory (batched)
            memoryIngestion.queueForBatch({
              sessionId,
              workflowId: config.workflowId,
              content: JSON.stringify({
                tool: event.tool,
                input: event.input,
                output: event.output
              }),
              contentType: 'tool_output',
              metadata: {
                tool: event.tool,
                duration: event.duration
              },
              eventId,
              toolName: event.tool
            })

            this.emit('session:tool_use', { sessionId, tool: event.tool })
          } else if (event.type === 'api_response') {
            await this.updateTokenUsage(sessionId, event.usage)

            // Ingest completion messages
            if (event.content) {
              memoryIngestion.queueForBatch({
                sessionId,
                workflowId: config.workflowId,
                content: event.content,
                contentType: 'completion',
                metadata: {
                  model: event.model,
                  tokens: event.usage
                },
                eventId
              })
            }
          }
        }
      } catch (error) {
        // Not JSON, just regular output
        const eventData: SessionEvent = {
          type: 'output',
          timestamp: new Date().toISOString(),
          data: { message: line }
        }

        await this.logEvent(sessionId, eventData)

        // Emit for WebSocket streaming
        this.emit('session:output', { sessionId, ...eventData })
      }
    }
  }

  /**
   * Handle stderr errors
   */
  private async handleError(sessionId: string, error: string) {
    const eventId = uuidv4()

    await this.logEvent(sessionId, {
      type: 'error',
      timestamp: new Date().toISOString(),
      data: { error }
    })

    // Ingest errors into memory (high importance)
    const config = this.sessionConfigs.get(sessionId)
    if (config && error.trim().length > 0) {
      memoryIngestion.queueForBatch({
        sessionId,
        workflowId: config.workflowId,
        content: error,
        contentType: 'error',
        metadata: {
          severity: 'error'
        },
        eventId,
        importanceScore: 0.8 // Errors are important to remember
      })
    }

    this.emit('session:error', { sessionId, error })
  }

  /**
   * Handle process exit
   */
  private async handleExit(sessionId: string, code: number | null, signal: string | null) {
    const status = code === 0 ? 'completed' : 'failed'

    await this.updateSessionStatus(sessionId, status)

    // Clean up
    this.sessions.delete(sessionId)
    this.sessionConfigs.delete(sessionId)
    this.lastActivity.delete(sessionId)

    await this.logEvent(sessionId, {
      type: 'complete',
      timestamp: new Date().toISOString(),
      data: { exitCode: code, signal }
    })

    this.emit('session:exit', { sessionId, status, code, signal })

    // Clean up temp config if it exists
    const process = this.sessions.get(sessionId)
    if (process && (process as any).tempConfigPath) {
      try {
        await fs.unlink((process as any).tempConfigPath)
        console.log(`🧹 Cleaned up temp config: ${(process as any).tempConfigPath}`)
      } catch (error) {
        console.warn(`⚠️ Failed to clean up temp config:`, error)
      }
    }
  }

  /**
   * Handle process errors
   */
  private async handleProcessError(sessionId: string, error: Error) {
    await this.updateSessionStatus(sessionId, 'failed', error.message)

    this.emit('session:failed', { sessionId, error: error.message })
  }

  /**
   * Stop a running session
   */
  async stop(sessionId: string): Promise<void> {
    const process = this.sessions.get(sessionId)

    if (!process) {
      throw new Error(`Session ${sessionId} not found`)
    }

    console.log(`🛑 Stopping session ${sessionId}`)

    // Send SIGTERM for graceful shutdown
    process.kill('SIGTERM')

    // Wait for process to exit (with timeout)
    await new Promise<void>((resolve) => {
      const timeout = setTimeout(() => {
        // Force kill if not exited
        console.warn(`⚠️  Session ${sessionId} did not exit gracefully, force killing`)
        process.kill('SIGKILL')
        resolve()
      }, 10000) // 10 second timeout

      process.on('exit', () => {
        clearTimeout(timeout)
        resolve()
      })
    })

    await this.updateSessionStatus(sessionId, 'completed')
  }

  /**
   * Kick a stalled session (send SIGINT)
   */
  async kick(sessionId: string): Promise<void> {
    const process = this.sessions.get(sessionId)

    if (!process) {
      throw new Error(`Session ${sessionId} not found`)
    }

    console.log(`🥾 Kicking session ${sessionId} (SIGINT)`)

    // Send SIGINT (Ctrl+C equivalent)
    process.kill('SIGINT')

    await this.logEvent(sessionId, {
      type: 'output',
      timestamp: new Date().toISOString(),
      data: { message: 'User kicked the session (SIGINT)' }
    })
  }

  /**
   * Restart a stalled session
   */
  async restart(sessionId: string): Promise<string> {
    console.log(`🔄 Restarting session ${sessionId}`)

    const config = this.sessionConfigs.get(sessionId)
    if (!config) {
      throw new Error(`Cannot restart session ${sessionId}: config not found`)
    }

    // Stop existing session
    try {
      await this.stop(sessionId)
    } catch (error) {
      console.warn(`Warning: Failed to stop session before restart:`, error)
    }

    // Wait a bit before restarting
    await new Promise(resolve => setTimeout(resolve, 2000))

    // Launch new session with same config
    const newSessionId = await this.launch(config)

    // Log restart event
    await this.logEvent(newSessionId, {
      type: 'output',
      timestamp: new Date().toISOString(),
      data: { message: `Restarted from session ${sessionId}` }
    })

    return newSessionId
  }

  /**
   * Clone a session (start new one with same config, keep old one running)
   */
  async clone(sessionId: string): Promise<string> {
    console.log(`👯 Cloning session ${sessionId}`)

    let config = this.sessionConfigs.get(sessionId)

    if (!config) {
      // Try to fetch from DB
      try {
        const result = await pool.query(
          'SELECT config_snapshot, workflow_id FROM sessions WHERE id = $1',
          [sessionId]
        )

        if (result.rowCount && result.rowCount > 0) {
          const row = result.rows[0]
          // Reconstruct config
          // We need to know if it was e2b or local. 
          // config_snapshot should have it.
          if (row.config_snapshot) {
            config = row.config_snapshot
          } else {
            // Fallback if no snapshot (legacy?)
            config = {
              workflowId: row.workflow_id,
              // Default to local if unknown? Or error?
              // We'll assume local for safety or error.
              runtime: 'local',
              // We need claudeFolderPath for local runtime, but we don't have it in DB if not in snapshot.
              // We can try to guess or just fail if it's missing.
              // For now, let's assume it's in env or default.
              claudeFolderPath: process.env.CLAUDE_FOLDER_PATH || '/Users/macuser/.claude'
            }
          }
        }
      } catch (err) {
        console.warn(`Failed to fetch session ${sessionId} from DB for cloning:`, err)
      }
    }

    if (!config) {
      throw new Error(`Cannot clone session ${sessionId}: config not found in memory or DB`)
    }

    // Launch new session with same config
    // Generate new ID automatically in launch()
    const newConfig = { ...config, sessionId: undefined }
    const newSessionId = await this.launch(newConfig)

    // Log clone event
    await this.logEvent(newSessionId, {
      type: 'output',
      timestamp: new Date().toISOString(),
      data: { message: `Cloned from session ${sessionId}` }
    })

    return newSessionId
  }

  /**
   * Get active sessions
   */
  getActiveSessions(): string[] {
    return Array.from(this.sessions.keys())
  }

  /**
   * Check if session is running
   */
  isRunning(sessionId: string): boolean {
    return this.sessions.has(sessionId)
  }

  /**
   * Get last activity time for session
   */
  getLastActivity(sessionId: string): Date | undefined {
    return this.lastActivity.get(sessionId)
  }

  /**
   * Update last activity time
   */
  private updateLastActivity(sessionId: string) {
    this.lastActivity.set(sessionId, new Date())
  }

  /**
   * Update session status in DB
   */
  private async updateSessionStatus(
    sessionId: string,
    status: string,
    error?: string
  ) {
    try {
      // Schema has last_activity_at, not updated_at
      const updates: string[] = ['status = $2', 'last_activity_at = NOW()']
      const params: any[] = [sessionId, status]

      if (status === 'completed' || status === 'failed') {
        updates.push('ended_at = NOW()')
      }

      if (error) {
        updates.push(`error_message = $${params.length + 1}`)
        params.push(error)
      }

      await pool.query(
        `UPDATE sessions SET ${updates.join(', ')} WHERE id = $1`,
        params
      )
    } catch (err) {
      console.error(`Failed to update session status for ${sessionId}:`, err)
    }
  }

  /**
   * Update token usage and cost
   */
  private async updateTokenUsage(sessionId: string, usage: any) {
    if (!usage) return

    const { input_tokens, output_tokens } = usage
    const cost = this.calculateCost(input_tokens, output_tokens)

    await pool.query(`
      UPDATE sessions
      SET
        input_tokens = COALESCE(input_tokens, 0) + $1,
        output_tokens = COALESCE(output_tokens, 0) + $2,
        cost_usd = COALESCE(cost_usd, 0) + $3,
        updated_at = NOW()
      WHERE id = $4
    `, [input_tokens, output_tokens, cost, sessionId])

    console.log(`[${sessionId}] Tokens: +${input_tokens} in, +${output_tokens} out, Cost: +$${cost.toFixed(6)}`)
  }

  /**
   * Calculate API cost (simplified pricing)
   */
  private calculateCost(inputTokens: number, outputTokens: number): number {
    // Sonnet 4 pricing: $3/MTok input, $15/MTok output
    const inputCost = (inputTokens / 1_000_000) * 3.0
    const outputCost = (outputTokens / 1_000_000) * 15.0
    return inputCost + outputCost
  }

  /**
   * Log event to database
   */
  private async logEvent(sessionId: string, event: SessionEvent) {
    try {
      await pool.query(
        'INSERT INTO events (session_id, event_type, timestamp, data) VALUES ($1, $2, NOW(), $3)',
        [sessionId, event.type, JSON.stringify(event.data)]
      )
    } catch (error) {
      console.error(`Failed to log event for session ${sessionId}:`, error)
    }
  }

  /**
   * Increment usage count for a component
   */
  private async incrementUsage(componentId: string) {
    try {
      await pool.query(`
        UPDATE components
        SET usage_count = COALESCE(usage_count, 0) + 1, updated_at = NOW()
        WHERE id = $1
      `, [componentId])
      console.log(`📈 Incremented usage for component ${componentId}`)
    } catch (error) {
      console.error(`Failed to increment usage for ${componentId}:`, error)
    }
  }
}

// Singleton instance
export const sessionLauncher = new SessionLauncher()
