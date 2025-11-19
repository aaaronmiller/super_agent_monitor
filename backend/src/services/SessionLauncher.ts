import { spawn, ChildProcess } from 'child_process'
import { EventEmitter } from 'events'
import path from 'path'
import { pool } from '../index'
import { v4 as uuidv4 } from 'uuid'

export interface SessionConfig {
  workflowId: string
  claudeFolderPath: string
  model?: string
  temperature?: number
  maxTokens?: number
}

export interface SessionEvent {
  type: 'start' | 'output' | 'error' | 'tool_use' | 'api_request' | 'api_response' | 'complete' | 'failed'
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
    const sessionId = uuidv4()

    try {
      // Create session record in database
      await pool.query(`
        INSERT INTO sessions (id, workflow_id, status, started_at)
        VALUES ($1, $2, 'pending', NOW())
      `, [sessionId, config.workflowId])

      // Spawn Claude Code process
      const claudeProcess = this.spawnClaudeProcess(sessionId, config)

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

    const process = spawn('claude', args, {
      cwd: path.dirname(config.claudeFolderPath),
      env: {
        ...process.env,
        ANTHROPIC_BASE_URL: process.env.CLAUDE_CODE_PROXY_URL || process.env.ANTHROPIC_BASE_URL,
        SESSION_ID: sessionId
      }
    })

    return process
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

    // Parse for structured events (JSON lines)
    const lines = output.split('\n').filter(line => line.trim())

    for (const line of lines) {
      try {
        // Try to parse as JSON (Claude Code outputs events as JSON)
        if (line.startsWith('{')) {
          const event = JSON.parse(line)
          await this.logEvent(sessionId, {
            type: event.type || 'output',
            timestamp: new Date().toISOString(),
            data: event
          })

          // Handle specific event types
          if (event.type === 'tool_use') {
            this.emit('session:tool_use', { sessionId, tool: event.tool })
          } else if (event.type === 'api_response') {
            await this.updateTokenUsage(sessionId, event.usage)
          }
        }
      } catch (error) {
        // Not JSON, just regular output
        await this.logEvent(sessionId, {
          type: 'output',
          timestamp: new Date().toISOString(),
          data: { message: line }
        })
      }
    }
  }

  /**
   * Handle stderr errors
   */
  private async handleError(sessionId: string, error: string) {
    await this.logEvent(sessionId, {
      type: 'error',
      timestamp: new Date().toISOString(),
      data: { error }
    })

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
   * Update session status in database
   */
  private async updateSessionStatus(sessionId: string, status: string, error?: string) {
    const updates: string[] = ['status = $1', 'updated_at = NOW()']
    const params: any[] = [status]

    if (status === 'completed' || status === 'failed') {
      updates.push('completed_at = NOW()')
    }

    if (error) {
      params.push(error)
      updates.push(`error = $${params.length}`)
    }

    params.push(sessionId)

    await pool.query(`
      UPDATE sessions
      SET ${updates.join(', ')}
      WHERE id = $${params.length}
    `, params)

    console.log(`[${sessionId}] Status updated: ${status}`)
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
      await pool.query(`
        INSERT INTO events (session_id, type, timestamp, data)
        VALUES ($1, $2, $3, $4)
      `, [sessionId, event.type, event.timestamp, JSON.stringify(event.data)])
    } catch (error) {
      console.error(`Failed to log event for session ${sessionId}:`, error)
    }
  }
}

// Singleton instance
export const sessionLauncher = new SessionLauncher()
