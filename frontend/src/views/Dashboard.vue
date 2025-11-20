<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-8">Dashboard</h1>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div class="card">
        <div class="text-sm text-gray-500 mb-1">Total Components</div>
        <div class="text-3xl font-bold">{{ stats?.total || 0 }}</div>
        <div class="text-xs text-gray-400 mt-2">
          {{ stats?.lastScan ? `Last scan: ${formatDate(stats.lastScan)}` : 'Not scanned yet' }}
        </div>
      </div>

      <div class="card">
        <div class="text-sm text-gray-500 mb-1">Workflows</div>
        <div class="text-3xl font-bold">{{ workflows.length }}</div>
        <router-link to="/workflows" class="text-xs text-primary-600 hover:text-primary-700 mt-2 inline-block">
          View all →
        </router-link>
      </div>

      <div class="card">
        <div class="text-sm text-gray-500 mb-1">Active Sessions</div>
        <div class="text-3xl font-bold">{{ activeSessions.length }}</div>
        <router-link to="/sessions" class="text-xs text-primary-600 hover:text-primary-700 mt-2 inline-block">
          Monitor →
        </router-link>
      </div>

      <div class="card">
        <div class="text-sm text-gray-500 mb-1">Phase Progress</div>
        <div class="text-3xl font-bold">35%</div>
        <div class="text-xs text-gray-400 mt-2">Phase 1 - MVP</div>
      </div>
    </div>

    <!-- Component Breakdown -->
    <div class="card mb-8">
      <h2 class="text-xl font-bold mb-4">Component Library</h2>
      <div class="grid grid-cols-5 gap-4">
        <div v-for="(count, category) in stats?.byCategory" :key="category" class="text-center">
          <div class="text-2xl font-bold text-primary-600">{{ count }}</div>
          <div class="text-sm text-gray-600 capitalize">{{ category }}s</div>
        </div>
      </div>
      <div class="mt-6">
        <router-link to="/components" class="btn btn-primary">
          Browse Components →
        </router-link>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="card">
        <h3 class="text-lg font-bold mb-4">Quick Actions</h3>
        <div class="space-y-3">
          <router-link to="/workflows/create" class="block w-full btn btn-primary text-left">
            🚀 Create New Workflow
          </router-link>
          <button @click="rescanComponents" :disabled="loading" class="w-full btn btn-secondary text-left">
            🔄 Rescan Components
          </button>
          <router-link to="/components" class="block w-full btn btn-secondary text-left">
            📚 Browse Library
          </router-link>
        </div>
      </div>

      <div class="card">
        <h3 class="text-lg font-bold mb-4">Recent Sessions</h3>
        <div v-if="sessions.length === 0" class="text-gray-500 text-sm">
          No sessions yet. Create a workflow to get started!
        </div>
        <div v-else class="space-y-2">
          <router-link
            v-for="session in sessions.slice(0, 5)"
            :key="session.id"
            :to="`/sessions/${session.id}`"
            class="block p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <div class="flex items-center justify-between">
              <div class="flex-1">
                <div class="font-medium text-sm">{{ session.workflow_name }}</div>
                <div class="text-xs text-gray-500">{{ formatDate(session.started_at) }}</div>
              </div>
              <span :class="['badge', getStatusBadgeClass(session.status)]">
                {{ session.status }}
              </span>
            </div>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed, ref } from 'vue'
import { useComponentsStore } from '../stores/components'
import { useWorkflowsStore } from '../stores/workflows'
import { useSessionsStore } from '../stores/sessions'

const componentsStore = useComponentsStore()
const workflowsStore = useWorkflowsStore()
const sessionsStore = useSessionsStore()

const stats = computed(() => componentsStore.stats)
const workflows = computed(() => workflowsStore.workflows)
const sessions = computed(() => sessionsStore.sessions)
const loading = ref(false)

const activeSessions = computed(() =>
  sessions.value.filter(s => s.status === 'active' || s.status === 'pending')
)

onMounted(async () => {
  await Promise.all([
    componentsStore.fetchStats(),
    workflowsStore.fetchWorkflows(),
    sessionsStore.fetchSessions({ limit: 10 })
  ])
})

async function rescanComponents() {
  loading.value = true
  try {
    await componentsStore.rescan()
    alert('Components rescanned successfully!')
  } catch (error) {
    alert('Failed to rescan components')
  } finally {
    loading.value = false
  }
}

function formatDate(dateString: string) {
  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffMins = Math.floor(diffMs / 60000)

  if (diffMins < 1) return 'Just now'
  if (diffMins < 60) return `${diffMins}m ago`

  const diffHours = Math.floor(diffMins / 60)
  if (diffHours < 24) return `${diffHours}h ago`

  const diffDays = Math.floor(diffHours / 24)
  if (diffDays < 7) return `${diffDays}d ago`

  return date.toLocaleDateString()
}

function getStatusBadgeClass(status: string) {
  switch (status) {
    case 'completed': return 'badge-success'
    case 'active': return 'badge-info'
    case 'pending': return 'badge-warning'
    case 'failed': return 'badge-error'
    default: return 'badge-warning'
  }
}
</script>
