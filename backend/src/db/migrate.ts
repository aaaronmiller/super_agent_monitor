#!/usr/bin/env bun
import { Pool } from 'pg'
import { readdir, readFile } from 'fs/promises'
import path from 'path'
import dotenv from 'dotenv'

dotenv.config()

const pool = new Pool({
  connectionString: process.env.DATABASE_URL || 'postgresql://postgres:postgres@localhost:5432/super_agent_monitor'
})

interface Migration {
  id: number
  filename: string
  applied_at: Date
}

/**
 * Create migrations tracking table
 */
async function createMigrationsTable() {
  await pool.query(`
    CREATE TABLE IF NOT EXISTS schema_migrations (
      id SERIAL PRIMARY KEY,
      filename VARCHAR(255) UNIQUE NOT NULL,
      applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    )
  `)
  console.log('✅ Migrations table ready')
}

/**
 * Get applied migrations
 */
async function getAppliedMigrations(): Promise<Set<string>> {
  const result = await pool.query<Migration>(
    'SELECT filename FROM schema_migrations ORDER BY id'
  )
  return new Set(result.rows.map(row => row.filename))
}

/**
 * Get pending migration files
 */
async function getPendingMigrations(appliedMigrations: Set<string>): Promise<string[]> {
  const migrationsDir = path.join(__dirname, '../../database/migrations')

  try {
    const files = await readdir(migrationsDir)
    const sqlFiles = files
      .filter(file => file.endsWith('.sql'))
      .sort() // Sort to ensure migrations run in order

    return sqlFiles.filter(file => !appliedMigrations.has(file))
  } catch (error: any) {
    if (error.code === 'ENOENT') {
      console.log('ℹ️  No migrations directory found')
      return []
    }
    throw error
  }
}

/**
 * Apply a single migration
 */
async function applyMigration(filename: string): Promise<void> {
  const migrationsDir = path.join(__dirname, '../../database/migrations')
  const filePath = path.join(migrationsDir, filename)

  console.log(`\n📄 Applying migration: ${filename}`)

  const sql = await readFile(filePath, 'utf-8')

  // Begin transaction
  const client = await pool.connect()

  try {
    await client.query('BEGIN')

    // Execute migration SQL
    await client.query(sql)

    // Record migration
    await client.query(
      'INSERT INTO schema_migrations (filename) VALUES ($1)',
      [filename]
    )

    await client.query('COMMIT')

    console.log(`   ✅ Applied: ${filename}`)
  } catch (error) {
    await client.query('ROLLBACK')
    console.error(`   ❌ Failed: ${filename}`)
    throw error
  } finally {
    client.release()
  }
}

/**
 * Rollback last migration
 */
async function rollbackMigration(): Promise<void> {
  const result = await pool.query<Migration>(
    'SELECT filename FROM schema_migrations ORDER BY id DESC LIMIT 1'
  )

  if (result.rows.length === 0) {
    console.log('ℹ️  No migrations to rollback')
    return
  }

  const filename = result.rows[0].filename
  console.log(`\n⏪ Rolling back migration: ${filename}`)

  // Check for rollback file (e.g., 001_initial.rollback.sql)
  const rollbackFilename = filename.replace('.sql', '.rollback.sql')
  const migrationsDir = path.join(__dirname, '../../database/migrations')
  const rollbackPath = path.join(migrationsDir, rollbackFilename)

  const client = await pool.connect()

  try {
    await client.query('BEGIN')

    // Try to execute rollback SQL if it exists
    try {
      const rollbackSql = await readFile(rollbackPath, 'utf-8')
      await client.query(rollbackSql)
      console.log(`   ✅ Executed rollback SQL`)
    } catch (error: any) {
      if (error.code === 'ENOENT') {
        console.log(`   ⚠️  No rollback file found (${rollbackFilename})`)
        console.log(`   ⚠️  Manual rollback may be required`)
      } else {
        throw error
      }
    }

    // Remove from migrations table
    await client.query(
      'DELETE FROM schema_migrations WHERE filename = $1',
      [filename]
    )

    await client.query('COMMIT')

    console.log(`   ✅ Rolled back: ${filename}`)
  } catch (error) {
    await client.query('ROLLBACK')
    console.error(`   ❌ Rollback failed: ${filename}`)
    throw error
  } finally {
    client.release()
  }
}

/**
 * Show migration status
 */
async function showStatus(): Promise<void> {
  const appliedMigrations = await getAppliedMigrations()
  const pendingMigrations = await getPendingMigrations(appliedMigrations)

  console.log('\n📊 Migration Status\n')

  if (appliedMigrations.size === 0) {
    console.log('   No migrations applied yet')
  } else {
    console.log(`   ✅ Applied (${appliedMigrations.size}):`)
    Array.from(appliedMigrations).forEach(filename => {
      console.log(`      - ${filename}`)
    })
  }

  if (pendingMigrations.length === 0) {
    console.log('\n   🎉 Database is up to date!')
  } else {
    console.log(`\n   ⏳ Pending (${pendingMigrations.length}):`)
    pendingMigrations.forEach(filename => {
      console.log(`      - ${filename}`)
    })
  }

  console.log('')
}

/**
 * Run all pending migrations
 */
async function migrate(): Promise<void> {
  console.log('🚀 Starting database migration...\n')

  try {
    // Test database connection
    await pool.query('SELECT NOW()')
    console.log('✅ Database connected')

    // Create migrations table if it doesn't exist
    await createMigrationsTable()

    // Get migrations to apply
    const appliedMigrations = await getAppliedMigrations()
    const pendingMigrations = await getPendingMigrations(appliedMigrations)

    if (pendingMigrations.length === 0) {
      console.log('\n✨ No pending migrations. Database is up to date!')
      return
    }

    console.log(`\nFound ${pendingMigrations.length} pending migration(s)`)

    // Apply each migration
    for (const filename of pendingMigrations) {
      await applyMigration(filename)
    }

    console.log(`\n✨ Successfully applied ${pendingMigrations.length} migration(s)!`)
  } catch (error) {
    console.error('\n❌ Migration failed:', error)
    throw error
  }
}

/**
 * Main function
 */
async function main() {
  const command = process.argv[2]

  try {
    switch (command) {
      case 'up':
      case undefined:
        await migrate()
        break

      case 'rollback':
        await rollbackMigration()
        break

      case 'status':
        await showStatus()
        break

      default:
        console.log('Usage:')
        console.log('  bun run db:migrate [command]')
        console.log('')
        console.log('Commands:')
        console.log('  up (default)  - Run pending migrations')
        console.log('  rollback      - Rollback last migration')
        console.log('  status        - Show migration status')
        process.exit(1)
    }
  } catch (error) {
    console.error('Error:', error)
    process.exit(1)
  } finally {
    await pool.end()
  }
}

main()
