#!/usr/bin/env bun
/**
 * Ironclad System Startup Script - Full Integration
 *
 * This script starts both the Archivist (Phase 2) and optionally prepares
 * for Smart Nudge (Phase 3). It integrates with your existing SAM server.
 *
 * Usage: bun run ironclad-start.ts
 *
 * This can be run:
 * 1. Alongside your existing backend server (as separate process)
 * 2. Integrated into your main server startup
 * 3. As a standalone watcher for development
 */

import { archivist } from './backend/src/services/Archivist'
import { WebSocketService } from './backend/src/services/WebSocketService'
import { smartNudge } from './backend/src/services/SmartNudge'
import { createServer } from 'http'

// Optional: Import your existing server to piggyback on WebSocket
// import { server as existingServer } from './backend/src/server'

async function startIronclad(mode: 'standalone' | 'integrated' | 'demo' = 'standalone') {
  console.log('🔮 Starting Ironclad Hybrid System...')
  console.log('=====================================')

  if (mode === 'integrated') {
    // Integration Mode: Add to existing SAM server
    console.log('📝 Running in INTEGRATED mode')

    console.log(`
    📋 INTEGRATION STEPS FOR YOUR MAIN SERVER:

    1. In backend/src/server.ts, add:
       ──────────────────────────────────────
       import { archivist } from './services/Archivist'
       import { smartNudge } from './services/SmartNudge'

       // After: webSocketService.initialize(server)
       archivist.start(webSocketService)

       // Add to SessionMonitor event listeners:
       sessionMonitor.on('session:stalled', async (data) => {
         if (data.stallDuration > 45000) {
           const nudge = await smartNudge.generateApiPayload(data.sessionId)
           webSocketService.broadcast(nudge)
         }
       })

    2. In backend/src/services/SessionLauncher.ts, apply BeadLauncherPatch.ts

    3. Restart your SAM server
    ──────────────────────────────────────
    `)

  } else if (mode === 'demo') {
    // Demo Mode: Minimal setup with test events
    console.log('🧪 Running in DEMO mode (test data)')

    const server = createServer()
    const wsService = new WebSocketService()
    wsService.initialize(server)

    await archivist.start(wsService)
    const PORT = process.env.IRONCLAD_PORT || '3001'
    server.listen(PORT)

    console.log(`🚀 Demo running: http://localhost:${PORT}/ws`)
    console.log('📝 Generating test beads in 3 seconds...')

    // Generate test beads
    setTimeout(async () => {
      const { beadFactory } = await import('./backend/src/services/BeadFactory')
      await beadFactory.initialize()

      // Test bead 1: Error
      const errorBead = await beadFactory.create(
        { type: 'error', data: { error: 'npm install failed: ENOENT' } },
        { sessionId: 'demo-agent', workflowId: 'test' }
      )

      // Test bead 2: Tool use
      const toolBead = await beadFactory.create(
        { type: 'tool_use', data: { tool: 'run_command', input: 'ls', output: 'file1\nfile2' } },
        { sessionId: 'demo-agent', workflowId: 'test' }
      )

      console.log('✅ Test beads created:', {
        error: errorBead?.id.slice(0, 8),
        tool: toolBead?.id.slice(0, 8)
      })

      // Test smart nudge
      const { smartNudge } = await import('./backend/src/services/SmartNudge')
      const nudge = await smartNudge.generate('demo-agent')
      console.log('🎯 Smart Nudge (demo):', nudge.nudge)

      // Broadcast via WebSocket
      wsService.broadcast({
        type: 'DEMO_COMPLETE',
        data: { beads: 2, nudge: nudge.nudge },
        timestamp: new Date().toISOString()
      })

      console.log('\n🎉 Demo complete! Check .beads/ directory')
      console.log('🛑 Ctrl+C to stop')
    }, 3000)

  } else {
    // Standalone Mode: Run Archivist as separate service
    console.log('🚀 Running in STANDALONE mode (production)')

    const server = createServer()
    const wsService = new WebSocketService()
    wsService.initialize(server)

    await archivist.start(wsService)

    const PORT = process.env.IRONCLAD_PORT || '3001'
    server.listen(PORT, () => {
      console.log(`📊 Ironclad Archivist: http://localhost:${PORT}/ws`)
      console.log('📝 Listening for .beads/ directory changes')
    })

    process.on('SIGINT', async () => {
      console.log('\n🛑 Shutting down Ironclad...')
      await archivist.stop()
      server.close()
      process.exit(0)
    })
  }

  // Show architecture diagram
  console.log('\n🏗️  ARCHITECTURE')
  console.log('================')
  console.log('Agent → BeadFactory (.beads/) → Archivist → Vector DB → SmartNudge')
  console.log('          ↑                    ↓')
  console.log('          └── Git (immutable) ─┘')

  console.log('\n📋 QUICK START')
  console.log('==============')
  console.log('1. Apply: bun run bead-init.ts')
  console.log('2. Patch: backend/src/services/SessionLauncher.ts')
  console.log('3. Start: bun run ironclad-start.ts --integrated')
  console.log('4. Test: Launch any agent, watch .beads/ populate')
}

// CLI usage
if (import.meta.main) {
  const args = process.argv.slice(2)
  let mode: 'standalone' | 'integrated' | 'demo' = 'standalone'

  if (args.includes('--integrated')) mode = 'integrated'
  else if (args.includes('--demo')) mode = 'demo'
  // default is standalone

  startIronclad(mode).catch(console.error)
}

export { startIronclad }