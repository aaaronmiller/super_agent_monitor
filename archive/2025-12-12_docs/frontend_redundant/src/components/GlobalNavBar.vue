<template>
  <nav class="bg-gradient-to-r from-[var(--theme-primary)] to-[var(--theme-primary-light)] border-b-2 border-[var(--theme-primary-dark)] px-4 py-4 shadow-lg sticky top-0 z-50 transition-colors duration-300">
    <div class="flex items-center justify-between max-w-[1920px] mx-auto">
      <!-- Left: Title & Status -->
      <div class="flex items-center space-x-6">
        <router-link to="/" class="flex items-center space-x-4 group">
          <h1 class="text-2xl font-bold text-white drop-shadow-md flex items-center">
             Multi-Agent Observability
          </h1>
        </router-link>
        
        <div class="h-6 w-px bg-white/20"></div>
        
        <div class="flex items-center space-x-2 text-sm">
           <div v-if="isConnected" class="flex items-center space-x-1.5">
            <span class="relative flex h-3 w-3">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
            </span>
            <span class="text-white font-semibold drop-shadow-md">Connected</span>
          </div>
          <div v-else class="flex items-center space-x-1.5">
             <span class="relative flex h-3 w-3">
              <span class="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>
            </span>
            <span class="text-white font-semibold drop-shadow-md">Disconnected</span>
          </div>
        </div>
      </div>

      <!-- Center: Event Count (Disler Style) -->
       <div class="hidden xl:flex items-center">
          <span class="text-base text-white font-semibold drop-shadow-md bg-[var(--theme-primary-dark)] px-3 py-1.5 rounded-full border border-white/30">
            {{ events.length }} Events
          </span>
       </div>
      
      <!-- Right: Navigation & Theme Toggle (Simplified for Header integration) -->
      <div class="flex items-center space-x-3">
         <!-- Nav Links as Icon Buttons to save space/match look -->
         <div class="flex items-center space-x-1">
            <router-link 
              v-for="item in navItems.slice(0, 3)" 
              :key="item.path" 
              :to="item.path"
              class="p-2 rounded-lg bg-white/20 hover:bg-white/30 text-white transition-all duration-200 border border-white/30 hover:border-white/50 backdrop-blur-sm"
              active-class="bg-white/40 shadow-inner"
              :title="item.name"
            >
              <span>{{ item.icon }}</span>
            </router-link>
         </div>

         <div class="h-6 w-px bg-white/20 mx-2"></div>

        <!-- Theme Toggle -->
        <div class="flex bg-white/10 rounded-lg p-1 border border-white/20">
          <button 
            v-for="t in displayThemes" 
            :key="t.id"
            @click="setTheme(t.id)"
            class="p-1.5 rounded-md text-xs font-medium transition-all duration-200 flex items-center justify-center min-w-[32px]"
            :class="currentTheme === t.id 
              ? 'bg-white text-[var(--theme-primary)] shadow-sm' 
              : 'text-white/70 hover:text-white hover:bg-white/10'"
            :title="t.name"
          >
            <span>{{ t.icon }}</span>
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import { useWebSocket } from '../composables/useWebSocket';
import { useThemes } from '../composables/useThemes';

const route = useRoute();
const { isConnected, events } = useWebSocket();
const { state, setTheme } = useThemes();

const currentTheme = computed(() => state.value.currentTheme);

const displayThemes = [
  { id: 'light', name: 'Light', icon: '☀️' },
  { id: 'dark', name: 'Dark', icon: '🌙' },
  { id: 'modern', name: 'Modern', icon: '💎' },
  { id: 'midnight-purple', name: 'Purple', icon: '🔮' },
];

const navItems = [
  { name: 'Monitor', path: '/', icon: '📊' },
  { name: 'Workflows', path: '/workflows', icon: '⚡' },
  { name: 'Sessions', path: '/sessions', icon: '💬' },
  { name: 'Components', path: '/components', icon: '🧩' },
  { name: 'Memory', path: '/memory', icon: '🧠' },
  { name: 'Analytics', path: '/analytics', icon: '📈' },
  { name: 'Converter', path: '/converter', icon: '⚗️' },
];
</script>
