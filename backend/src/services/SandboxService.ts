import { Sandbox } from '@e2b/code-interpreter'
import dotenv from 'dotenv'

dotenv.config()

export interface SandboxResult {
    stdout: string
    stderr: string
    error?: string
}

export class SandboxService {
    private apiKey: string

    constructor() {
        this.apiKey = process.env.E2B_API_KEY || ''
        if (!this.apiKey) {
            console.warn('⚠️ E2B_API_KEY is not set. Sandbox features will not work.')
        }
    }

    /**
     * Run a command in an E2B sandbox
     */
    async runCommand(command: string, cwd: string = '/home/user'): Promise<SandboxResult> {
        if (!this.apiKey) {
            throw new Error('E2B_API_KEY is not configured')
        }

        let sandbox: Sandbox | null = null

        try {
            console.log('Creating E2B sandbox...')
            sandbox = await Sandbox.create({ apiKey: this.apiKey })

            console.log(`Running command in sandbox: ${command}`)
            // Cast to any to access properties that might be missing in type definition but present in runtime
            const sbx = sandbox as any

            const result = await sbx.commands.run(command, { cwd })

            return {
                stdout: result.stdout,
                stderr: result.stderr,
            }
        } catch (error: any) {
            console.error('Sandbox execution failed:', error)
            return {
                stdout: '',
                stderr: error.message || String(error),
                error: error.message
            }
        } finally {
            if (sandbox) {
                console.log('Killing sandbox...')
                await sandbox.kill()
            }
        }
    }

    /**
     * Run a script file in the sandbox
     */
    async runScript(scriptContent: string, scriptName: string = 'script.py'): Promise<SandboxResult> {
        if (!this.apiKey) {
            throw new Error('E2B_API_KEY is not configured')
        }

        let sandbox: Sandbox | null = null

        try {
            console.log('Creating E2B sandbox...')
            sandbox = await Sandbox.create({ apiKey: this.apiKey })
            const sbx = sandbox as any

            // Write script to file
            await sbx.files.write(scriptName, scriptContent)

            // Run script
            const cmd = scriptName.endsWith('.py') ? `python3 ${scriptName}` : `bash ${scriptName}`
            console.log(`Running script: ${cmd}`)

            const result = await sbx.commands.run(cmd)

            return {
                stdout: result.stdout,
                stderr: result.stderr,
            }
        } catch (error: any) {
            console.error('Sandbox execution failed:', error)
            return {
                stdout: '',
                stderr: error.message || String(error),
                error: error.message
            }
        } finally {
            if (sandbox) {
                await sandbox.kill()
            }
        }
    }
}

export const sandboxService = new SandboxService()
