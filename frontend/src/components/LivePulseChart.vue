<template>
  <div class="bg-gradient-to-r from-[var(--theme-bg-primary)] to-[var(--theme-bg-secondary)] p-4 mobile:p-2 rounded-lg shadow-lg border border-[var(--theme-border-primary)]">
    <!-- Header -->
    <div class="flex items-center justify-between mb-4 mobile:mb-2">
      <div class="flex items-center space-x-3 mobile:space-x-2">
        <h2 class="text-xl mobile:text-lg font-bold text-[var(--theme-primary)] drop-shadow-sm flex items-center">
          <span class="mr-2 text-2xl mobile:text-xl animate-pulse">💓</span>
          Live Pulse
        </h2>
        <div class="flex items-center space-x-2 mobile:space-x-1">
          <span class="px-3 mobile:px-2 py-1 bg-[var(--theme-bg-tertiary)] rounded-full text-sm mobile:text-xs font-semibold text-[var(--theme-text-primary)] border border-[var(--theme-border-primary)] shadow-sm">
            <span class="text-[var(--theme-primary)] font-bold">{{ uniqueAgentCount }}</span> Active Agents
          </span>
          <span class="px-3 mobile:px-2 py-1 bg-[var(--theme-bg-tertiary)] rounded-full text-sm mobile:text-xs font-semibold text-[var(--theme-text-primary)] border border-[var(--theme-border-primary)] shadow-sm">
            <span class="text-[var(--theme-primary)] font-bold">{{ dataPoints.length }}</span> Events
          </span>
          <span v-if="toolCallCount > 0" class="px-3 mobile:px-2 py-1 bg-[var(--theme-bg-tertiary)] rounded-full text-sm mobile:text-xs font-semibold text-[var(--theme-text-primary)] border border-[var(--theme-border-primary)] shadow-sm">
            <span class="text-[var(--theme-primary)] font-bold">{{ toolCallCount }}</span> Tool Calls
          </span>
        </div>
      </div>
      
      <!-- Time Range Selector -->
      <div class="flex bg-[var(--theme-bg-tertiary)] rounded-lg p-1 shadow-inner">
        <button
          v-for="range in ['1m', '3m', '5m', '10m']"
          :key="range"
          @click="setTimeRange(range as any)"
          class="px-3 mobile:px-2 py-1 rounded-md text-sm mobile:text-xs font-medium transition-all duration-200"
          :class="timeRange === range 
            ? 'bg-[var(--theme-primary)] text-white shadow-md transform scale-105' 
            : 'text-[var(--theme-text-secondary)] hover:text-[var(--theme-text-primary)] hover:bg-[var(--theme-bg-primary)]'"
        >
          {{ range }}
        </button>
      </div>
    </div>

    <!-- Chart Container -->
    <div class="relative h-48 mobile:h-40 w-full bg-[var(--theme-bg-tertiary)] rounded-lg border border-[var(--theme-border-primary)] overflow-hidden shadow-inner">
      <canvas ref="canvas" class="absolute inset-0 w-full h-full"></canvas>
      
      <!-- Loading State -->
      <div v-if="dataPoints.length === 0" class="absolute inset-0 flex items-center justify-center text-[var(--theme-text-tertiary)]">
        <div class="flex flex-col items-center animate-pulse">
          <span class="text-3xl mb-2">📡</span>
          <span class="font-medium">Waiting for events...</span>
        </div>
      </div>
    </div>
    
    <!-- Metrics Footer -->
    <div class="mt-3 grid grid-cols-3 gap-4 mobile:gap-2 text-xs text-[var(--theme-text-secondary)]">
      <div class="text-center p-2 bg-[var(--theme-bg-tertiary)] rounded-lg border border-[var(--theme-border-primary)]">
        <span class="block font-bold text-[var(--theme-primary)]">{{ eventTimingMetrics.eventsPerSecond.toFixed(1) }}</span>
        <span class="text-[var(--theme-text-tertiary)]">Events/sec</span>
      </div>
      <div class="text-center p-2 bg-[var(--theme-bg-tertiary)] rounded-lg border border-[var(--theme-border-primary)]">
        <span class="block font-bold text-[var(--theme-primary)]">{{ eventTimingMetrics.peakEventsPerSecond.toFixed(1) }}</span>
        <span class="text-[var(--theme-text-tertiary)]">Peak/sec</span>
      </div>
      <div class="text-center p-2 bg-[var(--theme-bg-tertiary)] rounded-lg border border-[var(--theme-border-primary)]">
        <span class="block font-bold text-[var(--theme-primary)]">{{ eventTimingMetrics.avgTimeBetweenEvents.toFixed(0) }}ms</span>
        <span class="text-[var(--theme-text-tertiary)]">Avg Interval</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue';
import { ChartRenderer } from '../utils/chartRenderer';
import { useChartData } from '../composables/useChartData';
import { useEventEmojis } from '../composables/useEventEmojis';
import { useEventColors } from '../composables/useEventColors';
import type { HookEvent } from '../types';

const props = defineProps<{
  events: HookEvent[];
}>();

const canvas = ref<HTMLCanvasElement | null>(null);
let renderer: ChartRenderer | null = null;
let animationFrameId: number | null = null;

const { 
  timeRange, 
  dataPoints, 
  addEvent, 
  getChartData, 
  setTimeRange, 
  cleanup: cleanupChartData,
  clearData,
  uniqueAgentCount,
  uniqueAgentIdsInWindow,
  allUniqueAgentIds,
  toolCallCount,
  eventTimingMetrics
} = useChartData();

const { getEmojiForEventType } = useEventEmojis();
const { getHexColorForSession } = useEventColors();

// Expose unique agent IDs to parent
const emit = defineEmits<{
  (e: 'update:uniqueAgentIds', ids: string[]): void;
  (e: 'update:allAgentIds', ids: string[]): void;
}>();

watch(uniqueAgentIdsInWindow, (newIds) => {
  emit('update:uniqueAgentIds', Array.from(newIds));
});

watch(allUniqueAgentIds, (newIds) => {
  emit('update:allAgentIds', Array.from(newIds));
});

// Watch for new events from props
watch(() => props.events, (newEvents, oldEvents) => {
  // If we have new events, add them to the chart data
  // Only add events that are newer than what we have
  if (newEvents.length > (oldEvents?.length || 0)) {
    const addedEvents = newEvents.slice(oldEvents?.length || 0);
    addedEvents.forEach(event => {
      addEvent(event);
    });
  } else if (newEvents.length === 0 && (oldEvents?.length || 0) > 0) {
    // Events were cleared
    clearData();
  }
}, { deep: true });

const formatEventTypeLabel = (type: string) => {
  return getEmojiForEventType(type);
};

const render = () => {
  if (!renderer || !canvas.value) return;

  const data = getChartData();
  
  // Calculate max value for Y-axis scaling
  const maxValue = Math.max(...data.map(d => d.count), 1);
  
  renderer.clear();
  renderer.drawBackground();
  renderer.drawAxes();
  renderer.drawTimeLabels(timeRange.value);
  
  // Draw bars with colors based on the dominant session in that time slice
  // This is a simplification; ideally we'd show stacked bars or multiple colors
  renderer.drawBars(data, maxValue, 1, formatEventTypeLabel, getHexColorForSession);
  
  animationFrameId = requestAnimationFrame(render);
};

onMounted(() => {
  if (canvas.value) {
    renderer = new ChartRenderer(canvas.value, {
      colors: {
        primary: '#3b82f6', // Will be overridden by theme CSS variables in renderer if implemented
        glow: '#60a5fa',
        axis: '#9ca3af',
        text: '#6b7280'
      }
    });
    
    // Initial render loop
    render();
    
    // Handle window resize
    window.addEventListener('resize', () => {
      if (renderer) renderer.resize();
    });
    
    // Initialize with existing events if any
    if (props.events.length > 0) {
      props.events.forEach(event => addEvent(event));
    }
  }
});

onUnmounted(() => {
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId);
  }
  cleanupChartData();
  window.removeEventListener('resize', () => {
    if (renderer) renderer.resize();
  });
});
</script>
