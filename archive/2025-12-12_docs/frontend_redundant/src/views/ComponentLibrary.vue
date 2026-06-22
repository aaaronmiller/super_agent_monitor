<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex items-center justify-between mb-8">
      <h1 class="text-3xl font-bold">Component Library</h1>
      <button @click="rescan" :disabled="loading" class="btn btn-secondary">
        {{ loading ? 'Scanning...' : '🔄 Rescan' }}
      </button>
    </div>

    <!-- Search and Filters -->
    <div class="card mb-6">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="md:col-span-2">
          <input
            v-model="searchQuery"
            @input="handleSearch"
            type="text"
            placeholder="Search components by name, description, or tags..."
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          />
        </div>
        <select
          v-model="selectedCategory"
          @change="handleCategoryChange"
          class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
        >
          <option value="">All Categories</option>
          <option value="agent">Agents</option>
          <option value="skill">Skills</option>
          <option value="hook">Hooks</option>
          <option value="script">Scripts</option>
          <option value="orchestrator">Orchestrators</option>
        </select>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-12">
      <div class="text-gray-500">Loading components...</div>
    </div>

    <!-- Component Grid -->
    <div v-else-if="filteredComponents.length > 0">
      <!-- Category Sections -->
      <div v-for="category in visibleCategories" :key="category" class="mb-8">
        <h2 class="text-2xl font-bold mb-4 capitalize flex items-center">
          <span class="text-3xl mr-3">{{ getCategoryIcon(category) }}</span>
          {{ category }}s
          <span class="ml-3 text-sm font-normal text-gray-500">
            ({{ componentsByCategory[category]?.length || 0 }})
          </span>
        </h2>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div
            v-for="component in componentsByCategory[category]"
            :key="component.id"
            class="card hover:shadow-md transition-shadow cursor-pointer"
            @click="showDetails(component)"
          >
            <div class="flex items-start justify-between mb-3">
              <div class="flex-1">
                <h3 class="font-bold text-lg">{{ component.displayName || component.name }}</h3>
                <p class="text-sm text-gray-500 mt-1">{{ component.description || 'No description' }}</p>
              </div>
            </div>

            <div class="flex flex-wrap gap-2 mt-3">
              <span v-if="component.model" class="badge badge-info">{{ component.model }}</span>
              <span v-if="component.pattern" class="badge badge-success">{{ component.pattern }}</span>
              <span v-for="tag in component.tags?.slice(0, 3)" :key="tag" class="badge bg-gray-100 text-gray-700">
                {{ tag }}
              </span>
            </div>

            <div v-if="component.dependencies?.length" class="mt-3 text-xs text-gray-500">
              <span class="font-medium">Dependencies:</span> {{ component.dependencies.join(', ') }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-12">
      <div class="text-6xl mb-4">📦</div>
      <h3 class="text-xl font-bold text-gray-700 mb-2">No Components Found</h3>
      <p class="text-gray-500">
        {{ searchQuery ? 'Try a different search term' : 'No components available' }}
      </p>
    </div>

    <!-- Component Details Modal -->
    <div v-if="selectedComponent" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50" @click="selectedComponent = null">
      <div class="bg-white rounded-lg max-w-2xl w-full max-h-[80vh] overflow-auto" @click.stop>
        <div class="p-6">
          <div class="flex items-start justify-between mb-4">
            <div>
              <h2 class="text-2xl font-bold">{{ selectedComponent.displayName || selectedComponent.name }}</h2>
              <p class="text-gray-500 mt-1">{{ selectedComponent.category }}</p>
            </div>
            <button @click="selectedComponent = null" class="text-gray-400 hover:text-gray-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div class="space-y-4">
            <div>
              <h3 class="font-bold mb-2">Description</h3>
              <p class="text-gray-700">{{ selectedComponent.description || 'No description available' }}</p>
            </div>

            <div v-if="selectedComponent.tags?.length">
              <h3 class="font-bold mb-2">Tags</h3>
              <div class="flex flex-wrap gap-2">
                <span v-for="tag in selectedComponent.tags" :key="tag" class="badge bg-gray-100 text-gray-700">
                  {{ tag }}
                </span>
              </div>
            </div>

            <div v-if="selectedComponent.model">
              <h3 class="font-bold mb-2">Model</h3>
              <p class="text-gray-700">{{ selectedComponent.model }}</p>
            </div>

            <div v-if="selectedComponent.dependencies?.length">
              <h3 class="font-bold mb-2">Dependencies</h3>
              <ul class="list-disc list-inside text-gray-700">
                <li v-for="dep in selectedComponent.dependencies" :key="dep">{{ dep }}</li>
              </ul>
            </div>

            <div v-if="selectedComponent.incompatibilities?.length">
              <h3 class="font-bold mb-2">Incompatibilities</h3>
              <ul class="list-disc list-inside text-red-600">
                <li v-for="inc in selectedComponent.incompatibilities" :key="inc">{{ inc }}</li>
              </ul>
            </div>

            <div class="pt-4 border-t">
              <p class="text-sm text-gray-500">ID: <code class="bg-gray-100 px-2 py-1 rounded">{{ selectedComponent.id }}</code></p>
              <p v-if="selectedComponent.version" class="text-sm text-gray-500 mt-1">Version: {{ selectedComponent.version }}</p>
            </div>
          </div>

          <div class="mt-6 flex gap-3">
            <button @click="copyComponentId(selectedComponent.id)" class="btn btn-secondary flex-1">
              Copy ID
            </button>
            <button @click="selectedComponent = null" class="btn btn-primary flex-1">
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useComponentsStore, type Component } from '../stores/components'

const componentsStore = useComponentsStore()

const searchQuery = ref('')
const selectedCategory = ref('')
const selectedComponent = ref<Component | null>(null)
const loading = computed(() => componentsStore.loading)

const componentsByCategory = computed(() => {
  const filtered = filteredComponents.value
  const groups: Record<string, Component[]> = {
    agent: [],
    skill: [],
    hook: [],
    script: [],
    orchestrator: []
  }

  filtered.forEach(c => {
    if (c.category) {
      groups[c.category].push(c)
    }
  })

  return groups
})

const filteredComponents = computed(() => {
  return componentsStore.components
})

const visibleCategories = computed(() => {
  if (selectedCategory.value) {
    return [selectedCategory.value]
  }
  return ['agent', 'skill', 'hook', 'script', 'orchestrator'].filter(
    cat => componentsByCategory.value[cat]?.length > 0
  )
})

onMounted(async () => {
  await componentsStore.fetchComponents()
  await componentsStore.fetchStats()
})

async function handleSearch() {
  if (searchQuery.value.trim()) {
    await componentsStore.fetchComponents({ search: searchQuery.value })
  } else {
    await componentsStore.fetchComponents()
  }
}

async function handleCategoryChange() {
  if (selectedCategory.value) {
    await componentsStore.fetchComponents({ category: selectedCategory.value })
  } else {
    await componentsStore.fetchComponents()
  }
}

async function rescan() {
  try {
    await componentsStore.rescan()
    alert('Components rescanned successfully!')
  } catch (error) {
    alert('Failed to rescan components')
  }
}

function showDetails(component: Component) {
  selectedComponent.value = component
}

function getCategoryIcon(category: string) {
  const icons: Record<string, string> = {
    agent: '🤖',
    skill: '🎯',
    hook: '🪝',
    script: '📜',
    orchestrator: '🎼'
  }
  return icons[category] || '📦'
}

function copyComponentId(id: string) {
  navigator.clipboard.writeText(id)
  alert('Component ID copied to clipboard!')
}
</script>
