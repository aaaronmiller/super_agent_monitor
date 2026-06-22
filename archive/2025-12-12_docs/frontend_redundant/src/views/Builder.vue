<template>
  <div class="h-[calc(100vh-64px)] flex flex-col bg-[#0f172a]">
    <!-- Toast Notification -->
    <Transition name="toast">
      <div 
        v-if="toast.show" 
        class="fixed top-4 right-4 z-50 px-4 py-3 rounded-lg shadow-lg flex items-center gap-2"
        :class="toast.type === 'success' ? 'bg-emerald-600 text-white' : 'bg-red-600 text-white'"
      >
        <span>{{ toast.type === 'success' ? '✓' : '✕' }}</span>
        <span>{{ toast.message }}</span>
      </div>
    </Transition>

    <!-- Deploy Modal -->
    <div v-if="showDeployModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-40">
      <div class="bg-[#1e293b] rounded-lg p-6 w-96 shadow-xl border border-slate-700">
        <h3 class="text-lg font-bold text-white mb-4">Deploy Plan</h3>
        <label class="block text-sm text-slate-400 mb-2">Target Directory</label>
        <input 
          v-model="deployTargetDir" 
          type="text" 
          class="w-full bg-[#0f172a] text-white px-3 py-2 rounded border border-slate-600 focus:border-blue-500 focus:outline-none mb-4"
          placeholder="/path/to/target"
        />
        <div class="flex justify-end gap-3">
          <button @click="showDeployModal = false" class="px-4 py-2 text-slate-400 hover:text-white">Cancel</button>
          <button @click="confirmDeploy" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-500">Deploy</button>
        </div>
      </div>
    </div>

    <!-- Header -->
    <div class="bg-[#1e293b] border-b border-slate-700 px-6 py-4 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-white">Visual Agent Builder</h1>
        <p class="text-sm text-slate-400">Compose complex agents from modular components.</p>
      </div>
      <div class="flex items-center gap-3">
        <button @click="toggleJsonMode" class="px-3 py-2 text-slate-400 hover:text-white text-sm border border-slate-600 rounded hover:border-slate-500 transition-colors">
          {{ showJson ? '👁️ Visual Editor' : '{} JSON Editor' }}
        </button>
        <button 
          @click="savePlan" 
          class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors" 
          :disabled="saving"
        >
          {{ saving ? 'Saving...' : '💾 Save Plan' }}
        </button>
        <button 
          @click="openDeployModal" 
          class="px-4 py-2 bg-emerald-600 text-white rounded hover:bg-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors" 
          :disabled="deploying || !currentPlan.id"
        >
          {{ deploying ? 'Deploying...' : '🚀 Deploy' }}
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="flex-1 flex overflow-hidden">
      
      <!-- JSON Editor Mode -->
      <div v-if="showJson" class="flex-1 bg-[#0f172a] p-4 overflow-hidden flex flex-col">
        <div class="flex justify-between items-center mb-2 text-slate-400 text-sm">
          <span>Edit Plan Configuration (JSON)</span>
          <span v-if="jsonError" class="text-red-400">{{ jsonError }}</span>
        </div>
        <textarea 
          v-model="jsonContent" 
          class="flex-1 w-full bg-[#1e293b] text-emerald-400 font-mono p-4 rounded border border-slate-700 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none resize-none"
          spellcheck="false"
          @input="validateJson"
        ></textarea>
      </div>

      <!-- Visual Editor Mode -->
      <template v-else>
        <!-- Sidebar: Component Library -->
        <div class="w-80 bg-[#1e293b] border-r border-slate-700 flex flex-col">
          <div class="p-4 border-b border-slate-700">
            <h2 class="font-bold text-white">Component Library</h2>
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="Search components..." 
              class="w-full mt-2 text-sm bg-[#0f172a] text-white px-3 py-2 rounded border border-slate-600 focus:border-blue-500 focus:outline-none placeholder-slate-500"
            />
          </div>
          
          <!-- Loading State -->
          <div v-if="loading" class="flex-1 flex items-center justify-center">
            <div class="text-slate-400 flex items-center gap-2">
              <span class="animate-spin">⏳</span>
              <span>Loading components...</span>
            </div>
          </div>

          <!-- Error State -->
          <div v-else-if="loadError" class="flex-1 flex flex-col items-center justify-center p-4">
            <span class="text-red-400 text-4xl mb-2">⚠️</span>
            <p class="text-red-400 text-sm text-center">Failed to load components</p>
            <button @click="loadComponents" class="mt-2 text-blue-400 hover:text-blue-300 text-sm">Retry</button>
          </div>

          <div v-else class="flex-1 overflow-y-auto p-4 space-y-6">
            <!-- Orchestrators -->
            <div>
              <h3 class="text-xs font-bold text-slate-500 uppercase mb-2">Orchestrators</h3>
              <div class="space-y-2">
                <div 
                  v-for="orch in filteredComponents.orchestrators" 
                  :key="orch.name"
                  class="bg-[#0f172a] p-3 rounded border border-slate-700 cursor-pointer hover:border-purple-500 hover:shadow-sm transition-all"
                  @click="selectOrchestrator(orch)"
                  :class="{ 'ring-2 ring-purple-500 border-purple-500': currentPlan.orchestrator === orch.name }"
                >
                  <div class="font-medium text-sm text-white">{{ orch.name }}</div>
                  <div class="text-xs text-slate-500 truncate">{{ orch.description || orch.path }}</div>
                </div>
                <div v-if="filteredComponents.orchestrators.length === 0" class="text-slate-500 text-sm italic">
                  No orchestrators found
                </div>
              </div>
            </div>

            <!-- Agents -->
            <div>
              <h3 class="text-xs font-bold text-slate-500 uppercase mb-2">Agents</h3>
              <div class="space-y-2">
                <div 
                  v-for="agent in filteredComponents.agents" 
                  :key="agent.name"
                  class="bg-[#0f172a] p-3 rounded border border-slate-700 cursor-pointer hover:border-blue-500 hover:shadow-sm transition-all"
                  @click="addComponent(agent, 'agent')"
                >
                  <div class="flex items-center justify-between">
                    <span class="font-medium text-sm text-white">{{ agent.name }}</span>
                    <span class="text-xs text-blue-400">+ Add</span>
                  </div>
                </div>
                <div v-if="filteredComponents.agents.length === 0" class="text-slate-500 text-sm italic">
                  No agents found
                </div>
              </div>
            </div>

            <!-- Skills -->
            <div>
              <h3 class="text-xs font-bold text-slate-500 uppercase mb-2">Skills</h3>
              <div class="space-y-2">
                <div 
                  v-for="skill in filteredComponents.skills" 
                  :key="skill.name"
                  class="bg-[#0f172a] p-3 rounded border border-slate-700 cursor-pointer hover:border-teal-500 hover:shadow-sm transition-all"
                  @click="addComponent(skill, 'skill')"
                >
                  <div class="flex items-center justify-between">
                    <span class="font-medium text-sm text-white">{{ skill.name }}</span>
                    <span class="text-xs text-teal-400">+ Add</span>
                  </div>
                </div>
                <div v-if="filteredComponents.skills.length === 0" class="text-slate-500 text-sm italic">
                  No skills found
                </div>
              </div>
            </div>

            <!-- Hooks -->
            <div>
              <h3 class="text-xs font-bold text-slate-500 uppercase mb-2">Hooks</h3>
              <div class="space-y-2">
                <div 
                  v-for="hook in filteredComponents.hooks" 
                  :key="hook.name"
                  class="bg-[#0f172a] p-3 rounded border border-slate-700 cursor-pointer hover:border-amber-500 hover:shadow-sm transition-all"
                  @click="addComponent(hook, 'hook')"
                >
                  <div class="flex items-center justify-between">
                    <span class="font-medium text-sm text-white">{{ hook.name }}</span>
                    <span class="text-xs text-amber-400">+ Add</span>
                  </div>
                </div>
                <div v-if="filteredComponents.hooks.length === 0" class="text-slate-500 text-sm italic">
                  No hooks found
                </div>
              </div>
            </div>

            <!-- Scripts -->
            <div>
              <h3 class="text-xs font-bold text-slate-500 uppercase mb-2">Scripts</h3>
              <div class="space-y-2">
                <div 
                  v-for="script in filteredComponents.scripts" 
                  :key="script.name"
                  class="bg-[#0f172a] p-3 rounded border border-slate-700 cursor-pointer hover:border-rose-500 hover:shadow-sm transition-all"
                  @click="addComponent(script, 'script')"
                >
                  <div class="flex items-center justify-between">
                    <span class="font-medium text-sm text-white">{{ script.name }}</span>
                    <span class="text-xs text-rose-400">+ Add</span>
                  </div>
                </div>
                <div v-if="filteredComponents.scripts.length === 0" class="text-slate-500 text-sm italic">
                  No scripts found
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Canvas: Plan Composition -->
        <div class="flex-1 bg-[#0f172a] p-8 overflow-y-auto">
          <div class="max-w-3xl mx-auto space-y-6">
            
            <!-- Plan Settings -->
            <div class="bg-[#1e293b] rounded-lg shadow-lg p-6 border border-slate-700">
              <h3 class="text-lg font-bold mb-4 text-white">Plan Settings</h3>
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium mb-1 text-slate-300">Plan Name</label>
                  <input v-model="currentPlan.name" type="text" class="w-full bg-[#0f172a] text-white px-3 py-2 rounded border border-slate-600 focus:border-blue-500 focus:outline-none" />
                </div>
                <div>
                  <label class="block text-sm font-medium mb-1 text-slate-300">Version</label>
                  <input v-model="currentPlan.version" type="text" class="w-full bg-[#0f172a] text-white px-3 py-2 rounded border border-slate-600 focus:border-blue-500 focus:outline-none" />
                </div>
                <div class="col-span-2">
                  <label class="block text-sm font-medium mb-1 text-slate-300">Description</label>
                  <textarea v-model="currentPlan.description" class="w-full bg-[#0f172a] text-white px-3 py-2 rounded border border-slate-600 focus:border-blue-500 focus:outline-none resize-none" rows="2"></textarea>
                </div>
              </div>
            </div>

            <!-- Selected Orchestrator -->
            <div class="bg-[#1e293b] rounded-lg shadow-lg p-6 border-l-4 border-purple-500 border border-slate-700">
              <div class="flex items-center justify-between mb-2">
                <h3 class="text-lg font-bold text-purple-400">Orchestrator</h3>
                <span class="px-2 py-1 bg-purple-500/20 text-purple-300 text-xs rounded font-bold">Core Logic</span>
              </div>
              <div v-if="currentPlan.orchestrator" class="text-white font-medium">
                {{ currentPlan.orchestrator }}
              </div>
              <div v-else class="text-slate-500 italic">
                Select an orchestrator from the library...
              </div>
            </div>

            <!-- Components -->
            <div class="space-y-4">
              <h3 class="text-lg font-bold text-white">Components</h3>
              
              <div v-if="currentPlan.customComponents.length === 0" class="text-center py-8 border-2 border-dashed border-slate-600 rounded-lg">
                <p class="text-slate-400">No components added yet.</p>
                <p class="text-sm text-slate-500">Click items in the sidebar to add them.</p>
              </div>

              <div 
                v-for="(comp, idx) in currentPlan.customComponents" 
                :key="idx"
                class="bg-[#1e293b] rounded-lg shadow-lg p-4 flex items-center justify-between border border-slate-700"
                :class="getComponentBorderClass(comp.type)"
              >
                <div>
                  <div class="font-medium text-white">{{ comp.path.split('/').pop()?.replace('.md', '') }}</div>
                  <div class="text-xs text-slate-400 uppercase">{{ comp.type }}</div>
                </div>
                <button @click="removeComponent(idx)" class="text-red-400 hover:text-red-300 transition-colors">
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
import { ref, onMounted, computed } from 'vue'
import api from '../api/client'

interface ComponentItem {
  name: string
  path: string
  description?: string
}

interface Plan {
  id?: string
  name: string
  version: string
  description: string
  orchestrator: string
  workflows: string[]
  customComponents: {
    type: 'agent' | 'skill' | 'hook' | 'script' | 'mcp' | 'tool'
    path: string
  }[]
  settings: Record<string, unknown>
}

interface ComponentLibrary {
  orchestrators: ComponentItem[]
  agents: ComponentItem[]
  skills: ComponentItem[]
  hooks: ComponentItem[]
  scripts: ComponentItem[]
}

const components = ref<ComponentLibrary>({
  orchestrators: [],
  agents: [],
  skills: [],
  hooks: [],
  scripts: []
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
const loading = ref(false)
const loadError = ref(false)
const showJson = ref(false)
const jsonContent = ref('')
const jsonError = ref('')
const showDeployModal = ref(false)
const deployTargetDir = ref('')
const toast = ref({ show: false, message: '', type: 'success' as 'success' | 'error' })

function showToast(message: string, type: 'success' | 'error' = 'success') {
  toast.value = { show: true, message, type }
  setTimeout(() => {
    toast.value.show = false
  }, 3000)
}

onMounted(async () => {
  await loadComponents()
})

async function loadComponents() {
  loading.value = true
  loadError.value = false
  try {
    const { data } = await api.get('/plans/components')
    components.value = {
      orchestrators: data.orchestrators || [],
      agents: data.agents || [],
      skills: data.skills || [],
      hooks: data.hooks || [],
      scripts: data.scripts || []
    }
  } catch (error) {
    console.error('Failed to load components:', error)
    loadError.value = true
  } finally {
    loading.value = false
  }
}

const filteredComponents = computed(() => {
  const q = searchQuery.value.toLowerCase()
  return {
    orchestrators: components.value.orchestrators.filter(c => c.name.toLowerCase().includes(q)),
    agents: components.value.agents.filter(c => c.name.toLowerCase().includes(q)),
    skills: components.value.skills.filter(c => c.name.toLowerCase().includes(q)),
    hooks: components.value.hooks.filter(c => c.name.toLowerCase().includes(q)),
    scripts: components.value.scripts.filter(c => c.name.toLowerCase().includes(q))
  }
})

function selectOrchestrator(orch: ComponentItem) {
  currentPlan.value.orchestrator = orch.name
}

function addComponent(component: ComponentItem, type: 'agent' | 'skill' | 'hook' | 'script') {
  // Prevent duplicates
  const exists = currentPlan.value.customComponents.some(c => c.path === component.path)
  if (exists) {
    showToast('Component already added', 'error')
    return
  }
  currentPlan.value.customComponents.push({
    type,
    path: component.path
  })
}

function removeComponent(index: number) {
  currentPlan.value.customComponents.splice(index, 1)
}

function getComponentBorderClass(type: string): string {
  switch (type) {
    case 'agent': return 'border-l-4 border-l-blue-500'
    case 'skill': return 'border-l-4 border-l-teal-500'
    case 'hook': return 'border-l-4 border-l-amber-500'
    case 'script': return 'border-l-4 border-l-rose-500'
    default: return 'border-l-4 border-l-slate-500'
  }
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
      showToast('Cannot save: Invalid JSON', 'error')
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
    showToast('Plan saved successfully!')
  } catch (error) {
    showToast('Failed to save plan', 'error')
  } finally {
    saving.value = false
  }
}

function openDeployModal() {
  deployTargetDir.value = ''
  showDeployModal.value = true
}

async function confirmDeploy() {
  if (!currentPlan.value.id || !deployTargetDir.value) return
  
  showDeployModal.value = false
  deploying.value = true
  try {
    await api.post(`/plans/${currentPlan.value.id}/deploy`, { targetDir: deployTargetDir.value })
    showToast(`Plan deployed to ${deployTargetDir.value}`)
  } catch (error) {
    showToast('Failed to deploy plan', 'error')
  } finally {
    deploying.value = false
  }
}
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}
.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateX(20px);
}
</style>
