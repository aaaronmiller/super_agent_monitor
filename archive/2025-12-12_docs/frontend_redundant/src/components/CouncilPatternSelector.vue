<template>
  <div class="space-y-3">
    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
      Council Pattern
    </label>
    
    <!-- Use 2 columns max for better readability in constrained spaces -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
      <div
        v-for="pattern in patterns"
        :key="pattern.id"
        @click="selectPattern(pattern.id)"
        :class="[
          'cursor-pointer rounded-lg border-2 p-3 transition-all duration-200',
          selectedId === pattern.id
            ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/30'
            : 'border-gray-200 dark:border-gray-700 hover:border-gray-400 dark:hover:border-gray-500'
        ]"
      >
        <div class="flex items-start gap-2">
          <span class="text-xl flex-shrink-0">{{ pattern.icon }}</span>
          <div class="flex-1 min-w-0">
            <h4 class="font-semibold text-gray-900 dark:text-white text-sm truncate">
              {{ pattern.name }}
            </h4>
            <p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5 line-clamp-2">
              {{ pattern.description }}
            </p>
            <div class="flex gap-1.5 mt-1.5 flex-wrap">
              <span 
                class="inline-flex items-center px-1.5 py-0.5 rounded text-xs font-medium"
                :class="pattern.speedClass"
              >
                {{ pattern.speed }}
              </span>
              <span 
                class="inline-flex items-center px-1.5 py-0.5 rounded text-xs font-medium bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300"
              >
                {{ pattern.rounds }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <p class="text-xs text-gray-500 dark:text-gray-400 mt-2">
      {{ selectedPattern?.bestFor || 'Select a council pattern for orchestrated reasoning.' }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

interface CouncilPattern {
  id: string;
  name: string;
  icon: string;
  description: string;
  speed: string;
  speedClass: string;
  rounds: string;
  bestFor: string;
}

const patterns: CouncilPattern[] = [
  {
    id: 'adaptive-router',
    name: 'Adaptive Router',
    icon: '🧭',
    description: 'Auto-selects optimal pattern',
    speed: 'Variable',
    speedClass: 'bg-purple-100 dark:bg-purple-900 text-purple-700 dark:text-purple-300',
    rounds: 'Auto',
    bestFor: 'Best for: General purpose entry point when unsure which pattern to use.'
  },
  {
    id: 'ceo-council',
    name: 'CEO Council',
    icon: '🏛️',
    description: 'Deep multi-agent deliberation',
    speed: 'Slow',
    speedClass: 'bg-amber-100 dark:bg-amber-900 text-amber-700 dark:text-amber-300',
    rounds: '5',
    bestFor: 'Best for: Complex strategic decisions, architectural planning, nuanced writing.'
  },
  {
    id: 'playoff-debate',
    name: 'Playoff Debate',
    icon: '⚔️',
    description: 'Tournament-style elimination',
    speed: 'Medium',
    speedClass: 'bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300',
    rounds: '3',
    bestFor: 'Best for: Choosing between options, tech stack selection, binary decisions.'
  },
  {
    id: 'rcr-critique',
    name: 'RCR Protocol',
    icon: '🔄',
    description: 'Reflect → Critique → Refine',
    speed: 'Medium',
    speedClass: 'bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300',
    rounds: '3-4',
    bestFor: 'Best for: Code review, debugging, editing, polishing content.'
  },
  {
    id: 'research-deep-dive',
    name: 'Research Deep Dive',
    icon: '🔬',
    description: 'Parallel exhaustive search',
    speed: 'Slow',
    speedClass: 'bg-amber-100 dark:bg-amber-900 text-amber-700 dark:text-amber-300',
    rounds: '4',
    bestFor: 'Best for: Comprehensive research, finding obscure info, "tell me everything".'
  }
];

const props = defineProps<{
  modelValue?: string;
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void;
}>();

const selectedId = ref(props.modelValue || '');

const selectedPattern = computed(() => 
  patterns.find(p => p.id === selectedId.value)
);

const selectPattern = (id: string) => {
  selectedId.value = id;
  emit('update:modelValue', id);
};
</script>
