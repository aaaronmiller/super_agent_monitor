<template>
  <div class="container mx-auto px-4 py-8">
    <div v-if="session" class="max-w-6xl mx-auto">
      <div class="mb-6">
        <router-link to="/sessions" class="text-primary-600 hover:text-primary-700 text-sm">
          ← Back to Sessions
        </router-link>
      </div>

      <!-- Session Header with Control Panel -->
      <div class="card mb-6">
        <div class="flex items-start justify-between mb-4">
          <div>
            <div class="flex items-center gap-3">
              <h1 class="text-3xl font-bold">{{ session.workflow_name }}</h1>
              <span v-if="isConnected" class="w-3 h-3 bg-green-500 rounded-full animate-pulse" title="WebSocket Connected"></span>
              <span v-else class="w-3 h-3 bg-red-500 rounded-full" title="WebSocket Disconnected"></span>
            </div>
            <p class="text-gray-500 mt-1">Session ID: {{ session.id }}</p>
          </div>
          <span :class="['badge text-lg px-4 py-2', getStatusClass(liveStatus?.session?.status || session.status)]">
            {{ liveStatus?.session?.status || session.status }}
          </span>
        </div>

        <!-- Session Control Buttons -->
        <div class="flex gap-3 mb-4">
          <button
            v-if="session.status === 'pending'"
            @click="handleStart"
            :disabled="controlLoading"
            class="btn btn-primary"
          >
            <span v-if="!controlLoading">▶️ Start Session</span>
            <span v-else>Starting...</span>
          </button>

          <button
            v-if="session.status === 'active' || liveStatus?.live?.isActive"
            @click="handleStop"
            :disabled="controlLoading"
            class="btn btn-error"
          >
            <span v-if="!controlLoading">⏹️ Stop Session</span>
            <span v-else>Stopping...</span>
          </button>

          <button
            v-if="['active', 'stalled'].includes(session.status) || liveStatus?.live?.isActive"
            @click="handleKick"
            :disabled="controlLoading"
            class="btn btn-warning"
            title="Force interrupt (SIGINT)"
          >
            <span v-if="!controlLoading">🥾 Kick</span>
            <span v-else>Kicking...</span>
          </button>

          <button
            v-if="['active', 'stalled', 'failed'].includes(session.status)"
            @click="handleRestart"
            :disabled="controlLoading"
            class="btn btn-warning"
          >
            <span v-if="!controlLoading">🔄 Restart Session</span>
            <span v-else>Restarting...</span>
          </button>

          <button
            @click="handleClone"
            :disabled="controlLoading"
            class="btn btn-primary"
            title="Create a new session with same configuration"
          >
            <span v-if="!controlLoading">👯 Clone Session</span>
            <span v-else>Cloning...</span>
          </button>

          <button
            @click="loadSession(route.params.id as string)"
            class="btn btn-secondary"
            :disabled="controlLoading"
          >
            🔃 Refresh
          </button>
        </div>

        <!-- Live Status Info -->
        <div v-if="liveStatus?.live" class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
          <h3 class="font-semibold text-sm text-blue-900 mb-2">Live Status</h3>
          <div class="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm">
            <div>
              <span class="text-blue-600">Active:</span>
              <span class="ml-2 font-medium">{{ liveStatus.live.isActive ? '✅ Yes' : '❌ No' }}</span>
            </div>
            <div v-if="liveStatus.live.lastActivity">
              <span class="text-blue-600">Last Activity:</span>
              <span class="ml-2 font-medium">{{ liveStatus.live.timeSinceActivity }}s ago</span>
            </div>
            <div v-if="liveStatus.live.retryCount > 0">
              <span class="text-blue-600">Retries:</span>
              <span class="ml-2 font-medium">{{ liveStatus.live.retryCount }}</span>
            </div>
          </div>
        </div>

        <!-- Session Details -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div>
            <div class="text-sm text-gray-500">Started</div>
            <div class="font-medium">{{ formatDate(session.started_at) }}</div>
          </div>
          <div v-if="session.completed_at">
            <div class="text-sm text-gray-500">Completed</div>
            <div class="font-medium">{{ formatDate(session.completed_at) }}</div>
          </div>
          <div>
            <div class="text-sm text-gray-500">Cost</div>
            <div class="font-medium text-lg">
              ${{ (liveStatus?.session?.cost_usd || session.cost_usd || 0).toFixed(4) }}
            </div>
          </div>
          <div>
            <div class="text-sm text-gray-500">Total Tokens</div>
            <div class="font-medium text-lg">
              {{ ((liveStatus?.session?.input_tokens || session.input_tokens || 0) +
                  (liveStatus?.session?.output_tokens || session.output_tokens || 0)).toLocaleString() }}
            </div>
          </div>
        </div>
      </div>

      <!-- Token Usage Breakdown -->
      <div class="card mb-6">
        <h2 class="text-xl font-bold mb-4">Token Usage</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="bg-blue-50 p-4 rounded-lg">
            <div class="text-sm text-blue-600 mb-1">Input Tokens</div>
            <div class="text-2xl font-bold text-blue-900">
              {{ (liveStatus?.session?.input_tokens || session.input_tokens || 0).toLocaleString() }}
            </div>
            <div class="text-xs text-blue-500 mt-1">
              ${{ ((liveStatus?.session?.input_tokens || session.input_tokens || 0) / 1_000_000 * 3.0).toFixed(4) }}
            </div>
          </div>
          <div class="bg-purple-50 p-4 rounded-lg">
            <div class="text-sm text-purple-600 mb-1">Output Tokens</div>
            <div class="text-2xl font-bold text-purple-900">
              {{ (liveStatus?.session?.output_tokens || session.output_tokens || 0).toLocaleString() }}
            </div>
            <div class="text-xs text-purple-500 mt-1">
              ${{ ((liveStatus?.session?.output_tokens || session.output_tokens || 0) / 1_000_000 * 15.0).toFixed(4) }}
            </div>
          </div>
          <div class="bg-green-50 p-4 rounded-lg">
            <div class="text-sm text-green-600 mb-1">Total Cost</div>
            <div class="text-2xl font-bold text-green-900">
              ${{ estimatedCost.toFixed(4) }}
            </div>
            <div class="text-xs text-green-500 mt-1">
              Real-time Estimate (Kalman Filter)
            </div>
          </div>
        </div>
      </div>

      <!-- Live Terminal (Typewriter Effect) -->
      <div 
        class="card mb-6 bg-gray-900 text-green-400 font-mono cursor-pointer hover:bg-gray-800 transition-colors" 
        @click="flushTypewriter"
        title="Click to skip animation"
      >
        <div class="flex justify-between items-center mb-2 border-b border-gray-700 pb-2">
          <h2 class="text-lg font-bold">Live Terminal</h2>
          <span class="text-xs text-gray-500">Buffered Stream (Click to Skip)</span>
        </div>
        <pre class="whitespace-pre-wrap h-64 overflow-y-auto text-sm">{{ liveTerminalOutput || '> Waiting for output...' }}</pre>
      </div>

      <!-- Metrics -->
      <div v-if="metrics" class="card mb-6">
        <h2 class="text-xl font-bold mb-4">Session Metrics</h2>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
          <div>
            <div class="text-sm text-gray-500">Duration</div>
            <div class="text-2xl font-bold">{{ formatDuration(metrics.duration_seconds) }}</div>
          </div>
          <div>
            <div class="text-sm text-gray-500">Tool Calls</div>
            <div class="text-2xl font-bold">{{ metrics.tool_calls || 0 }}</div>
          </div>
          <div>
            <div class="text-sm text-gray-500">Errors</div>
            <div class="text-2xl font-bold" :class="metrics.errors > 0 ? 'text-red-600' : 'text-green-600'">
              {{ metrics.errors || 0 }}
            </div>
          </div>
          <div>
            <div class="text-sm text-gray-500">Avg Cost/1K Tokens</div>
            <div class="text-2xl font-bold">
              {{ metrics.cost_usd && metrics.total_tokens ?
                `$${(metrics.cost_usd / metrics.total_tokens * 1000).toFixed(3)}` : 'N/A' }}
            </div>
          </div>
        </div>
      </div>

      <!-- Real-time Events Stream -->
      <div class="card">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-bold">Live Events</h2>
          <div class="flex gap-2 items-center">
            <span v-if="isConnected" class="text-xs text-green-600 font-medium">● Live</span>
            <span v-else class="text-xs text-red-600 font-medium">● Disconnected</span>
            <button @click="clearEvents" class="btn btn-secondary text-sm">
              Clear
            </button>
          </div>
        </div>

        <div v-if="realtimeEvents.length > 0" class="space-y-2 max-h-96 overflow-y-auto">
          <div
            v-for="(event, idx) in realtimeEvents"
            :key="idx"
            :class="['p-4 rounded-lg border-l-4', getEventClass(event.type)]"
          >
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <div class="flex items-center gap-2">
                  <span class="font-medium">{{ event.type }}</span>
                  <span v-if="event.type.includes('stalled')" class="text-xs bg-yellow-100 text-yellow-800 px-2 py-0.5 rounded">
                    ⚠️ Stalled
                  </span>
                  <span v-if="event.type.includes('restarted')" class="text-xs bg-blue-100 text-blue-800 px-2 py-0.5 rounded">
                    🔄 Restarted
                  </span>
                  <span v-if="event.type === 'system_context'" class="text-xs bg-purple-100 text-purple-800 px-2 py-0.5 rounded">
                    🧠 Context Injected
                  </span>
                </div>
                <div class="text-sm text-gray-500 mt-1">{{ formatDate(event.timestamp) }}</div>
                
                <div v-if="event.type === 'system_context'" class="mt-2">
                  <details class="bg-white bg-opacity-50 p-2 rounded text-sm border border-purple-200">
                    <summary class="cursor-pointer font-medium text-purple-900 select-none">
                      Injected {{ event.data?.count || 0 }} memories
                    </summary>
                    <div class="mt-2 space-y-2 pl-2">
                      <div v-for="(mem, mIdx) in event.data?.memories" :key="mIdx" class="text-xs text-gray-700 border-l-2 border-purple-300 pl-2 bg-white p-2 rounded shadow-sm">
                        <div class="flex justify-between text-purple-700 mb-1">
                          <span class="font-bold">{{ formatDate(mem.timestamp) }}</span>
                          <span>Score: {{ mem.score?.toFixed(2) }}</span>
                        </div>
                        <div class="whitespace-pre-wrap font-mono text-gray-600">{{ mem.content }}</div>
                      </div>
                    </div>
                  </details>
                </div>

                <div v-else-if="event.type === 'session:tool_use' || event.type === 'tool_use'" class="mt-2">
                  <div class="bg-white bg-opacity-50 p-3 rounded text-sm border border-blue-200">
                    <div class="flex items-center gap-2 mb-2">
                      <span class="font-bold text-blue-800">🛠️ {{ event.data?.tool }}</span>
                      <span class="text-xs text-blue-600 bg-blue-100 px-2 py-0.5 rounded-full">Tool Call</span>
                    </div>
                    <div class="bg-gray-900 text-gray-300 p-2 rounded font-mono text-xs overflow-x-auto">
                      {{ JSON.stringify(event.data?.input, null, 2) }}
                    </div>
                  </div>
                </div>

                <pre v-else-if="event.data" class="text-xs text-gray-600 mt-2 overflow-x-auto bg-gray-50 p-2 rounded">{{ JSON.stringify(event.data, null, 2) }}</pre>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="text-center py-8 text-gray-500">
          <p>Waiting for events...</p>
          <p class="text-sm mt-2">Real-time events will appear here when the session is active</p>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-12">
      <p class="text-gray-500">Loading session...</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useSessionsStore } from '../stores/sessions'
import { useWebSocket, type WSMessage } from '../composables/useWebSocket'
import { CostEstimator } from '../utils/CostEstimator'
import { Typewriter } from '../utils/Typewriter'

const route = useRoute()
const sessionsStore = useSessionsStore()

const session = ref<any>(null)
const metrics = ref<any>(null)
const liveStatus = ref<any>(null)
const realtimeEvents = ref<WSMessage[]>([])
const controlLoading = ref(false)

// Runtime Reliability State
const estimatedCost = ref(0)
const liveTerminalOutput = ref('')
const estimator = new CostEstimator()
const typewriter = new Typewriter((text) => {
  liveTerminalOutput.value = text
})
let animationFrameId: number | null = null

// WebSocket connection
const { isConnected, subscribe, unsubscribe } = useWebSocket({
  url: '/ws',
  onMessage: (message: WSMessage) => {
    handleWebSocketMessage(message)
  },
  onConnect: () => {
    console.log('WebSocket connected, subscribing to session')
    const sessionId = route.params.id as string
    subscribe(sessionId)
  }
})

onMounted(async () => {
  const id = route.params.id as string
  await loadSession(id)
  await loadMetrics(id)
  await loadLiveStatus(id)
  
  // Initialize estimator with current cost
  if (session.value?.cost_usd) {
    estimator.updateMeasurement(session.value.cost_usd)
    estimatedCost.value = session.value.cost_usd
  }

  // Start animation loop for cost prediction
  let lastTime = performance.now()
  const loop = () => {
    const now = performance.now()
    const dt = (now - lastTime) / 1000
    lastTime = now
    
    estimatedCost.value = estimator.predict(dt)
    animationFrameId = requestAnimationFrame(loop)
  }
  loop()
})

onUnmounted(() => {
  const sessionId = route.params.id as string
  unsubscribe(sessionId)
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId)
  }
  typewriter.reset()
})

async function loadSession(id: string) {
  session.value = await sessionsStore.getSession(id)
}

async function loadMetrics(id: string) {
  try {
    metrics.value = await sessionsStore.getSessionMetrics(id)
  } catch (error) {
    console.error('Failed to load metrics')
  }
}

async function loadLiveStatus(id: string) {
  try {
    liveStatus.value = await sessionsStore.getSessionStatus(id)
  } catch (error) {
    console.error('Failed to load live status')
  }
}

async function handleStart() {
  controlLoading.value = true
  try {
    const id = route.params.id as string
    await sessionsStore.startSession(id)
    await loadSession(id)
    await loadLiveStatus(id)
  } catch (error) {
    console.error('Failed to start session:', error)
    alert('Failed to start session')
  } finally {
    controlLoading.value = false
  }
}

async function handleStop() {
  controlLoading.value = true
  try {
    const id = route.params.id as string
    await sessionsStore.stopSession(id)
    await loadSession(id)
    await loadLiveStatus(id)
  } catch (error) {
    console.error('Failed to stop session:', error)
    alert('Failed to stop session')
  } finally {
    controlLoading.value = false
  }
}

async function handleRestart() {
  if (!confirm('Are you sure you want to restart this session?')) return

  controlLoading.value = true
  try {
    const id = route.params.id as string
    const result = await sessionsStore.restartSession(id)

    // Navigate to new session if different ID
    if (result.newSessionId && result.newSessionId !== id) {
      alert(`Session restarted with new ID: ${result.newSessionId}`)
      // Optionally navigate to new session
      // router.push(`/sessions/${result.newSessionId}`)
    }

    await loadSession(id)
    await loadLiveStatus(id)
  } catch (error) {
    console.error('Failed to restart session:', error)
    alert('Failed to restart session')
  } finally {
    controlLoading.value = false
  }
}

async function handleClone() {
  if (!confirm('Create a new session with the same configuration?')) return

  controlLoading.value = true
  try {
    const id = route.params.id as string
    const result = await sessionsStore.cloneSession(id)
    
    if (result.newSessionId) {
      alert(`Session cloned! New ID: ${result.newSessionId}`)
      // Navigate to new session
      // router.push(`/sessions/${result.newSessionId}`)
    }
  } catch (error) {
    console.error('Failed to clone session:', error)
    alert('Failed to clone session')
  } finally {
    controlLoading.value = false
  }
}

function handleWebSocketMessage(message: WSMessage) {
  console.log('WebSocket message:', message)

  // Add to events feed
  realtimeEvents.value.unshift(message)

  // Keep only last 100 events
  if (realtimeEvents.value.length > 100) {
    realtimeEvents.value = realtimeEvents.value.slice(0, 100)
  }

  // Update session data based on event type
  if (message.type === 'session:launched' || message.type === 'session:exit' || message.type === 'session:stalled') {
    const id = route.params.id as string
    loadSession(id)
    loadLiveStatus(id)
  }

  // Update metrics if we received token usage info
  if (message.data?.usage || message.data?.tokens) {
    const id = route.params.id as string
    loadLiveStatus(id)
  }
  
  // Feed Runtime Reliability Utilities
  if (message.data?.cost_usd) {
    estimator.updateMeasurement(message.data.cost_usd)
  }
  
  // Handle Terminal Output (stdout or session:output)
  if (message.type === 'stdout' && message.data?.text) {
    typewriter.push(message.data.text)
  } else if (message.type === 'session:output' && message.data?.message) {
    typewriter.push(message.data.message)
  }
  
  if (message.type === 'session:thinking') {
    estimator.setThinking(true)
  } else if (message.type === 'session:generating' || message.type === 'stdout' || message.type === 'session:output') {
    estimator.setThinking(false)
  }
}

function clearEvents() {
  realtimeEvents.value = []
}

function flushTypewriter() {
  typewriter.flush()
}

function formatDate(dateString: string) {
  return new Date(dateString).toLocaleString()
}

function formatDuration(seconds: number) {
  if (seconds < 60) return `${Math.round(seconds)}s`
  const minutes = Math.floor(seconds / 60)
  const secs = Math.round(seconds % 60)
  return `${minutes}m ${secs}s`
}

function getStatusClass(status: string) {
  const classes: Record<string, string> = {
    completed: 'badge-success',
    active: 'badge-info',
    pending: 'badge-warning',
    failed: 'badge-error',
    stalled: 'badge-warning'
  }
  return classes[status] || 'badge-info'
}

function getEventClass(eventType: string) {
  if (eventType.includes('error') || eventType.includes('failed')) {
    return 'bg-red-50 border-red-500'
  }
  if (eventType.includes('stalled')) {
    return 'bg-yellow-50 border-yellow-500'
  }
  if (eventType.includes('launched') || eventType.includes('restarted')) {
    return 'bg-green-50 border-green-500'
  }
  if (eventType.includes('tool_use')) {
    return 'bg-blue-50 border-blue-500'
  }
  if (eventType === 'system_context') {
    return 'bg-purple-50 border-purple-500'
  }
  return 'bg-gray-50 border-gray-300'
}
</script>
