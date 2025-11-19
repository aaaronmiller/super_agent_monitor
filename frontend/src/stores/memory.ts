import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../api/client'

export interface Memory {
  id: string
  content: string
  contentType: string
  metadata: Record<string, any>
  toolName?: string
  timestamp: string
  importanceScore: number
  tags: string[]
  similarityScore?: number
  sessionId: string
  workflowId: string
}

export interface RetrievalQuery {
  query: string
  workflowId?: string
  sessionId?: string
  contentTypes?: string[]
  tags?: string[]
  limit?: number
  minSimilarity?: number
  minImportance?: number
  keywords?: string[]
}

export const useMemoryStore = defineStore('memory', () => {
  const memories = ref<Memory[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  /**
   * Search memories using RAG
   */
  async function searchMemories(query: RetrievalQuery) {
    loading.value = true
    error.value = null

    try {
      const { data } = await api.post('/memory/retrieve', query)
      memories.value = data.memories
      return data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Failed to search memories'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Get session context
   */
  async function getSessionContext(sessionId: string, limit: number = 20) {
    loading.value = true
    error.value = null

    try {
      const { data } = await api.get(`/memory/session/${sessionId}/context`, {
        params: { limit }
      })
      return data.memories
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Failed to get session context'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Get workflow history
   */
  async function getWorkflowHistory(workflowId: string, currentSessionId: string, limit: number = 10) {
    loading.value = true
    error.value = null

    try {
      const { data } = await api.get(`/memory/workflow/${workflowId}/history`, {
        params: { currentSessionId, limit }
      })
      return data.memories
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Failed to get workflow history'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Find similar memories
   */
  async function findSimilar(entryId: string, limit: number = 5) {
    loading.value = true
    error.value = null

    try {
      const { data } = await api.get(`/memory/${entryId}/similar`, {
        params: { limit }
      })
      return data.memories
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Failed to find similar memories'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Get memory details
   */
  async function getMemory(entryId: string) {
    loading.value = true
    error.value = null

    try {
      const { data } = await api.get(`/memory/${entryId}`)
      return data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Failed to get memory'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Get workflow statistics
   */
  async function getWorkflowStats(workflowId: string) {
    loading.value = true
    error.value = null

    try {
      const { data } = await api.get(`/memory/workflow/${workflowId}/stats`)
      return data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Failed to get stats'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    memories,
    loading,
    error,
    searchMemories,
    getSessionContext,
    getWorkflowHistory,
    findSimilar,
    getMemory,
    getWorkflowStats
  }
})
