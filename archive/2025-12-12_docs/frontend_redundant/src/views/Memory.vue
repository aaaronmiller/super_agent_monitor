<template>
  <div class="container mx-auto px-4 py-8">
    <div class="max-w-6xl mx-auto">
      <h1 class="text-3xl font-bold mb-6">Memory Search</h1>

      <!-- Search Form -->
      <div class="card mb-6">
        <div class="mb-4">
          <label class="block text-sm font-medium mb-2">Filter / Search</label>
          <textarea
            v-model="query"
            placeholder="Type to filter instantly, or click Search for deep retrieval..."
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            rows="3"
          ></textarea>
        </div>

        <!-- Filters -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div>
            <label class="block text-sm font-medium mb-2">Content Type</label>
            <select
              v-model="contentType"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
            >
              <option value="">All Types</option>
              <option value="tool_output">Tool Outputs</option>
              <option value="completion">Completions</option>
              <option value="error">Errors</option>
              <option value="user_input">User Inputs</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium mb-2">Min Similarity (for Search)</label>
            <input
              v-model.number="minSimilarity"
              type="number"
              min="0"
              max="1"
              step="0.1"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
            />
          </div>

          <div>
            <label class="block text-sm font-medium mb-2">Limit (for Search)</label>
            <input
              v-model.number="limit"
              type="number"
              min="1"
              max="50"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
            />
          </div>
        </div>

        <!-- Keywords -->
        <div class="mb-4">
          <label class="block text-sm font-medium mb-2">Keywords (optional, comma-separated)</label>
          <input
            v-model="keywordsInput"
            placeholder="e.g., authentication, database, error"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
          />
        </div>

        <!-- Search Button -->
        <button
          @click="handleSearch"
          :disabled="loading"
          class="btn btn-primary w-full md:w-auto"
        >
          <span v-if="!loading">🔍 Deep Search (RAG)</span>
          <span v-else>Searching...</span>
        </button>
      </div>

      <!-- Error -->
      <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
        {{ error }}
      </div>

      <!-- Results -->
      <div v-if="filteredMemories.length > 0" class="mb-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-2xl font-bold">Memories</h2>
          <span class="text-gray-500">{{ filteredMemories.length }} items</span>
        </div>

        <div class="space-y-4">
          <div
            v-for="memory in filteredMemories"
            :key="memory.id"
            @click="viewMemoryDetails(memory.id)"
            :class="['card cursor-pointer hover:shadow-lg transition-shadow', getMemoryClass(memory.contentType)]"
          >
            <!-- Header -->
            <div class="flex items-start justify-between mb-3">
              <div class="flex items-center gap-2">
                <span class="text-2xl">{{ getMemoryIcon(memory.contentType) }}</span>
                <div>
                  <span class="font-medium">{{ formatContentType(memory.contentType) }}</span>
                  <div class="text-sm text-gray-500">
                    {{ new Date(memory.timestamp).toLocaleString() }}
                  </div>
                </div>
              </div>
              <div class="flex flex-col items-end gap-1">
                <span v-if="memory.similarityScore !== undefined" class="badge badge-info">
                  {{ (memory.similarityScore * 100).toFixed(0) }}% match
                </span>
                <span :class="['text-xs', getImportanceClass(memory.importanceScore)]">
                  Importance: {{ memory.importanceScore.toFixed(2) }}
                </span>
              </div>
            </div>

            <!-- Content Preview -->
            <div class="text-gray-700 mb-3">
              <div class="line-clamp-3">{{ memory.content }}</div>
            </div>

            <!-- Tags & Tool -->
            <div class="flex items-center gap-2 flex-wrap">
              <span v-if="memory.toolName" class="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                🔧 {{ memory.toolName }}
              </span>
              <span
                v-for="tag in memory.tags.slice(0, 5)"
                :key="tag"
                class="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded"
              >
                {{ tag }}
              </span>
              <span v-if="memory.tags.length > 5" class="text-xs text-gray-500">
                +{{ memory.tags.length - 5 }} more
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- No Results -->
      <div
        v-else-if="!loading"
        class="text-center py-12 text-gray-500"
      >
        <p class="text-lg">No memories found</p>
        <p class="text-sm mt-2">Try adjusting your filter or performing a Deep Search</p>
      </div>

      <!-- Memory Detail Modal -->
      <div
        v-if="selectedMemory"
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
        @click="closeModal"
      >
        <div class="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto" @click.stop>
          <div class="p-6">
            <!-- Modal Header -->
            <div class="flex items-start justify-between mb-4">
              <div class="flex items-center gap-3">
                <span class="text-3xl">{{ getMemoryIcon(selectedMemory.content_type) }}</span>
                <div>
                  <h3 class="text-2xl font-bold">{{ formatContentType(selectedMemory.content_type) }}</h3>
                  <p class="text-sm text-gray-500">{{ new Date(selectedMemory.timestamp).toLocaleString() }}</p>
                </div>
              </div>
              <button @click="closeModal" class="text-gray-500 hover:text-gray-700 text-2xl">
                ×
              </button>
            </div>

            <!-- Stats -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <div>
                <div class="text-sm text-gray-500">Importance</div>
                <div class="text-lg font-bold">{{ selectedMemory.importance_score.toFixed(2) }}</div>
              </div>
              <div v-if="selectedMemory.tool_name">
                <div class="text-sm text-gray-500">Tool</div>
                <div class="text-lg font-bold">{{ selectedMemory.tool_name }}</div>
              </div>
              <div v-if="selectedMemory.accessStats">
                <div class="text-sm text-gray-500">Access Count</div>
                <div class="text-lg font-bold">{{ selectedMemory.accessStats.access_count }}</div>
              </div>
              <div v-if="selectedMemory.accessStats?.avg_relevance">
                <div class="text-sm text-gray-500">Avg Relevance</div>
                <div class="text-lg font-bold">{{ (selectedMemory.accessStats.avg_relevance * 100).toFixed(0) }}%</div>
              </div>
            </div>

            <!-- Content -->
            <div class="mb-6">
              <h4 class="font-semibold mb-2">Content</h4>
              <pre class="text-sm text-gray-700 whitespace-pre-wrap bg-gray-50 p-4 rounded-lg overflow-x-auto">{{ selectedMemory.content }}</pre>
            </div>

            <!-- Metadata -->
            <div v-if="Object.keys(selectedMemory.metadata || {}).length > 0" class="mb-6">
              <h4 class="font-semibold mb-2">Metadata</h4>
              <pre class="text-sm text-gray-700 bg-gray-50 p-4 rounded-lg overflow-x-auto">{{ JSON.stringify(selectedMemory.metadata, null, 2) }}</pre>
            </div>

            <!-- Tags -->
            <div class="mb-6">
              <h4 class="font-semibold mb-2">Tags</h4>
              <div class="flex flex-wrap gap-2">
                <span
                  v-for="tag in selectedMemory.tags"
                  :key="tag"
                  class="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm"
                >
                  {{ tag }}
                </span>
              </div>
            </div>

            <!-- Similar Memories -->
            <div v-if="similarMemories.length > 0">
              <h4 class="font-semibold mb-2">Similar Memories</h4>
              <div class="space-y-2">
                <div
                  v-for="similar in similarMemories"
                  :key="similar.id"
                  @click="viewMemoryDetails(similar.id)"
                  class="p-3 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 transition-colors"
                >
                  <div class="flex items-center justify-between mb-1">
                    <span class="text-sm font-medium">{{ formatContentType(similar.contentType) }}</span>
                    <span class="text-xs badge badge-info">
                      {{ (similar.similarityScore * 100).toFixed(0) }}% similar
                    </span>
                  </div>
                  <div class="text-sm text-gray-600 line-clamp-2">{{ similar.content }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useMemoryStore } from '../stores/memory'
import type { Memory } from '../stores/memory'

const memoryStore = useMemoryStore()

const query = ref('')
const contentType = ref('')
const minSimilarity = ref(0.5)
const limit = ref(10)
const keywordsInput = ref('')

const displayedMemories = ref<Memory[]>([])
const selectedMemory = ref<any>(null)
const similarMemories = ref<Memory[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

onMounted(async () => {
  await loadRecentMemories()
})

async function loadRecentMemories() {
  loading.value = true
  try {
    const data = await memoryStore.fetchRecentMemories(50)
    displayedMemories.value = data.memories
  } catch (err) {
    console.error('Failed to load recent memories:', err)
  } finally {
    loading.value = false
  }
}

const filteredMemories = computed(() => {
  let result = displayedMemories.value

  // Client-side text filter
  if (query.value) {
    const q = query.value.toLowerCase()
    result = result.filter(m => 
      m.content.toLowerCase().includes(q) || 
      m.tags.some(t => t.toLowerCase().includes(q)) ||
      (m.toolName && m.toolName.toLowerCase().includes(q))
    )
  }

  // Client-side type filter
  if (contentType.value) {
    result = result.filter(m => m.contentType === contentType.value)
  }

  return result
})

async function handleSearch() {
  if (!query.value) {
    await loadRecentMemories()
    return
  }

  loading.value = true
  error.value = null

  try {
    const keywords = keywordsInput.value
      .split(',')
      .map(k => k.trim())
      .filter(k => k.length > 0)

    const result = await memoryStore.searchMemories({
      query: query.value,
      contentTypes: contentType.value ? [contentType.value] : undefined,
      minSimilarity: minSimilarity.value,
      limit: limit.value,
      keywords: keywords.length > 0 ? keywords : undefined
    })

    displayedMemories.value = result.memories
  } catch (err: any) {
    error.value = err.message || 'Search failed'
  } finally {
    loading.value = false
  }
}

async function viewMemoryDetails(entryId: string) {
  try {
    const details = await memoryStore.getMemory(entryId)
    selectedMemory.value = details

    // Load similar memories
    similarMemories.value = await memoryStore.findSimilar(entryId, 5)
  } catch (err) {
    console.error('Failed to load memory details:', err)
  }
}

function closeModal() {
  selectedMemory.value = null
  similarMemories.value = []
}

function getMemoryIcon(contentType: string): string {
  const icons: Record<string, string> = {
    tool_output: '🔧',
    completion: '✅',
    error: '❌',
    user_input: '💬',
    system_message: '💻'
  }
  return icons[contentType] || '📄'
}

function formatContentType(contentType: string): string {
  return contentType
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

function getMemoryClass(contentType: string): string {
  const classes: Record<string, string> = {
    error: 'border-l-4 border-red-500',
    completion: 'border-l-4 border-green-500',
    tool_output: 'border-l-4 border-blue-500',
    user_input: 'border-l-4 border-purple-500'
  }
  return classes[contentType] || 'border-l-4 border-gray-300'
}

function getImportanceClass(score: number): string {
  if (score >= 0.8) return 'text-green-600 font-semibold'
  if (score >= 0.5) return 'text-blue-600'
  return 'text-gray-500'
}
</script>
