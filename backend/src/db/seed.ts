import { pool } from './pool'
import { v4 as uuidv4 } from 'uuid'

async function seed() {
    console.log('🌱 Seeding database...')

    try {
        // 1. Create "Hello World" Workflow Template
        const helloWorldId = '00000000-0000-0000-0000-000000000001'

        // Check if exists
        const check = await pool.query('SELECT id FROM workflows WHERE id = $1', [helloWorldId])

        if (check.rowCount === 0) {
            await pool.query(`
        INSERT INTO workflows (id, name, description, definition, is_template)
        VALUES ($1, $2, $3, $4, $5)
      `, [
                helloWorldId,
                'Hello World Agent',
                'A simple starter agent to verify your setup.',
                {
                    model: 'claude-3-5-sonnet-20241022',
                    temperature: 0.7,
                    maxTokens: 1024,
                    systemPrompt: 'You are a helpful assistant. Say "Hello World" and explain what you can do.',
                    tools: []
                },
                true
            ])
            console.log('✅ Created "Hello World" template')
        } else {
            console.log('ℹ️ "Hello World" template already exists')
        }

        // 2. Create "Research Assistant" Template
        const researchId = '00000000-0000-0000-0000-000000000002'
        const checkResearch = await pool.query('SELECT id FROM workflows WHERE id = $1', [researchId])

        if (checkResearch.rowCount === 0) {
            await pool.query(`
        INSERT INTO workflows (id, name, description, definition, is_template)
        VALUES ($1, $2, $3, $4, $5)
      `, [
                researchId,
                'Research Assistant',
                'An agent capable of searching the web and summarizing findings.',
                {
                    model: 'claude-3-5-sonnet-20241022',
                    temperature: 0.5,
                    maxTokens: 4096,
                    systemPrompt: 'You are a research assistant. Use the available tools to search for information and provide comprehensive summaries.',
                    tools: ['search_web', 'read_url_content']
                },
                true
            ])
            console.log('✅ Created "Research Assistant" template')
        } else {
            console.log('ℹ️ "Research Assistant" template already exists')
        }

        // 3. Create "Grok Test" Template
        const grokId = '00000000-0000-0000-0000-000000000003'
        const checkGrok = await pool.query('SELECT id FROM workflows WHERE id = $1', [grokId])

        if (checkGrok.rowCount === 0) {
            await pool.query(`
        INSERT INTO workflows (id, name, description, definition, is_template)
        VALUES ($1, $2, $3, $4, $5)
      `, [
                grokId,
                'Grok Test Agent',
                'A test agent using the free Grok model via OpenRouter.',
                {
                    model: 'free grok 4.1 fast:free',
                    temperature: 0.7,
                    maxTokens: 4096,
                    systemPrompt: 'You are a helpful assistant powered by Grok.',
                    tools: []
                },
                true
            ])
            console.log('✅ Created "Grok Test" template')
        } else {
            console.log('ℹ️ "Grok Test" template already exists')
        }

        console.log('✨ Seeding complete!')
    } catch (error) {
        console.error('❌ Seeding failed:', error)
        process.exit(1)
    } finally {
        await pool.end()
    }
}

seed()
