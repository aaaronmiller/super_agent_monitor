<template>
  <div class="container mx-auto px-4 py-8">
    <div v-if="session" class="max-w-6xl mx-auto">
      <div class="mb-6">
        <router-link to="/sessions" class="text-primary-600 hover:text-primary-700 text-sm">
          ← Back to Sessions
        </router-link>
      </div>

      <!-- Session Header -->
      <div class="card mb-6">
        <div class="flex items-start justify-between mb-4">
          <div>
            <h1 class="text-3xl font-bold">{{ session.workflow_name }}</h1>
            <p class="text-gray-500 mt-1">Session ID: {{ session.id }}</p>
          </div>
          <span :class="['badge text-lg px-4 py-2', getStatusClass(session.status)]">
            {{ session.status }}
          </span>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div>
            <div class="text-sm text-gray-500">Started</div>
            <div class="font-medium">{{ formatDate(session.started_at) }}</div>
          </div>
          <div v-if="session.completed_at">
            <div class="text-sm text-gray-500">Completed</div>
            <div class="font-medium">{{ formatDate(session.completed_at) }}</div>
          </div>
          <div v-if="session.cost_usd">
            <div class="text-sm text-gray-500">Cost</div>
            <div class="font-medium">${{ session.cost_usd.toFixed(4) }}</div>
          </div>
          <div v-if="session.input_tokens">
            <div class="text-sm text-gray-500">Total Tokens</div>
            <div class="font-medium">{{ (session.input_tokens + session.output_tokens).toLocaleString() }}</div>
          </div>
        </div>
      </div>

      <!-- Metrics -->
      <div v-if="metrics" class="card mb-6">
        <h2 class="text-xl font-bold mb-4">Metrics</h2>
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
            <div class="text-sm text-gray-500">Avg Cost/Token</div>
            <div class="text-2xl font-bold">
              {{ metrics.cost_usd && metrics.total_tokens ?
                `$${(metrics.cost_usd / metrics.total_tokens * 1000).toFixed(3)}` : 'N/A' }}
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Events -->
      <div class="card">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-bold">Recent Events</h2>
          <button @click="loadEvents" class="btn btn-secondary text-sm">
            Refresh
          </button>
        </div>

        <div v-if="events.length > 0" class="space-y-2">
          <div
            v-for="event in events"
            :key="event.id"
            class="p-4 bg-gray-50 rounded-lg"
          >
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <div class="font-medium">{{ event.type }}</div>
                <div class="text-sm text-gray-500">{{ formatDate(event.timestamp) }}</div>
                <pre v-if="event.data" class="text-xs text-gray-600 mt-2 overflow-x-auto">{{ JSON.stringify(event.data, null, 2) }}</pre>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="text-center py-8 text-gray-500">
          No events recorded yet
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useSessionsStore } from '../stores/sessions'

const route = useRoute()
const sessionsStore = useSessionsStore()

const session = ref<any>(null)
const metrics = ref<any>(null)
const events = ref<any[]>([])

onMounted(async () => {
  const id = route.params.id as string
  await loadSession(id)
  await loadMetrics(id)
  await loadEvents()
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

async function loadEvents() {
  try {
    const id = route.params.id as string
    const result = await sessionsStore.getSessionEvents(id, { limit: 20 })
    events.value = result.events
  } catch (error) {
    console.error('Failed to load events')
  }
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
</script>
