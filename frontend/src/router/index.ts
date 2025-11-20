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
    }
  ]
})

export default router
