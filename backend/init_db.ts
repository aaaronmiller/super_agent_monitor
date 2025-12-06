import { Pool } from 'pg'
import fs from 'fs/promises'
import path from 'path'
import dotenv from 'dotenv'

dotenv.config()

const pool = new Pool({
    connectionString: process.env.DATABASE_URL || 'postgresql://postgres:postgres@localhost:5432/super_agent_monitor'
})

async function initDb() {
    try {
        const schemaPath = path.join(__dirname, 'src/db/schema.sql')
        const schema = await fs.readFile(schemaPath, 'utf-8')

        console.log('Applying schema...')
        await pool.query(schema)
        console.log('✅ Schema applied successfully')
    } catch (error) {
        console.error('❌ Failed to apply schema:', error)
    } finally {
        await pool.end()
    }
}

initDb()
