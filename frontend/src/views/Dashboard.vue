<template>
  <div class="min-h-screen bg-[var(--theme-bg-primary)] text-[var(--theme-text-primary)] transition-colors duration-300">
    <!-- Main Content Area -->
    <main class="max-w-[1920px] mx-auto p-6 mobile:p-2 h-[calc(100vh-64px)] overflow-hidden flex flex-col">
      
      <!-- View Toggle & Title (Moved from Header) -->
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl font-bold text-[var(--theme-text-primary)]">Dashboard</h2>
        
        <div class="flex bg-[var(--theme-bg-tertiary)] rounded-lg p-1 border border-[var(--theme-border-primary)] shadow-inner">
          <button 
            @click="activeView = 'monitor'"
            class="px-4 py-2 rounded-md text-sm font-medium transition-all duration-200 flex items-center space-x-2"
            :class="activeView === 'monitor' 
              ? 'bg-[var(--theme-primary)] text-white shadow-md' 
              : 'text-[var(--theme-text-secondary)] hover:text-[var(--theme-text-primary)] hover:bg-[var(--theme-bg-primary)]'"
          >
            <span>📊</span>
            <span>Monitor</span>
          </button>
          <button 
            @click="activeView = 'deploy'"
            class="px-4 py-2 rounded-md text-sm font-medium transition-all duration-200 flex items-center space-x-2"
            :class="activeView === 'deploy' 
              ? 'bg-[var(--theme-primary)] text-white shadow-md' 
              : 'text-[var(--theme-text-secondary)] hover:text-[var(--theme-text-primary)] hover:bg-[var(--theme-bg-primary)]'"
          >
            <span>🚀</span>
            <span>Deploy</span>
          </button>
        </div>
      </div>
      
      <!-- Monitor View -->
      <div v-show="activeView === 'monitor'" class="flex-1 flex flex-col space-y-4 h-full overflow-hidden">
        <!-- Top Section: Pulse Chart & Filters -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 flex-shrink-0">
          <!-- Live Pulse Chart (2/3 width) -->
          <div class="lg:col-span-2">
            <LivePulseChart 
              :events="events" 
              @update:unique-agent-ids="uniqueAgentIds = $event"
              @update:all-agent-ids="allAgentIds = $event"
            />
          </div>
          
          <!-- Filter Panel (1/3 width) -->
          <div class="lg:col-span-1 h-full">
            <FilterPanel 
              v-model:filters="filters" 
              :events="events"
            />
          </div>
        </div>
        
        <!-- Bottom Section: Event Timeline -->
        <div class="flex-1 min-h-0 bg-[var(--theme-bg-secondary)] rounded-lg shadow-lg border border-[var(--theme-border-primary)] flex flex-col overflow-hidden relative">
          <EventTimeline 
            :events="events" 
            :filters="filters"
            v-model:stick-to-bottom="stickToBottom"
            :unique-app-names="uniqueAgentIds"
            :all-app-names="allAgentIds"
            @select-agent="handleSelectAgent"
          />
          
          <!-- Stick Scroll Button -->
          <StickScrollButton 
            :stick-to-bottom="stickToBottom" 
            @toggle="toggleStickToBottom"
          />
        </div>
      </div>

      <!-- Deploy View (Placeholder for now) -->
      <div v-show="activeView === 'deploy'" class="flex-1 flex items-center justify-center bg-[var(--theme-bg-secondary)] rounded-lg border border-[var(--theme-border-primary)]">
        <div class="text-center">
          <div class="text-6xl mb-4">🚀</div>
          <h2 class="text-3xl font-bold text-[var(--theme-primary)] mb-2">Deployment Center</h2>
          <p class="text-[var(--theme-text-secondary)] text-lg">Workflow deployment features coming soon...</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useWebSocket } from '../composables/useWebSocket';

import LivePulseChart from '../components/LivePulseChart.vue';
import EventTimeline from '../components/EventTimeline.vue';
import FilterPanel from '../components/FilterPanel.vue';
import StickScrollButton from '../components/StickScrollButton.vue';

// State
const activeView = ref<'monitor' | 'deploy'>('monitor');
const filters = ref({
  sourceApp: '',
  sessionId: '',
  eventType: ''
});
const stickToBottom = ref(true);
const uniqueAgentIds = ref<string[]>([]);
const allAgentIds = ref<string[]>([]);

// Composables
const { events, isConnected } = useWebSocket();

// Methods
const toggleStickToBottom = () => {
  stickToBottom.value = !stickToBottom.value;
};

const handleSelectAgent = (agentId: string) => {
  // Extract app name and session from agent ID (format: "app:session")
  const [app, session] = agentId.split(':');
  
  // Update filters to focus on this agent
  filters.value = {
    ...filters.value,
    sourceApp: app || '',
    sessionId: session || ''
  };
};


</script>

<style>
/* Global transitions for theme changes */
* {
  transition-property: background-color, border-color, color, fill, stroke;
  transition-duration: 200ms;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}
</style>
