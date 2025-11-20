<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex items-center justify-between mb-8">
      <h1 class="text-3xl font-bold">Workflows</h1>
      <router-link to="/workflows/create" class="btn btn-primary">
        + Create Workflow
      </router-link>
    </div>

    <!-- Workflows Grid -->
    <div v-if="workflows.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="workflow in workflows"
        :key="workflow.id"
        class="card hover:shadow-md transition-shadow"
      >
        <div class="flex items-start justify-between mb-3">
          <div class="flex-1">
            <h3 class="font-bold text-lg">{{ workflow.name }}</h3>
            <p class="text-sm text-gray-500 mt-1">{{ workflow.template_id }}</p>
          </div>
          <span :class="['badge', getStatusClass(workflow.status)]">
            {{ workflow.status }}
          </span>
        </div>

        <div class="text-sm text-gray-600 mb-4">
          Created: {{ formatDate(workflow.created_at) }}
        </div>

        <div class="flex gap-2">
          <router-link :to="`/workflows/${workflow.id}`" class="btn btn-secondary flex-1 text-sm">
            View
          </router-link>
          <button @click="deleteWorkflow(workflow.id)" class="btn btn-secondary text-sm">
            Delete
          </button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-12">
      <div class="text-6xl mb-4">🔄</div>
      <h3 class="text-xl font-bold text-gray-700 mb-2">No Workflows Yet</h3>
      <p class="text-gray-500 mb-6">Create your first workflow to get started</p>
      <router-link to="/workflows/create" class="btn btn-primary">
        Create Workflow
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useWorkflowsStore } from '../stores/workflows'

const workflowsStore = useWorkflowsStore()
const workflows = computed(() => workflowsStore.workflows)

onMounted(async () => {
  await workflowsStore.fetchWorkflows()
})

async function deleteWorkflow(id: string) {
  if (confirm('Are you sure you want to delete this workflow?')) {
    await workflowsStore.deleteWorkflow(id)
  }
}

function getStatusClass(status: string) {
  return status === 'active' ? 'badge-success' : 'badge-info'
}

function formatDate(dateString: string) {
  return new Date(dateString).toLocaleDateString()
}
</script>
