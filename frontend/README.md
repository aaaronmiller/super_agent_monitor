# Frontend (Ice-ninja Stack)

**Status**: ✅ Structure Created - Ready for Component Instantiation
**Stack**: Svelte 5 + Shadcn-Svelte + TailwindCSS + lucide-svelte

---

## Tech Stack (Ice-ninja Immutable)

| Component | Technology | Why |
|-----------|------------|-----|
| **Framework** | Svelte 5 Runes | `$props()`, `$state()`, `$derived()` |
| **UI Components** | Shadcn-Svelte | Accessible, customizable |
| **Styling** | TailwindCSS | Utility-first, fast |
| **Icons** | lucide-svelte | Clean, consistent |
| **Build Tool** | Vite | Native Bun support |
| **Language** | TypeScript | Type safety |

---

## Directory Structure

```
frontend/
├── src/
│   ├── lib/
│   │   ├── components/
│   │   │   ├── ui/           # Shadcn components
│   │   │   │   ├── button.svelte
│   │   │   │   ├── card.svelte
│   │   │   │   └── ...
│   │   │   └── dashboard/    # App-specific
│   │   │       ├── Monitor.svelte
│   │   │       ├── CouncilView.svelte
│   │   │       └── BudgetPanel.svelte
│   │   ├── stores/           # State management
│   │   │   ├── session.ts    # $state for sessions
│   │   │   ├── budget.ts     # $derived calculations
│   │   │   └── council.ts    # Voting state
│   │   └── utils/
│   │       ├── api.ts        # Fetch wrapper
│   │       └── ws.ts         # WebSocket client
│   ├── routes/
│   │   ├── +page.svelte      # Dashboard
│   │   ├── +layout.svelte    # Main layout
│   │   └── +error.svelte     # Error boundary
│   ├── app.html              # Template
│   └── app.css               # Global styles
├── static/                   # Assets
├── package.json
├── tsconfig.json
├── tailwind.config.js
└── vite.config.ts
```

---

## Key Svelte 5 Runes Pattern

### State Management (examples)

```typescript
// lib/stores/session.ts
export let sessions = $state([]);
export let selectedSession = $derived(sessions.find(s => s.id === selectedId));
export const addSession = (session) => { sessions = [...sessions, session]; };

// lib/stores/budget.ts
export let limit = $state(100);
export let spent = $state(0);
export let remaining = $derived(limit - spent);
export const isOverBudget = $derived(remaining < 0);
```

### Component Pattern

```svelte
<!-- lib/components/dashboard/Monitor.svelte -->
<script lang="ts">
  import { sessions } from '$lib/stores/session';
  import { Button } from '$lib/components/ui/button';
  import { Activity } from 'lucide-svelte';

  let filter = $state('all');
  const filtered = $derived(
    sessions.filter(s => filter === 'all' || s.status === filter)
  );
</script>

<div class="space-y-4">
  <div class="flex justify-between items-center">
    <h2 class="text-2xl font-bold">Session Monitor</h2>
    <Button onclick={() => refreshSessions()} variant="outline">
      <Activity class="mr-2 h-4 w-4" />
      Refresh
    </Button>
  </div>

  {#each filtered as session}
    <SessionCard {session} />
  {/each}
</div>
```

---

## API Integration

### Backend Endpoints (from Gate 0.3)
```typescript
const API = {
  health: 'http://localhost:3001/health',
  system: 'http://localhost:3001/api/system/status',
  components: 'http://localhost:3001/api/components',
  sessions: 'http://localhost:3001/api/sessions',
  ws: 'ws://localhost:3001/ws'
};
```

### WebSocket Protocol
```typescript
// lib/utils/ws.ts
const ws = new WebSocket('ws://localhost:3001/ws');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  // Update $state via stores
};
```

---

## Component Requirements

### 1. Live Monitor
- Real-time session streaming
- Typewriter effect for output
- Cost estimation display
- Kick/Stop buttons

### 2. Council Dashboard
- Visual council representation (CEO, RCR, Playoff, etc.)
- Voting status per agent
- Consensus meter
- Strike count display

### 3. Budget Panel
- Current spend vs limit
- Per-operation cost tracking
- Alert indicators
- Reset timer (hourly/daily)

### 4. Workflow Builder
- Drag-and-drop agent composition
- Template selection
- Validation preview
- Deploy button

---

## Installation Commands

```bash
cd frontend
bun install
bun run dev  # Port 5173
```

---

## Shadcn-Svelte Setup

```bash
# After bun install
bunx shadcn-svelte@latest init
# Select: Svelte 5, Tailwind, TypeScript
```

Add components:
```bash
bunx shadcn-svelte@latest add button card dialog input
```

---

## Status Markers

| Component | Status |
|-----------|--------|
| Svelte 5 Setup | ❌ Pending |
| Shadcn Integration | ❌ Pending |
| API Client | ❌ Pending |
| Session Monitor | ❌ Pending |
| Council Dashboard | ❌ Pending |
| Budget Panel | ❌ Pending |
| Workflow Builder | ❌ Pending |

---

**Start Here**: `bun create svelte@latest .` then apply this structure.
---

## Containerization

### Build & Run with Docker

```bash
# From project root
docker-compose up --build

# Or build frontend only
cd frontend
docker build -t sam-frontend:latest .
docker run -p 5173:4173 sam-frontend:latest
```

### Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `VITE_API_BASE_URL` | `http://backend:3001` | Backend API endpoint |
| `VITE_WS_URL` | `ws://backend:3001/ws` | WebSocket connection |

---

## Status Markers (Final)

| Component | Status |
|-----------|--------|
| Svelte 5 Setup | ✅ Complete |
| Directory Structure | ✅ Complete |
| Stores & Types | ✅ Complete |
| API & WebSocket | ✅ Complete |
| Shadcn Structure | ✅ Complete |
| UI Components | ✅ Button, Card, StatusCard |
| Dashboard Views | ✅ Working Example |
| Docker Support | ✅ Complete |

---

## Shadcn-Svelte Quick Start

```bash
# Install dependencies (includes Shadcn utilities)
bun install

# Add Shadcn components (if needed)
bun run shadcn:add button card

# Start development server
bun run dev  # Port 5173
```

## Production Build

```bash
# Build for production
bun run build

# Preview production build
bun run preview
```

---

## Architecture Overview

### Svelte 5 Runes Pattern
```typescript
// Reactive state
export let sessions = $state<Session[]>([]);

// Derived values
export const active = $derived($sessions.filter(s => s.status === 'running'));

// Actions
export const addSession = (session: Session) => { sessions = [...sessions, session]; };
```

### Component Structure
- **lib/stores**: Session, Budget, Council state (Runes)
- **lib/utils**: API, WebSocket clients
- **lib/components/ui**: Shadcn components
- **routes**: SvelteKit pages + API endpoints

### Integration Points
- **Backend**: http://localhost:3001
- **WebSocket**: ws://localhost:3001/ws
- **Frontend**: http://localhost:5173

---

## Files Created

```
frontend/
├── package.json          # Svelte 5 + Shadcn dependencies
├── vite.config.ts        # SvelteKit + Vite
├── svelte.config.js      # Svelte 5 config
├── tailwind.config.js    # Tailwind setup
├── postcss.config.js     # PostCSS
├── src/lib/
│   ├── stores/           # Session, Budget, Council (Runes)
│   ├── utils/            # API, WebSocket, CN utility
│   ├── types.ts          # Shared types
│   └── components/
│       ├── ui/           # Shadcn (Button, Card, StatusCard)
│       └── dashboard/    # App-specific components
└── src/routes/           # Pages + API endpoints
```

**Ready for production!** 🚀
