# Super Agent Monitor

**Autonomous multi-agent workflow management and monitoring platform for Claude Code**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Phase](https://img.shields.io/badge/Phase-Foundation_(Week_1)-blue)](IMPLEMENTATION-TASKS.md)

---

## 🚀 **What is This?**

Super Agent Monitor is a **visual orchestration platform** for autonomous Claude Code agent swarms. Think "Zapier for AI agents" or "Datadog for agent monitoring".

### **Key Features**

- 🎯 **One-Click Workflows**: Mix-and-match from 100+ pre-configured components
- 👁️ **Real-Time Monitoring**: Watch agents work with live token/cost tracking
- 🤖 **Autonomous Operation**: Headless sessions with intelligent stall detection
- 💰 **Cost Optimization**: 90%+ savings through smart model routing
- 🧠 **RAG Memory**: Agents learn from past successes across workflows
- 🔄 **Workflow Portability**: Share complete workflows as `.workflow` packages

---

## 📋 **Quick Start**

### **Prerequisites**

- Node.js 18+ or Bun 1.0+
- PostgreSQL 16+ with pgvector extension
- Docker & Docker Compose (optional but recommended)
- Claude Code installed globally
- claude-code-proxy installed globally

### **Installation**

```bash
# Clone repository
git clone https://github.com/aaaronmiller/super_agent_monitor.git
cd super_agent_monitor

# Copy environment variables
cp .env.example .env
# Edit .env with your API keys

# Start with Docker Compose (easiest)
docker-compose up

# OR install dependencies manually
cd backend && bun install
cd ../frontend && npm install

# Run database migrations
cd backend && bun run db:migrate

# Start services
cd backend && bun run dev
cd frontend && npm run dev
```

### **First Workflow**

1. Open http://localhost:5173
2. Click "New Workflow"
3. Select "Deep Research" template
4. Click "Start Workflow"
5. Watch agents work in real-time!

---

## 🏗️ **Architecture**

```
User Browser (Vue 3)
    ↓ REST API + SSE
Backend (Bun/Node.js)
    ↓
PostgreSQL + pgvector (Memory)
    ↓
Temp Workflows (.claude folders)
    ↓
Claude Code CLI (Headless)
    ↓
Claude Code Proxy (Interception Layer)
    ↓
Anthropic API (or OpenRouter/vLLM/Ollama)
```

**Key Decisions:**
- **Claude Code Proxy** sits between CLI and API for monitoring
- **Component Library** provides mix-and-match agents/skills/hooks
- **RAG Memory** enables cross-workflow learning
- **Orchestration Patterns**: CEO-Worker, Star, Round-Robin

See [PRD-FINAL.md](PRD-FINAL.md) for complete architecture documentation.

---

## 📦 **Component Library**

### **Agents** (5 currently, 20 planned)
- `researcher-primary`: Lead research coordinator
- `web-scraper`: Web content gathering
- `code-reviewer`: Quality & security review
- `tester`: Test generation specialist
- `analyzer`: Data analysis & insights

### **Skills** (1 currently, 20 planned)
- `web-search-advanced`: Expert search techniques

### **Orchestration Patterns**
- **CEO-Worker**: Planner + specialized workers (80% of use cases)
- **Star Topology**: Hub broadcasts, agents pull work (parallel execution)
- **Round-Robin**: Simple cycling (stateless tasks)

---

## 🎯 **Roadmap**

### **Phase 0** (Weeks 1-2) - Foundation ✅ IN PROGRESS
- [x] Database schema
- [x] Directory structure
- [x] Docker Compose setup
- [x] 5 example agents
- [ ] Component registry
- [ ] Basic API endpoints

### **Phase 1** (Weeks 3-5) - Workflow Engine
- [ ] Workflow generator (.yaml → .claude folder)
- [ ] Smart component recommendations
- [ ] Component library UI
- [ ] Workflow CRUD API

### **Phase 2** (Weeks 6-8) - Session Management
- [ ] Headless Claude Code launcher
- [ ] Stall detection & auto-recovery
- [ ] Session monitoring
- [ ] Session controls UI

### **Phase 3** (Weeks 9-11) - Monitoring Dashboard
- [ ] Integrate multi-agent-workflow backend
- [ ] Real-time event streaming
- [ ] Custom UI overlays (30%)
- [ ] Token/cost tracking

### **Phase 4** (Weeks 12-14) - RAG Memory
- [ ] Vector database (pgvector)
- [ ] Embedding service
- [ ] Semantic search
- [ ] Context injection

### **Phase 5** (Weeks 15-17) - Polish
- [ ] Cleanup scheduler
- [ ] Export/import workflows
- [ ] 100+ component library
- [ ] Documentation

### **Phase 6** (Week 18) - Beta
- [ ] Testing
- [ ] 10 beta users
- [ ] Launch!

**Post-MVP (Month 6+):**
- 🔥 **Model Debates** (viral feature): Watch AI models argue
- **Congress Voting**: Byzantine fault tolerance
- **Marketplace**: Community-shared workflows
- **Visual Editor**: Drag-and-drop workflow builder

See [IMPLEMENTATION-TASKS.md](IMPLEMENTATION-TASKS.md) for detailed task breakdown.

---

## 📊 **Project Status**

- **Current Phase**: Phase 0 (Week 1)
- **Progress**: 15% (Foundation complete)
- **Next Milestone**: Workflow generator (Week 3)
- **MVP Target**: Week 18
- **Total Effort**: 296 hours estimated

---

## 🤝 **Contributing**

We're currently in **early development** (pre-alpha). Contributions welcome once we hit beta (Week 18).

Interested in early access? [Join the waitlist](#) (coming soon)

---

## 📄 **License**

MIT License - see [LICENSE](LICENSE) for details.

### **Third-Party Licenses**

This project uses [multi-agent-workflow](https://github.com/apolopena/multi-agent-workflow) for monitoring capabilities, licensed under MIT.

See [ATTRIBUTIONS.md](ATTRIBUTIONS.md) for complete list of dependencies.

---

## 📚 **Documentation**

- [PRD-FINAL.md](PRD-FINAL.md) - Complete product requirements
- [IMPLEMENTATION-TASKS.md](IMPLEMENTATION-TASKS.md) - Detailed task breakdown
- [LICENSE-RECOMMENDATIONS.md](LICENSE-RECOMMENDATIONS.md) - Licensing strategy

---

## 🙋 **FAQ**

### **Q: Why another agent management tool?**
A: Existing tools require manual .claude folder configuration. We automate this with visual workflow management and real-time monitoring.

### **Q: How is this different from multi-agent-workflow?**
A: We extend multi-agent-workflow with workflow generation, component libraries, RAG memory, and autonomous session management.

### **Q: Can I use my own models?**
A: Yes! Configure any model via claude-code-proxy (Claude, GPT, Gemini, local models via Ollama/vLLM).

### **Q: What's the cost?**
A: Self-hosted is free (MIT license). You pay for API usage (Claude, OpenAI, etc.). We achieve 90%+ cost savings through smart routing.

### **Q: When will it be ready?**
A: MVP in 18 weeks (target: May 2025). Beta signups available soon.

---

## 📧 **Contact**

- **Issues**: [GitHub Issues](https://github.com/aaaronmiller/super_agent_monitor/issues)
- **Discussions**: [GitHub Discussions](https://github.com/aaaronmiller/super_agent_monitor/discussions)
- **Twitter**: [@super_agent_mon](https://twitter.com/super_agent_mon) (coming soon)

---

**Built with ❤️ for the AI agent community**

*"Making agent orchestration beautiful and accessible to everyone"*
