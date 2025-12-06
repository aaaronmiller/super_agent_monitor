<template>
  <div class="h-full flex flex-col p-6 max-w-4xl mx-auto w-full">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2 flex items-center gap-3">
        <span class="text-4xl">⚗️</span>
        MCP Transmuter
      </h1>
      <p class="text-gray-600 dark:text-gray-400 text-lg">
        Convert Model Context Protocol (MCP) servers into standalone Skill scripts.
      </p>
    </div>

    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
      <div class="p-6 space-y-6">
        <!-- Input Form -->
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">
              MCP Server Source
            </label>
            <div class="relative">
              <input
                v-model="serverUrl"
                type="text"
                placeholder="e.g., /path/to/mcp/server or https://github.com/org/repo"
                class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all font-mono text-sm"
                :disabled="converting"
              />
              <div class="absolute right-3 top-3 text-gray-400 cursor-pointer hover:text-blue-500" @click="loadExample" title="Load Example">
                🔗
              </div>
            </div>
            <div class="mt-2 flex justify-between items-center">
              <p class="text-xs text-gray-500 dark:text-gray-400">
                Provide a local directory path or a URL to an MCP server repository.
              </p>
              <button @click="loadExample" class="text-xs text-blue-500 hover:text-blue-600 font-medium">
                Load Example
              </button>
            </div>
          </div>

          <div>
            <label class="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">
              Output Name (Optional)
            </label>
            <input
              v-model="outputName"
              type="text"
              placeholder="e.g., my-custom-skill"
              class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all font-mono text-sm"
              :disabled="converting"
            />
          </div>
        </div>

        <!-- Action Button -->
        <div class="pt-4">
          <button
            @click="convert"
            :disabled="!serverUrl || converting"
            class="w-full py-4 px-6 rounded-lg font-bold text-white text-lg shadow-md transition-all transform hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center gap-3"
            :class="converting ? 'bg-gray-500' : 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500'"
          >
            <span v-if="converting" class="animate-spin text-2xl">⚡</span>
            <span v-else class="text-2xl">✨</span>
            {{ converting ? 'Transmuting...' : 'Transmute to Skill' }}
          </button>
        </div>

        <!-- Results / Logs -->
        <div v-if="result || error || logs.length > 0" class="mt-8 pt-6 border-t border-gray-200 dark:border-gray-700 animate-fade-in">
          <h3 class="text-sm font-bold text-gray-500 uppercase tracking-wider mb-4">Transmutation Log</h3>
          
          <div class="bg-gray-900 rounded-lg p-4 font-mono text-sm overflow-x-auto max-h-96 overflow-y-auto shadow-inner border border-gray-700">
            <div v-for="(log, index) in logs" :key="index" class="mb-1 text-gray-300">
              <span class="text-blue-400">➜</span> {{ log }}
            </div>
            
            <div v-if="error" class="mt-4 text-red-400 font-bold border-l-4 border-red-500 pl-3 py-1 bg-red-900/20 rounded-r">
              ❌ Error: {{ error }}
            </div>

            <div v-if="result" class="mt-6 pt-4 border-t border-gray-700">
              <div class="text-green-400 font-bold text-lg mb-2 flex items-center gap-2">
                <span>✅</span> Success!
              </div>
              <div class="text-gray-300 mb-2">Skill created at:</div>
              <div class="bg-black/50 p-3 rounded border border-gray-700 text-green-300 break-all select-all">
                {{ result.path }}
              </div>
              <div class="mt-4 text-gray-400 text-xs">
                You can now use this skill in your agent workflows.
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import api from '../services/api';

const serverUrl = ref('');
const outputName = ref('');
const converting = ref(false);
const logs = ref<string[]>([]);
const error = ref<string | null>(null);
const result = ref<{ path: string } | null>(null);

const loadExample = () => {
  serverUrl.value = 'beyond-mcp/apps/1_mcp_server';
  outputName.value = 'example-mcp-skill';
};

const convert = async () => {
  if (!serverUrl.value) return;

  converting.value = true;
  error.value = null;
  result.value = null;
  logs.value = ['Initializing transmutation process...', `Source: ${serverUrl.value}`];

  try {
    // Simulate some logs for better UX (since the API might be fast or opaque)
    setTimeout(() => logs.value.push('Analyzing MCP server structure...'), 500);
    setTimeout(() => logs.value.push('Extracting tools and resources...'), 1000);
    setTimeout(() => logs.value.push('Generating Python AST...'), 1500);

    const response = await api.post('/converter/mcp-to-skill', {
      mcpServerUrl: serverUrl.value,
      name: outputName.value || undefined
    });

    logs.value.push('Compiling final skill script...');
    
    // Wait a bit to show the final logs before success
    setTimeout(() => {
      result.value = response.data;
      logs.value.push('Transmutation complete.');
      converting.value = false;
    }, 2000);

  } catch (err: any) {
    console.error('Conversion failed:', err);
    error.value = err.response?.data?.error || err.message || 'Unknown error occurred';
    converting.value = false;
  }
};
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
