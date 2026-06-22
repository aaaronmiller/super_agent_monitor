import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../api/client'

export interface Workflow {
  id: string
  name: string
  description?: string
  template_id?: string
  status: string
  config?: any
  created_at: string
  updated_at?: string
}

export const useWorkflowsStore = defineStore('workflows', () => {
  const workflows = ref<Workflow[]>([])
  const templates = ref<any[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchTemplates() {
    loading.value = true
    error.value = null
    
    try {
      const { data } = await api.get('/workflows')
      templates.value = data.workflows
      return data.workflows
    } catch (err: any) {
      error.value = err.response?.data?.error?.message || 'Failed to fetch templates'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchWorkflows() {
    loading.value = true
    error.value = null
    
    try {
      const { data } = await api.get('/workflows/instances/list')
      workflows.value = data.instances
      return data.instances
    } catch (err: any) {
      error.value = err.response?.data?.error?.message || 'Failed to fetch workflows'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function getWorkflow(id: string) {
    try {
      const { data } = await api.get(`/workflows/instances/${id}`)
      return data.instance
    } catch (err: any) {
      error.value = err.response?.data?.error?.message || 'Failed to fetch workflow'
      throw err
    }
  }

  async function createWorkflow(templateId: string, name?: string) {
    loading.value = true
    try {
      const { data } = await api.post('/workflows/instances', {
        templateId,
        name
      })
      await fetchWorkflows()
      return data.instance
    } catch (err: any) {
      error.value = err.response?.data?.error?.message || 'Failed to create workflow'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteWorkflow(id: string) {
    loading.value = true
    try {
      await api.delete(`/workflows/instances/${id}`)
      await fetchWorkflows()
    } catch (err: any) {
      error.value = err.response?.data?.error?.message || 'Failed to delete workflow'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function validateWorkflow(id: string) {
    try {
      const { data } = await api.post(`/workflows/${id}/validate`)
      return data
    } catch (err: any) {
      throw err
    }
  }

  async function generateWorkflow(id: string) {
    loading.value = true
    try {
      const { data } = await api.post(`/workflows/${id}/generate`)
      return data
    } catch (err: any) {
      error.value = err.response?.data?.error?.message || 'Failed to generate workflow'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    workflows,
    templates,
    loading,
    error,
    fetchTemplates,
    fetchWorkflows,
    getWorkflow,
    createWorkflow,
    deleteWorkflow,
    validateWorkflow,
    generateWorkflow
  }
})
