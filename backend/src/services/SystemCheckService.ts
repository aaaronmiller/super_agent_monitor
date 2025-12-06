import { exec } from 'child_process'
import util from 'util'
import { pool } from '../db/pool'
import fs from 'fs/promises'
import path from 'path'
import os from 'os'

import { proxyService } from './ProxyService'

const execAsync = util.promisify(exec)

export interface SystemStatus {
    database: { status: 'ok' | 'error'; message?: string }
    claudeAuth: { status: 'ok' | 'error'; message?: string }
    environment: { status: 'ok' | 'error'; message?: string }
    proxy: { status: 'ok' | 'error'; message?: string }
    timestamp: string
}

export class SystemCheckService {

    /**
     * Run all system checks
     */
    async runAllChecks(): Promise<SystemStatus> {
        const [database, claudeAuth, environment, proxy] = await Promise.all([
            this.checkDatabase(),
            this.checkClaudeAuth(),
            this.checkEnvironment(),
            this.checkProxy()
        ])

        return {
            database,
            claudeAuth,
            environment,
            proxy,
            timestamp: new Date().toISOString()
        }
    }

    /**
     * Check Proxy Status
     */
    private async checkProxy() {
        const port = proxyService.getPort()
        if (port > 0) {
            return { status: 'ok' as const, message: `Active on port ${port}` }
        }
        return { status: 'error' as const, message: 'Proxy not running' }
    }

    /**
     * Check Database Connection and Extensions
     */
    private async checkDatabase() {
        try {
            // Check connection
            await pool.query('SELECT 1')

            // Check pgvector extension
            const res = await pool.query("SELECT * FROM pg_extension WHERE extname = 'vector'")
            if (res.rows.length === 0) {
                return { status: 'error' as const, message: 'pgvector extension not installed' }
            }

            return { status: 'ok' as const }
        } catch (error) {
            return { status: 'error' as const, message: (error as Error).message }
        }
    }

    /**
     * Check Claude CLI Authentication
     */
    private async checkClaudeAuth() {
        try {
            // 1. Check if claude is in PATH
            try {
                await execAsync('which claude')
            } catch {
                return { status: 'error' as const, message: 'Claude CLI not found in PATH' }
            }

            // 2. Check session file existence (Fast check)
            const homeDir = os.homedir()
            const sessionPath = path.join(homeDir, '.anthropic', 'session.json')
            try {
                await fs.access(sessionPath)
                return { status: 'ok' as const }
            } catch {
                // Fallback: Try running a command (Slow check)
                // We use a timeout to prevent hanging
                try {
                    await new Promise((resolve, reject) => {
                        exec('claude auth token', { timeout: 5000 }, (error, stdout) => {
                            if (error) reject(error)
                            else resolve(stdout)
                        })
                    })
                    return { status: 'ok' as const }
                } catch (error) {
                    return { status: 'error' as const, message: 'Claude CLI not authenticated' }
                }
            }
        } catch (error) {
            return { status: 'error' as const, message: (error as Error).message }
        }
    }

    /**
     * Check Environment Variables
     */
    private async checkEnvironment() {
        const missing: string[] = []

        if (!process.env.OPENAI_API_KEY) missing.push('OPENAI_API_KEY')
        if (!process.env.E2B_API_KEY) missing.push('E2B_API_KEY')

        if (missing.length > 0) {
            return { status: 'error' as const, message: `Missing keys: ${missing.join(', ')}` }
        }

        return { status: 'ok' as const }
    }
}

export const systemCheckService = new SystemCheckService()
