<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-8">Visual Documentation & Methodologies</h1>

    <!-- User Journey Map -->
    <div class="card mb-12">
      <h2 class="text-xl font-bold mb-6">🗺️ User Journey & Progression Map</h2>
      
      <div class="flex flex-col md:flex-row items-center justify-center gap-4 relative">
        <!-- Start -->
        <div class="step-card bg-gray-100">
          <div class="text-2xl mb-2">🏁</div>
          <div class="font-bold">Start</div>
          <div class="text-xs text-gray-500">User Input</div>
        </div>

        <div class="arrow">⬇️</div>

        <!-- Quickstart Path -->
        <div class="flex-1 border-2 border-dashed border-primary-200 rounded-xl p-4 bg-primary-50">
          <div class="text-center text-primary-700 font-bold mb-4">🚀 Quickstart (The "Magic Box")</div>
          <div class="flex flex-col md:flex-row items-center gap-4">
            <div class="step-card bg-white">
              <div class="text-2xl mb-2">🧠</div>
              <div class="font-bold">Adaptive Router</div>
              <div class="text-xs text-gray-500">Auto-Council</div>
            </div>
            <div class="arrow">➡️</div>
            <div class="step-card bg-white">
              <div class="text-2xl mb-2">📝</div>
              <div class="font-bold">Generated Plan</div>
              <div class="text-xs text-gray-500">Dynamic Config</div>
            </div>
            <div class="arrow">➡️</div>
            <div class="step-card bg-white">
              <div class="text-2xl mb-2">🤖</div>
              <div class="font-bold">Agent Runtime</div>
              <div class="text-xs text-gray-500">Local + Proxy</div>
            </div>
          </div>
        </div>

        <div class="arrow">⬇️</div>

        <!-- Monitor -->
        <div class="step-card bg-gray-800 text-white">
          <div class="text-2xl mb-2">🖥️</div>
          <div class="font-bold">Live Monitor</div>
          <div class="text-xs text-gray-400">Feedback Loop</div>
        </div>
      </div>
    </div>

    <!-- Agent Lineages -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <!-- Researcher -->
      <div class="card border-t-4 border-blue-500">
        <h3 class="text-lg font-bold mb-4 flex items-center gap-2">
          <span class="text-2xl">🔍</span> The Researcher
        </h3>
        <p class="text-sm text-gray-600 mb-4">Exhaustive information gathering via recursive decomposition.</p>
        
        <div class="bg-gray-50 p-4 rounded-lg space-y-3">
          <div class="flex items-center gap-2 text-sm">
            <span class="badge badge-info">1</span>
            <span>Deconstruct Topic</span>
          </div>
          <div class="flex items-center gap-2 text-sm">
            <span class="badge badge-info">2</span>
            <span>Parallel Search (A, B, C)</span>
          </div>
          <div class="flex items-center gap-2 text-sm">
            <span class="badge badge-info">3</span>
            <span>Synthesize & Cite</span>
          </div>
        </div>
      </div>

      <!-- Coder -->
      <div class="card border-t-4 border-green-500">
        <h3 class="text-lg font-bold mb-4 flex items-center gap-2">
          <span class="text-2xl">💻</span> The Coder
        </h3>
        <p class="text-sm text-gray-600 mb-4">High-quality implementation via RCR Protocol.</p>
        
        <div class="bg-gray-50 p-4 rounded-lg space-y-3">
          <div class="flex items-center gap-2 text-sm">
            <span class="badge badge-success">1</span>
            <span>Implement Code</span>
          </div>
          <div class="flex items-center gap-2 text-sm">
            <span class="badge badge-warning">2</span>
            <span>Reflect & Critique</span>
          </div>
          <div class="flex items-center gap-2 text-sm">
            <span class="badge badge-success">3</span>
            <span>Refine & Fix</span>
          </div>
        </div>
      </div>

      <!-- Planner -->
      <div class="card border-t-4 border-purple-500">
        <h3 class="text-lg font-bold mb-4 flex items-center gap-2">
          <span class="text-2xl">🧠</span> The Planner
        </h3>
        <p class="text-sm text-gray-600 mb-4">Strategic decomposition via OODA Loop.</p>
        
        <div class="bg-gray-50 p-4 rounded-lg space-y-3">
          <div class="flex items-center gap-2 text-sm">
            <span class="badge badge-info">1</span>
            <span>Observe Context</span>
          </div>
          <div class="flex items-center gap-2 text-sm">
            <span class="badge badge-info">2</span>
            <span>Orient (RAG)</span>
          </div>
          <div class="flex items-center gap-2 text-sm">
            <span class="badge badge-purple">3</span>
            <span>Decide & Delegate</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.step-card {
  @apply flex flex-col items-center justify-center p-4 rounded-lg shadow-sm border border-gray-200 w-32 h-32 text-center transition-transform hover:scale-105;
}
.arrow {
  @apply text-2xl text-gray-300 font-bold;
}
.badge-purple {
  @apply bg-purple-100 text-purple-800 px-2 py-0.5 rounded text-xs font-medium;
}
</style>
