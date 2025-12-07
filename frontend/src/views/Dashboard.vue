<template>
  <div class="h-screen w-screen bg-[var(--theme-bg-primary)] text-[var(--theme-text-primary)] transition-colors duration-300 overflow-hidden">
    <!-- Main Content Area -->
    <main class="w-full h-full flex flex-col">
      
      <!-- View Toggle & Title (Compact Header) -->
      <div class="flex items-center justify-between px-4 py-2 bg-[#0f172a] border-b border-slate-800 flex-shrink-0">
        <h2 class="text-xl font-bold text-[var(--theme-text-primary)]">Dashboard</h2>
        
        <!-- Cost Sparkline (conditionally shown) -->
        <CostSparkline :events="events" class="mr-4" />

        <div class="flex bg-[var(--theme-bg-tertiary)] rounded-lg p-1 border border-[var(--theme-border-primary)] shadow-inner relative z-20">
          <button 
            data-testid="tab-monitor"
            @click="activeView = 'monitor'"
            class="px-4 py-2 rounded-md text-sm font-medium transition-all duration-200 flex items-center space-x-2 cursor-pointer relative"
            :class="activeView === 'monitor' 
              ? 'bg-[var(--theme-primary)] text-white shadow-md' 
              : 'text-[var(--theme-text-secondary)] hover:text-[var(--theme-text-primary)] hover:bg-[var(--theme-bg-primary)]'"
          >
            <span>📊</span>
            <span>Monitor</span>
          </button>
          <button 
             data-testid="tab-deploy"
            @click="activeView = 'deploy'"
            class="px-4 py-2 rounded-md text-sm font-medium transition-all duration-200 flex items-center space-x-2 cursor-pointer relative"
            :class="activeView === 'deploy' 
              ? 'bg-[var(--theme-primary)] text-white shadow-md' 
              : 'text-[var(--theme-text-secondary)] hover:text-[var(--theme-text-primary)] hover:bg-[var(--theme-bg-primary)]'"
          >
            <span>🚀</span>
            <span>Deploy</span>
          </button>
          <button 
             data-testid="tab-settings"
            @click="activeView = 'settings'"
            class="px-4 py-2 rounded-md text-sm font-medium transition-all duration-200 flex items-center space-x-2 cursor-pointer relative"
            :class="activeView === 'settings' 
              ? 'bg-[var(--theme-primary)] text-white shadow-md' 
              : 'text-[var(--theme-text-secondary)] hover:text-[var(--theme-text-primary)] hover:bg-[var(--theme-bg-primary)]'"
          >
            <span>⚙️</span>
            <span>Settings</span>
          </button>
        </div>
      </div>
      
      <!-- Monitor View (Disler Advanced 3-Column Layout) -->
      <div v-if="activeView === 'monitor'" class="flex-1 flex overflow-hidden">
        
        <!-- Left Sidebar: Agent Status -->
        <div class="w-[280px] flex-shrink-0 hidden xl:block h-full overflow-y-auto bg-[var(--theme-bg-secondary)] border-r border-[var(--theme-border-primary)]">
           <AgentStatusList 
              :events="events"
              :unique-agent-ids="uniqueAgentIds"
           />
        </div>

        <!-- Center Panel: Timeline & Pulse -->
        <div class="flex-1 flex flex-col h-full min-w-0 bg-[#020617] relative">
            
            <!-- Top Bar: Stats & Filters -->
            <div class="flex-shrink-0 bg-[#0f172a] border-b border-[var(--theme-border-primary)] p-3 flex flex-col gap-3 z-20">
               <!-- Row 1: Global Stats (Disler Style) -->
               <div class="flex items-center justify-between text-xs font-mono text-slate-400">
                  <div class="flex items-center gap-4">
                     <div>Active: <span class="text-white font-bold">{{ activeAgentsCount }}</span></div>
                     <div>Running: <span class="text-white font-bold">{{ runningAgentsCount }}</span></div>
                     <div>Logs: <span class="text-white font-bold">{{ events.length }}</span></div>
                  </div>
                  <div class="flex items-center gap-4">
                     <div>Cost: <span class="text-emerald-400 font-bold">${{ totalCost.toFixed(2) }}</span></div>
                     <button class="hover:text-white transition-colors" @click="clearEvents()">CLEAR ALL</button>
                  </div>
               </div>

               <!-- Row 2: Filter Bar -->
               <div class="flex items-center justify-between gap-3">
                  <!-- Type Toggles -->
                  <div class="flex items-center gap-1">
                     <button 
                       @click="toggleFilter('RESPONSE')"
                       class="px-2 py-1 rounded text-[10px] font-bold uppercase transition-colors flex items-center gap-1 border"
                       :class="filters.eventType === 'RESPONSE' ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/50' : 'bg-emerald-500/5 text-emerald-400/70 border-emerald-500/20 hover:bg-emerald-500/10'"
                     >
                       <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span> RESPONSE
                     </button>
                     <button 
                       @click="toggleFilter('TOOL')"
                       class="px-2 py-1 rounded text-[10px] font-bold uppercase transition-colors flex items-center gap-1 border"
                       :class="filters.eventType === 'TOOL' ? 'bg-amber-500/20 text-amber-400 border-amber-500/50' : 'bg-amber-500/5 text-amber-400/70 border-amber-500/20 hover:bg-amber-500/10'"
                     >
                       <span class="w-1.5 h-1.5 rounded-full bg-amber-500"></span> TOOL
                     </button>
                     <button 
                       @click="toggleFilter('THINKING')"
                       class="px-2 py-1 rounded text-[10px] font-bold uppercase transition-colors flex items-center gap-1 border"
                        :class="filters.eventType === 'THINKING' ? 'bg-purple-500/20 text-purple-400 border-purple-500/50' : 'bg-purple-500/5 text-purple-400/70 border-purple-500/20 hover:bg-purple-500/10'"
                     >
                       <span class="w-1.5 h-1.5 rounded-full bg-purple-500"></span> THINKING
                     </button>
                      <button 
                        @click="toggleFilter('HOOK')"
                        class="px-2 py-1 rounded text-[10px] font-bold uppercase transition-colors flex items-center gap-1 border"
                        :class="filters.eventType === 'HOOK' ? 'bg-teal-500/20 text-teal-400 border-teal-500/50' : 'bg-teal-500/5 text-teal-400/70 border-teal-500/20 hover:bg-teal-500/10'"
                      >
                       <span class="w-1.5 h-1.5 rounded-full bg-teal-500"></span> HOOK
                     </button>
                  </div>

                  <!-- Middle: Search -->
                  <div class="flex-1 max-w-sm relative">
                     <input 
                       v-model="searchQuery"
                       type="text" 
                       placeholder="Search agents, events, tasks..."
                       class="w-full bg-[#1e293b] text-slate-300 text-xs px-3 py-1.5 rounded border border-slate-700 focus:border-blue-500 focus:outline-none placeholder-slate-500 pr-8"
                     />
                     <button
                       v-if="searchQuery"
                       @click="searchQuery = ''"
                       class="absolute right-2 top-1/2 transform -translate-y-1/2 text-slate-500 hover:text-white"
                     >
                       ✕
                     </button>
                  </div>

                  <!-- Right: Auto-Follow -->
                   <button 
                     @click="toggleStickToBottom"
                     class="px-3 py-1.5 rounded text-[10px] font-bold uppercase tracking-wide border transition-all"
                     :class="stickToBottom ? 'bg-blue-600 text-white border-blue-500 shadow-md shadow-blue-900/20' : 'bg-slate-800 text-slate-400 border-slate-700 hover:bg-slate-700'"
                   >
                     AUTO-FOLLOW
                   </button>
               </div>
            </div>

            <!-- Agent Swim Lane (Optional/Collapsible - keeping for now but maybe less prominent?) -->
            <div v-if="selectedAgentLanes.length > 0" class="flex-shrink-0 w-full bg-[var(--theme-bg-secondary)] border-b border-[var(--theme-border-primary)] px-3 py-2">
              <AgentSwimLaneContainer
                :selected-agents="selectedAgentLanes"
                :events="events"
                :time-range="currentTimeRange"
                @update:selected-agents="selectedAgentLanes = $event"
              />
            </div>

            <!-- Event Timeline (Center Fill) -->
             <div class="flex-1 overflow-hidden relative">
                <EventTimeline 
                  :events="events" 
                  :filters="filters"
                  :search-query="searchQuery"
                  v-model:stick-to-bottom="stickToBottom"
                  :unique-app-names="uniqueAgentIds"
                  :all-app-names="allAgentIds"
                  @select-agent="handleSelectAgent"
                  @select-event="selectedEvent = $event"
                />
                
                <!-- Floating Controls -->
                <div class="absolute bottom-6 right-6 flex gap-2">
                   <StickScrollButton 
                    :stick-to-bottom="stickToBottom" 
                    @toggle="toggleStickToBottom"
                  />
                </div>
            </div>
        </div>

        <!-- Right Sidebar: Details -->
        <div class="w-[350px] flex-shrink-0 hidden lg:block h-full overflow-y-auto bg-[#0f172a] border-l border-[var(--theme-border-primary)]">
            <EventDetailPanel :selected-event="selectedEvent" />
        </div>

      </div>

      <!-- Deploy View -->
      <div v-if="activeView === 'deploy'" class="flex-1 flex flex-col bg-[var(--theme-bg-secondary)] rounded-lg border border-[var(--theme-border-primary)] p-6 overflow-y-auto">
        <div class="max-w-5xl mx-auto w-full">
          <h2 class="text-2xl font-bold mb-6 text-[var(--theme-text-primary)] flex items-center">
            <span class="mr-3 text-3xl">🚀</span> 
            Deploy New Session
          </h2>
          
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <!-- Left Column: Configuration -->
            <div class="space-y-6">
              <!-- Workflow Selection -->
              <div class="bg-[var(--theme-bg-primary)] p-5 rounded-xl border border-[var(--theme-border-primary)] shadow-sm">
                 <label class="block text-sm font-semibold mb-3 text-[var(--theme-text-primary)]">
                  1. Select Workflow Template
                </label>
                <div class="space-y-3">
                  <div 
                    v-for="template in templates" 
                    :key="template.id"
                    @click="selectedTemplateId = template.id"
                    :class="[
                      'cursor-pointer p-3 rounded-lg border text-left transition-all',
                      selectedTemplateId === template.id 
                        ? 'border-[var(--theme-primary)] bg-[var(--theme-bg-tertiary)] ring-1 ring-[var(--theme-primary)]' 
                        : 'border-[var(--theme-border-secondary)] hover:border-[var(--theme-border-primary)]'
                    ]"
                  >
                    <div class="font-medium text-[var(--theme-text-primary)]">{{ template.name }}</div>
                    <div class="text-xs text-[var(--theme-text-secondary)] mt-1">{{ template.description || 'No description' }}</div>
                  </div>
                </div>
              </div>

              <!-- Orchestrator Selection -->
              <div class="bg-[var(--theme-bg-primary)] p-5 rounded-xl border border-[var(--theme-border-primary)] shadow-sm">
                <label class="block text-sm font-semibold mb-3 text-[var(--theme-text-primary)]">
                  2. Select Prime Council (Orchestrator)
                </label>
                <CouncilPatternSelector v-model="selectedOrchestrator" />
              </div>
              
               <!-- Advanced Options -->
              <div class="bg-[var(--theme-bg-primary)] p-5 rounded-xl border border-[var(--theme-border-primary)] shadow-sm">
                <label class="block text-sm font-semibold mb-3 text-[var(--theme-text-primary)]">
                  3. Runtime Configuration
                </label>
                <div class="flex flex-col gap-4">
                  <label class="flex items-center gap-3 cursor-pointer p-2 hover:bg-[var(--theme-bg-tertiary)] rounded-lg transition-colors">
                    <input type="checkbox" v-model="useE2B" class="checkbox checkbox-primary w-5 h-5 rounded border-gray-400">
                    <div>
                      <span class="font-medium text-[var(--theme-text-primary)]">E2B Sandbox Environment</span>
                      <p class="text-xs text-[var(--theme-text-secondary)]">Run safely in a cloud container (Recommended)</p>
                    </div>
                  </label>
                  
                  <label class="flex items-center gap-3 cursor-pointer p-2 hover:bg-[var(--theme-bg-tertiary)] rounded-lg transition-colors">
                    <input type="checkbox" v-model="contextInjection" class="checkbox checkbox-secondary w-5 h-5 rounded border-gray-400">
                    <div>
                      <span class="font-medium text-[var(--theme-text-primary)]">Context Injection (RAG)</span>
                      <p class="text-xs text-[var(--theme-text-secondary)]">Inject relevant files and docs into context</p>
                    </div>
                  </label>
                </div>
              </div>
            </div>

            <!-- Right Column: Task Details -->
            <div class="flex flex-col space-y-6">
              <div class="bg-[var(--theme-bg-primary)] p-5 rounded-xl border border-[var(--theme-border-primary)] shadow-sm flex-1 flex flex-col">
                <label class="block text-sm font-semibold mb-3 text-[var(--theme-text-primary)]">
                  4. Task Details
                </label>
                
                <div class="mb-4">
                  <label class="block text-xs font-medium text-[var(--theme-text-secondary)] mb-1">Session Name</label>
                  <input 
                    v-model="sessionName"
                    type="text"
                    placeholder="e.g., 'Tetris Game Implementation'"
                    class="w-full px-4 py-2 rounded-lg bg-[var(--theme-bg-secondary)] border border-[var(--theme-border-secondary)] text-[var(--theme-text-primary)] focus:outline-none focus:border-[var(--theme-primary)]"
                  />
                </div>
                
                <div class="flex-1 flex flex-col">
                  <label class="block text-xs font-medium text-[var(--theme-text-secondary)] mb-1">Instruction / Prompt</label>
                  <textarea 
                    v-model="initialPrompt"
                    class="flex-1 px-4 py-3 rounded-lg bg-[var(--theme-bg-secondary)] border border-[var(--theme-border-secondary)] text-[var(--theme-text-primary)] focus:outline-none focus:border-[var(--theme-primary)] font-mono text-sm leading-relaxed"
                    placeholder="Describe the objective for the Council..."
                  ></textarea>
                </div>
              </div>
              
              <!-- Action Bar -->
              <div class="flex items-center justify-end gap-4 pt-4">
                 <div v-if="error" class="text-red-500 text-sm px-4">
                  {{ error }}
                </div>
                
                <button 
                  @click="handleDeploy"
                  :disabled="deploying || !isValid"
                  class="px-8 py-3 bg-[var(--theme-primary)] hover:bg-blue-600 text-white font-bold rounded-lg shadow-lg transform transition-all active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                >
                  <span v-if="deploying" class="animate-spin">⏳</span>
                  <span v-else>🚀</span>
                  <span>{{ deploying ? 'Initializing Council...' : 'Launch Session' }}</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Settings View -->
      <div v-if="activeView === 'settings'" class="flex-1 flex flex-col bg-[var(--theme-bg-secondary)] rounded-lg border border-[var(--theme-border-primary)] p-6 overflow-y-auto">
        <div class="max-w-2xl mx-auto w-full">
          <h2 class="text-2xl font-bold mb-6 text-[var(--theme-text-primary)] flex items-center">
            <span class="mr-3 text-3xl">⚙️</span> 
            Visualization Settings
          </h2>
          
          <VisualizationSettingsPanel />
          
          <p class="mt-6 text-sm text-[var(--theme-text-tertiary)]">
            These settings control which enhanced data indicators are displayed in the Monitor view.
            Changes are saved automatically and persist across sessions.
          </p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useWebSocket } from '../composables/useWebSocket';
import { useWorkflowsStore } from '../stores/workflows';
import { useSessionsStore } from '../stores/sessions';
import { useRouter } from 'vue-router'; // Although we stay on dashboard mostly, we might redirect

import EventTimeline from '../components/EventTimeline.vue';
import FilterPanel from '../components/FilterPanel.vue';
import StickScrollButton from '../components/StickScrollButton.vue';
import CouncilPatternSelector from '../components/CouncilPatternSelector.vue';
import AgentSwimLaneContainer from '../components/AgentSwimLaneContainer.vue'; // New Disler Import
import AgentStatusList from '../components/AgentStatusList.vue';
import EventDetailPanel from '../components/EventDetailPanel.vue';
import CostSparkline from '../components/CostSparkline.vue';
import VisualizationSettingsPanel from '../components/VisualizationSettingsPanel.vue';
import type { TimeRange } from '../types';

// State
const activeView = ref<'monitor' | 'deploy' | 'settings'>('monitor');
const filters = ref({
  sourceApp: '',
  sessionId: '',
  eventType: ''
});
const stickToBottom = ref(true);
const uniqueAgentIds = ref<string[]>([]);
const allAgentIds = ref<string[]>([]);

// Disler UI State
const selectedAgentLanes = ref<string[]>([]);
const currentTimeRange = ref<TimeRange>('1m');
const selectedEvent = ref<any>(null); // Track selected event for details panel

// Computed stats for Header
const activeAgentsCount = computed(() => uniqueAgentIds.value.length);
const runningAgentsCount = computed(() => {
  // Simple heuristic: agents with events in last 60s
  const now = Date.now();
  const activeIds = new Set<string>();
  
  if (!events.value) return 0;
  
  // Iterate backwards for efficiency
  for (let i = events.value.length - 1; i >= 0; i--) {
     const evt = events.value[i];
     const evtTime = new Date(evt.timestamp).getTime();
     // If older than 60s, stop (assuming mostly sorted)
     if (now - evtTime > 60000) break;
     
     const id = `${evt.source_app}:${evt.session_id.slice(0, 8)}`;
     activeIds.add(id);
  }
  return activeIds.size;
});
const totalCost = computed(() => {
  return events.value.reduce((acc, evt) => acc + (evt.cost_usd || 0), 0);
});

// Deploy State
const selectedTemplateId = ref('');
const selectedOrchestrator = ref('ceo-council'); // Default
const sessionName = ref('');
const initialPrompt = ref('');
const useE2B = ref(true); // Default to E2B as per task focus
const contextInjection = ref(true);
const deploying = ref(false);
const error = ref('');

// Stores
const workflowsStore = useWorkflowsStore();
const sessionsStore = useSessionsStore();
const router = useRouter(); // If needed for complex nav

const templates = computed(() => workflowsStore.templates);

// Computed
const isValid = computed(() => {
  return selectedTemplateId.value && sessionName.value && initialPrompt.value; 
});


// Composables
const { events, isConnected, clearEvents } = useWebSocket();

// State
const searchQuery = ref('');

// Methods
const toggleFilter = (type: string) => {
  if (filters.value.eventType === type) {
    filters.value.eventType = ''; // Toggle off
  } else {
    filters.value.eventType = type;
  }
};

const toggleStickToBottom = () => {
  stickToBottom.value = !stickToBottom.value;
};

// Updated handleSelectAgent to support Swim Lane Toggling
const handleSelectAgent = (agentId: string) => {
  // Extract app name and session from agent ID (format: "app:session")
  const [app, session] = agentId.split(':');
  
  // Logic from Disler repo: Toggle swim lane for comparison
  const index = selectedAgentLanes.value.indexOf(agentId);
  if (index >= 0) {
     selectedAgentLanes.value.splice(index, 1);
  } else {
     selectedAgentLanes.value.push(agentId);
  }

  // Also update filters to focus? Or maybe just keep filter as is.
  // The Disler repo kept filters separate. Let's respect that.
  // But if user wants to filter list, they use filter panel.
  // Swim lanes are for visual comparison.
};

const handleDeploy = async () => {
  if (!isValid.value) return;
  deploying.value = true;
  error.value = '';
  
  try {
    // 1. Create Workflow Instance logic
    // We need to use workflowsStore to create an instance from template
    // console.log('Creating workflow instance...', selectedTemplateId.value, sessionName.value);
    
    // Check if we need to fetch templates first?
    if (!selectedTemplateId.value) throw new Error("No template selected");

    const instance = await workflowsStore.createWorkflow(selectedTemplateId.value, sessionName.value);
    
    if (!instance || !instance.id) throw new Error("Failed to create workflow instance");
    
    if (!instance || !instance.id) throw new Error("Failed to create workflow instance");
    
    // console.log('Workflow created:', instance.id);

    // 2. Launch Session logic
    // Use sessionsStore to launch
    const session = await sessionsStore.createSession(
      instance.id,
      selectedOrchestrator.value,
      initialPrompt.value,
      contextInjection.value,
      useE2B.value ? 'e2b' : 'local'
    );
    
    // 3. Switch to Monitor View & Filter
    activeView.value = 'monitor';
    
    // Set filters to the new session
    // Wait for a moment for socket to potentially pick it up?
    // Actually just set filter immediately.
    filters.value = {
      sourceApp: '',
      sessionId: session.id, 
      eventType: ''
    };
    
    // Add to unique agents list manually if needed to ensure it appears in dropdown immediately? 
    // FilterPanel usually reacts to `events` but `filters` can be set manually.
    
    // Reset form
    initialPrompt.value = '';
    sessionName.value = '';

    // Feedback
    alert(`Session "${session.id}" launched successfully!`);
    
  } catch (err: any) {
    console.error("Deploy failed:", err);
    error.value = err.message || "Deployment failed";
  } finally {
    deploying.value = false;
  }
};

onMounted(async () => {
  // Fetch templates for the deploy view
  await workflowsStore.fetchTemplates();
  
  // Auto-select first template if available
  if (templates.value.length > 0 && !selectedTemplateId.value) {
    selectedTemplateId.value = templates.value[0].id;
  }
});

</script>

<style>
/* Global transitions for theme changes */
* {
  transition-property: background-color, border-color, color, fill, stroke;
  transition-duration: 200ms;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}

/* Custom Scrollbar for dashboard containers */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}
::-webkit-scrollbar-track {
  background: transparent; 
}
::-webkit-scrollbar-thumb {
  background: var(--theme-border-secondary); 
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: var(--theme-border-primary); 
}
</style>
