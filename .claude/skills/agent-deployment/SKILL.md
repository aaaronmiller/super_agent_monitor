# Skill: Agent Deployment

## Description
This skill provides the capability to deploy, manage, and orchestrate other agents using the Super Agent Monitor infrastructure. It covers usage of the `deploy.sh` CLI, sandbox selection (Local vs. E2B), and model configuration.

## Dependencies
- `deploy.sh` script in project root
- `start.sh` (for dashboard availability)
- `E2B_API_KEY` (for E2B sandboxes)

## Capabilities

### 1. Deploy Agent (CLI)
**Command**: `./deploy.sh <project_path> [options]`

**Options**:
- `--prompt "..."`: The instruction for the agent.
- `--e2b`: Use a secure, remote E2B sandbox (Recommended for untrusted code).
- `--model <model_id>`: Select specific LLM (default: `google/gemini-2.0-flash-exp:free`).
- `--sandbox`: Use local ephemeral sandbox (Default if --e2b not present).

**Examples**:
```bash
# Deploy a researcher agent to a local sandbox
./deploy.sh ./my-project --prompt "Research quantum computing trends"

# Deploy a coder agent to a secure E2B sandbox with Claude 3.5 Sonnet
./deploy.sh ./my-app --e2b --model "anthropic/claude-3-5-sonnet" --prompt "Refactor the login component"
```

### 2. Session Management
- **Dashboard**: Monitor live deployments at `http://localhost:5173`
- **Stop Session**: Use the Dashboard UI or `Ctrl+C` in the deploying terminal.
- **Logs**: Session logs are synced back to `<project_path>/logs/`.

### 3. Verification
- Verify successful deployment by checking `logs/session_start.json`.
- Ensure the agent's output appears in the dashboard timeline.

## Reference: Agent Catalog
The following agents are available for deployment. Use these names in your prompts or manual configurations.

| Agent Name | Role / Specialization |
|:-----------|:----------------------|
| **analyzer** | Analyzes codebases, project structures, and requirements. |
| **architect** | High-level system design, pattern selection, and infrastructure planning. |
| **backend-expert** | Node.js, Python, Databases, API design, and server-side logic. |
| **code-reviewer** | Audits code for best practices, bugs, security, and performance. |
| **database-admin** | SQL optimization, schema design, migrations, and data management. |
| **devops-expert** | CI/CD, Docker, Kubernetes, Cloud (AWS/GCP/Azure), and deployment scripts. |
| **docs-scraper** | Crawls and indexes documentation sites for knowledge retrieval. |
| **documentation-writer** | Creates technical documentation, READMEs, API references, and guides. |
| **file-analyzer** | Deep analysis of specific file types and content structures. |
| **frontend-expert** | Vue, React, CSS/Tailwind, UI/UX implementation. |
| **github-searcher** | searches GitHub for code snippets, libraries, and reference implementations. |
| **prd-finder** | Locates and extracts Product Requirement Documents in a file tree. |
| **prd-rater** | Evaluates PRD quality against standard scoring metrics. |
| **product-manager** | Define features, prioritize backlogs, and ensure user alignment. |
| **project-tagger** | Applies semantic tags and metadata to project artifacts. |
| **qa-engineer** | Writes test plans, automated test scripts, and performs manual verification. |
| **researcher-primary** | General purpose web research and information synthesis. |
| **security-expert** | Audits for vulnerabilities, secret leaks, and security best practices. |
| **tester** | Focused execution of unit and integration tests. |
| **web-scraper** | General purpose web extraction and content parsing. |

### Natural Language Invocation
The Prime Council's **Adaptive Router** maps natural language intent to these agents automatically.

**Examples:**
- "I need to fix a bug in the API" -> **backend-expert** + **code-reviewer**
- "Design a new microservice architecture" -> **architect**
- "Update the README with new installation steps" -> **documentation-writer**
- "Check for security vulnerabilities" -> **security-expert**
- "Deploy this to E2B" -> **devops-expert** (with `agent-deployment` skill)
