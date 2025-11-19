import express from 'express'
import cors from 'cors'
import { Pool } from 'pg'
import dotenv from 'dotenv'
import { componentsRouter } from './routes/components'
import { workflowsRouter } from './routes/workflows'
import { sessionsRouter } from './routes/sessions'

dotenv.config()

const app = express()
const PORT = process.env.PORT || 3001

// Database connection pool
export const pool = new Pool({
  connectionString: process.env.DATABASE_URL || 'postgresql://postgres:postgres@localhost:5432/super_agent_monitor'
})

// Middleware
app.use(cors())
app.use(express.json())

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() })
})

// API routes
app.use('/api/components', componentsRouter)
app.use('/api/workflows', workflowsRouter)
app.use('/api/sessions', sessionsRouter)

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

    app.listen(PORT, () => {
      console.log(`✅ Server running on http://localhost:${PORT}`)
      console.log(`📚 API: http://localhost:${PORT}/api`)
      console.log(`🏥 Health: http://localhost:${PORT}/health`)
      console.log('')
      console.log('🎯 Ready to serve workflows and components')
    })
  } catch (error) {
    console.error('❌ Failed to start server:', error)
    process.exit(1)
  }
}

start()
