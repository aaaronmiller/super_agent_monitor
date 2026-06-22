<template>
  <div class="flex flex-col h-full bg-[#0f172a] border-l border-[#1e293b] overflow-hidden">
    
    <!-- Top Bar: Selected Agent Info -->
    <div v-if="selectedEvent" class="p-4 border-b border-[#1e293b] bg-[#1e293b]/50">
       <div class="flex items-center justify-between mb-2">
          <span class="text-xs font-mono text-indigo-400">Selected Event</span>
          <span class="text-xs text-slate-500 font-mono">{{ formatTime(selectedEvent.timestamp) }}</span>
       </div>
       <div class="flex items-center gap-2">
          <div class="w-2 h-2 rounded-full bg-emerald-500"></div>
          <h2 class="text-lg font-bold text-white tracking-tight">{{ selectedEvent.source_app }}</h2>
       </div>
       <div class="mt-2 text-xs text-slate-400 font-mono">
          Session: <span class="text-slate-300">{{ selectedEvent.session_id }}</span>
       </div>
    </div>
    
    <!-- Content Area -->
    <div v-if="selectedEvent" class="flex-1 overflow-y-auto p-4 space-y-6">
      
      <!-- Orchestrator Thinking Card (Purple) -->
      <div v-if="selectedEvent.hook_event_type === 'Thinking' || selectedEvent.payload?.thoughts" class="space-y-2">
         <h3 class="text-xs font-bold text-purple-400 uppercase tracking-widest flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-purple-500 animate-pulse"></span>
            ORCHESTRATOR THINKING
         </h3>
         <div class="bg-[#1e1b4b]/30 rounded-lg border border-purple-500/30 p-4 shadow-[0_0_15px_rgba(168,85,247,0.1)]">
            <p class="text-xs text-slate-300 leading-relaxed font-mono whitespace-pre-wrap">
              {{ selectedEvent.payload?.thoughts || selectedEvent.payload?.content || selectedEvent.summary }}
            </p>
         </div>
      </div>

      <!-- Orchestrator Action/Tool Card (Orange) -->
      <div v-if="toolInfo" class="space-y-2">
        <h3 class="text-xs font-bold text-amber-500 uppercase tracking-widest flex items-center gap-2">
          <span>⚡ ORCHESTRATOR ACTION</span>
        </h3>
        <div class="bg-[#451a03]/20 rounded-lg border border-amber-500/30 p-0 overflow-hidden">
           <div class="bg-amber-950/30 px-3 py-2 border-b border-amber-500/20 flex justify-between items-center">
              <span class="text-xs font-bold text-amber-200 font-mono">Tool: {{ toolInfo.tool }}</span>
              <span class="text-[9px] text-amber-500/80 uppercase tracking-wider">Parameters</span>
           </div>
           <div class="p-3 bg-[#0f172a]/50">
             <pre class="text-[10px] sm:text-xs font-mono text-amber-100/90 overflow-x-auto whitespace-pre-wrap">{{ toolInfo.detail }}</pre>
           </div>
        </div>
      </div>

       <!-- Hook Type (If not covered above) -->
      <div v-if="!toolInfo && selectedEvent.hook_event_type !== 'Thinking'" class="space-y-2">
        <h3 class="text-xs font-bold text-teal-500 uppercase tracking-widest flex items-center gap-2">
          <span>🪝 Event Type</span>
        </h3>
        <div class="inline-block px-2 py-1 rounded bg-teal-500/10 border border-teal-500/30 text-teal-400 text-xs font-mono">
           {{ selectedEvent.hook_event_type }}
        </div>
      </div>

      <!-- Full Payload (Collapsible/Scrollable) -->
      <div class="space-y-2 pt-4 border-t border-slate-800/50">
        <h3 class="text-[10px] font-bold text-slate-600 uppercase tracking-widest">
          Raw Payload
        </h3>
        <div class="bg-[#020617] rounded border border-slate-800 p-3 overflow-hidden group hover:border-slate-700 transition-colors">
           <pre class="text-[9px] font-mono text-slate-500 overflow-x-auto group-hover:text-slate-400 transition-colors">{{ JSON.stringify(selectedEvent, null, 2) }}</pre>
        </div>
      </div>

    </div>

    <!-- Empty State -->
    <div v-else class="flex-1 flex flex-col items-center justify-center text-slate-500 p-8 text-center">
       <div class="text-4xl mb-4 opacity-20">🖱️</div>
       <p class="text-sm">Select an event from the timeline to view details.</p>
    </div>

    <!-- Footer Stats -->
    <div class="p-3 bg-[#020617] border-t border-[#1e293b] flex justify-between text-[10px] font-mono text-slate-500">
       <div v-if="selectedEvent">Payload Size: {{ JSON.stringify(selectedEvent).length }}b</div>
       <div v-if="selectedEvent">Context: 123 tokens</div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { HookEvent } from '../types';
import { format } from 'date-fns';

const props = defineProps<{
  selectedEvent: HookEvent | null;
}>();

const formatTime = (iso: string) => {
  if (!iso) return '';
  return format(new Date(iso), 'HH:mm:ss');
};

const toolInfo = computed(() => {
  if (!props.selectedEvent) return null;
  const evt = props.selectedEvent;
  
  // Try to extract tool info similar to how EventRow does it
  if (evt.hook_event_type?.includes("Tool") || evt.data?.tool) {
     return {
        tool: evt.data?.tool || evt.data?.name || "Unknown Tool",
        detail: JSON.stringify(evt.data?.input || evt.data?.args || {}, null, 2)
     }
  }
  return null;
});

</script>
