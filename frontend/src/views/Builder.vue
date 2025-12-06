<template>
  <div class="h-[calc(100vh-64px)] flex flex-col">
    <!-- Header -->
    <div class="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Visual Agent Builder</h1>
        <p class="text-sm text-gray-500">Compose complex agents from modular components.</p>
      </div>
      <div class="flex items-center gap-3">
        <button @click="toggleJsonMode" class="btn btn-ghost text-sm">
          {{ showJson ? '👁️ Visual Editor' : '{} JSON Editor' }}
        </button>
        <button @click="savePlan" class="btn btn-primary" :disabled="saving">
          {{ saving ? 'Saving...' : '💾 Save Plan' }}
        </button>
        <button @click="deployPlan" class="btn btn-secondary" :disabled="deploying || !currentPlan.id">
          {{ deploying ? 'Deploying...' : '🚀 Deploy' }}
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="flex-1 flex overflow-hidden">
      
      <!-- JSON Editor Mode -->
      <div v-if="showJson" class="flex-1 bg-gray-900 p-4 overflow-hidden flex flex-col">
        <div class="flex justify-between items-center mb-2 text-gray-400 text-sm">
          <span>Edit Plan Configuration (JSON)</span>
          <span v-if="jsonError" class="text-red-400">{{ jsonError }}</span>
        </div>
        <textarea 
          v-model="jsonContent" 
          class="flex-1 w-full bg-gray-800 text-green-400 font-mono p-4 rounded border border-gray-700 focus:border-green-500 focus:ring-1 focus:ring-green-500 outline-none resize-none"
          spellcheck="false"
          @input="validateJson"
        ></textarea>
      </div>

      <!-- Visual Editor Mode -->
      <template v-else>
        <!-- Sidebar: Component Library -->
        <div class="w-80 bg-gray-50 border-r border-gray-200 flex flex-col">
          <div class="p-4 border-b border-gray-200">
            <h2 class="font-bold text-gray-700">Component Library</h2>
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="Search components..." 
              class="input w-full mt-2 text-sm"
            />
          </div>
          
          <div class="flex-1 overflow-y-auto p-4 space-y-6">
            <!-- Orchestrators -->
            <div>
              <h3 class="text-xs font-bold text-gray-500 uppercase mb-2">Orchestrators</h3>
              <div class="space-y-2">
                <div 
                  v-for="orch in filteredComponents.orchestrators" 
                  :key="orch.name"
                  class="bg-white p-3 rounded border border-gray-200 cursor-pointer hover:border-primary-500 hover:shadow-sm transition-all"
                  @click="selectOrchestrator(orch)"
                  :class="{ 'ring-2 ring-primary-500': currentPlan.orchestrator === orch.name }"
                >
                  <div class="font-medium text-sm">{{ orch.name }}</div>
                  <div class="text-xs text-gray-500 truncate">{{ orch.path }}</div>
                </div>
              </div>
            </div>

            <!-- Agents -->
            <div>
              <h3 class="text-xs font-bold text-gray-500 uppercase mb-2">Agents</h3>
              <div class="space-y-2">
                <div 
                  v-for="agent in filteredComponents.agents" 
                  :key="agent.name"
                  class="bg-white p-3 rounded border border-gray-200 cursor-pointer hover:border-primary-500 hover:shadow-sm transition-all"
                  @click="addAgent(agent)"
                >
                  <div class="flex items-center justify-between">
                    <span class="font-medium text-sm">{{ agent.name }}</span>
                    <span class="text-xs text-gray-400">+ Add</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Canvas: Plan Composition -->
        <div class="flex-1 bg-gray-100 p-8 overflow-y-auto">
          <div class="max-w-3xl mx-auto space-y-6">
            
            <!-- Plan Settings -->
            <div class="bg-white rounded-lg shadow p-6">
              <h3 class="text-lg font-bold mb-4">Plan Settings</h3>
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium mb-1">Plan Name</label>
                  <input v-model="currentPlan.name" type="text" class="input w-full" />
                </div>
                <div>
                  <label class="block text-sm font-medium mb-1">Version</label>
                  <input v-model="currentPlan.version" type="text" class="input w-full" />
                </div>
                <div class="col-span-2">
                  <label class="block text-sm font-medium mb-1">Description</label>
                  <textarea v-model="currentPlan.description" class="input w-full" rows="2"></textarea>
                </div>
              </div>
            </div>

            <!-- Selected Orchestrator -->
            <div class="bg-white rounded-lg shadow p-6 border-l-4 border-purple-500">
              <div class="flex items-center justify-between mb-2">
                <h3 class="text-lg font-bold text-purple-700">Orchestrator</h3>
                <span class="badge badge-purple">Core Logic</span>
              </div>
              <div v-if="currentPlan.orchestrator" class="text-gray-900 font-medium">
                {{ currentPlan.orchestrator }}
              </div>
              <div v-else class="text-gray-400 italic">
                Select an orchestrator from the library...
              </div>
            </div>

            <!-- Workflows / Agents -->
            <div class="space-y-4">
              <h3 class="text-lg font-bold text-gray-700">Workflows & Agents</h3>
              
              <div v-if="currentPlan.customComponents.length === 0" class="text-center py-8 border-2 border-dashed border-gray-300 rounded-lg">
                <p class="text-gray-500">No components added yet.</p>
                <p class="text-sm text-gray-400">Click items in the sidebar to add them.</p>
              </div>

              <div 
                v-for="(comp, idx) in currentPlan.customComponents" 
                :key="idx"
                class="bg-white rounded-lg shadow p-4 flex items-center justify-between border-l-4 border-blue-500"
              >
                <div>
                  <div class="font-medium">{{ comp.path.split('/').pop()?.replace('.md', '') }}</div>
                  <div class="text-xs text-gray-500 uppercase">{{ comp.type }}</div>
                </div>
                <button @click="removeComponent(idx)" class="text-red-500 hover:text-red-700">
                  ✕
                </button>
              </div>
            </div>

          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import api from '../services/api'

interface Component {
  name: string
  path: string
}

interface Plan {
  id?: string
  name: string
  version: string
  description: string
  orchestrator: string
  workflows: string[]
  customComponents: {
    type: 'mcp' | 'skill' | 'tool' | 'agent'
    path: string
  }[]
  settings: any
}

const components = ref<{ orchestrators: Component[], agents: Component[] }>({
  orchestrators: [],
  agents: []
})

const currentPlan = ref<Plan>({
  name: 'New Plan',
  version: '0.1.0',
  description: '',
  orchestrator: '',
  workflows: [],
  customComponents: [],
  settings: {}
})

const searchQuery = ref('')
const saving = ref(false)
const deploying = ref(false)
const showJson = ref(false)
const jsonContent = ref('')
const jsonError = ref('')

onMounted(async () => {
  await loadComponents()
})

async function loadComponents() {
  try {
    const { data } = await api.get('/plans/components')
    components.value = data
  } catch (error) {
    console.error('Failed to load components:', error)
  }
}

const filteredComponents = computed(() => {
  const q = searchQuery.value.toLowerCase()
  return {
    orchestrators: components.value.orchestrators.filter(c => c.name.toLowerCase().includes(q)),
    agents: components.value.agents.filter(c => c.name.toLowerCase().includes(q))
  }
})

function selectOrchestrator(orch: Component) {
  currentPlan.value.orchestrator = orch.name
}

function addAgent(agent: Component) {
  currentPlan.value.customComponents.push({
    type: 'agent',
    path: agent.path
  })
}

function removeComponent(index: number) {
  currentPlan.value.customComponents.splice(index, 1)
}

function toggleJsonMode() {
  if (showJson.value) {
    // Switching back to Visual
    try {
      const parsed = JSON.parse(jsonContent.value)
      currentPlan.value = parsed
      showJson.value = false
      jsonError.value = ''
    } catch (e) {
      jsonError.value = 'Invalid JSON: ' + (e as Error).message
    }
  } else {
    // Switching to JSON
    jsonContent.value = JSON.stringify(currentPlan.value, null, 2)
    showJson.value = true
  }
}

function validateJson() {
  try {
    JSON.parse(jsonContent.value)
    jsonError.value = ''
  } catch (e) {
    jsonError.value = (e as Error).message
  }
}

async function savePlan() {
  // Ensure we sync from JSON if in JSON mode
  if (showJson.value) {
    try {
      currentPlan.value = JSON.parse(jsonContent.value)
    } catch (e) {
      alert('Cannot save: Invalid JSON')
      return
    }
  }

  saving.value = true
  try {
    const { data } = await api.post('/plans', currentPlan.value)
    currentPlan.value = data
    if (showJson.value) {
      jsonContent.value = JSON.stringify(currentPlan.value, null, 2)
    }
    alert('Plan saved successfully!')
  } catch (error) {
    alert('Failed to save plan')
  } finally {
    saving.value = false
  }
}

async function deployPlan() {
  if (!currentPlan.value.id) return
  
  const targetDir = prompt('Enter target directory path for deployment:')
  if (!targetDir) return

  deploying.value = true
  try {
    await api.post(`/plans/${currentPlan.value.id}/deploy`, { targetDir })
    alert(`Plan deployed to ${targetDir}`)
  } catch (error) {
    alert('Failed to deploy plan')
  } finally {
    deploying.value = false
  }
}
</script>
