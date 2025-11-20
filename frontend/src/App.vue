<template>
  <div class="min-h-screen flex flex-col">
    <!-- Header -->
    <header class="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div class="container mx-auto px-4">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center space-x-8">
            <router-link to="/" class="flex items-center space-x-2">
              <div class="w-8 h-8 bg-gradient-to-br from-primary-500 to-primary-700 rounded-lg"></div>
              <span class="text-xl font-bold">Super Agent Monitor</span>
            </router-link>
            
            <nav class="hidden md:flex space-x-6">
              <router-link
                to="/"
                class="nav-link"
                active-class="nav-link-active"
              >
                Dashboard
              </router-link>
              <router-link
                to="/components"
                class="nav-link"
                active-class="nav-link-active"
              >
                Components
              </router-link>
              <router-link
                to="/workflows"
                class="nav-link"
                active-class="nav-link-active"
              >
                Workflows
              </router-link>
              <router-link
                to="/sessions"
                class="nav-link"
                active-class="nav-link-active"
              >
                Sessions
              </router-link>
              <router-link
                to="/memory"
                class="nav-link"
                active-class="nav-link-active"
              >
                Memory
              </router-link>
              <router-link
                to="/analytics"
                class="nav-link"
                active-class="nav-link-active"
              >
                Analytics
              </router-link>
            </nav>
          </div>
          
          <div class="flex items-center space-x-4">
            <span class="text-sm text-gray-500">v0.2.0 (Phase 2)</span>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-1">
      <router-view />
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-gray-200 mt-auto">
      <div class="container mx-auto px-4 py-6">
        <div class="text-center text-sm text-gray-500">
          <p>Elastic License 2.0 &copy; 2025 Super Agent Monitor Contributors</p>
          <p class="mt-1">Autonomous multi-agent workflows powered by Claude Code</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.nav-link {
  @apply text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium transition-colors;
}

.nav-link-active {
  @apply text-primary-600 bg-primary-50;
}
</style>
