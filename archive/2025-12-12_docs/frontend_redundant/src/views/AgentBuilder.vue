<template>
  <div class="container mx-auto px-4 py-8 max-w-4xl">
    <div class="flex items-center justify-between mb-8">
      <h1 class="text-3xl font-bold">Agent Builder</h1>
      <router-link to="/components" class="btn btn-secondary">Back to Library</router-link>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Sidebar: Metadata -->
      <div class="lg:col-span-1 space-y-6">
        <div class="card">
          <h2 class="text-xl font-bold mb-4">Metadata</h2>
          
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Name (ID)</label>
              <input 
                v-model="metadata.name" 
                type="text" 
                placeholder="my-agent"
                class="w-full px-3 py-2 border rounded-lg"
                :disabled="isEditing"
              />
              <p class="text-xs text-gray-500 mt-1">Unique identifier (kebab-case)</p>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Display Name</label>
              <input 
                v-model="metadata.displayName" 
                type="text" 
                placeholder="My Custom Agent"
                class="w-full px-3 py-2 border rounded-lg"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Category</label>
              <select 
                v-model="metadata.category" 
                class="w-full px-3 py-2 border rounded-lg"
                :disabled="isEditing"
              >
                <option value="agent">Agent</option>
                <option value="orchestrator">Orchestrator</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
              <textarea 
                v-model="metadata.description" 
                rows="3"
                class="w-full px-3 py-2 border rounded-lg"
              ></textarea>
            </div>
          </div>
        </div>

        <div class="card">
          <h2 class="text-xl font-bold mb-4">Actions</h2>
          <button 
            @click="saveComponent" 
            :disabled="saving"
            class="btn btn-primary w-full flex justify-center items-center gap-2"
          >
            <span v-if="saving">Saving...</span>
            <span v-else>💾 Save Component</span>
          </button>
        </div>
      </div>

      <!-- Main: Editor -->
      <div class="lg:col-span-2">
        <div class="card h-full flex flex-col">
          <h2 class="text-xl font-bold mb-4">Prompt Template</h2>
          <p class="text-sm text-gray-500 mb-4">
            Define the system prompt and behavior. Use Markdown.
          </p>
          
          <textarea 
            v-model="content" 
            class="flex-1 w-full p-4 font-mono text-sm border rounded-lg bg-gray-50 focus:bg-white transition-colors"
            placeholder="# System Prompt..."
          ></textarea>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
// const route = useRoute() // For edit mode later

const isEditing = ref(false)
const saving = ref(false)

const metadata = ref({
  name: '',
  displayName: '',
  category: 'agent',
  description: ''
})

const content = ref('')

async function saveComponent() {
  if (!metadata.value.name) {
    alert('Please enter a name')
    return
  }

  saving.value = true
  try {
    // Construct file content with YAML frontmatter
    const fileContent = `---
name: ${metadata.value.name}
displayName: ${metadata.value.displayName}
description: ${metadata.value.description}
category: ${metadata.value.category}
---

${content.value}
`
    const id = `${metadata.value.category}:${metadata.value.name}`

    const res = await fetch('http://localhost:3001/api/components', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        id,
        content: fileContent
      })
    })

    if (!res.ok) throw new Error('Failed to save')

    alert('Component saved successfully!')
    router.push('/components')
  } catch (error) {
    console.error(error)
    alert('Error saving component')
  } finally {
    saving.value = false
  }
}
</script>
