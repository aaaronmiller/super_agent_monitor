import { EventEmitter } from 'events'
import { sessionLauncher } from './SessionLauncher'
import { pool } from '../index'

export interface MonitorConfig {
  stallDetectionSeconds: number  // Time without activity to consider stalled
  checkIntervalSeconds: number    // How often to check for stalls
  maxRetries: number              // Max auto-restart attempts
}

const DEFAULT_CONFIG: MonitorConfig = {
  stallDetectionSeconds: 300,  // 5 minutes
  checkIntervalSeconds: 60,    // 1 minute
  maxRetries: 3
}

export class SessionMonitor extends EventEmitter {
  private config: MonitorConfig
  private intervalId: NodeJS.Timeout | null = null
  private retryCount: Map<string, number> = new Map()
  private isRunning: boolean = false

  constructor(config: Partial<MonitorConfig> = {}) {
    super()
    this.config = { ...DEFAULT_CONFIG, ...config }
  }

  /**
   * Start monitoring sessions
   */
  start() {
    if (this.isRunning) {
      console.warn('⚠️  SessionMonitor already running')
      return
    }

    console.log('🔍 Starting SessionMonitor')
    console.log(`   Stall detection: ${this.config.stallDetectionSeconds}s`)
    console.log(`   Check interval: ${this.config.checkIntervalSeconds}s`)
    console.log(`   Max retries: ${this.config.maxRetries}`)

    this.isRunning = true

    // Start periodic checks
    this.intervalId = setInterval(
      () => this.checkAllSessions(),
      this.config.checkIntervalSeconds * 1000
    )

    // Run initial check
    this.checkAllSessions()

    this.emit('monitor:started')
  }

  /**
   * Stop monitoring
   */
  stop() {
    if (!this.isRunning) {
      return
    }

    console.log('🛑 Stopping SessionMonitor')

    if (this.intervalId) {
      clearInterval(this.intervalId)
      this.intervalId = null
    }

    this.isRunning = false
    this.emit('monitor:stopped')
  }

  /**
   * Check all active sessions for stalls
   */
  private async checkAllSessions() {
    const activeSessions = sessionLauncher.getActiveSessions()

    if (activeSessions.length === 0) {
      return
    }

    console.log(`🔍 Checking ${activeSessions.length} active sessions for stalls...`)

    for (const sessionId of activeSessions) {
      await this.checkSession(sessionId)
    }
  }

  /**
   * Check a single session for stall
   */
  private async checkSession(sessionId: string) {
    const lastActivity = sessionLauncher.getLastActivity(sessionId)

    if (!lastActivity) {
      console.warn(`⚠️  No last activity recorded for session ${sessionId}`)
      return
    }

    const now = new Date()
    const timeSinceActivity = (now.getTime() - lastActivity.getTime()) / 1000 // seconds

    // Check if stalled
    if (timeSinceActivity > this.config.stallDetectionSeconds) {
      console.warn(`⚠️  Session ${sessionId} appears stalled (${Math.round(timeSinceActivity)}s since activity)`)

      await this.handleStall(sessionId, timeSinceActivity)
    }
  }

  /**
   * Handle stalled session
   */
  private async handleStall(sessionId: string, stallDuration: number) {
    // Update session status to stalled
    await pool.query(`
      UPDATE sessions
      SET status = 'stalled', updated_at = NOW()
      WHERE id = $1
    `, [sessionId])

    // Check retry count
    const retries = this.retryCount.get(sessionId) || 0

    this.emit('session:stalled', {
      sessionId,
      stallDuration,
      retries,
      maxRetries: this.config.maxRetries
    })

    if (retries >= this.config.maxRetries) {
      console.error(`❌ Session ${sessionId} exceeded max retries (${this.config.maxRetries}), giving up`)

      // Mark as failed
      await pool.query(`
        UPDATE sessions
        SET status = 'failed', error = 'Exceeded max restart attempts', completed_at = NOW()
        WHERE id = $1
      `, [sessionId])

      // Stop the session
      try {
        await sessionLauncher.stop(sessionId)
      } catch (error) {
        console.error(`Error stopping failed session ${sessionId}:`, error)
      }

      // Clean up retry count
      this.retryCount.delete(sessionId)

      this.emit('session:failed', { sessionId, reason: 'max_retries_exceeded' })

      return
    }

    // Attempt auto-restart
    console.log(`🔄 Auto-restarting stalled session ${sessionId} (attempt ${retries + 1}/${this.config.maxRetries})`)

    try {
      const newSessionId = await sessionLauncher.restart(sessionId)

      // Increment retry count for new session
      this.retryCount.set(newSessionId, retries + 1)

      // Remove old session retry count
      this.retryCount.delete(sessionId)

      console.log(`✅ Session restarted: ${sessionId} → ${newSessionId}`)

      this.emit('session:restarted', {
        oldSessionId: sessionId,
        newSessionId,
        attempt: retries + 1
      })
    } catch (error) {
      console.error(`❌ Failed to restart session ${sessionId}:`, error)

      this.emit('session:restart_failed', {
        sessionId,
        error: (error as Error).message
      })
    }
  }

  /**
   * Reset retry count for a session (call when session completes successfully)
   */
  resetRetryCount(sessionId: string) {
    this.retryCount.delete(sessionId)
  }

  /**
   * Get retry count for a session
   */
  getRetryCount(sessionId: string): number {
    return this.retryCount.get(sessionId) || 0
  }

  /**
   * Get monitor statistics
   */
  getStats() {
    return {
      isRunning: this.isRunning,
      activeSessions: sessionLauncher.getActiveSessions().length,
      sessionsWithRetries: this.retryCount.size,
      config: this.config
    }
  }

  /**
   * Update monitor configuration
   */
  updateConfig(config: Partial<MonitorConfig>) {
    this.config = { ...this.config, ...config }
    console.log('📝 SessionMonitor config updated:', this.config)
    this.emit('monitor:config_updated', this.config)
  }
}

// Singleton instance
export const sessionMonitor = new SessionMonitor()

// Listen to session launcher events
sessionLauncher.on('session:exit', ({ sessionId, status }) => {
  if (status === 'completed') {
    // Reset retry count on successful completion
    sessionMonitor.resetRetryCount(sessionId)
  }
})
