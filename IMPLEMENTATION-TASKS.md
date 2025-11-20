# **Super Agent Monitor: Detailed Implementation Tasks**

**Status**: Ready for Development
**Timeline**: 18 Weeks (MVP)
**Last Updated**: 2025-11-19

---

## 📋 Task Organization

Tasks are organized by:
- **Phase** (0-6)
- **Priority** (P0=Critical, P1=High, P2=Medium)
- **Dependencies** (must complete X before Y)
- **Estimated Hours**
- **Specific Files** to create/modify

---

# PHASE 0: Foundation & Setup (Weeks 1-2)

## Task 0.1: Repository & Git Submodules **[P0]**
**Estimated**: 4 hours
**Dependencies**: None

### Subtasks:
- [ ] **0.1.1** Initialize git repository structure
  ```bash
  mkdir -p frontend/src/{components,views,stores}
  mkdir -p backend/src/{api,services,db}
  mkdir -p external
  mkdir -p components/{agents,skills,hooks,scripts,orchestrators,subagents}
  mkdir -p workflows
  mkdir -p docs
  ```

- [ ] **0.1.2** Add multi-agent-workflow as git submodule
  ```bash
  git submodule add https://github.com/apolopena/multi-agent-workflow.git external/multi-agent-workflow
  git submodule update --init --recursive
  ```

- [ ] **0.1.3** Create `.gitignore`
  ```
  # File: .gitignore
  node_modules/
  .super_agent_monitor/
  .env
  .env.local
  *.log
  dist/
  build/
  .DS_Store
  ```

- [ ] **0.1.4** Create `README.md` with quick start guide
  ```markdown
  # Super Agent Monitor

  Autonomous multi-agent workflow management platform.

  ## Quick Start
  1. Install dependencies: `npm install`
  2. Set up database: `npm run db:migrate`
  3. Start dev server: `npm run dev`
  ```

---

## Task 0.2: Database Setup **[P0]**
**Estimated**: 6 hours
**Dependencies**: None

### Subtasks:
- [ ] **0.2.1** Create database schema file
  - **File**: `backend/src/db/schema.sql`
  - **Content**: All tables from PRD (workflows, sessions, components, memories)
  - **Include**: Indexes, extensions (pgvector), foreign keys

- [ ] **0.2.2** Create migration scripts
  - **File**: `backend/src/db/migrations/001_initial.sql`
  - **Tool**: Consider using Drizzle ORM or Knex.js

- [ ] **0.2.3** Set up database connection
  - **File**: `backend/src/db/client.ts`
  ```typescript
  import { Pool } from 'pg'

  export const db = new Pool({
    connectionString: process.env.DATABASE_URL,
    max: 20
  })

  export async function query(text: string, params?: any[]) {
    const result = await db.query(text, params)
    return result
  }
  ```

- [ ] **0.2.4** Create seed data script
  - **File**: `backend/src/db/seeds/components.ts`
  - **Action**: Insert 5 example components per category

- [ ] **0.2.5** Write database helper functions
  - **File**: `backend/src/db/helpers.ts`
  - **Functions**: `insertWorkflow()`, `getSession()`, `searchMemories()`

---

## Task 0.3: Component Library Seed **[P0]**
**Estimated**: 12 hours
**Dependencies**: None

### Subtasks:
- [ ] **0.3.1** Create 5 example agents
  - **Files**:
    - `components/agents/researcher-primary.md`
    - `components/agents/web-scraper.md`
    - `components/agents/code-reviewer.md`
    - `components/agents/tester.md`
    - `components/agents/analyzer.md`
  - **Format**: Markdown with YAML frontmatter (see PRD example)

- [ ] **0.3.2** Create 5 example skills
  - **Files**:
    - `components/skills/web-search-advanced/SKILL.md`
    - `components/skills/api-design/SKILL.md`
    - `components/skills/db-optimization/SKILL.md`
    - `components/skills/security-audit/SKILL.md`
    - `components/skills/testing-patterns/SKILL.md`
  - **Structure**: Each skill in subfolder with SKILL.md + scripts/

- [ ] **0.3.3** Create 5 example hooks
  - **Files**:
    - `components/hooks/cost-tracker.py`
    - `components/hooks/stall-detector.py`
    - `components/hooks/format-enforcer.sh`
    - `components/hooks/permission-gate.py`
    - `components/hooks/session-logger.py`

- [ ] **0.3.4** Create 5 example scripts
  - **Files**:
    - `components/scripts/fetch-url.py`
    - `components/scripts/parse-pdf.py`
    - `components/scripts/extract-citations.py`
    - `components/scripts/analyze-sentiment.py`
    - `components/scripts/generate-summary.py`

- [ ] **0.3.5** Create 3 orchestrator prompts
  - **Files**:
    - `components/orchestrators/ceo-coordinator.md`
    - `components/orchestrators/research-coordinator.md`
    - `components/orchestrators/dev-coordinator.md`

- [ ] **0.3.6** Create 2 subagent prompts
  - **Files**:
    - `components/subagents/focused-coder.md`
    - `components/subagents/thorough-reviewer.md`

---

## Task 0.4: Workflow Templates **[P1]**
**Estimated**: 6 hours
**Dependencies**: 0.3

### Subtasks:
- [ ] **0.4.1** Create deep-research workflow
  - **File**: `workflows/deep-research.yaml`
  - **Components**: researcher-primary, web-scraper, citation-analyzer
  - **Pattern**: ceo-worker

- [ ] **0.4.2** Create fast-coder workflow
  - **File**: `workflows/fast-coder.yaml`
  - **Components**: code-reviewer, tester
  - **Pattern**: star

- [ ] **0.4.3** Create security-audit workflow
  - **File**: `workflows/security-audit.yaml`
  - **Components**: analyzer, security-audit skill
  - **Pattern**: round-robin

---

## Task 0.5: Development Environment **[P0]**
**Estimated**: 4 hours
**Dependencies**: None

### Subtasks:
- [ ] **0.5.1** Create Docker Compose configuration
  - **File**: `docker-compose.yml`
  ```yaml
  version: '3.8'
  services:
    postgres:
      image: postgres:16
      environment:
        POSTGRES_DB: super_agent_monitor
        POSTGRES_PASSWORD: dev_password
      ports:
        - "5432:5432"
      volumes:
        - postgres_data:/var/lib/postgresql/data

    backend:
      build: ./backend
      ports:
        - "3000:3000"
      environment:
        DATABASE_URL: postgresql://postgres:dev_password@postgres:5432/super_agent_monitor
      depends_on:
        - postgres

    frontend:
      build: ./frontend
      ports:
        - "5173:5173"
      volumes:
        - ./frontend:/app

  volumes:
    postgres_data:
  ```

- [ ] **0.5.2** Create backend package.json
  - **File**: `backend/package.json`
  ```json
  {
    "name": "super-agent-monitor-backend",
    "version": "1.0.0",
    "scripts": {
      "dev": "bun run --watch src/index.ts",
      "db:migrate": "bun run src/db/migrate.ts",
      "db:seed": "bun run src/db/seed.ts"
    },
    "dependencies": {
      "express": "^4.18.0",
      "pg": "^8.11.0",
      "pgvector": "^0.1.0",
      "cors": "^2.8.5",
      "dotenv": "^16.0.0"
    }
  }
  ```

- [ ] **0.5.3** Create frontend package.json
  - **File**: `frontend/package.json`
  ```json
  {
    "name": "super-agent-monitor-frontend",
    "version": "1.0.0",
    "scripts": {
      "dev": "vite",
      "build": "vite build"
    },
    "dependencies": {
      "vue": "^3.3.0",
      "pinia": "^2.1.0",
      "vue-router": "^4.2.0",
      "axios": "^1.4.0"
    },
    "devDependencies": {
      "@vitejs/plugin-vue": "^4.2.0",
      "typescript": "^5.0.0",
      "vite": "^4.3.0"
    }
  }
  ```

- [ ] **0.5.4** Create environment variable templates
  - **File**: `.env.example`
  ```
  DATABASE_URL=postgresql://postgres:password@localhost:5432/super_agent_monitor
  ANTHROPIC_API_KEY=sk-ant-...
  OPENAI_API_KEY=sk-...
  CLAUDE_CODE_PROXY_URL=http://localhost:8082
  ```

---

# PHASE 1: Workflow Engine (Weeks 3-5)

## Task 1.1: Workflow Schema Validator **[P0]**
**Estimated**: 8 hours
**Dependencies**: 0.2

### Subtasks:
- [ ] **1.1.1** Define TypeScript workflow interface
  - **File**: `backend/src/types/workflow.ts`
  ```typescript
  export interface Workflow {
    id: string
    name: string
    description: string
    version: string
    author: string
    tags: string[]
    orchestration: {
      pattern: 'ceo-worker' | 'star' | 'round-robin'
      model: string
      systemPrompt: string
      thinkingBudget?: number
    }
    components: {
      agents: string[]
      skills: string[]
      hooks: string[]
      scripts: string[]
    }
    memory: {
      enabled: boolean
      persistence: 'session' | 'permanent'
      rag: boolean
      retrievalK: number
    }
    lifecycle: {
      haltDetectionSeconds: number
      autoRestart: boolean
      maxRetries: number
      kickPrompt: string
    }
  }
  ```

- [ ] **1.1.2** Create validation function using Zod
  - **File**: `backend/src/validators/workflow.ts`
  ```typescript
  import { z } from 'zod'

  export const workflowSchema = z.object({
    name: z.string().min(1).max(255),
    orchestration: z.object({
      pattern: z.enum(['ceo-worker', 'star', 'round-robin']),
      model: z.string(),
      // ... full schema
    }),
    // ... rest of schema
  })

  export function validateWorkflow(data: unknown) {
    return workflowSchema.parse(data)
  }
  ```

- [ ] **1.1.3** Add validation tests
  - **File**: `backend/src/validators/__tests__/workflow.test.ts`
  ```typescript
  import { describe, test, expect } from 'bun:test'
  import { validateWorkflow } from '../workflow'

  describe('Workflow Validator', () => {
    test('validates valid workflow', () => {
      const workflow = { /* valid data */ }
      expect(() => validateWorkflow(workflow)).not.toThrow()
    })

    test('rejects invalid pattern', () => {
      const workflow = { orchestration: { pattern: 'invalid' } }
      expect(() => validateWorkflow(workflow)).toThrow()
    })
  })
  ```

---

## Task 1.2: Workflow Generator Service **[P0]**
**Estimated**: 16 hours
**Dependencies**: 1.1, 0.3

### Subtasks:
- [ ] **1.2.1** Create workflow generator class
  - **File**: `backend/src/services/workflow-generator.ts`
  ```typescript
  import { Workflow } from '../types/workflow'
  import fs from 'fs/promises'
  import path from 'path'

  export class WorkflowGenerator {
    async generate(workflow: Workflow): Promise<string> {
      const workflowId = crypto.randomUUID()
      const workflowPath = `.super_agent_monitor/workflows/${workflowId}/.claude`

      // Create directory structure
      await this.createDirectories(workflowPath)

      // Copy components
      await this.copyAgents(workflow.components.agents, workflowPath)
      await this.copySkills(workflow.components.skills, workflowPath)
      await this.copyHooks(workflow.components.hooks, workflowPath)
      await this.copyScripts(workflow.components.scripts, workflowPath)

      // Generate CLAUDE.md
      await this.generateClaudeMd(workflow, workflowPath)

      // Generate settings.json
      await this.generateSettings(workflow, workflowPath)

      return workflowId
    }

    private async createDirectories(basePath: string) {
      await fs.mkdir(path.join(basePath, 'agents'), { recursive: true })
      await fs.mkdir(path.join(basePath, 'skills'), { recursive: true })
      await fs.mkdir(path.join(basePath, 'hooks'), { recursive: true })
      await fs.mkdir(path.join(basePath, 'scripts'), { recursive: true })
    }

    private async copyAgents(agents: string[], basePath: string) {
      for (const agent of agents) {
        const src = `components/agents/${agent}.md`
        const dest = path.join(basePath, 'agents', `${agent}.md`)
        await fs.copyFile(src, dest)
      }
    }

    // ... similar methods for skills, hooks, scripts

    private async generateClaudeMd(workflow: Workflow, basePath: string) {
      const orchestratorPrompt = await fs.readFile(
        `components/orchestrators/${workflow.orchestration.systemPrompt}`,
        'utf-8'
      )

      const claudeMd = `# ${workflow.name}

${workflow.description}

## Orchestration Pattern: ${workflow.orchestration.pattern}

${orchestratorPrompt}

## Available Agents
${workflow.components.agents.map(a => `- ${a}`).join('\n')}

## Available Skills
${workflow.components.skills.map(s => `- ${s}`).join('\n')}
`

      await fs.writeFile(path.join(basePath, 'CLAUDE.md'), claudeMd)
    }
  }
  ```

- [ ] **1.2.2** Add component validation (check dependencies)
  - **Function**: `validateComponentDependencies()`
  - **Logic**: Parse component frontmatter, check if dependencies exist

- [ ] **1.2.3** Add template variable substitution
  - **Function**: `substituteVariables(content, vars)`
  - **Example**: Replace `{{PROJECT_NAME}}` with actual project name

- [ ] **1.2.4** Create workflow manifest generator
  - **File**: Generated as `.super_agent_monitor/workflows/{id}/manifest.json`
  - **Content**: Resolved component paths, timestamps, metadata

- [ ] **1.2.5** Add generation tests
  - **File**: `backend/src/services/__tests__/workflow-generator.test.ts`

---

## Task 1.3: Component Registry **[P0]**
**Estimated**: 12 hours
**Dependencies**: 0.3

### Subtasks:
- [ ] **1.3.1** Create component registry service
  - **File**: `backend/src/services/component-registry.ts`
  ```typescript
  import fs from 'fs/promises'
  import path from 'path'
  import matter from 'gray-matter'

  export interface Component {
    name: string
    displayName: string
    category: string
    description: string
    tags: string[]
    dependencies: string[]
    incompatibilities: string[]
    content: string
    metadata: Record<string, any>
  }

  export class ComponentRegistry {
    private components: Map<string, Component> = new Map()

    async scan() {
      const categories = ['agents', 'skills', 'hooks', 'scripts', 'orchestrators', 'subagents']

      for (const category of categories) {
        const dir = `components/${category}`
        await this.scanCategory(dir, category)
      }
    }

    private async scanCategory(dir: string, category: string) {
      const files = await fs.readdir(dir, { withFileTypes: true })

      for (const file of files) {
        if (file.isDirectory()) {
          // Skills are subdirectories
          const skillFile = path.join(dir, file.name, 'SKILL.md')
          if (await this.fileExists(skillFile)) {
            await this.parseComponent(skillFile, category)
          }
        } else if (file.name.endsWith('.md')) {
          await this.parseComponent(path.join(dir, file.name), category)
        }
      }
    }

    private async parseComponent(filePath: string, category: string) {
      const content = await fs.readFile(filePath, 'utf-8')
      const { data, content: body } = matter(content)

      const component: Component = {
        name: data.name || path.basename(filePath, '.md'),
        displayName: data.displayName || data.name,
        category,
        description: data.description || '',
        tags: data.tags || [],
        dependencies: data.dependencies || [],
        incompatibilities: data.incompatibilities || [],
        content: body,
        metadata: data
      }

      this.components.set(component.name, component)
    }

    getAll(): Component[] {
      return Array.from(this.components.values())
    }

    getByCategory(category: string): Component[] {
      return this.getAll().filter(c => c.category === category)
    }

    search(query: string, tags?: string[]): Component[] {
      let results = this.getAll()

      if (query) {
        const lowerQuery = query.toLowerCase()
        results = results.filter(c =>
          c.name.toLowerCase().includes(lowerQuery) ||
          c.description.toLowerCase().includes(lowerQuery)
        )
      }

      if (tags && tags.length > 0) {
        results = results.filter(c =>
          tags.some(tag => c.tags.includes(tag))
        )
      }

      return results
    }
  }
  ```

- [ ] **1.3.2** Add component metadata parser
  - **Library**: Use `gray-matter` for YAML frontmatter parsing
  - **Install**: `npm install gray-matter`

- [ ] **1.3.3** Create component compatibility checker
  - **Function**: `checkCompatibility(selectedComponents: string[])`
  - **Logic**: Check for incompatibilities, return errors if found

- [ ] **1.3.4** Add registry persistence to database
  - **Action**: After scanning, insert components into database
  - **Table**: `components` table

---

## Task 1.4: Smart Component Recommendations **[P1]**
**Estimated**: 8 hours
**Dependencies**: 1.3

### Subtasks:
- [ ] **1.4.1** Create recommendation service
  - **File**: `backend/src/services/recommendations.ts`
  ```typescript
  import { ComponentRegistry } from './component-registry'

  export class RecommendationService {
    constructor(private registry: ComponentRegistry) {}

    recommend(selectedComponents: string[]): string[] {
      const recommendations = new Set<string>()

      // 1. Add required dependencies
      for (const name of selectedComponents) {
        const component = this.registry.getAll().find(c => c.name === name)
        if (component) {
          component.dependencies.forEach(dep => recommendations.add(dep))
        }
      }

      // 2. Find common pairings
      const pairings = this.findCommonPairings(selectedComponents)
      pairings.forEach(p => recommendations.add(p))

      // 3. Balance categories (if 3 agents, suggest 2-3 skills)
      const balance = this.balanceCategories(selectedComponents)
      balance.forEach(b => recommendations.add(b))

      // Remove already selected
      selectedComponents.forEach(c => recommendations.delete(c))

      return Array.from(recommendations)
    }

    private findCommonPairings(selected: string[]): string[] {
      // TODO: Implement collaborative filtering
      // For MVP, use hardcoded common pairings
      const commonPairs: Record<string, string[]> = {
        'researcher-primary': ['web-scraper', 'citation-analyzer'],
        'code-reviewer': ['tester'],
        'web-scraper': ['parse-pdf', 'extract-citations']
      }

      const pairings: string[] = []
      for (const component of selected) {
        if (commonPairs[component]) {
          pairings.push(...commonPairs[component])
        }
      }
      return pairings
    }

    private balanceCategories(selected: string[]): string[] {
      // Count by category
      const counts: Record<string, number> = {}
      for (const name of selected) {
        const component = this.registry.getAll().find(c => c.name === name)
        if (component) {
          counts[component.category] = (counts[component.category] || 0) + 1
        }
      }

      // If 3+ agents but no skills, suggest skills
      if (counts.agents >= 3 && !counts.skills) {
        return this.registry.getByCategory('skills').slice(0, 2).map(s => s.name)
      }

      return []
    }
  }
  ```

- [ ] **1.4.2** Track usage statistics for recommendations
  - **Action**: Increment `components.usage_count` on workflow creation
  - **Use**: Recommend most popular components

---

## Task 1.5: Workflow & Component APIs **[P0]**
**Estimated**: 10 hours
**Dependencies**: 1.1, 1.2, 1.3

### Subtasks:
- [ ] **1.5.1** Create workflow API routes
  - **File**: `backend/src/api/workflows.ts`
  ```typescript
  import express from 'express'
  import { WorkflowGenerator } from '../services/workflow-generator'
  import { validateWorkflow } from '../validators/workflow'
  import { db } from '../db/client'

  const router = express.Router()
  const generator = new WorkflowGenerator()

  // POST /api/workflows - Create workflow
  router.post('/', async (req, res) => {
    try {
      const workflow = validateWorkflow(req.body)

      // Generate .claude folder
      const workflowId = await generator.generate(workflow)

      // Save to database
      await db.query(
        `INSERT INTO workflows (id, name, description, definition, version, author, tags)
         VALUES ($1, $2, $3, $4, $5, $6, $7)`,
        [workflowId, workflow.name, workflow.description, workflow, workflow.version, workflow.author, workflow.tags]
      )

      res.json({ id: workflowId, workflow })
    } catch (error) {
      res.status(400).json({ error: error.message })
    }
  })

  // GET /api/workflows - List workflows
  router.get('/', async (req, res) => {
    const { tags, template, recent } = req.query

    let query = 'SELECT * FROM workflows WHERE 1=1'
    const params: any[] = []

    if (tags) {
      query += ' AND tags && $1'
      params.push(tags.split(','))
    }

    if (template === 'true') {
      query += ' AND is_template = true'
    }

    query += ' ORDER BY last_used_at DESC NULLS LAST'

    if (recent) {
      query += ` LIMIT ${parseInt(recent as string)}`
    }

    const result = await db.query(query, params)
    res.json(result.rows)
  })

  // GET /api/workflows/:id - Get workflow
  router.get('/:id', async (req, res) => {
    const result = await db.query('SELECT * FROM workflows WHERE id = $1', [req.params.id])
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Workflow not found' })
    }
    res.json(result.rows[0])
  })

  // PUT /api/workflows/:id - Update workflow
  router.put('/:id', async (req, res) => {
    const workflow = validateWorkflow(req.body)
    await db.query(
      `UPDATE workflows SET name = $1, description = $2, definition = $3, updated_at = NOW()
       WHERE id = $4`,
      [workflow.name, workflow.description, workflow, req.params.id]
    )
    res.json({ success: true })
  })

  // DELETE /api/workflows/:id - Delete workflow
  router.delete('/:id', async (req, res) => {
    await db.query('DELETE FROM workflows WHERE id = $1', [req.params.id])
    // Also delete .claude folder
    await fs.rm(`.super_agent_monitor/workflows/${req.params.id}`, { recursive: true })
    res.json({ success: true })
  })

  export default router
  ```

- [ ] **1.5.2** Create component API routes
  - **File**: `backend/src/api/components.ts`
  ```typescript
  import express from 'express'
  import { ComponentRegistry } from '../services/component-registry'
  import { RecommendationService } from '../services/recommendations'

  const router = express.Router()
  const registry = new ComponentRegistry()
  const recommendations = new RecommendationService(registry)

  // Initialize registry on startup
  registry.scan()

  // GET /api/components - List components
  router.get('/', async (req, res) => {
    const { category, tags, q } = req.query

    let components = registry.getAll()

    if (category) {
      components = registry.getByCategory(category as string)
    }

    if (tags || q) {
      const tagArray = tags ? (tags as string).split(',') : undefined
      components = registry.search(q as string, tagArray)
    }

    res.json(components)
  })

  // GET /api/components/:id - Get component
  router.get('/:id', async (req, res) => {
    const component = registry.getAll().find(c => c.name === req.params.id)
    if (!component) {
      return res.status(404).json({ error: 'Component not found' })
    }
    res.json(component)
  })

  // GET /api/components/recommend - Get recommendations
  router.get('/recommend', async (req, res) => {
    const selected = (req.query.selected as string || '').split(',').filter(Boolean)
    const recommended = recommendations.recommend(selected)
    res.json(recommended)
  })

  // GET /api/components/validate - Check compatibility
  router.get('/validate', async (req, res) => {
    const ids = (req.query.ids as string).split(',')
    const components = ids.map(id => registry.getAll().find(c => c.name === id)).filter(Boolean)

    const errors: string[] = []
    for (const component of components) {
      for (const incompatible of component.incompatibilities) {
        if (ids.includes(incompatible)) {
          errors.push(`${component.name} is incompatible with ${incompatible}`)
        }
      }
    }

    res.json({ valid: errors.length === 0, errors })
  })

  export default router
  ```

- [ ] **1.5.3** Create main server file
  - **File**: `backend/src/index.ts`
  ```typescript
  import express from 'express'
  import cors from 'cors'
  import workflowRoutes from './api/workflows'
  import componentRoutes from './api/components'

  const app = express()

  app.use(cors())
  app.use(express.json())

  app.use('/api/workflows', workflowRoutes)
  app.use('/api/components', componentRoutes)

  const PORT = process.env.PORT || 3000
  app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`)
  })
  ```

---

## Task 1.6: Basic UI - Component Library Browser **[P1]**
**Estimated**: 12 hours
**Dependencies**: 1.5

### Subtasks:
- [ ] **1.6.1** Set up Vue 3 project structure
  - **File**: `frontend/vite.config.ts`
  - **File**: `frontend/tsconfig.json`
  - **Action**: Initialize Vite + Vue 3 + TypeScript

- [ ] **1.6.2** Create component library browser
  - **File**: `frontend/src/components/ComponentLibrary.vue`
  ```vue
  <template>
    <div class="component-library">
      <div class="filters">
        <select v-model="selectedCategory" @change="filterComponents">
          <option value="">All Categories</option>
          <option value="agents">Agents</option>
          <option value="skills">Skills</option>
          <option value="hooks">Hooks</option>
          <option value="scripts">Scripts</option>
        </select>

        <input
          v-model="searchQuery"
          @input="filterComponents"
          placeholder="Search components..."
        />
      </div>

      <div class="component-list">
        <div
          v-for="component in filteredComponents"
          :key="component.name"
          class="component-card"
          @click="selectComponent(component)"
        >
          <h3>{{ component.displayName }}</h3>
          <p>{{ component.description }}</p>
          <div class="tags">
            <span v-for="tag in component.tags" :key="tag" class="tag">
              {{ tag }}
            </span>
          </div>
        </div>
      </div>

      <div v-if="selectedComponent" class="component-detail">
        <h2>{{ selectedComponent.displayName }}</h2>
        <div class="markdown-content" v-html="renderMarkdown(selectedComponent.content)"></div>
        <button @click="addToWorkflow(selectedComponent)">Add to Workflow</button>
      </div>
    </div>
  </template>

  <script setup lang="ts">
  import { ref, computed, onMounted } from 'vue'
  import axios from 'axios'
  import { marked } from 'marked'

  interface Component {
    name: string
    displayName: string
    category: string
    description: string
    tags: string[]
    content: string
  }

  const components = ref<Component[]>([])
  const selectedCategory = ref('')
  const searchQuery = ref('')
  const selectedComponent = ref<Component | null>(null)

  const filteredComponents = computed(() => {
    let filtered = components.value

    if (selectedCategory.value) {
      filtered = filtered.filter(c => c.category === selectedCategory.value)
    }

    if (searchQuery.value) {
      const query = searchQuery.value.toLowerCase()
      filtered = filtered.filter(c =>
        c.name.toLowerCase().includes(query) ||
        c.description.toLowerCase().includes(query)
      )
    }

    return filtered
  })

  async function loadComponents() {
    const response = await axios.get('http://localhost:3000/api/components')
    components.value = response.data
  }

  function selectComponent(component: Component) {
    selectedComponent.value = component
  }

  function renderMarkdown(content: string) {
    return marked(content)
  }

  function addToWorkflow(component: Component) {
    // TODO: Emit event to parent component
    console.log('Adding to workflow:', component.name)
  }

  onMounted(() => {
    loadComponents()
  })
  </script>

  <style scoped>
  .component-library {
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 1rem;
    padding: 1rem;
  }

  .component-list {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .component-card {
    border: 1px solid #ccc;
    padding: 1rem;
    border-radius: 4px;
    cursor: pointer;
  }

  .component-card:hover {
    background: #f0f0f0;
  }

  .tags {
    display: flex;
    gap: 0.5rem;
    margin-top: 0.5rem;
  }

  .tag {
    background: #e0e0e0;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 0.875rem;
  }
  </style>
  ```

---

# PHASE 2: Session Management (Weeks 6-8)

## Task 2.1: Session Launcher **[P0]**
**Estimated**: 12 hours
**Dependencies**: 1.2

### Subtasks:
- [ ] **2.1.1** Create session manager service
  - **File**: `backend/src/services/session-manager.ts`
  ```typescript
  import { spawn, ChildProcess } from 'child_process'
  import { db } from '../db/client'

  export class SessionManager {
    private sessions: Map<string, ChildProcess> = new Map()

    async launch(workflowId: string): Promise<string> {
      const sessionId = crypto.randomUUID()

      // Configure environment
      process.env.ANTHROPIC_BASE_URL = 'http://localhost:8082'

      // Launch Claude Code in headless mode
      const claudeProcess = spawn('claude', [
        '--headless',
        `--config=.super_agent_monitor/workflows/${workflowId}/.claude`,
        `--session-id=${sessionId}`,
        '--output-format=json'
      ], {
        env: process.env,
        stdio: ['ignore', 'pipe', 'pipe']
      })

      // Store process
      this.sessions.set(sessionId, claudeProcess)

      // Create session record
      await db.query(
        `INSERT INTO sessions (id, workflow_id, status, started_at, last_activity_at)
         VALUES ($1, $2, 'running', NOW(), NOW())`,
        [sessionId, workflowId]
      )

      // Monitor stdout/stderr
      claudeProcess.stdout?.on('data', (data) => {
        console.log(`[${sessionId}] ${data}`)
      })

      claudeProcess.stderr?.on('data', (data) => {
        console.error(`[${sessionId}] ${data}`)
      })

      claudeProcess.on('exit', async (code) => {
        console.log(`Session ${sessionId} exited with code ${code}`)
        this.sessions.delete(sessionId)

        const status = code === 0 ? 'completed' : 'failed'
        await db.query(
          `UPDATE sessions SET status = $1, ended_at = NOW() WHERE id = $2`,
          [status, sessionId]
        )
      })

      return sessionId
    }

    async terminate(sessionId: string, signal: 'SIGTERM' | 'SIGKILL' = 'SIGTERM') {
      const process = this.sessions.get(sessionId)
      if (!process) {
        throw new Error(`Session ${sessionId} not found`)
      }

      process.kill(signal)

      await db.query(
        `UPDATE sessions SET status = 'terminated', ended_at = NOW() WHERE id = $1`,
        [sessionId]
      )
    }

    getProcess(sessionId: string): ChildProcess | undefined {
      return this.sessions.get(sessionId)
    }
  }
  ```

- [ ] **2.1.2** Add Claude Code installation detection
  - **Function**: `async function isClaudeInstalled(): Promise<boolean>`
  - **Logic**: Check if `claude` command exists in PATH

- [ ] **2.1.3** Create installation helper
  - **Function**: `async function installClaude(): Promise<void>`
  - **Logic**: Run `curl -fsSL https://claude.ai/install.sh | bash`

---

## Task 2.2: Stall Detection & Recovery **[P0]**
**Estimated**: 14 hours
**Dependencies**: 2.1

### Subtasks:
- [ ] **2.2.1** Create stall detector service
  - **File**: `backend/src/services/stall-detector.ts`
  ```typescript
  import { db } from '../db/client'
  import fs from 'fs/promises'

  export class StallDetector {
    private checkInterval: NodeJS.Timeout | null = null

    start() {
      // Check every 30 seconds
      this.checkInterval = setInterval(() => this.check(), 30000)
    }

    stop() {
      if (this.checkInterval) {
        clearInterval(this.checkInterval)
      }
    }

    private async check() {
      // Get all running sessions
      const result = await db.query(
        `SELECT id, workflow_id, last_activity_at FROM sessions WHERE status = 'running'`
      )

      const now = Date.now()

      for (const session of result.rows) {
        const lastActivity = new Date(session.last_activity_at).getTime()
        const inactiveSec = (now - lastActivity) / 1000

        // Check workflow's halt detection threshold
        const workflowResult = await db.query(
          `SELECT definition FROM workflows WHERE id = $1`,
          [session.workflow_id]
        )
        const workflow = workflowResult.rows[0].definition
        const threshold = workflow.lifecycle?.haltDetectionSeconds || 300

        if (inactiveSec > threshold) {
          console.log(`Session ${session.id} stalled (${inactiveSec}s inactive)`)
          await this.handleStall(session.id, workflow)
        }
      }
    }

    private async handleStall(sessionId: string, workflow: any) {
      // Update status
      await db.query(
        `UPDATE sessions SET status = 'stalled', stall_count = stall_count + 1 WHERE id = $1`,
        [sessionId]
      )

      // Get stall count
      const result = await db.query(`SELECT stall_count FROM sessions WHERE id = $1`, [sessionId])
      const stallCount = result.rows[0].stall_count

      const maxRetries = workflow.lifecycle?.maxRetries || 3

      if (stallCount > maxRetries) {
        console.log(`Session ${sessionId} exceeded max retries, marking as failed`)
        await db.query(
          `UPDATE sessions SET status = 'failed', error_message = 'Max retries exceeded' WHERE id = $1`,
          [sessionId]
        )
        return
      }

      // Attempt recovery
      const autoRestart = workflow.lifecycle?.autoRestart ?? true
      if (autoRestart) {
        await this.recover(sessionId, workflow)
      }
    }

    private async recover(sessionId: string, workflow: any) {
      console.log(`Attempting recovery for session ${sessionId}`)

      // Update status
      await db.query(`UPDATE sessions SET status = 'recovering' WHERE id = $1`, [sessionId])

      // Strategy 1: Try to inject kick prompt (if Claude Code supports it)
      const kicked = await this.tryKick(sessionId, workflow.lifecycle?.kickPrompt)

      if (kicked) {
        await db.query(
          `UPDATE sessions SET status = 'running', last_activity_at = NOW() WHERE id = $1`,
          [sessionId]
        )
        return
      }

      // Strategy 2: Graceful restart
      const restarted = await this.gracefulRestart(sessionId)

      if (restarted) {
        await db.query(
          `UPDATE sessions SET status = 'running', retry_count = retry_count + 1, last_activity_at = NOW() WHERE id = $1`,
          [sessionId]
        )
        return
      }

      // Strategy 3: Force restart
      await this.forceRestart(sessionId)
      await db.query(
        `UPDATE sessions SET status = 'running', retry_count = retry_count + 1, last_activity_at = NOW() WHERE id = $1`,
        [sessionId]
      )
    }

    private async tryKick(sessionId: string, kickPrompt?: string): Promise<boolean> {
      // TODO: Research if Claude Code supports prompt injection to running session
      // For now, return false
      return false
    }

    private async gracefulRestart(sessionId: string): Promise<boolean> {
      try {
        const sessionManager = new SessionManager()

        // Send SIGTERM
        await sessionManager.terminate(sessionId, 'SIGTERM')

        // Wait 5 seconds for graceful shutdown
        await new Promise(resolve => setTimeout(resolve, 5000))

        // Check if process exited
        const process = sessionManager.getProcess(sessionId)
        if (process) {
          // Still running, force kill
          return false
        }

        // Get workflow ID
        const result = await db.query(`SELECT workflow_id FROM sessions WHERE id = $1`, [sessionId])
        const workflowId = result.rows[0].workflow_id

        // Relaunch with same session ID (Claude Code should resume from transcript)
        // TODO: Research if we can reuse session ID
        await sessionManager.launch(workflowId)

        return true
      } catch (error) {
        console.error(`Graceful restart failed:`, error)
        return false
      }
    }

    private async forceRestart(sessionId: string): Promise<void> {
      const sessionManager = new SessionManager()

      // Send SIGKILL
      await sessionManager.terminate(sessionId, 'SIGKILL')

      // Get workflow ID
      const result = await db.query(`SELECT workflow_id FROM sessions WHERE id = $1`, [sessionId])
      const workflowId = result.rows[0].workflow_id

      // Relaunch fresh
      await sessionManager.launch(workflowId)
    }
  }
  ```

- [ ] **2.2.2** Parse claude-code-proxy logs for activity
  - **Function**: `async function getLastProxyActivity(sessionId: string): Promise<Date>`
  - **Logic**: Parse `~/.claude-proxy/requests.log`, find last request for session

- [ ] **2.2.3** Research Claude Code session resume capability
  - **Action**: Test if Claude Code can resume from transcript after restart
  - **Document**: Findings in `docs/claude-code-resume.md`

---

## Task 2.3: Session API **[P0]**
**Estimated**: 8 hours
**Dependencies**: 2.1, 2.2

### Subtasks:
- [ ] **2.3.1** Create session API routes
  - **File**: `backend/src/api/sessions.ts`
  ```typescript
  import express from 'express'
  import { SessionManager } from '../services/session-manager'
  import { db } from '../db/client'

  const router = express.Router()
  const sessionManager = new SessionManager()

  // POST /api/sessions - Create session
  router.post('/', async (req, res) => {
    const { workflowId } = req.body

    if (!workflowId) {
      return res.status(400).json({ error: 'workflowId required' })
    }

    const sessionId = await sessionManager.launch(workflowId)
    res.json({ sessionId })
  })

  // GET /api/sessions - List sessions
  router.get('/', async (req, res) => {
    const { status, workflowId } = req.query

    let query = 'SELECT * FROM sessions WHERE 1=1'
    const params: any[] = []

    if (status) {
      query += ' AND status = $' + (params.length + 1)
      params.push(status)
    }

    if (workflowId) {
      query += ' AND workflow_id = $' + (params.length + 1)
      params.push(workflowId)
    }

    query += ' ORDER BY started_at DESC'

    const result = await db.query(query, params)
    res.json(result.rows)
  })

  // GET /api/sessions/:id - Get session
  router.get('/:id', async (req, res) => {
    const result = await db.query('SELECT * FROM sessions WHERE id = $1', [req.params.id])
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Session not found' })
    }
    res.json(result.rows[0])
  })

  // POST /api/sessions/:id/kick - Inject kick prompt
  router.post('/:id/kick', async (req, res) => {
    // TODO: Implement if Claude Code supports it
    res.status(501).json({ error: 'Not implemented yet' })
  })

  // POST /api/sessions/:id/restart - Restart session
  router.post('/:id/restart', async (req, res) => {
    const stallDetector = new StallDetector()
    await stallDetector.recover(req.params.id, req.body.workflow)
    res.json({ success: true })
  })

  // DELETE /api/sessions/:id - Terminate session
  router.delete('/:id', async (req, res) => {
    await sessionManager.terminate(req.params.id)
    res.json({ success: true })
  })

  export default router
  ```

---

## Task 2.4: Session Controls UI **[P1]**
**Estimated**: 10 hours
**Dependencies**: 2.3

### Subtasks:
- [ ] **2.4.1** Create session list component
  - **File**: `frontend/src/components/SessionList.vue`
  ```vue
  <template>
    <div class="session-list">
      <h2>Sessions</h2>

      <div class="filters">
        <select v-model="filterStatus" @change="loadSessions">
          <option value="">All</option>
          <option value="running">Running</option>
          <option value="completed">Completed</option>
          <option value="failed">Failed</option>
        </select>
      </div>

      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Workflow</th>
            <th>Status</th>
            <th>Started</th>
            <th>Duration</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="session in sessions" :key="session.id">
            <td>{{ session.id.substring(0, 8) }}</td>
            <td>{{ session.workflow_id }}</td>
            <td>
              <span :class="`status-${session.status}`">
                {{ session.status }}
              </span>
            </td>
            <td>{{ formatDate(session.started_at) }}</td>
            <td>{{ calculateDuration(session) }}</td>
            <td>
              <button v-if="session.status === 'running'" @click="terminate(session.id)">
                Stop
              </button>
              <button v-if="session.status === 'stalled'" @click="restart(session.id)">
                Restart
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>

  <script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import axios from 'axios'

  interface Session {
    id: string
    workflow_id: string
    status: string
    started_at: string
    ended_at?: string
  }

  const sessions = ref<Session[]>([])
  const filterStatus = ref('')

  async function loadSessions() {
    const params: any = {}
    if (filterStatus.value) {
      params.status = filterStatus.value
    }

    const response = await axios.get('http://localhost:3000/api/sessions', { params })
    sessions.value = response.data
  }

  async function terminate(sessionId: string) {
    await axios.delete(`http://localhost:3000/api/sessions/${sessionId}`)
    await loadSessions()
  }

  async function restart(sessionId: string) {
    await axios.post(`http://localhost:3000/api/sessions/${sessionId}/restart`)
    await loadSessions()
  }

  function formatDate(date: string) {
    return new Date(date).toLocaleString()
  }

  function calculateDuration(session: Session) {
    const start = new Date(session.started_at).getTime()
    const end = session.ended_at ? new Date(session.ended_at).getTime() : Date.now()
    const durationSec = Math.floor((end - start) / 1000)

    const minutes = Math.floor(durationSec / 60)
    const seconds = durationSec % 60

    return `${minutes}m ${seconds}s`
  }

  onMounted(() => {
    loadSessions()
    // Refresh every 5 seconds
    setInterval(loadSessions, 5000)
  })
  </script>

  <style scoped>
  .session-list {
    padding: 1rem;
  }

  table {
    width: 100%;
    border-collapse: collapse;
  }

  th, td {
    padding: 0.5rem;
    text-align: left;
    border-bottom: 1px solid #ccc;
  }

  .status-running {
    color: green;
  }

  .status-stalled {
    color: orange;
  }

  .status-failed {
    color: red;
  }

  .status-completed {
    color: blue;
  }
  </style>
  ```

---

# PHASE 3: Monitoring Dashboard (Weeks 9-11)

## Task 3.1: Integrate Multi-Agent-Workflow Backend **[P0]**
**Estimated**: 10 hours
**Dependencies**: 0.1

### Subtasks:
- [ ] **3.1.1** Analyze multi-agent-workflow codebase
  - **Action**: Document architecture in `docs/multi-agent-workflow-integration.md`
  - **Files to review**:
    - `external/multi-agent-workflow/server/index.ts`
    - `external/multi-agent-workflow/server/events.ts`
    - `external/multi-agent-workflow/server/hooks.ts`

- [ ] **3.1.2** Create API wrapper
  - **File**: `backend/src/api/monitoring.ts`
  ```typescript
  import express from 'express'
  import { createProxyMiddleware } from 'http-proxy-middleware'

  const router = express.Router()

  // Proxy all requests to multi-agent-workflow backend
  router.use('/', createProxyMiddleware({
    target: 'http://localhost:3001',  // multi-agent-workflow runs on 3001
    changeOrigin: true,
    pathRewrite: {
      '^/api/monitoring': ''  // Strip /api/monitoring prefix
    }
  }))

  export default router
  ```

- [ ] **3.1.3** Start multi-agent-workflow backend
  - **File**: `backend/src/services/monitoring-backend.ts`
  ```typescript
  import { spawn, ChildProcess } from 'child_process'

  export class MonitoringBackend {
    private process: ChildProcess | null = null

    start() {
      // Start multi-agent-workflow server
      this.process = spawn('bun', ['run', 'server/index.ts'], {
        cwd: 'external/multi-agent-workflow',
        stdio: 'inherit'
      })

      console.log('Monitoring backend started on port 3001')
    }

    stop() {
      if (this.process) {
        this.process.kill()
      }
    }
  }
  ```

---

## Task 3.2: Custom UI Overlays (30%) **[P0]**
**Estimated**: 16 hours
**Dependencies**: 3.1

### Subtasks:
- [ ] **3.2.1** Create workflow selector dropdown
  - **File**: `frontend/src/components/WorkflowSelector.vue`
  ```vue
  <template>
    <div class="workflow-selector">
      <select v-model="selectedWorkflowId" @change="switchWorkflow">
        <option value="">Select Workflow</option>
        <option v-for="workflow in workflows" :key="workflow.id" :value="workflow.id">
          {{ workflow.name }}
        </option>
      </select>

      <button @click="startWorkflow" :disabled="!selectedWorkflowId">
        Start
      </button>
    </div>
  </template>

  <script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import axios from 'axios'

  const workflows = ref([])
  const selectedWorkflowId = ref('')

  const emit = defineEmits(['workflow-changed', 'workflow-started'])

  async function loadWorkflows() {
    const response = await axios.get('http://localhost:3000/api/workflows')
    workflows.value = response.data
  }

  function switchWorkflow() {
    emit('workflow-changed', selectedWorkflowId.value)
  }

  async function startWorkflow() {
    const response = await axios.post('http://localhost:3000/api/sessions', {
      workflowId: selectedWorkflowId.value
    })
    emit('workflow-started', response.data.sessionId)
  }

  onMounted(() => {
    loadWorkflows()
  })
  </script>
  ```

- [ ] **3.2.2** Create model usage widget
  - **File**: `frontend/src/components/ModelUsageWidget.vue`
  ```vue
  <template>
    <div class="model-usage-widget">
      <h3>Model Usage</h3>

      <div v-for="(usage, model) in modelUsage" :key="model" class="model-row">
        <span class="model-name">{{ model }}</span>
        <span class="token-count">{{ usage.tokens }} tokens</span>
        <span class="cost">${{ usage.cost.toFixed(4) }}</span>
        <div class="usage-bar" :style="{ width: `${(usage.tokens / totalTokens) * 100}%` }"></div>
      </div>

      <div class="totals">
        <strong>Total:</strong>
        <span>{{ totalTokens }} tokens</span>
        <span>${{ totalCost.toFixed(4) }}</span>
      </div>
    </div>
  </template>

  <script setup lang="ts">
  import { ref, computed, onMounted } from 'vue'
  import axios from 'axios'

  const props = defineProps<{ sessionId: string }>()

  interface ModelUsage {
    tokens: number
    cost: number
  }

  const modelUsage = ref<Record<string, ModelUsage>>({})

  const totalTokens = computed(() => {
    return Object.values(modelUsage.value).reduce((sum, u) => sum + u.tokens, 0)
  })

  const totalCost = computed(() => {
    return Object.values(modelUsage.value).reduce((sum, u) => sum + u.cost, 0)
  })

  async function loadModelUsage() {
    const response = await axios.get(`http://localhost:3000/api/proxy/metrics/${props.sessionId}`)
    modelUsage.value = response.data.modelUsage
  }

  onMounted(() => {
    loadModelUsage()
    setInterval(loadModelUsage, 5000)  // Refresh every 5s
  })
  </script>
  ```

- [ ] **3.2.3** Create session controls toolbar
  - **File**: `frontend/src/components/SessionControls.vue`

- [ ] **3.2.4** Integrate multi-agent-workflow dashboard
  - **File**: `frontend/src/components/MonitorDashboard.vue`
  - **Action**: Import and wrap multi-agent-workflow Vue components

---

## Task 3.3: Claude-Code-Proxy Data Integration **[P0]**
**Estimated**: 10 hours
**Dependencies**: 2.1

### Subtasks:
- [ ] **3.3.1** Research claude-code-proxy log format
  - **Action**: Inspect proxy installation, document findings in `docs/claude-code-proxy-integration.md`
  - **Expected log location**: `~/.claude-proxy/requests.log` or similar

- [ ] **3.3.2** Create proxy log parser
  - **File**: `backend/src/services/proxy-log-parser.ts`
  ```typescript
  import fs from 'fs/promises'
  import { Tail } from 'tail'

  export interface ProxyLogEntry {
    timestamp: Date
    sessionId: string
    model: string
    tokensIn: number
    tokensOut: number
    cost: number
    latencyMs: number
  }

  export class ProxyLogParser {
    private tail: Tail | null = null
    private entries: ProxyLogEntry[] = []

    async start(logPath: string) {
      this.tail = new Tail(logPath)

      this.tail.on('line', (line: string) => {
        const entry = this.parseLine(line)
        if (entry) {
          this.entries.push(entry)
          this.emit('entry', entry)
        }
      })

      this.tail.on('error', (error: Error) => {
        console.error('Proxy log tail error:', error)
      })
    }

    private parseLine(line: string): ProxyLogEntry | null {
      try {
        // TODO: Adjust parsing based on actual log format
        const data = JSON.parse(line)

        return {
          timestamp: new Date(data.timestamp),
          sessionId: data.session_id,
          model: data.model,
          tokensIn: data.tokens_in,
          tokensOut: data.tokens_out,
          cost: data.cost_usd,
          latencyMs: data.latency_ms
        }
      } catch (error) {
        return null
      }
    }

    getEntries(sessionId: string): ProxyLogEntry[] {
      return this.entries.filter(e => e.sessionId === sessionId)
    }

    getMetrics(sessionId: string) {
      const entries = this.getEntries(sessionId)

      const modelUsage: Record<string, { tokens: number, cost: number }> = {}

      for (const entry of entries) {
        if (!modelUsage[entry.model]) {
          modelUsage[entry.model] = { tokens: 0, cost: 0 }
        }
        modelUsage[entry.model].tokens += entry.tokensIn + entry.tokensOut
        modelUsage[entry.model].cost += entry.cost
      }

      return {
        totalTokens: entries.reduce((sum, e) => sum + e.tokensIn + e.tokensOut, 0),
        totalCost: entries.reduce((sum, e) => sum + e.cost, 0),
        modelUsage
      }
    }

    stop() {
      if (this.tail) {
        this.tail.unwatch()
      }
    }
  }
  ```

- [ ] **3.3.3** Create proxy metrics API
  - **File**: `backend/src/api/proxy.ts`
  ```typescript
  import express from 'express'
  import { ProxyLogParser } from '../services/proxy-log-parser'

  const router = express.Router()
  const parser = new ProxyLogParser()

  // Start watching proxy logs
  parser.start(process.env.CLAUDE_PROXY_LOG_PATH || '~/.claude-proxy/requests.log')

  // GET /api/proxy/metrics/:sessionId
  router.get('/metrics/:sessionId', (req, res) => {
    const metrics = parser.getMetrics(req.params.sessionId)
    res.json(metrics)
  })

  export default router
  ```

---

# PHASE 4: RAG Memory (Weeks 12-14)

## Task 4.1: Vector Database Setup **[P0]**
**Estimated**: 6 hours
**Dependencies**: 0.2

### Subtasks:
- [ ] **4.1.1** Install pgvector extension
  ```sql
  -- Run in PostgreSQL
  CREATE EXTENSION IF NOT EXISTS vector;
  ```

- [ ] **4.1.2** Create memories table (already in schema.sql from Task 0.2.1)

- [ ] **4.1.3** Create vector index
  ```sql
  CREATE INDEX idx_memories_embedding
    ON memories USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);
  ```

---

## Task 4.2: Embedding Service **[P0]**
**Estimated**: 10 hours
**Dependencies**: 4.1

### Subtasks:
- [ ] **4.2.1** Create embedding service
  - **File**: `backend/src/services/embedding.ts`
  ```typescript
  import axios from 'axios'

  export class EmbeddingService {
    private apiKey: string

    constructor(apiKey: string) {
      this.apiKey = apiKey
    }

    async embed(text: string): Promise<number[]> {
      // Use OpenAI API
      const response = await axios.post(
        'https://api.openai.com/v1/embeddings',
        {
          model: 'text-embedding-3-small',
          input: text
        },
        {
          headers: {
            'Authorization': `Bearer ${this.apiKey}`,
            'Content-Type': 'application/json'
          }
        }
      )

      return response.data.data[0].embedding
    }

    async embedBatch(texts: string[]): Promise<number[][]> {
      const response = await axios.post(
        'https://api.openai.com/v1/embeddings',
        {
          model: 'text-embedding-3-small',
          input: texts
        },
        {
          headers: {
            'Authorization': `Bearer ${this.apiKey}`,
            'Content-Type': 'application/json'
          }
        }
      )

      return response.data.data.map((item: any) => item.embedding)
    }
  }
  ```

- [ ] **4.2.2** (Optional) Create local ONNX embedding service
  - **Library**: `@xenova/transformers`
  - **Model**: `Xenova/all-MiniLM-L6-v2`
  - **Benefit**: No API costs, faster for local dev

---

## Task 4.3: RAG Engine **[P0]**
**Estimated**: 12 hours
**Dependencies**: 4.2

### Subtasks:
- [ ] **4.3.1** Create RAG engine service
  - **File**: `backend/src/services/rag-engine.ts`
  ```typescript
  import { db } from '../db/client'
  import { EmbeddingService } from './embedding'

  export class RAGEngine {
    constructor(private embeddingService: EmbeddingService) {}

    async search(query: string, k: number = 5, workflowId?: string): Promise<any[]> {
      // Generate query embedding
      const queryEmbedding = await this.embeddingService.embed(query)

      // Vector similarity search
      let sql = `
        SELECT
          id,
          content,
          content_type,
          metadata,
          1 - (embedding <=> $1::vector) AS similarity
        FROM memories
        WHERE 1=1
      `
      const params: any[] = [JSON.stringify(queryEmbedding)]

      if (workflowId) {
        sql += ' AND (workflow_id = $2 OR workflow_id IS NULL)'
        params.push(workflowId)
      }

      sql += ' ORDER BY embedding <=> $1::vector LIMIT $' + (params.length + 1)
      params.push(k)

      const result = await db.query(sql, params)
      return result.rows
    }

    async store(
      sessionId: string,
      workflowId: string,
      content: string,
      contentType: 'output' | 'learning' | 'pattern' | 'error',
      metadata?: any
    ) {
      const embedding = await this.embeddingService.embed(content)

      await db.query(
        `INSERT INTO memories (session_id, workflow_id, content_type, content, embedding, metadata)
         VALUES ($1, $2, $3, $4, $5::vector, $6)`,
        [sessionId, workflowId, contentType, content, JSON.stringify(embedding), metadata]
      )
    }

    async annotate(memoryId: string, annotation: string, score: number = 2.0) {
      await db.query(
        `UPDATE memories SET
           metadata = COALESCE(metadata, '{}'::jsonb) || jsonb_build_object('annotation', $2),
           retrieval_score = $3
         WHERE id = $1`,
        [memoryId, annotation, score]
      )
    }
  }
  ```

- [ ] **4.3.2** Create context injection function
  - **Function**: `async function injectContext(workflowId: string, claudeMdPath: string)`
  - **Logic**: Search memories, prepend to CLAUDE.md

- [ ] **4.3.3** Create learning capture function
  - **Function**: `async function captureSessionLearnings(sessionId: string)`
  - **Logic**: Parse session outputs, extract key learnings, store as memories

---

## Task 4.4: Memory API **[P0]**
**Estimated**: 6 hours
**Dependencies**: 4.3

### Subtasks:
- [ ] **4.4.1** Create memory API routes
  - **File**: `backend/src/api/memory.ts`
  ```typescript
  import express from 'express'
  import { RAGEngine } from '../services/rag-engine'
  import { EmbeddingService } from '../services/embedding'

  const router = express.Router()
  const embeddingService = new EmbeddingService(process.env.OPENAI_API_KEY!)
  const ragEngine = new RAGEngine(embeddingService)

  // GET /api/memory/search?q=...&workflowId=...
  router.get('/search', async (req, res) => {
    const { q, workflowId, k = 5 } = req.query

    if (!q) {
      return res.status(400).json({ error: 'Query required' })
    }

    const results = await ragEngine.search(q as string, parseInt(k as string), workflowId as string)
    res.json(results)
  })

  // POST /api/memory
  router.post('/', async (req, res) => {
    const { sessionId, workflowId, content, contentType, metadata } = req.body

    await ragEngine.store(sessionId, workflowId, content, contentType, metadata)
    res.json({ success: true })
  })

  // POST /api/memory/annotate/:id
  router.post('/annotate/:id', async (req, res) => {
    const { annotation, score } = req.body
    await ragEngine.annotate(req.params.id, annotation, score)
    res.json({ success: true })
  })

  // GET /api/memory/sessions/:sessionId
  router.get('/sessions/:sessionId', async (req, res) => {
    const result = await db.query(
      'SELECT * FROM memories WHERE session_id = $1 ORDER BY created_at DESC',
      [req.params.sessionId]
    )
    res.json(result.rows)
  })

  export default router
  ```

---

## Task 4.5: Memory Viewer UI **[P1]**
**Estimated**: 8 hours
**Dependencies**: 4.4

### Subtasks:
- [ ] **4.5.1** Create memory viewer component
  - **File**: `frontend/src/components/MemoryViewer.vue`
  ```vue
  <template>
    <div class="memory-viewer">
      <h3>Retrieved Memories</h3>

      <div class="search-bar">
        <input
          v-model="searchQuery"
          @keyup.enter="search"
          placeholder="Search memories..."
        />
        <button @click="search">Search</button>
      </div>

      <div class="memory-list">
        <div
          v-for="memory in memories"
          :key="memory.id"
          class="memory-card"
          :class="`type-${memory.content_type}`"
        >
          <div class="memory-header">
            <span class="type-badge">{{ memory.content_type }}</span>
            <span class="similarity">{{ (memory.similarity * 100).toFixed(1) }}% match</span>
            <span class="date">{{ formatDate(memory.created_at) }}</span>
          </div>

          <div class="memory-content">
            {{ truncate(memory.content, 200) }}
          </div>

          <div v-if="memory.metadata?.annotation" class="annotation">
            📝 {{ memory.metadata.annotation }}
          </div>

          <button @click="annotate(memory.id)">Add Annotation</button>
        </div>
      </div>
    </div>
  </template>

  <script setup lang="ts">
  import { ref } from 'vue'
  import axios from 'axios'

  interface Memory {
    id: string
    content: string
    content_type: string
    similarity: number
    created_at: string
    metadata?: any
  }

  const props = defineProps<{ workflowId?: string }>()

  const searchQuery = ref('')
  const memories = ref<Memory[]>([])

  async function search() {
    const params: any = { q: searchQuery.value }
    if (props.workflowId) {
      params.workflowId = props.workflowId
    }

    const response = await axios.get('http://localhost:3000/api/memory/search', { params })
    memories.value = response.data
  }

  async function annotate(memoryId: string) {
    const annotation = prompt('Enter your annotation:')
    if (!annotation) return

    await axios.post(`http://localhost:3000/api/memory/annotate/${memoryId}`, {
      annotation,
      score: 2.0  // Boost retrieval score
    })

    search()  // Refresh
  }

  function truncate(text: string, length: number) {
    return text.length > length ? text.substring(0, length) + '...' : text
  }

  function formatDate(date: string) {
    return new Date(date).toLocaleString()
  }
  </script>

  <style scoped>
  .memory-viewer {
    padding: 1rem;
  }

  .memory-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-top: 1rem;
  }

  .memory-card {
    border: 1px solid #ccc;
    padding: 1rem;
    border-radius: 4px;
  }

  .memory-header {
    display: flex;
    gap: 1rem;
    margin-bottom: 0.5rem;
  }

  .type-badge {
    background: #007bff;
    color: white;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 0.875rem;
  }

  .similarity {
    color: green;
    font-weight: bold;
  }

  .annotation {
    margin-top: 0.5rem;
    padding: 0.5rem;
    background: #f0f0f0;
    border-radius: 4px;
    font-style: italic;
  }
  </style>
  ```

---

# PHASE 5: Lifecycle & Polish (Weeks 15-17)

## Task 5.1: Cleanup Scheduler **[P0]**
**Estimated**: 10 hours
**Dependencies**: None

### Subtasks:
- [ ] **5.1.1** Create cleanup service
  - **File**: `backend/src/services/cleanup-scheduler.ts`
  ```typescript
  import { CronJob } from 'cron'
  import { db } from '../db/client'
  import fs from 'fs/promises'
  import archiver from 'archiver'

  export class CleanupScheduler {
    private job: CronJob | null = null

    start() {
      // Run daily at 3am
      this.job = new CronJob('0 3 * * *', async () => {
        console.log('Running cleanup job...')
        await this.cleanup()
      })

      this.job.start()
    }

    stop() {
      if (this.job) {
        this.job.stop()
      }
    }

    async cleanup() {
      // Age-based cleanup (30 days)
      await this.cleanupByAge()

      // Size-based cleanup (1GB threshold)
      await this.cleanupBySize()
    }

    private async cleanupByAge() {
      const result = await db.query(`
        SELECT id FROM workflows
        WHERE last_used_at < NOW() - INTERVAL '30 days'
          AND is_permanent = false
        ORDER BY last_used_at ASC
      `)

      for (const row of result.rows) {
        console.log(`Archiving workflow ${row.id} (age-based)`)
        await this.archiveWorkflow(row.id)
      }
    }

    private async cleanupBySize() {
      // Get total storage
      const result = await db.query(`
        SELECT SUM(storage_bytes) as total FROM workflows WHERE is_permanent = false
      `)
      const totalBytes = parseInt(result.rows[0].total || '0')
      const thresholdBytes = 1_000_000_000  // 1GB

      if (totalBytes <= thresholdBytes) {
        return  // Under threshold
      }

      // Delete oldest until under threshold
      const toDelete = totalBytes - thresholdBytes
      let deleted = 0

      const workflows = await db.query(`
        SELECT id, storage_bytes FROM workflows
        WHERE is_permanent = false
        ORDER BY last_used_at ASC
      `)

      for (const workflow of workflows.rows) {
        if (deleted >= toDelete) break

        console.log(`Archiving workflow ${workflow.id} (size-based)`)
        await this.archiveWorkflow(workflow.id)
        deleted += workflow.storage_bytes
      }
    }

    private async archiveWorkflow(workflowId: string) {
      const workflowPath = `.super_agent_monitor/workflows/${workflowId}`
      const archivePath = `.super_agent_monitor/archive/${workflowId}.tar.gz`

      // Create archive
      await fs.mkdir('.super_agent_monitor/archive', { recursive: true })

      const output = fs.createWriteStream(archivePath)
      const archive = archiver('tar', { gzip: true })

      archive.pipe(output)
      archive.directory(workflowPath, false)
      await archive.finalize()

      // Wait for archive to finish
      await new Promise(resolve => output.on('close', resolve))

      // Delete original
      await fs.rm(workflowPath, { recursive: true })

      // Update database
      await db.query(
        `UPDATE workflows SET storage_bytes = 0 WHERE id = $1`,
        [workflowId]
      )

      console.log(`Archived workflow ${workflowId}`)
    }
  }
  ```

- [ ] **5.1.2** Add pre-cleanup notifications
  - **Action**: Query workflows that will be deleted in 7 days
  - **UI**: Show banner: "Workflow X will be deleted on DATE. Click to save permanently."

---

## Task 5.2: Workflow Export/Import **[P0]**
**Estimated**: 10 hours
**Dependencies**: 1.2

### Subtasks:
- [ ] **5.2.1** Create export function
  - **File**: `backend/src/services/workflow-exporter.ts`
  ```typescript
  import fs from 'fs/promises'
  import archiver from 'archiver'

  export class WorkflowExporter {
    async export(workflowId: string): Promise<string> {
      // Get workflow from database
      const result = await db.query('SELECT * FROM workflows WHERE id = $1', [workflowId])
      const workflow = result.rows[0]

      // Create temp directory
      const tempDir = `.super_agent_monitor/temp/${workflowId}`
      await fs.mkdir(tempDir, { recursive: true })

      // Write workflow.json
      await fs.writeFile(
        `${tempDir}/workflow.json`,
        JSON.stringify(workflow.definition, null, 2)
      )

      // Copy components
      await fs.mkdir(`${tempDir}/components`, { recursive: true })
      for (const agent of workflow.definition.components.agents) {
        await fs.copyFile(
          `components/agents/${agent}.md`,
          `${tempDir}/components/${agent}.md`
        )
      }
      // ... copy skills, hooks, scripts

      // Generate README
      const readme = `# ${workflow.name}

${workflow.description}

## Installation

\`\`\`bash
# Import this workflow
curl -X POST http://localhost:3000/api/workflows/import \\
  -F "file=@${workflowId}.workflow"
\`\`\`

## Components

- Agents: ${workflow.definition.components.agents.join(', ')}
- Skills: ${workflow.definition.components.skills.join(', ')}
`
      await fs.writeFile(`${tempDir}/README.md`, readme)

      // Create ZIP
      const outputPath = `.super_agent_monitor/exports/${workflowId}.workflow`
      await fs.mkdir('.super_agent_monitor/exports', { recursive: true })

      const output = fs.createWriteStream(outputPath)
      const archive = archiver('zip')

      archive.pipe(output)
      archive.directory(tempDir, false)
      await archive.finalize()

      await new Promise(resolve => output.on('close', resolve))

      // Cleanup temp
      await fs.rm(tempDir, { recursive: true })

      return outputPath
    }
  }
  ```

- [ ] **5.2.2** Create import function with conflict resolution
  - **Logic**: Extract ZIP, check for component conflicts, prompt user, apply resolution

---

## Task 5.3: Populate Component Library **[P1]**
**Estimated**: 20 hours
**Dependencies**: 0.3

### Subtasks:
- [ ] **5.3.1** Create 15 more agents (total 20)
- [ ] **5.3.2** Create 15 more skills (total 20)
- [ ] **5.3.3** Create 5 more hooks (total 10)
- [ ] **5.3.4** Create 15 more scripts (total 20)
- [ ] **5.3.5** Create 2 more orchestrators (total 5)
- [ ] **5.3.6** Create 8 more subagent prompts (total 10)

---

## Task 5.4: Documentation **[P1]**
**Estimated**: 12 hours
**Dependencies**: All

### Subtasks:
- [ ] **5.4.1** Write user guide
  - **File**: `docs/USER-GUIDE.md`
  - **Sections**: Installation, creating workflows, monitoring sessions, RAG memory

- [ ] **5.4.2** Write API reference
  - **File**: `docs/API-REFERENCE.md`
  - **Tool**: Generate from OpenAPI spec

- [ ] **5.4.3** Create architecture diagram
  - **File**: `docs/architecture.png`
  - **Tool**: Draw.io or Mermaid

- [ ] **5.4.4** Record demo video
  - **Tool**: Loom or OBS Studio
  - **Content**: Create workflow → Launch session → Monitor in real-time

---

# PHASE 6: Testing & Beta (Week 18)

## Task 6.1: End-to-End Testing **[P0]**
**Estimated**: 16 hours
**Dependencies**: All

### Subtasks:
- [ ] **6.1.1** Write integration tests
  - **File**: `backend/src/__tests__/integration.test.ts`
  - **Scenarios**:
    - Create workflow → Launch session → Session completes
    - Session stalls → Auto-recovery succeeds
    - Cleanup job runs → Old workflows archived

- [ ] **6.1.2** Write UI tests
  - **Tool**: Playwright or Cypress
  - **Scenarios**:
    - Browse components → Create workflow → Start session → Monitor

- [ ] **6.1.3** Load testing
  - **Tool**: k6 or Artillery
  - **Scenario**: 10 concurrent sessions, measure performance

---

## Task 6.2: Beta Launch **[P0]**
**Estimated**: 8 hours
**Dependencies**: 6.1

### Subtasks:
- [ ] **6.2.1** Deploy to staging environment
  - **Platform**: Railway, Render, or DigitalOcean
  - **Setup**: PostgreSQL + Backend + Frontend

- [ ] **6.2.2** Recruit 10 beta users
  - **Channels**: r/ClaudeAI, Twitter, Hacker News

- [ ] **6.2.3** Create onboarding checklist
  - [ ] Install Claude Code
  - [ ] Install claude-code-proxy
  - [ ] Configure models
  - [ ] Create first workflow
  - [ ] Launch session

- [ ] **6.2.4** Collect feedback
  - **Tool**: Google Forms or Typeform
  - **Questions**: What worked? What didn't? Feature requests?

---

# SUMMARY: Task Counts by Phase

| Phase | Tasks | Estimated Hours | Key Deliverables |
|-------|-------|-----------------|------------------|
| **Phase 0** | 5 | 32h | Database, component seed, templates, Docker setup |
| **Phase 1** | 6 | 66h | Workflow engine, component registry, APIs, basic UI |
| **Phase 2** | 4 | 44h | Session launcher, stall detection, recovery, UI |
| **Phase 3** | 3 | 36h | Monitoring dashboard integration, custom overlays |
| **Phase 4** | 5 | 42h | RAG system (embedding, search, injection) |
| **Phase 5** | 4 | 52h | Cleanup, export/import, library population, docs |
| **Phase 6** | 2 | 24h | Testing, beta launch |
| **TOTAL** | **29** | **296h** | **~18 weeks @ 16h/week** |

---

# NEXT STEPS

1. **Week 1**: Start with Phase 0 tasks (foundation)
2. **Daily standup**: Review completed tasks, blockers
3. **Weekly milestone**: Demo working features
4. **Continuous**: Update task list as needed

**Ready to start? Begin with Task 0.1!** 🚀
