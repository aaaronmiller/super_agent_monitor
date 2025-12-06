<template>
  <div class="container mx-auto px-4 py-8">
    <div v-if="workflow" class="max-w-4xl mx-auto">
      <div class="mb-6">
        <router-link to="/workflows" class="text-primary-600 hover:text-primary-700 text-sm">
          ← Back to Workflows
        </router-link>
      </div>

      <div class="card mb-6">
        <div class="flex items-start justify-between mb-4">
          <div>
            <h1 class="text-3xl font-bold">{{ workflow.name }}</h1>
            <p class="text-gray-500 mt-1">Template: {{ workflow.template_id }}</p>
          </div>
          <div class="flex items-center gap-3">
            <span :class="['badge', workflow.status === 'active' ? 'badge-success' : 'badge-info']">
              {{ workflow.status }}
            </span>
            <button @click="showStartModal = true" class="btn btn-primary btn-sm">
              ▶ Start Session
            </button>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4 text-sm">
          <div>
            <span class="text-gray-500">Created:</span>
            <span class="ml-2">{{ formatDate(workflow.created_at) }}</span>
          </div>
          <div v-if="workflow.updated_at">
            <span class="text-gray-500">Updated:</span>
            <span class="ml-2">{{ formatDate(workflow.updated_at) }}</span>
          </div>
        </div>
      </div>

      <div class="card">
        <h2 class="text-xl font-bold mb-4">Recent Sessions</h2>
        <div v-if="workflow.recent_sessions?.length > 0" class="space-y-2">
          <router-link
            v-for="session in workflow.recent_sessions"
            :key="session.id"
            :to="`/sessions/${session.id}`"
            class="block p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <div class="flex items-center justify-between">
              <div>
                <div class="font-medium">Session {{ session.id.slice(0, 8) }}</div>
                <div class="text-sm text-gray-500">
                  Started: {{ formatDate(session.started_at) }}
                </div>
              </div>
              <span :class="['badge', getStatusClass(session.status)]">
                {{ session.status }}
              </span>
            </div>
          </router-link>
        </div>
        <div v-else class="text-gray-500 text-center py-8">
          No sessions yet
        </div>
      </div>
    </div>

    <!-- Start Session Modal -->
    <StartSessionModal
      v-if="showStartModal"
      :workflow-id="workflow.id"
      @close="showStartModal = false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import StartSessionModal from '../components/StartSessionModal.vue'

const route = useRoute()
const router = useRouter()
const workflowsStore = useWorkflowsStore()
const sessionsStore = useSessionsStore()
const componentsStore = useComponentsStore()


const workflow = ref<any>(null)
const showStartModal = ref(false)

onMounted(async () => {
  const id = route.params.id as string
  await Promise.all([
    workflowsStore.getWorkflow(id).then(w => workflow.value = w),
    componentsStore.fetchComponents({ category: 'orchestrator' })
  ])
})

function formatDate(dateString: string) {
  return new Date(dateString).toLocaleString()
}

function getStatusClass(status: string) {
  const classes: Record<string, string> = {
    completed: 'badge-success',
    active: 'badge-info',
    pending: 'badge-warning',
    failed: 'badge-error'
  }
  return classes[status] || 'badge-info'
}
</script>
