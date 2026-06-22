<template>
  <div class="bg-[var(--theme-bg-primary)] rounded-xl border border-[var(--theme-border-primary)] p-5 shadow-lg">
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-lg font-bold text-[var(--theme-text-primary)] flex items-center gap-2">
        <span>⚙️</span>
        <span>Visualization Settings</span>
      </h3>
      <button 
        @click="resetToDefaults"
        class="text-xs text-[var(--theme-text-tertiary)] hover:text-[var(--theme-primary)] transition-colors"
        title="Reset to defaults"
      >
        Reset
      </button>
    </div>
    
    <div class="space-y-3">
      <!-- Council Indicator -->
      <label class="flex items-center justify-between p-3 bg-[var(--theme-bg-secondary)] rounded-lg cursor-pointer hover:bg-[var(--theme-bg-tertiary)] transition-colors">
        <div class="flex items-center gap-3">
          <span class="text-xl">🏛️</span>
          <div>
            <div class="font-medium text-sm text-[var(--theme-text-primary)]">Council Indicator</div>
            <div class="text-xs text-[var(--theme-text-tertiary)]">Show orchestrator pattern badge</div>
          </div>
        </div>
        <input 
          type="checkbox" 
          :checked="settings.showCouncilIndicator"
          @change="toggleSetting('showCouncilIndicator')"
          class="toggle toggle-primary"
        />
      </label>

      <!-- E2B Status -->
      <label class="flex items-center justify-between p-3 bg-[var(--theme-bg-secondary)] rounded-lg cursor-pointer hover:bg-[var(--theme-bg-tertiary)] transition-colors">
        <div class="flex items-center gap-3">
          <span class="text-xl">📦</span>
          <div>
            <div class="font-medium text-sm text-[var(--theme-text-primary)]">E2B Status</div>
            <div class="text-xs text-[var(--theme-text-tertiary)]">Show sandbox/local runtime indicator</div>
          </div>
        </div>
        <input 
          type="checkbox" 
          :checked="settings.showE2BStatus"
          @change="toggleSetting('showE2BStatus')"
          class="toggle toggle-primary"
        />
      </label>

      <!-- Cost Sparkline -->
      <label class="flex items-center justify-between p-3 bg-[var(--theme-bg-secondary)] rounded-lg cursor-pointer hover:bg-[var(--theme-bg-tertiary)] transition-colors">
        <div class="flex items-center gap-3">
          <span class="text-xl">💰</span>
          <div>
            <div class="font-medium text-sm text-[var(--theme-text-primary)]">Cost Sparkline</div>
            <div class="text-xs text-[var(--theme-text-tertiary)]">Show cumulative cost chart</div>
          </div>
        </div>
        <input 
          type="checkbox" 
          :checked="settings.showCostSparkline"
          @change="toggleSetting('showCostSparkline')"
          class="toggle toggle-primary"
        />
      </label>

      <!-- RAG Indicator -->
      <label class="flex items-center justify-between p-3 bg-[var(--theme-bg-secondary)] rounded-lg cursor-pointer hover:bg-[var(--theme-bg-tertiary)] transition-colors">
        <div class="flex items-center gap-3">
          <span class="text-xl">📚</span>
          <div>
            <div class="font-medium text-sm text-[var(--theme-text-primary)]">RAG Indicator</div>
            <div class="text-xs text-[var(--theme-text-tertiary)]">Show context injection status</div>
          </div>
        </div>
        <input 
          type="checkbox" 
          :checked="settings.showRagIndicator"
          @change="toggleSetting('showRagIndicator')"
          class="toggle toggle-primary"
        />
      </label>

      <!-- Token Flow Overlay (Advanced) -->
      <label class="flex items-center justify-between p-3 bg-[var(--theme-bg-secondary)] rounded-lg cursor-pointer hover:bg-[var(--theme-bg-tertiary)] transition-colors border border-dashed border-[var(--theme-border-secondary)]">
        <div class="flex items-center gap-3">
          <span class="text-xl">🔀</span>
          <div>
            <div class="font-medium text-sm text-[var(--theme-text-primary)]">Token Flow Overlay</div>
            <div class="text-xs text-[var(--theme-text-tertiary)]">Show input/output token heatmap (experimental)</div>
          </div>
        </div>
        <input 
          type="checkbox" 
          :checked="settings.showTokenFlowOverlay"
          @change="toggleSetting('showTokenFlowOverlay')"
          class="toggle toggle-secondary"
        />
      </label>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useVisualizationSettings } from '../composables/useVisualizationSettings';

const { settings, toggleSetting, resetToDefaults } = useVisualizationSettings();
</script>

<style scoped>
/* Custom toggle styling using CSS variables */
.toggle {
  appearance: none;
  width: 44px;
  height: 24px;
  background-color: var(--theme-bg-tertiary);
  border: 2px solid var(--theme-border-secondary);
  border-radius: 12px;
  position: relative;
  cursor: pointer;
  transition: all 0.2s ease;
}

.toggle::before {
  content: '';
  position: absolute;
  top: 2px;
  left: 2px;
  width: 16px;
  height: 16px;
  background-color: var(--theme-text-tertiary);
  border-radius: 50%;
  transition: all 0.2s ease;
}

.toggle:checked {
  background-color: var(--theme-primary);
  border-color: var(--theme-primary);
}

.toggle:checked::before {
  transform: translateX(20px);
  background-color: white;
}

.toggle-secondary:checked {
  background-color: var(--theme-secondary, #8b5cf6);
  border-color: var(--theme-secondary, #8b5cf6);
}
</style>
