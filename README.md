# Super Agent Monitor

**The Autonomous Multi-Agent Orchestration Platform**

[![License: Elastic-2.0](https://img.shields.io/badge/License-Elastic--2.0-blue.svg)](LICENSE)
[![Orchestration: Adversarial](https://img.shields.io/badge/Orchestration-Adversarial-red.svg)](components/orchestrators/README.md)
[![Runtime: Local+Proxy](https://img.shields.io/badge/Runtime-Local%2BProxy-green.svg)](backend/src/services/ProxyService.ts)

---

## 🌟 The Vision

Super Agent Monitor is not just a wrapper; it is a **Command Center for Autonomous Intelligence**.

Imagine this: You sit down at your terminal or the GUI. You select a **Council Architecture**—perhaps a "CEO Council" for strategy or a "Researcher Swarm" for deep analysis. You input your task: *"Analyze the market viability of quantum-resistant cryptography."*

At that moment, the **Council** awakens. It deconstructs your command into a series of optimized instructions. It doesn't just run a script; it dynamically formulates a **Plan**—a bespoke configuration of sub-agents, skills, and tools tailored specifically to your request.

This Plan is then deployed into a **Secure Local Runtime**. The system spins up a headless Claude Code process, but with a twist: it is tethered to a **Local Man-in-the-Middle Proxy**. This proxy gives us god-mode powers: we can route models dynamically, inject context from your past history (RAG), and even "Kick" the agent if it stalls.

As the agent works, you watch in real-time. The **Live Terminal** streams its thought process with a smooth typewriter effect. The **Cost Estimator** predicts the bill at 60fps. You are no longer a passive observer; you are the Conductor of a Symphony of Intelligence.

---

## 🗺️ How It Works (The User Journey)

```mermaid
graph TD
    Start((Start)) --> Choice{Choose Mode}
    
    subgraph Quickstart ["🚀 Quickstart (The 'Magic Box')"]
        Choice -->|I have a task| Input[Input Task/Prompt]
        Input --> Auto[Adaptive Router (Auto-Council)]
        Auto -->|Deconstructs| Plan[Generated Plan]
        Plan -->|Executes| Agent[Agent Runtime]
        Agent -->|Feedback| UI[Live Monitor]
    end
    
    subgraph DeepDive ["🤿 Deep Dive (The 'Architect')"]
        Choice -->|I want control| Builder[Agent/Workflow Builder]
        Builder -->|Edit| Templates[Templates & Skills]
        Builder -->|Compose| CustomPlan[Custom Workflow]
        CustomPlan -->|Deploy| Agent
    end
    
    UI -->|Review| History[Session History]
    UI -->|Intervene| Kick[Kick/Stop]
    UI -->|Analyze| Metrics[Cost & Performance]
```

---

## 🚀 Core Features

### 1. 🏛️ Council Architectures (Orchestration)
We don't just "prompt" the model; we structure its cognition.
*   **CEO Council**: Simulates a debate between a CEO, CTO, and Product Officer to reach a balanced decision.
*   **RCR Protocol**: The "Coder" lineage uses a **Reflect-Critique-Refine** loop to self-correct code before you ever see it.
*   **Deep Dive**: The "Researcher" lineage recursively decomposes topics and searches in parallel.
*   *See [Visual Methodologies](docs/VISUALS.md) for detailed diagrams.*

### 2. 🛡️ Runtime Reliability (The "Smooth Operator")
*   **Adaptive Cost Estimator**: A Kalman Filter algorithm predicts costs in real-time, eliminating "price jitter."
*   **UI Smoothing**: A variable-speed typewriter buffer ensures the terminal output flows like water, never lagging or jumping.
*   **Stall Detection**: Our Local Proxy monitors "heartbeats." If an agent freezes, the system knows. You can then use the **Kick Button** to send a `SIGINT` and unfreeze it without killing the session.

## 🌟 Key Features

### 🧠 Intelligent Agent Orchestration
- **Workflow Engine**: Define complex agent behaviors using JSON-based workflows.
- **Subagent Swarms**: Deploy multiple specialized agents (Research, Coding, QA) in the `.claude` directory.
- **"The Architect"**: A visual builder to design and validate your agent plans.

### 🛠️ Advanced Tooling
- **MCP Converter ("The Transmuter")**: Instantly convert any MCP Server (`server.py`) into a Claude Code Skill.
- **"Plan Deployer"**: An MCP tool to programmatically deploy full agent orchestrators via JSON.
- **E2B Sandbox Integration**: Run untrusted agents in secure, isolated cloud sandboxes.

### 📊 Deep Observability
- **Session Monitor**: Real-time tracking of agent "thoughts", tool use, and output.
- **"Cronos" Scheduler**: Schedule agents to run on a recurring basis (cron).
- **RAG Memory**: Agents remember past sessions and learn from mistakes.

## 📂 The `.claude` Architecture

The `.claude` directory is the heart of your agent swarm. Each subdirectory represents a distinct "Plan" or "Orchestrator".

```
.claude/
├── research-team/          # Plan Name
│   ├── CLAUDE.md           # The "Brain": System prompt & instructions
│   ├── config.json         # The "Body": Model, temperature, tools
│   ├── scripts/            # Custom tools for this agent
│   └── memory/             # Agent-specific memory
├── coding-assistant/
│   └── ...
└── ...
```

### How to Deploy a New Agent
1. **Manual**: Create a folder in `.claude/`, add `CLAUDE.md` and `config.json`.
2. **Via MCP**: Use the "Plan Deployer" tool to send a JSON definition.
3. **Via Builder**: Use the GUI to design and save the plan.

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- Python 3.10+
- Docker (for PostgreSQL)
- E2B API Key (optional, for sandboxing)

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/aaaronmiller/super_agent_monitor.git
    cd super_agent_monitor
    ```

2.  **Setup Backend**
    ```bash
    cd backend
    cp .env.example .env  # Add your API keys!
    bun install
    bun run db:migrate
    bun run dev
    ```

3.  **Setup Frontend**
    ```bash
    cd ../frontend
    bun install
    bun run dev
    ```

4.  **Launch!**
    Open `http://localhost:5173` and behold the Command Center.

---

## 🏗️ Architecture: Local + Proxy

Unlike cloud-hosted solutions that introduce latency and privacy risks, Super Agent Monitor runs **Locally**.

1.  **SessionLauncher**: Spawns a child process (`claude`) on your machine.
2.  **ProxyService**: Starts a local HTTP server (e.g., port 3002).
3.  **Injection**: The `claude` process is configured with `HTTP_PROXY=http://127.0.0.1:3002`.
4.  **Control**: All traffic passes through our proxy, allowing us to log, monitor, and interrupt the stream at will.

---

## 🌌 Beyond MCP Integration

This project integrates experimental concepts from the `beyond-mcp` initiative, extending the capabilities of the Model Context Protocol.

### Features
- **MCP Transmuter**: Convert standard MCP servers into standalone "Skill" scripts using the [MCP Converter UI](/converter).
- **Example Servers**: Includes a sample MCP server (`beyond-mcp/apps/1_mcp_server`) that can be loaded directly in the converter.
- **Advanced Agents**: Additional agent definitions (e.g., `docs-scraper`) have been imported into the component library.

### Usage
1. Navigate to the **Converter** page in the dashboard.
2. Click **Load Example** to populate the form with the local example server.
3. Click **Transmute to Skill** to generate a Python script.
4. Use the generated skill in your agent workflows.

---

## 🤝 Contributing

We welcome contributions to the **Orchestration Library**. If you have a new prompting strategy or validation pattern, submit a PR to `components/orchestrators/templates/`.

**Built for the Agentic Future.**

