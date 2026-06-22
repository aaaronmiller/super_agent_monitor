<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-8">Sessions</h1>

    <!-- Filters -->
    <div class="card mb-6">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <select
          v-model="statusFilter"
          @change="fetchFilteredSessions"
          class="px-4 py-2 border border-gray-300 rounded-lg"
        >
          <option value="">All Statuses</option>
          <option value="pending">Pending</option>
          <option value="active">Active</option>
          <option value="completed">Completed</option>
          <option value="failed">Failed</option>
          <option value="stalled">Stalled</option>
        </select>
      </div>
    </div>

    <!-- Sessions List -->
    <div v-if="sessions.length > 0" class="space-y-4">
      <router-link
        v-for="session in sessions"
        :key="session.id"
        :to="`/sessions/${session.id}`"
        class="card hover:shadow-md transition-shadow block"
      >
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <div class="flex items-center gap-3 mb-2">
              <h3 class="font-bold text-lg">{{ session.workflow_name }}</h3>
              <span :class="['badge', getStatusClass(session.status)]">
                {{ session.status }}
              </span>
            </div>

            <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-gray-600">
              <div>
                <span class="text-gray-500">Started:</span>
                <span class="ml-1">{{ formatDate(session.started_at) }}</span>
              </div>
              <div v-if="session.completed_at">
                <span class="text-gray-500">Completed:</span>
                <span class="ml-1">{{ formatDate(session.completed_at) }}</span>
              </div>
              <div v-if="session.cost_usd">
                <span class="text-gray-500">Cost:</span>
                <span class="ml-1">${{ session.cost_usd.toFixed(4) }}</span>
              </div>
              <div v-if="session.input_tokens">
                <span class="text-gray-500">Tokens:</span>
                <span class="ml-1">{{ (session.input_tokens + session.output_tokens).toLocaleString() }}</span>
              </div>
            </div>
          </div>
        </div>
      </router-link>
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-12">
      <div class="text-6xl mb-4">📊</div>
      <h3 class="text-xl font-bold text-gray-700 mb-2">No Sessions Found</h3>
      <p class="text-gray-500">Create a workflow and start a session</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useSessionsStore } from '../stores/sessions'

const sessionsStore = useSessionsStore()
const statusFilter = ref('')

const sessions = computed(() => sessionsStore.sessions)

onMounted(async () => {
  await fetchFilteredSessions()
})

async function fetchFilteredSessions() {
  const params: any = { limit: 50 }
  if (statusFilter.value) {
    params.status = statusFilter.value
  }
  await sessionsStore.fetchSessions(params)
}

function formatDate(dateString: string) {
  const date = new Date(dateString)
  return date.toLocaleString()
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
