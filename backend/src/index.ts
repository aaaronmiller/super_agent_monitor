import express from 'express'
import cors from 'cors'
import { Pool } from 'pg'
import dotenv from 'dotenv'
import { createServer } from 'http'
import { componentsRouter } from './routes/components'
import { workflowsRouter } from './routes/workflows'
import { sessionsRouter } from './routes/sessions'
import { sessionControlRouter } from './routes/session-control'
import { memoryRouter } from './routes/memory'
import { analyticsRouter } from './routes/analytics'
import { schedulerRouter } from './routes/scheduler'
import { plansRouter } from './routes/plans'
import { converterRouter } from './routes/converter'
import localModelsRouter from './routes/localModels'
import { webSocketService } from './services/WebSocketService'
import { sessionMonitor } from './services/SessionMonitor'
import { sessionLauncher } from './services/SessionLauncher'
import { schedulerService } from './services/SchedulerService'

dotenv.config()

const app = express()
const PORT = process.env.PORT || 3001

import { pool } from './db/pool'

// Export pool for other modules
export { pool }

// Middleware
app.use(cors())
app.use(express.json())

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() })
})

// System Status Check
app.get('/api/system/status', async (req, res) => {
  const { systemCheckService } = await import('./services/SystemCheckService')
  const status = await systemCheckService.runAllChecks()
  res.json(status)
})

// API routes
app.use('/api/components', componentsRouter)
app.use('/api/workflows', workflowsRouter)
app.use('/api/sessions', sessionsRouter)
app.use('/api/sessions', sessionControlRouter)
app.use('/api/memory', memoryRouter)
app.use('/api/analytics', analyticsRouter)
app.use('/api/scheduler', schedulerRouter)
app.use('/api/plans', plansRouter)
app.use('/api/converter', converterRouter)
app.use('/api/local-models', localModelsRouter)

// Error handling
app.use((err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.error('Error:', err)

  if (process.env.NODE_ENV === 'production') {
    res.status(err.status || 500).json({
      error: {
        code: err.code || 'INTERNAL_ERROR',
        message: 'An error occurred'
      }
    })
  } else {
    res.status(err.status || 500).json({
      error: {
        code: err.code || 'INTERNAL_ERROR',
        message: err.message,
        stack: err.stack
      }
    })
  }
})

// Start server
async function start() {
  try {
    // Test database connection
    await pool.query('SELECT NOW()')
    console.log('✅ Database connected')

    // Initialize component registry (scan components directory)
    const { componentRegistry } = await import('./services/ComponentRegistry')
    await componentRegistry.scan()
    console.log('✅ Component registry initialized')

    // Initialize Scheduler
    await schedulerService.init()
    console.log('✅ Scheduler initialized')

    // Create HTTP server
    const server = createServer(app)

    // Initialize WebSocket server
    webSocketService.initialize(server)
    console.log('✅ WebSocket service initialized')

    // Start session monitor
    sessionMonitor.start()
    console.log('✅ Session monitor started')

    // Start HTTP server
    server.listen(PORT, () => {
      console.log(`✅ Server running on http://localhost:${PORT}`)
      console.log(`📚 API: http://localhost:${PORT}/api`)
      console.log(`🏥 Health: http://localhost:${PORT}/health`)
      console.log(`🔌 WebSocket: ws://localhost:${PORT}/ws`)
      console.log('')
      console.log('🎯 Ready to serve workflows and manage sessions')
    })

    // Graceful shutdown
    const shutdown = async () => {
      console.log('\n🛑 Shutting down gracefully...')

      // Stop accepting new connections
      server.close(() => {
        console.log('✅ HTTP server closed')
      })

      // Stop session monitor
      sessionMonitor.stop()
      console.log('✅ Session monitor stopped')

      // Stop all active sessions
      const activeSessions = sessionLauncher.getActiveSessions()
      console.log(`🛑 Stopping ${activeSessions.length} active sessions...`)
      for (const sessionId of activeSessions) {
        try {
          await sessionLauncher.stop(sessionId)
        } catch (error) {
          console.error(`Error stopping session ${sessionId}:`, error)
        }
      }

      // Shutdown WebSocket server
      webSocketService.shutdown()
      console.log('✅ WebSocket service shut down')

      // Close database pool
      await pool.end()
      console.log('✅ Database pool closed')

      console.log('👋 Shutdown complete')
      process.exit(0)
    }

    process.on('SIGTERM', shutdown)
    process.on('SIGINT', shutdown)

  } catch (error) {
    console.error('❌ Failed to start server:', error)
    process.exit(1)
  }
}

start()
