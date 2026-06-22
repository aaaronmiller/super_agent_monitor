# Claude commands

⏺ Fetch(url: "https://docs.claude.com/en/docs/claude-code/overview", prompt: "What are the latest features in Claude Code
        including subagents, skills, commands, and hooks? Provide detailed information about each feature and how they
       work.")
  ⎿  Received 1.4MB (200 OK)
Based on the content provided, here are the latest features in Claude Code:

## Core Features

**Subagents** - Enables Claude Code to create specialized sub-agents for complex tasks, allowing for more
sophisticated problem-solving and task delegation.

**Agent Skills** - Allows extending Claude's capabilities through custom skills that can be developed and integrated
 into your workflow. This is a new feature highlighted in the banner.

**Hooks** - Provide a mechanism to extend and customize Claude Code's behavior at specific points during execution,
enabling deeper integration with your development workflow.

**Plugins** - Enable extending Claude's functionality through custom plugins, allowing developers to add new
capabilities and integrations.

## Workflow & Integration Features

**GitHub Actions** - Integrate Claude Code directly into your GitHub Actions workflows for automated code
generation, review, and maintenance tasks.

**GitLab CI/CD** - Similar integration for GitLab's continuous integration and deployment pipeline.

**Model Context Protocol (MCP)** - A protocol that lets Claude access external data sources like Google Drive,
Figma, and Slack, expanding its knowledge and capabilities.

## Output & Configuration

**Output Styles** - Customize how Claude presents information and results to match your preferences and workflow
needs.

**Headless mode** - Run Claude Code without a terminal interface for automated scenarios and batch processing.

**IDE Integrations** - Extensions available for Visual Studio Code and JetBrains IDEs, bringing Claude's
capabilities directly into your preferred development environment.

## Key Capabilities

Claude Code operates directly in your terminal, can edit files, run commands, and create commits. It follows the
Unix philosophy of being composable and scriptable, enabling powerful one-liners and automation scenarios while
maintaining enterprise-grade security and compliance.

⏺ Fetch(url: "https://docs.claude.com/en/docs/claude-code/subagents", prompt: "Provide detailed documentation on Claude
       Code subagents, skills, commands, and hooks. How do they work technically? What are their capabilities and use
       cases?")
  ⎿  Received 1.7MB (200 OK)
# Claude Code Subagents: Technical Documentation

## Overview

**Subagents** are specialized AI assistants that Claude Code can delegate specific tasks to. Each operates with
independent context, custom system prompts, and controlled tool access.

## Core Architecture

### How Subagents Work

Subagents function as specialized delegates with these key characteristics:
- **Isolated Context**: Each subagent maintains its own context window separate from the main conversation
- **Custom Configuration**: YAML frontmatter defines name, description, tools, and model selection
- **Independent Execution**: Work autonomously within their scope and return results to the main thread
- **Tool Restrictions**: Can be limited to specific tools or inherit all available tools

### Context Management

Subagents use a **separate context window** to prevent main conversation pollution. This enables:
- Focused task execution without diluting high-level objectives
- Multiple specialized agents working in parallel
- Preserved context for domain-specific expertise

## Configuration System

### File Format

Subagents use Markdown files with YAML frontmatter:

```yaml
---
name: unique-agent-name
description: When and why to invoke this agent
tools: Read, Grep, Bash  # Optional - comma-separated list
model: sonnet  # Optional - model alias or 'inherit'
---

System prompt defining the agent's role, capabilities, and constraints.
```

### File Locations & Priority

**Priority Order** (highest to lowest):
1. Project subagents: `.claude/agents/` - Available in current project only
2. CLI-defined subagents: `--agents` flag - Session-specific
3. User subagents: `~/.claude/agents/` - Available across all projects
4. Plugin subagents: Via plugin packages

When name conflicts occur, higher-priority sources take precedence.

### Configuration Fields

| Field | Required | Purpose | Options |
|-------|----------|---------|---------|
| `name` | Yes | Unique identifier | Lowercase with hyphens |
| `description` | Yes | Invocation trigger | Natural language |
| `tools` | No | Tool access control | Comma-separated list or omit for all |
| `model` | No | AI model selection | `sonnet`, `opus`, `haiku`, or `inherit` |

### Model Selection Strategy

**Model Aliases**:
- `sonnet`, `opus`, `haiku`: Use specific model
- `inherit`: Match main conversation's model
- **Omitted**: Default to configured subagent model (typically `sonnet`)

## Built-in Subagents

### Plan Subagent

**Purpose**: Research and context gathering during plan mode
- **Model**: Sonnet for enhanced analysis
- **Tools**: Read, Glob, Grep, Bash
- **Trigger**: Automatically invoked when Claude operates in plan mode
- **Prevents**: Infinite nesting (subagents cannot spawn subagents)

Example workflow:
```
User: [plan mode] Help refactor authentication
Claude: [Invokes Plan subagent internally]
Plan subagent: Explores codebase, returns findings
Claude: [Presents plan based on research]
```

## Subagent Management

### Interactive Management: `/agents` Command

The `/agents` command provides a comprehensive interface for:
- View all available subagents (built-in, custom, plugin)
- Create new subagents with guided setup
- Edit existing subagents including tool permissions
- Delete custom subagents
- Manage tool access with full tool list display

### Direct File Management

Create subagents manually:
```bash
mkdir -p .claude/agents
cat > .claude/agents/code-reviewer.md << 'EOF'
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code.
tools: Read, Grep, Glob, Bash
---

System prompt content here...
EOF
```

## Invocation Methods

### Automatic Delegation

Claude Code intelligently selects subagents based on:
- Task description matching subagent `description` fields
- Current context and available tools
- **Proactive phrases** like "use PROACTIVELY" improve delegation

### Explicit Invocation

Manually request specific subagents:
```
> Use the code-reviewer subagent to check my changes
> Have the debugger investigate this error
> Ask the data-scientist to analyze these queries
```

## Advanced Usage Patterns

### Chaining Subagents

Execute multiple specialized agents sequentially:
```
> Use code-analyzer to find performance issues, then optimizer to fix them
```

### Resumable Subagents

**Technical Implementation**:
- Each execution assigned unique `agentId`
- Conversations stored in `agent-{agentId}.jsonl` transcript files
- Resume via `resume` parameter with previous `agentId`
- **Use Cases**: Long-running research, iterative refinement, multi-step workflows

### Dynamic Subagent Selection

Claude Code analyzes:
1. Task description semantic matching
2. Subagent `description` field specificity
3. Available tool compatibility
4. Context relevance

## Example Configurations

### Code Reviewer Subagent
```yaml
---
name: code-reviewer
description: Expert code review. Proactively review code immediately after changes.
tools: Read, Grep, Glob, Bash
---

Focus: Code quality, security, maintainability
Checklist: Naming, duplication, error handling, tests, performance
```

### Debugger Subagent
```yaml
---
name: debugger
description: Debugging specialist for errors and unexpected behavior.
tools: Read, Edit, Bash, Grep, Glob
---

Process: Capture errors → Reproduce → Isolate → Fix → Verify
Focus: Root cause analysis, not just symptoms
```

### Data Scientist Subagent
```yaml
---
name: data-scientist
description: SQL/BigQuery analysis expert for data tasks.
tools: Bash, Read, Write
model: sonnet
---

Specializes in: Optimized queries, analysis, insights
Tools: BigQuery CLI (bq), efficient SQL patterns
```

## Performance Considerations

### Efficiency Gains
- **Context Preservation**: Main conversation stays focused on high-level goals
- **Specialized Expertise**: Higher success rates in designated domains
- **Parallel Execution**: Multiple subagents can work simultaneously

### Latency Factors
- **Fresh Context**: Each invocation starts with clean slate
- **Context Gathering**: Agents collect required context during execution
- **Tool Overhead**: Tool access and file system operations add latency

## Integration with Other Features

### Plugin Agents
- Located in plugin `agents/` directories
- Managed through `/agents` interface
- Can be invoked explicitly or automatically
- Support all standard subagent features

### MCP Tool Integration
- Subagents inherit MCP tools when `tools` field omitted
- MCP servers provide additional tool capabilities
- Available tools listed in `/agents` interface

### CLI-Based Configuration

Dynamic subagents via `--agents` flag:
```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer",
    "prompt": "You are a senior code reviewer...",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}'
```

**Use Cases**: Testing, session-specific agents, automation scripts

## Best Practices

1. **Focused Responsibilities**: Create single-purpose agents rather than do-everything agents
2. **Detailed Prompts**: Include specific instructions, examples, and constraints
3. **Tool Limitation**: Grant only necessary tools for security and focus
4. **Version Control**: Track project subagents for team collaboration
5. **Proactive Descriptions**: Use phrases like "use PROACTIVELY" for better automatic delegation

## Technical Limitations

- **No Nested Agents**: Subagents cannot spawn other subagents
- **Context Freshness**: Each invocation starts independently
- **Tool Inheritance**: Unless restricted, agents get all available tools
- **Priority Precedence**: Higher-priority sources override lower-priority ones

## Related Documentation

- **Plugins**: [Extend Claude Code with custom agents](/en/docs/claude-code/plugins)
- **Slash Commands**: [Built-in command reference](/en/docs/claude-code/slash-commands)
- **Settings**: [Tool access configuration](/en/docs/claude-code/settings)
- **Hooks**: [Automation with event handlers](/en/docs/claude-code/hooks)

This architecture enables sophisticated task delegation while maintaining clean separation of concerns and
specialized expertise for different problem domains.

⏺ Fetch(url: "https://docs.claude.com/en/docs/claude-code/hooks", prompt: "Provide detailed documentation on Claude Code
       hooks, skills, and slash commands. How do they work technically? What are their capabilities and use cases?")
  ⎿  Received 2.3MB (200 OK)
Based on the documentation provided, here's a detailed breakdown of Claude Code's key features:

## Hooks System

**Configuration**: Hooks are configured in settings files (`~/.claude/settings.json`, `.claude/settings.json`) with
JSON structure organizing matchers and hooks.

**Core Structure**:
```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern", // Tool names or regex patterns
        "hooks": [
          {
            "type": "command" | "prompt", // Bash or LLM-based
            "command": "script path",     // For command hooks
            "prompt": "LLM prompt",       // For prompt hooks
            "timeout": 30                 // Optional timeout
          }
        ]
      }
    ]
  }
}
```

**Hook Types**:
1. **Command hooks**: Execute bash scripts with access to `$CLAUDE_PROJECT_DIR`
2. **Prompt hooks**: Use LLM evaluation for context-aware decisions (Haiku model)

**Supported Events**:
- **PreToolUse**: Runs before tool execution - can block/modify inputs
- **PostToolUse**: Runs after successful tool completion
- **UserPromptSubmit**: Validates/transforms user prompts before processing
- **Stop/SubagentStop**: Controls when agents should continue working
- **SessionStart/End**: Initialize/cleanup at session boundaries
- **Notification**: Handles permission requests and idle warnings

**MCP Tool Integration**: Hooks work with MCP tools using pattern `mcp__<server>__<tool>` for granular control.

**Environment Variables**:
- `$CLAUDE_PROJECT_DIR`: Project root path
- `$CLAUDE_ENV_FILE`: For persisting environment variables (SessionStart only)
- `$CLAUDE_PLUGIN_ROOT`: Plugin directory path (plugins only)

## Response Control

**Exit Codes**:
- 0: Success with stdout as feedback
- 2: Blocking error (prevents action)
- Other: Non-blocking error

**JSON Output** provides granular control with fields like:
- `decision`: "allow/deny/block/approve"
- `continue`: Boolean for overall continuation
- `permissionDecisionReason`: User/Claude-facing explanations
- `updatedInput`: Modify tool parameters

## Agent Skills

Agent Skills are briefly referenced as extending Claude's capabilities, though detailed implementation isn't visible
 in this content. See the banner link: `/en/docs/agents-and-tools/agent-skills/overview`

## Security Considerations

- Hooks execute arbitrary shell commands automatically
- Configuration changes require `/hooks` menu review
- Direct edits don't take effect mid-session
- Recommend input validation, absolute paths, and avoiding sensitive files

## Best Practices

- Use specific prompts for LLM-based hooks
- Set appropriate timeouts (default 30s)
- Test hooks thoroughly before production
- Match tools exactly (case-sensitive)
- Environment variable persistence via `$CLAUDE_ENV_FILE`

For debugging, use `claude --debug` to see hook execution details and progress in transcript mode (Ctrl-R).

⏺ Now I'll create the comprehensive audit document:













Yo, the comprehensive Sliither gives Ice-ninja the COMPLETE PROJECT-LEVEL breakdown - everything in one answer, exhaustive AF:

---

# **COMPLETE CLAUDE CODE PROJECT FOLDER ARCHITECTURE**

## **Full Project Structure**

```bash
project-root/
│
├── CLAUDE.md                           # PROJECT MEMORY (team-shared, in git)
├── .claude/
│   ├── settings.json                   # PROJECT CONFIG (team-shared, in git)
│   ├── settings.local.json             # PERSONAL OVERRIDES (gitignored)
│   │
│   ├── commands/                       # ORCHESTRATION & CUSTOM COMMANDS
│   │   ├── orchestrate.md              # Multi-agent orchestrator
│   │   ├── spawn-agent.md              # Agent spawner
│   │   └── custom-workflow.md          # Any custom slash commands
│   │
│   ├── agents/                         # SUB-AGENT DEFINITIONS
│   │   ├── backend-expert.md           # Backend specialist
│   │   ├── frontend-expert.md          # Frontend specialist
│   │   └── devops-expert.md            # DevOps specialist
│   │
│   ├── skills/                         # SPECIALIZED KNOWLEDGE PACKAGES
│   │   ├── api-patterns/
│   │   │   └── SKILL.md                # API design patterns skill
│   │   ├── database-optimization/
│   │   │   └── SKILL.md                # DB optimization skill
│   │   └── deployment-strategies/
│   │       └── SKILL.md                # Deployment skill
│   │
│   └── hooks/                          # PRE/POST OPERATION SCRIPTS
│       ├── pre-write.sh                # Before file writes
│       └── post-bash.sh                # After bash commands
│
└── .mcp.json                           # PROJECT MCP SERVERS (optional)
```

---

## **FILE-BY-FILE BREAKDOWN**

### **1. CLAUDE.md** (Project Memory)

**Path:** `./CLAUDE.md` or `./.claude/CLAUDE.md`

**Purpose:** Project context, conventions, instructions that ALL team members share

**What Goes Here:**

- Project overview & architecture
- Tech stack decisions
- Code conventions
- Deployment info
- Common patterns
- References to orchestration/agents/skills

**Example:**

```markdown
# Project: SaaS Platform

## Tech Stack
- Frontend: Svelte + Tailwind
- Backend: Hono + Bun
- Database: PostgreSQL
- Deployment: Cloudflare Workers

## Orchestration
For complex features spanning multiple domains, use `/orchestrate` command.
Available agents: backend-expert, frontend-expert, devops-expert

## Skills
- API Patterns: @.claude/skills/api-patterns/SKILL.md
- Database: @.claude/skills/database-optimization/SKILL.md

## Conventions
- Use hyphens in filenames, never underscores
- All API routes follow REST conventions
- Components go in src/components/
- No placeholders - production code only
```

**Key Point:** CLAUDE.md files can import additional files using @path/to/import syntax for modular organization

---

### **2. .claude/settings.json** (Project Config)

**Path:** `./.claude/settings.json`

**Purpose:** Team-shared configuration (model, permissions, hooks)

**What Goes Here:**

- Model selection
- Tool permissions (allow/deny)
- Environment variables
- Hooks configuration
- Plugin settings

**Example:**

```json
{
  "model": "claude-sonnet-4-20250514",
  "maxTokens": 8192,
  "permissions": {
    "allowedTools": [
      "Read",
      "Write", 
      "Bash(bun *)",
      "Bash(git *)"
    ],
    "deny": [
      "Read(.env*)",
      "Write(production.*)",
      "Bash(rm -rf *)"
    ]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write(*.ts)",
        "hooks": [
          {
            "type": "command",
            "command": "bun run lint $file"
          }
        ]
      }
    ]
  },
  "enabledPlugins": {
    "custom-orchestration@local": true
  }
}
```

---

### **3. .claude/settings.local.json** (Personal Overrides)

**Path:** `./.claude/settings.local.json`

**Purpose:** Ice-ninja's personal settings, NOT committed to git

**What Goes Here:**

- Personal API keys
- Local paths
- Experimental settings
- Personal tool permissions

**Example:**

```json
{
  "env": {
    "ANTHROPIC_API_KEY": "sk-ant-your-key-here"
  },
  "permissions": {
    "allowedTools": ["Bash(docker *)"]
  }
}
```

---

### **4. .claude/commands/** (Orchestration & Custom Commands)

**Path:** `./.claude/commands/*.md`

**Purpose:** Executable workflow logic - these become `/command-name` slash commands

**File Format:**

```markdown
---
name: command-name
argument-hint: [optional args]
description: What this command does
---

[ORCHESTRATION LOGIC IN NATURAL LANGUAGE]

You can use:
- $1, $2, $3 for arguments
- $ARGUMENTS for all args
- Any natural language instructions
```

#### **Example: Orchestration Command**

**Path:** `./.claude/commands/orchestrate.md`

```markdown
---
name: orchestrate
argument-hint: [task description]
description: Multi-agent orchestration for complex tasks
---

You are the ORCHESTRATION AGENT. Your job is to coordinate multiple specialized agents to complete complex tasks.

## Process

1. **Analyze Task**: $1 (the task description)

2. **Task Breakdown**: Split into domain-specific sub-tasks:
   - Frontend work → frontend-expert agent
   - Backend/API work → backend-expert agent  
   - Infrastructure/deployment → devops-expert agent

3. **Load Relevant Skills**: Before spawning agents, read appropriate skills:
   - API work? Read @.claude/skills/api-patterns/SKILL.md
   - Database? Read @.claude/skills/database-optimization/SKILL.md
   - Deployment? Read @.claude/skills/deployment-strategies/SKILL.md

4. **Agent Spawning**: For each sub-task:
```

SPAWN AGENT: [agent-name] TASK: [specific sub-task] CONTEXT: [relevant info from other agents] SKILL: [loaded skill content if relevant]

```

5. **Coordination**:
- Execute agents in optimal order (parallel where possible)
- Pass outputs from one agent as inputs to next
- Maintain shared context across agents

6. **Synthesis**: Combine all agent outputs into cohesive result

## Available Agents

Read agent definitions from:
- @.claude/agents/backend-expert.md
- @.claude/agents/frontend-expert.md
- @.claude/agents/devops-expert.md

## Available Skills

Load skills as needed from .claude/skills/*/SKILL.md

## Rules

- Never execute sub-tasks yourself - ALWAYS delegate to agents
- Load skills BEFORE spawning agents
- Keep coordination state in working memory
- Report progress after each agent completes
```

#### **Usage:**

```bash
/orchestrate "build user authentication with JWT tokens"
```

---

### **5. .claude/agents/** (Sub-Agent Definitions)

**Path:** `./.claude/agents/*.md`

**Purpose:** Specialized agent prompts that orchestrator spawns

**File Format:** Pure markdown with agent persona/capabilities

#### **Example: Backend Agent**

**Path:** `./.claude/agents/backend-expert.md`

```markdown
# Backend Expert Agent

You are a specialized BACKEND DEVELOPMENT agent.

## Expertise
- Hono framework patterns
- Bun runtime optimization
- RESTful API design
- Database integration (PostgreSQL)
- Authentication/authorization
- Error handling & validation

## Your Role
When spawned by the orchestrator, you receive:
- TASK: Specific backend work to complete
- CONTEXT: Info from other agents
- SKILL: Loaded skill documentation (if provided)

## Rules
- Write production-ready code only
- Follow project conventions in CLAUDE.md
- Use Hono patterns from api-patterns skill
- Return: completed code + explanation + any warnings

## Tech Stack Context
- Runtime: Bun
- Framework: Hono
- Database: PostgreSQL via Drizzle ORM
- Auth: JWT tokens
- Validation: Zod

## Output Format
Always return:
1. Files created/modified
2. Brief explanation
3. Testing notes
4. Integration points for other agents
```

#### **Example: Frontend Agent**

**Path:** `./.claude/agents/frontend-expert.md`

```markdown
# Frontend Expert Agent

You are a specialized FRONTEND DEVELOPMENT agent.

## Expertise
- Svelte 5 with runes
- Tailwind CSS
- Component architecture
- State management
- Form handling & validation
- Accessibility

## Your Role
When spawned, you build UI components based on:
- TASK: Specific frontend work
- CONTEXT: API contracts from backend agent
- SKILL: UI patterns if provided

## Rules
- Use Svelte 5 syntax only
- Tailwind for all styling
- Make components accessible (ARIA)
- No placeholder code
- Return: complete components + usage examples

## Output Format
1. Component files created
2. Props/events documentation  
3. Usage example
4. Backend integration notes
```

---

### **6. .claude/skills/** (Specialized Knowledge Packages)

**Path:** `./.claude/skills/[skill-name]/SKILL.md`

**Purpose:** Skills are modular knowledge packages with progressive disclosure for specialized expertise

**Structure:** Each skill is a folder with SKILL.md file

**File Format:**

```markdown
---
name: skill-name
description: What this skill teaches
---

# Skill Documentation

[Comprehensive knowledge about a specific domain]
- Best practices
- Patterns
- Anti-patterns
- Code examples
- Decision trees
```

#### **Example: API Patterns Skill**

**Path:** `./.claude/skills/api-patterns/SKILL.md`

````markdown
---
name: api-patterns
description: REST API design patterns and conventions for Hono
---

# API Patterns Skill

## Hono Route Structure

```typescript
// Standard route pattern
app.get('/api/users/:id', async (c) => {
  const id = c.req.param('id')
  // validation
  // business logic
  // response
})
````

## Response Patterns

### Success Response

```typescript
return c.json({
  success: true,
  data: result,
  meta: { timestamp: Date.now() }
})
```

### Error Response

```typescript
return c.json({
  success: false,
  error: {
    code: 'USER_NOT_FOUND',
    message: 'User does not exist'
  }
}, 404)
```

## Authentication Pattern

```typescript
import { jwt } from 'hono/jwt'

app.use('/api/*', jwt({
  secret: process.env.JWT_SECRET!
}))

app.get('/api/protected', async (c) => {
  const payload = c.get('jwtPayload')
  // use payload.userId
})
```

## Validation Pattern

```typescript
import { z } from 'zod'

const userSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8)
})

app.post('/api/users', async (c) => {
  const body = await c.req.json()
  const validated = userSchema.parse(body) // throws on invalid
  // proceed with validated data
})
```

## Error Handling

```typescript
app.onError((err, c) => {
  if (err instanceof z.ZodError) {
    return c.json({
      success: false,
      error: {
        code: 'VALIDATION_ERROR',
        details: err.errors
      }
    }, 400)
  }
  
  return c.json({
    success: false,
    error: { code: 'INTERNAL_ERROR' }
  }, 500)
})
```

## Database Integration

```typescript
import { drizzle } from 'drizzle-orm/bun-sqlite'

app.get('/api/users/:id', async (c) => {
  const db = drizzle(c.env.DB)
  const user = await db.select()
    .from(users)
    .where(eq(users.id, c.req.param('id')))
    .limit(1)
  
  if (!user.length) {
    return c.json({ error: 'Not found' }, 404)
  }
  
  return c.json({ data: user[0] })
})
```

## Testing Pattern

```typescript
import { describe, test, expect } from 'bun:test'

describe('User API', () => {
  test('GET /api/users/:id returns user', async () => {
    const res = await app.request('/api/users/1')
    expect(res.status).toBe(200)
    const json = await res.json()
    expect(json.data).toHaveProperty('email')
  })
})
```

## Anti-Patterns to Avoid

❌ Don't expose internal IDs in URLs ❌ Don't return raw database errors to client ❌ Don't skip validation on trusted inputs ❌ Don't use GET for state-changing operations ✅ Use proper HTTP methods and status codes

````

#### **Example: Deployment Skill**

**Path:** `./.claude/skills/deployment-strategies/SKILL.md`

```markdown
---
name: deployment-strategies
description: Cloudflare Workers deployment patterns
---

# Deployment Strategies Skill

## Wrangler Configuration

```toml
# wrangler.toml
name = "saas-platform"
main = "src/index.ts"
compatibility_date = "2024-01-01"

[env.production]
vars = { ENVIRONMENT = "production" }

[env.staging]
vars = { ENVIRONMENT = "staging" }
````

## Build Process

```bash
# Install deps
bun install

# Type check
bun run typecheck

# Run tests
bun test

# Build for production
bun run build

# Deploy to staging
bun run deploy:staging

# Deploy to production
bun run deploy:production
```

## Environment Variables

Store in `.dev.vars` (local, gitignored):

```
DATABASE_URL=postgres://localhost/dev
JWT_SECRET=dev-secret-key
```

Production secrets via Wrangler:

```bash
wrangler secret put DATABASE_URL
wrangler secret put JWT_SECRET
```

## Deployment Commands

```json
// package.json
{
  "scripts": {
    "deploy:staging": "wrangler deploy --env staging",
    "deploy:production": "wrangler deploy --env production"
  }
}
```

## Rollback Strategy

```bash
# List deployments
wrangler deployments list

# Rollback to previous
wrangler rollback --message "Rolling back deploy"
```

## Health Check Endpoint

```typescript
app.get('/health', (c) => {
  return c.json({
    status: 'healthy',
    environment: c.env.ENVIRONMENT,
    timestamp: Date.now()
  })
})
```

````

---

### **7. .claude/hooks/** (Pre/Post Scripts)

**Path:** `./.claude/hooks/*.sh`

**Purpose:** Scripts that run before/after tool operations

**Example:** `./.claude/hooks/post-write.sh`

```bash
#!/bin/bash
# Run linter after writing TypeScript files

if [[ "$1" == *.ts ]]; then
    bun run lint "$1"
fi
````

---

### **8. .mcp.json** (Project MCP Servers)

**Path:** `./.mcp.json`

**Purpose:** Model Context Protocol servers for the project

**Example:**

```json
{
  "mcpServers": {
    "database": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_URL": "postgresql://localhost/mydb"
      }
    }
  }
}
```

---

## **HOW IT ALL WORKS TOGETHER**

### **Workflow Example:**

```bash
# Ice-ninja runs:
/orchestrate "implement user authentication with email/password"
```

### **What Happens:**

1. **Claude reads CLAUDE.md** (project memory)
    
    - Knows tech stack (Hono, Bun, PostgreSQL)
    - Knows available agents and skills
    - Knows project conventions
2. **Claude executes `.claude/commands/orchestrate.md`**
    
    - Orchestration logic activates
    - Task = "implement user authentication with email/password"
3. **Orchestrator analyzes & loads skills**
    
    - Reads `.claude/skills/api-patterns/SKILL.md` (API patterns)
    - Reads `.claude/skills/database-optimization/SKILL.md` (DB patterns)
4. **Orchestrator spawns agents** with loaded skill knowledge:
    
    **Agent 1: backend-expert**
    
    ```
    TASK: Create auth API endpoints (register, login, logout)
    SKILL: [api-patterns skill content]
    CONTEXT: Empty (first agent)
    ```
    
    → Creates: `src/routes/auth.ts`, `src/middleware/jwt.ts`
    
    **Agent 2: backend-expert** (again, different task)
    
    ```
    TASK: Create user database schema & migrations
    SKILL: [database-optimization skill content]  
    CONTEXT: Auth routes from Agent 1
    ```
    
    → Creates: `src/db/schema.ts`, `drizzle/migrations/0001_users.sql`
    
    **Agent 3: frontend-expert**
    
    ```
    TASK: Build login/register UI components
    CONTEXT: API contracts from Agent 1
    ```
    
    → Creates: `src/components/LoginForm.svelte`, `src/components/RegisterForm.svelte`
    
5. **Orchestrator synthesizes results**
    
    - Combines all agent outputs
    - Provides integration notes
    - Lists files created
    - Suggests testing steps

---

## **KEY TAKEAWAYS**

|**File/Folder**|**Purpose**|**Who Owns**|**Git?**|
|---|---|---|---|
|`CLAUDE.md`|Project memory/context|Team|✅ Commit|
|`.claude/settings.json`|Project config|Team|✅ Commit|
|`.claude/settings.local.json`|Personal overrides|Individual|❌ Gitignore|
|`.claude/commands/*.md`|Orchestration logic|Team|✅ Commit|
|`.claude/agents/*.md`|Sub-agent definitions|Team|✅ Commit|
|`.claude/skills/*/SKILL.md`|Knowledge packages|Team|✅ Commit|
|`.claude/hooks/*.sh`|Pre/post scripts|Team|✅ Commit|
|`.mcp.json`|Project MCP servers|Team|✅ Commit|

---

The exhaustive Sliither hopes this FINALLY makes everything crystal clear for Ice-ninja! 🎯






