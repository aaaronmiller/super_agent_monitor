import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../api/client'

export interface Component {
  id: string
  name: string
  displayName?: string
  description?: string
  category: 'agent' | 'skill' | 'hook' | 'script' | 'orchestrator'
  tags?: string[]
  dependencies?: string[]
  model?: string
  version?: string
  pattern?: string
}

export const useComponentsStore = defineStore('components', () => {
  const components = ref<Component[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const stats = ref<any>(null)

  const componentsByCategory = computed(() => {
    const groups: Record<string, Component[]> = {
      agent: [],
      skill: [],
      hook: [],
      script: [],
      orchestrator: []
    }
    
    components.value.forEach(c => {
      if (c.category) {
        groups[c.category].push(c)
      }
    })
    
    return groups
  })

  async function fetchComponents(params?: { category?: string; tag?: string; search?: string }) {
    loading.value = true
    error.value = null
    
    try {
      const { data } = await api.get('/components', { params })
      components.value = data.components
      return data.components
    } catch (err: any) {
      error.value = err.response?.data?.error?.message || 'Failed to fetch components'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchStats() {
    try {
      const { data } = await api.get('/components/stats')
      stats.value = data
      return data
    } catch (err: any) {
      console.error('Failed to fetch stats:', err)
      throw err
    }
  }

  async function getComponent(id: string) {
    try {
      const { data } = await api.get(`/components/${id}`)
      return data.component
    } catch (err: any) {
      error.value = err.response?.data?.error?.message || 'Failed to fetch component'
      throw err
    }
  }

  async function getRecommendations(selectedComponentIds: string[]) {
    try {
      const { data } = await api.post('/components/recommendations', {
        selectedComponents: selectedComponentIds
      })
      return data.recommendations
    } catch (err: any) {
      console.error('Failed to get recommendations:', err)
      throw err
    }
  }

  async function rescan() {
    loading.value = true
    try {
      const { data } = await api.post('/components/scan')
      await fetchComponents()
      await fetchStats()
      return data
    } catch (err: any) {
      error.value = err.response?.data?.error?.message || 'Failed to rescan components'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    components,
    loading,
    error,
    stats,
    componentsByCategory,
    fetchComponents,
    fetchStats,
    getComponent,
    getRecommendations,
    rescan
  }
})
