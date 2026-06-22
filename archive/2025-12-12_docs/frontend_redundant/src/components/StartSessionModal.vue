<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
      <h3 class="text-xl font-bold mb-4 text-gray-900 dark:text-white">Start New Session</h3>
      
      <!-- Council Pattern Selection -->
      <div class="mb-6 border-b border-gray-200 dark:border-gray-700 pb-6">
        <CouncilPatternSelector v-model="selectedOrchestrator" />
      </div>

      <!-- Local Model Selection (collapsible) -->
      <div class="mb-4">
        <button 
          @click="showLocalModels = !showLocalModels"
          class="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-blue-600"
        >
          <span>{{ showLocalModels ? '▼' : '▶' }}</span>
          Local Model Options (LM Studio)
        </button>
        <div v-if="showLocalModels" class="mt-3 pl-4 border-l-2 border-blue-200 dark:border-blue-700">
          <LocalModelSelector v-model="selectedLocalModel" @model-config="handleModelConfig" />
        </div>
      </div>

      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Initial Prompt (Optional)</label>
        <textarea 
          v-model="initialPrompt" 
          rows="3" 
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-900 text-gray-900 dark:text-white"
          placeholder="Describe the task for the agent..."
        ></textarea>
      </div>

      <div class="mb-4">
        <label class="flex items-center gap-2 cursor-pointer">
          <input type="checkbox" v-model="contextInjection" class="checkbox checkbox-primary">
          <span class="text-sm font-medium text-gray-700 dark:text-gray-300">Enable Context Injection (Auto-RAG)</span>
        </label>
        <p class="text-xs text-gray-500 dark:text-gray-400 mt-1 ml-6">
          Automatically search project history and inject relevant context into the agent's initial prompt.
        </p>
      </div>

      <div class="mb-6">
        <label class="flex items-center gap-2 cursor-pointer">
          <input type="checkbox" v-model="useE2B" class="checkbox checkbox-secondary">
          <span class="text-sm font-medium text-gray-700 dark:text-gray-300">Run in E2B Sandbox</span>
        </label>
        <p class="text-xs text-gray-500 dark:text-gray-400 mt-1 ml-6">
          Execute the agent in a secure, isolated cloud environment.
        </p>
      </div>

      <div class="flex justify-end gap-3">
        <button @click="$emit('close')" class="btn btn-secondary">Cancel</button>
        <button @click="startSession" :disabled="starting" class="btn btn-primary">
          {{ starting ? 'Starting...' : 'Start Session' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useSessionsStore } from '../stores/sessions'
import { useComponentsStore } from '../stores/components'
import { useRouter } from 'vue-router'
import CouncilPatternSelector from './CouncilPatternSelector.vue'
import LocalModelSelector from './LocalModelSelector.vue'

const props = defineProps<{
  workflowId: string
}>()

const emit = defineEmits(['close', 'started'])

const sessionsStore = useSessionsStore()
const componentsStore = useComponentsStore()
const router = useRouter()

const selectedOrchestrator = ref('')
const selectedLocalModel = ref('')
const initialPrompt = ref('')
const contextInjection = ref(true)
const useE2B = ref(false)
const starting = ref(false)
const showLocalModels = ref(false)

const orchestrators = computed(() => componentsStore.componentsByCategory.orchestrator || [])

interface ModelConfig {
  id: string;
  name: string;
  temperature?: number;
  max_tokens?: number;
}

const modelConfig = ref<ModelConfig | null>(null)

const handleModelConfig = (config: ModelConfig) => {
  modelConfig.value = config
}

onMounted(async () => {
  if (orchestrators.value.length === 0) {
    await componentsStore.fetchComponents({ category: 'orchestrator' })
  }
})

async function startSession() {
  starting.value = true
  try {
    const session = await sessionsStore.createSession(
      props.workflowId,
      selectedOrchestrator.value || undefined,
      initialPrompt.value,
      contextInjection.value,
      useE2B.value ? 'e2b' : 'local'
    )
    emit('started', session.id)
    router.push(`/sessions/${session.id}`)
  } catch (error) {
    alert('Failed to start session')
  } finally {
    starting.value = false
  }
}
</script>

