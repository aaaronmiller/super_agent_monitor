<template>
  <nav class="bg-gradient-to-r from-[var(--theme-bg-secondary)] to-[var(--theme-bg-primary)] border-b border-[var(--theme-border-primary)] px-6 py-3 shadow-md sticky top-0 z-50 transition-colors duration-300">
    <div class="flex items-center justify-between max-w-[1920px] mx-auto">
      <!-- Left: Title & Status -->
      <div class="flex items-center space-x-6">
        <router-link to="/" class="flex items-center space-x-4 group">
          <h1 class="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-[var(--theme-primary)] to-[var(--theme-primary-light)] drop-shadow-sm flex items-center">
            <span class="text-3xl mr-2 transform group-hover:scale-110 transition-transform">🕵️‍♂️</span>
            Super Agent Monitor
          </h1>
        </router-link>
        
        <div class="h-6 w-px bg-[var(--theme-border-primary)]"></div>
        
        <div class="flex items-center space-x-2 text-sm">
          <span class="flex h-2.5 w-2.5 rounded-full" :class="isConnected ? 'bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.6)]' : 'bg-red-500'"></span>
          <span :class="isConnected ? 'text-green-600 dark:text-green-400 font-medium' : 'text-red-600 dark:text-red-400 font-medium'">
            {{ isConnected ? 'Connected' : 'Disconnected' }}
          </span>
        </div>
      </div>

      <!-- Center: Navigation Links -->
      <div class="hidden xl:flex items-center space-x-1 bg-[var(--theme-bg-tertiary)] rounded-lg p-1 border border-[var(--theme-border-primary)] shadow-inner">
        <router-link 
          v-for="item in navItems" 
          :key="item.path" 
          :to="item.path"
          class="px-3 py-1.5 rounded-md text-sm font-medium transition-all duration-200 flex items-center space-x-2"
          active-class="bg-[var(--theme-primary)] text-white shadow-md"
          :class="$route.path === item.path ? '' : 'text-[var(--theme-text-secondary)] hover:text-[var(--theme-text-primary)] hover:bg-[var(--theme-bg-primary)]'"
        >
          <span>{{ item.icon }}</span>
          <span>{{ item.name }}</span>
        </router-link>
      </div>
      
      <!-- Right: Theme Toggle -->
      <div class="flex items-center space-x-4">
        <div class="flex bg-[var(--theme-bg-tertiary)] rounded-lg p-1 border border-[var(--theme-border-primary)] shadow-inner">
          <button 
            v-for="t in displayThemes" 
            :key="t.id"
            @click="setTheme(t.id)"
            class="px-3 py-1.5 rounded-md text-xs font-medium transition-all duration-200 flex items-center space-x-1"
            :class="currentTheme === t.id 
              ? 'bg-[var(--theme-primary)] text-white shadow-md transform scale-105' 
              : 'text-[var(--theme-text-secondary)] hover:text-[var(--theme-text-primary)] hover:bg-[var(--theme-bg-primary)]'"
          >
            <span>{{ t.icon }}</span>
            <span class="hidden 2xl:inline">{{ t.name }}</span>
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
const { isConnected } = useWebSocket();
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
