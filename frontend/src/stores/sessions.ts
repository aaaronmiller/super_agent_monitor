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

  async function createSession(workflowId: string, orchestratorId?: string, initialPrompt?: string, contextInjection?: boolean, runtime?: 'local' | 'e2b') {
    loading.value = true
    try {
      const { data } = await api.post('/sessions', { workflowId, orchestratorId, initialPrompt, contextInjection, runtime })
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

  // Session Control Methods
  async function startSession(id: string) {
    try {
      const { data } = await api.post(`/sessions/${id}/start`)
      return data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Failed to start session'
      throw err
    }
  }

  async function stopSession(id: string) {
    try {
      const { data } = await api.post(`/sessions/${id}/stop`)
      return data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Failed to stop session'
      throw err
    }
  }

  async function restartSession(id: string) {
    try {
      const { data } = await api.post(`/sessions/${id}/restart`)
      return data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Failed to restart session'
      throw err
    }
  }

  async function cloneSession(id: string) {
    try {
      const { data } = await api.post(`/sessions/${id}/clone`)
      return data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Failed to clone session'
      throw err
    }
  }

  async function kickSession(id: string) {
    try {
      const { data } = await api.post(`/sessions/${id}/kick`)
      return data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Failed to kick session'
      throw err
    }
  }

  async function getSessionStatus(id: string) {
    try {
      const { data } = await api.get(`/sessions/${id}/status`)
      return data
    } catch (err: any) {
      throw err
    }
  }

  async function getMonitorStats() {
    try {
      const { data } = await api.get('/sessions/monitor/stats')
      return data
    } catch (err: any) {
      throw err
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
    deleteSession,
    startSession,
    stopSession,
    restartSession,
    kickSession,
    getSessionStatus,
    getMonitorStats
  }
})
