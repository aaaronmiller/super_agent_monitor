<template>
  <div 
    v-if="visible"
    class="flex items-center gap-1.5 px-2 py-1 bg-[var(--theme-bg-tertiary)] rounded-lg border border-[var(--theme-border-primary)] shadow-sm"
    :title="`Cumulative cost: $${totalCost.toFixed(4)}`"
  >
    <span class="text-lg mobile:text-base">💰</span>
    <div class="flex items-end gap-0.5 h-4">
      <!-- Sparkline bars -->
      <div 
        v-for="(value, index) in normalizedData"
        :key="index"
        class="w-1 bg-gradient-to-t from-green-500 to-emerald-400 rounded-t-sm transition-all duration-300"
        :style="{ height: `${Math.max(value * 100, 5)}%` }"
      ></div>
    </div>
    <span class="text-sm mobile:text-xs font-bold text-[var(--theme-text-primary)]">
      ${{ formatCost(totalCost) }}
    </span>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch, onMounted, onUnmounted } from 'vue';
import { useVisualizationSettings } from '../composables/useVisualizationSettings';
import type { HookEvent } from '../types';

interface CostDataPoint {
  timestamp: number;
  cost: number;
}

const props = defineProps<{
  sessionId?: string;
  events: HookEvent[];
}>();

const { settings } = useVisualizationSettings();
const visible = computed(() => settings.value.showCostSparkline);

// Track cost over time (last 10 data points)
const costHistory = ref<CostDataPoint[]>([]);
const maxDataPoints = 10;

// Calculate total cost from events
const totalCost = computed(() => {
  return props.events.reduce((sum, event) => {
    // Extract cost from event data if available
    const eventCost = event.cost_usd || event.cost || 0;
    return sum + eventCost;
  }, 0);
});

// Normalize data for sparkline display
const normalizedData = computed(() => {
  if (costHistory.value.length === 0) return Array(maxDataPoints).fill(0);
  
  const costs = costHistory.value.map(d => d.cost);
  const max = Math.max(...costs, 0.001); // Avoid division by zero
  
  // Pad with zeros if less than maxDataPoints
  const padded = [...costs];
  while (padded.length < maxDataPoints) {
    padded.unshift(0);
  }
  
  return padded.slice(-maxDataPoints).map(c => c / max);
});

// Update history when total cost changes
watch(totalCost, (newCost) => {
  costHistory.value.push({
    timestamp: Date.now(),
    cost: newCost
  });
  
  // Keep only last N points
  if (costHistory.value.length > maxDataPoints) {
    costHistory.value = costHistory.value.slice(-maxDataPoints);
  }
}, { immediate: true });

// Format cost for display
const formatCost = (cost: number): string => {
  if (cost < 0.01) return cost.toFixed(4);
  if (cost < 1) return cost.toFixed(3);
  return cost.toFixed(2);
};
</script>
