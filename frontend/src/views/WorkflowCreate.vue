<template>
  <div class="container mx-auto px-4 py-8 max-w-4xl">
    <h1 class="text-3xl font-bold mb-8">Create Workflow</h1>

    <div class="card">
      <h2 class="text-xl font-bold mb-6">Select Template</h2>

      <div v-if="loading" class="text-center py-12">
        <div class="text-gray-500">Loading templates...</div>
      </div>

      <div v-else class="space-y-4">
        <div
          v-for="template in templates"
          :key="template.id"
          class="p-4 border-2 rounded-lg cursor-pointer transition-all"
          :class="selectedTemplate === template.id ? 'border-primary-500 bg-primary-50' : 'border-gray-200 hover:border-gray-300'"
          @click="selectedTemplate = template.id"
        >
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <h3 class="font-bold text-lg">{{ template.name }}</h3>
              <p class="text-sm text-gray-600 mt-1">{{ template.description }}</p>

              <div class="flex gap-2 mt-3">
                <span class="badge badge-info">{{ template.pattern }}</span>
                <span class="badge bg-gray-100 text-gray-700">{{ template.model }}</span>
              </div>

              <div class="grid grid-cols-4 gap-4 mt-3 text-sm">
                <div>
                  <span class="text-gray-500">Agents:</span>
                  <span class="font-medium ml-1">{{ template.components.agents }}</span>
                </div>
                <div>
                  <span class="text-gray-500">Skills:</span>
                  <span class="font-medium ml-1">{{ template.components.skills }}</span>
                </div>
                <div>
                  <span class="text-gray-500">Hooks:</span>
                  <span class="font-medium ml-1">{{ template.components.hooks }}</span>
                </div>
                <div>
                  <span class="text-gray-500">Scripts:</span>
                  <span class="font-medium ml-1">{{ template.components.scripts }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="selectedTemplate" class="pt-6 border-t">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Workflow Name (optional)
          </label>
          <input
            v-model="workflowName"
            type="text"
            placeholder="My Custom Workflow"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
          />
        </div>

        <div v-if="selectedTemplate" class="flex gap-3 pt-4">
          <button @click="createWorkflow" :disabled="creating" class="btn btn-primary flex-1">
            {{ creating ? 'Creating...' : 'Create Workflow' }}
          </button>
          <button @click="$router.push('/workflows')" class="btn btn-secondary">
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useWorkflowsStore } from '../stores/workflows'

const router = useRouter()
const workflowsStore = useWorkflowsStore()

const selectedTemplate = ref('')
const workflowName = ref('')
const creating = ref(false)

const templates = computed(() => workflowsStore.templates)
const loading = computed(() => workflowsStore.loading)

onMounted(async () => {
  await workflowsStore.fetchTemplates()
})

async function createWorkflow() {
  creating.value = true
  try {
    const workflow = await workflowsStore.createWorkflow(
      selectedTemplate.value,
      workflowName.value || undefined
    )
    alert('Workflow created successfully!')
    router.push(`/workflows/${workflow.id}`)
  } catch (error) {
    alert('Failed to create workflow')
  } finally {
    creating.value = false
  }
}
</script>
