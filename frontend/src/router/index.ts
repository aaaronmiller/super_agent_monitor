import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: () => import('../views/Dashboard.vue')
    },
    {
      path: '/components',
      name: 'components',
      component: () => import('../views/ComponentLibrary.vue')
    },
    {
      path: '/components/new',
      name: 'agent-builder',
      component: () => import('../views/AgentBuilder.vue')
    },
    {
      path: '/workflows',
      name: 'workflows',
      component: () => import('../views/WorkflowList.vue')
    },
    {
      path: '/workflows/create',
      name: 'workflow-create',
      component: () => import('../views/WorkflowCreate.vue')
    },
    {
      path: '/workflows/:id',
      name: 'workflow-detail',
      component: () => import('../views/WorkflowDetail.vue')
    },
    {
      path: '/sessions',
      name: 'sessions',
      component: () => import('../views/SessionList.vue')
    },
    {
      path: '/sessions/:id',
      name: 'session-detail',
      component: () => import('../views/SessionDetail.vue')
    },
    {
      path: '/memory',
      name: 'memory',
      component: () => import('../views/Memory.vue')
    },
    {
      path: '/analytics',
      name: 'analytics',
      component: () => import('../views/Analytics.vue')
    },
    {
      path: '/scheduler',
      name: 'scheduler',
      component: () => import('../views/Scheduler.vue')
    },
    {
      path: '/builder',
      name: 'builder',
      component: () => import('../views/Builder.vue')
    },
    {
      path: '/converter',
      name: 'converter',
      component: () => import('../views/McpConverter.vue')
    },
    {
      path: '/help',
      name: 'help',
      component: () => import('../views/Help.vue')
    }
  ]
})

export default router
