import { Pool } from 'pg'
import dotenv from 'dotenv'

dotenv.config()

// Database connection pool
export const pool = new Pool({
    connectionString: process.env.DATABASE_URL || 'postgresql://postgres:postgres@localhost:5432/super_agent_monitor'
})
