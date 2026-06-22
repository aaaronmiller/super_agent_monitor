<template>
  <div class="inline-flex items-center gap-1">
    <!-- Council Indicator -->
    <span 
      v-if="showCouncilIndicator && councilType"
      class="text-xs opacity-80"
      :title="councilTooltip"
    >
      {{ councilIcon }}
    </span>
    
    <!-- E2B Status -->
    <span 
      v-if="showE2BStatus"
      class="w-2 h-2 rounded-full"
      :class="isE2B ? 'bg-green-500 shadow-green-500/50 shadow-sm' : 'bg-gray-400'"
      :title="isE2B ? 'Running in E2B Sandbox' : 'Running Locally'"
    ></span>
    
    <!-- RAG Indicator -->
    <span 
      v-if="showRagIndicator && hasRag"
      class="text-xs opacity-80"
      title="Context Injection (RAG) Enabled"
    >
      📚
    </span>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useVisualizationSettings } from '../composables/useVisualizationSettings';

const props = defineProps<{
  /** Orchestrator/Council type (e.g., 'ceo-council', 'playoff-debate') */
  councilType?: string;
  /** Whether running in E2B sandbox */
  isE2B?: boolean;
  /** Whether RAG/context injection is enabled */
  hasRag?: boolean;
}>();

const { settings } = useVisualizationSettings();

const showCouncilIndicator = computed(() => settings.value.showCouncilIndicator);
const showE2BStatus = computed(() => settings.value.showE2BStatus);
const showRagIndicator = computed(() => settings.value.showRagIndicator);

// Map council type to icon
const councilIcon = computed(() => {
  switch (props.councilType) {
    case 'ceo-council': return '🏛️';
    case 'playoff-debate': return '⚔️';
    case 'rcr-critique': return '🔄';
    case 'research-deep-dive': return '🔬';
    case 'adaptive-router': return '🧭';
    default: return '';
  }
});

// Map council type to tooltip
const councilTooltip = computed(() => {
  switch (props.councilType) {
    case 'ceo-council': return 'CEO Council (5-round deliberation)';
    case 'playoff-debate': return 'Playoff Debate (tournament elimination)';
    case 'rcr-critique': return 'RCR Protocol (reflect-critique-refine)';
    case 'research-deep-dive': return 'Research Deep Dive (exhaustive search)';
    case 'adaptive-router': return 'Adaptive Router (auto-select pattern)';
    default: return 'Unknown Council Pattern';
  }
});
</script>
