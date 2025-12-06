<template>
  <div class="space-y-3">
    <div class="flex items-center justify-between">
      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
        Local Model <span class="text-xs text-gray-400">(LM Studio)</span>
      </label>
      <div class="flex items-center gap-2">
        <span 
          class="w-2 h-2 rounded-full"
          :class="status.available ? 'bg-green-500 animate-pulse' : 'bg-red-500'"
        ></span>
        <span class="text-xs text-gray-500 dark:text-gray-400">
          {{ status.available ? 'Connected' : 'Disconnected' }}
        </span>
        <button 
          @click="refreshStatus" 
          class="text-xs text-blue-500 hover:text-blue-600"
          :disabled="loading"
        >
          ↻
        </button>
      </div>
    </div>

    <div v-if="status.available" class="space-y-3">
      <!-- Model Selector -->
      <select
        v-model="selectedModel"
        @change="emitModel"
        class="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
      >
        <option value="">Select a model...</option>
        <option v-for="model in models" :key="model.id" :value="model.id">
          {{ formatModelName(model.id) }}
        </option>
      </select>

      <!-- Recommended Models Cards -->
      <div v-if="showRecommended" class="grid grid-cols-2 gap-2">
        <div
          v-for="(config, key) in recommendedConfigs"
          :key="key"
          @click="selectRecommended(config)"
          class="cursor-pointer p-3 rounded-lg border border-gray-200 dark:border-gray-700 hover:border-blue-400 dark:hover:border-blue-500 transition-colors"
        >
          <h5 class="font-medium text-sm text-gray-900 dark:text-white">
            {{ config.name }}
          </h5>
          <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
            {{ config.description }}
          </p>
          <div class="flex flex-wrap gap-1 mt-2">
            <span 
              v-for="tag in config.bestFor" 
              :key="tag"
              class="px-1.5 py-0.5 text-xs rounded bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300"
            >
              {{ tag }}
            </span>
          </div>
        </div>
      </div>

      <button
        @click="showRecommended = !showRecommended"
        class="text-xs text-blue-500 hover:text-blue-600"
      >
        {{ showRecommended ? 'Hide recommendations' : 'Show recommended models' }}
      </button>
    </div>

    <div v-else class="bg-amber-50 dark:bg-amber-900/30 rounded-lg p-3 border border-amber-200 dark:border-amber-700">
      <p class="text-sm text-amber-700 dark:text-amber-300">
        <span class="mr-1">⚠️</span>
        LM Studio not detected. Start LM Studio and ensure it's running on port 1234.
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api from '../services/api';

interface LocalModel {
  id: string;
  object: string;
  owned_by: string;
}

interface ModelConfig {
  id: string;
  name: string;
  description: string;
  temperature: number;
  max_tokens: number;
  bestFor: string[];
}

const props = defineProps<{
  modelValue?: string;
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void;
  (e: 'model-config', config: ModelConfig): void;
}>();

const status = ref({ available: false, models: [] as LocalModel[], error: '' });
const models = ref<LocalModel[]>([]);
const selectedModel = ref(props.modelValue || '');
const loading = ref(false);
const showRecommended = ref(false);
const recommendedConfigs = ref<Record<string, ModelConfig>>({});

const refreshStatus = async () => {
  loading.value = true;
  try {
    const response = await api.get('/local-models/status');
    status.value = response.data;
    models.value = response.data.models || [];
  } catch (error) {
    status.value = { available: false, models: [], error: 'Failed to connect' };
  } finally {
    loading.value = false;
  }
};

const loadRecommendations = async () => {
  try {
    const response = await api.get('/local-models/recommended');
    recommendedConfigs.value = response.data.models || {};
  } catch (error) {
    console.warn('Failed to load recommendations:', error);
  }
};

const formatModelName = (id: string): string => {
  // Clean up model ID for display
  return id
    .replace(/-mlx-4bit$/, '')
    .replace(/-instruct$/, '')
    .split('/')
    .pop() || id;
};

const emitModel = () => {
  emit('update:modelValue', selectedModel.value);
};

const selectRecommended = (config: ModelConfig) => {
  selectedModel.value = config.id;
  emit('update:modelValue', config.id);
  emit('model-config', config);
};

onMounted(() => {
  refreshStatus();
  loadRecommendations();
});
</script>
