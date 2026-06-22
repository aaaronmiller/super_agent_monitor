<template>
  <div class="bg-white rounded-lg shadow p-4 mb-6">
    <h3 class="text-sm font-bold text-gray-500 uppercase mb-3">System Status</h3>
    
    <div v-if="loading" class="text-sm text-gray-400">Checking system...</div>
    
    <div v-else class="space-y-3">
      <!-- Database -->
      <div class="flex items-center justify-between">
        <span class="text-sm font-medium">Database</span>
        <div class="flex items-center gap-2">
          <span 
            class="w-3 h-3 rounded-full"
            :class="status?.database.status === 'ok' ? 'bg-green-500' : 'bg-red-500'"
          ></span>
          <span v-if="status?.database.status === 'error'" class="text-xs text-red-500">
            {{ status.database.message }}
          </span>
        </div>
      </div>

      <!-- Claude Auth -->
      <div class="flex items-center justify-between">
        <span class="text-sm font-medium">Claude Auth</span>
        <div class="flex items-center gap-2">
          <span 
            class="w-3 h-3 rounded-full"
            :class="status?.claudeAuth.status === 'ok' ? 'bg-green-500' : 'bg-red-500'"
          ></span>
          <span v-if="status?.claudeAuth.status === 'error'" class="text-xs text-red-500">
            {{ status.claudeAuth.message }}
          </span>
        </div>
      </div>

      <!-- Environment -->
      <div class="flex items-center justify-between">
        <span class="text-sm font-medium">Environment</span>
        <div class="flex items-center gap-2">
          <span 
            class="w-3 h-3 rounded-full"
            :class="status?.environment.status === 'ok' ? 'bg-green-500' : 'bg-red-500'"
          ></span>
          <span v-if="status?.environment.status === 'error'" class="text-xs text-red-500">
            {{ status.environment.message }}
          </span>
        </div>
      </div>

      <!-- Proxy -->
      <div class="flex items-center justify-between">
        <span class="text-sm font-medium">Local Proxy</span>
        <div class="flex items-center gap-2">
          <span 
            class="w-3 h-3 rounded-full"
            :class="status?.proxy?.status === 'ok' ? 'bg-green-500' : 'bg-red-500'"
          ></span>
          <span v-if="status?.proxy?.status === 'error'" class="text-xs text-red-500">
            {{ status.proxy.message }}
          </span>
          <span v-else-if="status?.proxy?.message" class="text-xs text-gray-500">
            {{ status.proxy.message }}
          </span>
        </div>
      </div>
    </div>

    <button 
      @click="checkStatus" 
      class="mt-4 text-xs text-primary-600 hover:text-primary-800 flex items-center gap-1"
    >
      <span v-if="loading">↻ Checking...</span>
      <span v-else>↻ Refresh Status</span>
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface StatusItem {
  status: 'ok' | 'error'
  message?: string
}

interface SystemStatus {
  database: StatusItem
  claudeAuth: StatusItem
  environment: StatusItem
  proxy: StatusItem
  timestamp: string
}

const status = ref<SystemStatus | null>(null)
const loading = ref(false)

async function checkStatus() {
  loading.value = true
  try {
    const res = await fetch('http://127.0.0.1:3001/api/system/status')
    status.value = await res.json()
  } catch (error) {
    console.error('Failed to check system status:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  checkStatus()
})
</script>
