<template>
  <div class="min-h-screen flex flex-col bg-[var(--theme-bg-primary)] text-[var(--theme-text-primary)] transition-colors duration-300">
    <GlobalNavBar />

    <!-- Main Content -->
    <main class="flex-1 relative">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import GlobalNavBar from './components/GlobalNavBar.vue'
import { onMounted } from 'vue'
import { useThemes } from './composables/useThemes'

const { state, setTheme } = useThemes()

onMounted(() => {
  // Initialize theme globally
  setTheme(state.value.currentTheme)
})
</script>

<style>
/* Global transitions for theme changes */
* {
  transition-property: background-color, border-color, color, fill, stroke;
  transition-duration: 200ms;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}
</style>

