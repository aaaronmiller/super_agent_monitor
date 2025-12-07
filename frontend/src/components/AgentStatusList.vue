<template>
  <div class="flex flex-col h-full bg-[#0f172a] border-r border-[#1e293b]">
    <!-- Header -->
    <div class="p-4 border-b border-[#1e293b] flex items-center justify-between">
      <h3 class="text-sm font-bold text-gray-400 tracking-wider">AGENTS</h3>
      <div class="text-xs text-slate-500 font-mono">{{ displayAgents ? displayAgents.length : 0 }} Total</div>
    </div>

    <!-- Agent List -->
    <div class="flex-1 overflow-y-auto p-4 space-y-3">
      <!-- Empty State -->
      <div v-if="displayAgents.length === 0" class="text-center py-8 text-slate-500">
        <div class="text-2xl mb-2">😴</div>
        <div class="text-xs">No active agents</div>
        <div class="text-[10px] text-slate-600 mt-1">Waiting for events...</div>
      </div>

      <div 
        v-for="agent in displayAgents" 
        :key="agent.id"
        class="bg-[#1e293b] rounded-lg border border-slate-700/50 p-3 hover:border-slate-600 transition-colors group relative overflow-hidden"
      >
        <!-- Status Indicator Strip -->
        <div 
          class="absolute left-0 top-0 bottom-0 w-1 transition-colors"
          :class="agent.status === 'RUNNING' ? 'bg-emerald-500' : 'bg-slate-600'"
        ></div>

        <div class="pl-2 flex flex-col gap-2">
          <!-- Top Row: Name & Status Badge -->
          <div class="flex items-center justify-between">
             <span class="text-sm font-bold text-slate-200 truncate">{{ agent.name }}</span>
             <span 
               class="text-[10px] font-bold px-1.5 py-0.5 rounded border uppercase tracking-wide"
               :class="agent.status === 'RUNNING' 
                 ? 'bg-blue-900/40 text-blue-400 border-blue-500/30' 
                 : 'bg-slate-800 text-slate-500 border-slate-700'"
             >
               {{ agent.status }}
             </span>
          </div>

          <!-- Template Label (Disler V2) -->
          <div class="flex items-center gap-1.5 -mt-1">
             <div class="w-2 h-2 rounded bg-slate-600"></div>
             <span class="text-[10px] text-slate-500 font-mono">Template: {{ agent.template }}</span>
          </div>

          <!-- Description / Last Message Snippet (Optional - from screenshot text) -->
          <p class="text-[10px] text-slate-400 leading-tight line-clamp-2 min-h-[2.5em]">
            {{ agent.lastMessage || 'Waiting for tasks...' }}
          </p>

          <!-- Context Window Usage Bar -->
          <div class="space-y-1 mt-1">
            <div class="flex justify-between text-[10px] text-slate-500 font-mono uppercase tracking-wider">
              <span>Context Window</span>
              <span class="text-slate-400">{{ (agent.contextUsed / 1000).toFixed(0) }}k / 200k</span>
            </div>
            <div class="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden flex">
               <div 
                 class="h-full bg-blue-500 rounded-full" 
                 :style="{ width: Math.min((agent.contextUsed / 200000 * 100), 100) + '%' }"
               ></div>
            </div>
          </div>

          <!-- Bottom Row: Stats Icons & Cost -->
          <div class="flex items-center justify-between mt-2 pt-2 border-t border-slate-700/50">
             <div class="flex items-center gap-3">
                <span class="text-[10px] text-slate-400 flex items-center gap-1" title="Messages">
                  💬 <span class="text-slate-300 font-bold">{{ agent.messages }}</span>
                </span>
                <span class="text-[10px] text-slate-400 flex items-center gap-1" title="Tools">
                  ⚡ <span class="text-amber-400 font-bold">{{ agent.tools }}</span>
                </span>
                 <span class="text-[10px] text-slate-400 flex items-center gap-1" title="Hooks">
                  🪝 <span class="text-teal-400 font-bold">{{ agent.hooks }}</span>
                </span>
                 <span class="text-[10px] text-slate-400 flex items-center gap-1" title="Thoughts">
                  🧠 <span class="text-purple-400 font-bold">{{ agent.thoughts }}</span>
                </span>
             </div>
             <div class="text-xs font-mono text-slate-500">
               ${{ agent.cost.toFixed(3) }}
             </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

import type { HookEvent } from '../types';

const props = defineProps<{
  events: HookEvent[];
  uniqueAgentIds: string[];
}>();

// Aggregate agent stats from events
const displayAgents = computed(() => {
  // Build agent stats from event stream
  const agentStats = new Map<string, {
    id: string;
    name: string;
    messages: number;
    tools: number;
    hooks: number;
    thoughts: number;
    cost: number;
    lastMessage: string;
    lastEventTime: number;
  }>();

  // Process events to build stats
  for (const event of props.events) {
    const agentId = event.source_app || 'unknown';
    const eventType = event.hook_event_type || '';
    
    if (!agentStats.has(agentId)) {
      agentStats.set(agentId, {
        id: agentId,
        name: agentId,
        messages: 0,
        tools: 0,
        hooks: 0,
        thoughts: 0,
        cost: 0,
        lastMessage: '',
        lastEventTime: 0
      });
    }

    const stats = agentStats.get(agentId)!;
    
    // Count by event type
    if (eventType.toLowerCase().includes('tool')) {
      stats.tools++;
    } else if (eventType.toLowerCase().includes('hook') || eventType.toLowerCase().includes('pre') || eventType.toLowerCase().includes('post')) {
      stats.hooks++;
    } else if (eventType.toLowerCase().includes('think')) {
      stats.thoughts++;
    } else {
      stats.messages++;
    }

    // Accumulate cost
    stats.cost += event.cost_usd || 0;

    // Track latest message
    const eventTime = new Date(event.timestamp || 0).getTime();
    if (eventTime > stats.lastEventTime) {
      stats.lastEventTime = eventTime;
      stats.lastMessage = event.summary || event.hook_event_type || 'Processing...';
    }
  }

  // If we have real data, return it
  if (agentStats.size > 0) {
    return Array.from(agentStats.values()).map(stats => ({
      id: stats.id,
      name: stats.name,
      status: (Date.now() - stats.lastEventTime) < 60000 ? 'RUNNING' : 'IDLE', // Active within last minute
      contextUsed: Math.min(stats.messages * 1000 + stats.tools * 500, 200000), // Estimate context usage
      contextLimit: 200000,
      messages: stats.messages,
      tools: stats.tools,
      hooks: stats.hooks,
      thoughts: stats.thoughts,
      model: 'SONNET-3.5',
      cost: stats.cost,
      template: stats.name.includes('qa') ? 'qa-agent' : 'agent-template',
      lastMessage: stats.lastMessage.substring(0, 100) + (stats.lastMessage.length > 100 ? '...' : '')
    }));
  }

  // Return empty if no events (don't show false mocks in production)
  return [];
});

</script>
