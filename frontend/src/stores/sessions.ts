import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../api/client'

export interface Session {
  id: string
  workflow_id: string
  workflow_name?: string
  status: 'pending' | 'active' | 'completed' | 'failed' | 'stalled'
  started_at: string
  completed_at?: string
  cost_usd?: number
  input_tokens?: number
  output_tokens?: number
  error?: string
}

export const useSessionsStore = defineStore('sessions', () => {
  const sessions = ref<Session[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchSessions(params?: { workflowId?: string; status?: string; limit?: number }) {
    loading.value = true
    error.value = null
    
    try {
      const { data } = await api.get('/sessions', { params })
      sessions.value = data.sessions
      return data.sessions
    } catch (err: any) {
      error.value = err.response?.data?.error?.message || 'Failed to fetch sessions'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function getSession(id: string) {
    try {
      const { data } = await api.get(`/sessions/${id}`)
      return data.session
    } catch (err: any) {
      error.value = err.response?.data?.error?.message || 'Failed to fetch session'
      throw err
    }
  }

  async function getSessionMetrics(id: string) {
    try {
      const { data } = await api.get(`/sessions/${id}/metrics`)
      return data.metrics
    } catch (err: any) {
      throw err
    }
  }

  async function getSessionEvents(id: string, params?: { limit?: number; offset?: number; type?: string }) {
    try {
      const { data } = await api.get(`/sessions/${id}/events`, { params })
      return data
    } catch (err: any) {
      throw err
    }
  }

  async function createSession(workflowId: string) {
    loading.value = true
    try {
      const { data } = await api.post('/sessions', { workflowId })
      await fetchSessions()
      return data.session
    } catch (err: any) {
      error.value = err.response?.data?.error?.message || 'Failed to create session'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateSession(id: string, updates: Partial<Session>) {
    loading.value = true
    try {
      const { data } = await api.patch(`/sessions/${id}`, updates)
      await fetchSessions()
      return data.session
    } catch (err: any) {
      error.value = err.response?.data?.error?.message || 'Failed to update session'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteSession(id: string) {
    loading.value = true
    try {
      await api.delete(`/sessions/${id}`)
      await fetchSessions()
    } catch (err: any) {
      error.value = err.response?.data?.error?.message || 'Failed to delete session'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    sessions,
    loading,
    error,
    fetchSessions,
    getSession,
    getSessionMetrics,
    getSessionEvents,
    createSession,
    updateSession,
    deleteSession
  }
})
