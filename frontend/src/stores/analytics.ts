import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../api/client'

export interface CostTimeSeries {
  time_bucket: string
  session_count: number
  total_cost: number
  total_input_tokens: number
  total_output_tokens: number
  avg_cost_per_session: number
}

export interface WorkflowAnalytics {
  id: string
  name: string
  description?: string
  total_sessions: number
  completed_sessions: number
  failed_sessions: number
  stalled_sessions: number
  total_cost: number
  avg_cost: number
  total_tokens: number
  avg_duration_seconds: number
  success_rate: number
}

export interface StatusDistribution {
  status: string
  count: number
  percentage: number
}

export interface AnalyticsSummary {
  total_sessions: number
  completed_count: number
  failed_count: number
  active_count: number
  stalled_count: number
  total_cost: number
  total_tokens: number
  unique_workflows: number
  success_rate: number
}

export const useAnalyticsStore = defineStore('analytics', () => {
  const loading = ref(false)
  const error = ref<string | null>(null)

  /**
   * Get cost analytics over time
   */
  async function getCostAnalytics(params?: {
    timeRange?: string
    granularity?: string
    workflowId?: string
  }) {
    loading.value = true
    error.value = null

    try {
      const { data } = await api.get('/analytics/costs', { params })
      return data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Failed to fetch cost analytics'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Get workflow performance analytics
   */
  async function getWorkflowAnalytics(params?: { timeRange?: string }) {
    loading.value = true
    error.value = null

    try {
      const { data } = await api.get('/analytics/workflows', { params })
      return data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Failed to fetch workflow analytics'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Get session status distribution
   */
  async function getStatusDistribution(params?: {
    timeRange?: string
    workflowId?: string
  }) {
    loading.value = true
    error.value = null

    try {
      const { data } = await api.get('/analytics/status-distribution', { params })
      return data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Failed to fetch status distribution'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Get token usage breakdown
   */
  async function getTokenUsage(params?: {
    timeRange?: string
    workflowId?: string
  }) {
    loading.value = true
    error.value = null

    try {
      const { data } = await api.get('/analytics/token-usage', { params })
      return data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Failed to fetch token usage'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Get top costly sessions
   */
  async function getTopCosts(params?: {
    limit?: number
    timeRange?: string
    workflowId?: string
  }) {
    loading.value = true
    error.value = null

    try {
      const { data } = await api.get('/analytics/top-costs', { params })
      return data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Failed to fetch top costs'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Get activity heatmap
   */
  async function getActivityHeatmap(params?: {
    timeRange?: string
    workflowId?: string
  }) {
    loading.value = true
    error.value = null

    try {
      const { data } = await api.get('/analytics/activity-heatmap', { params })
      return data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Failed to fetch activity heatmap'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Get dashboard summary
   */
  async function getSummary(params?: { timeRange?: string }) {
    loading.value = true
    error.value = null

    try {
      const { data } = await api.get('/analytics/summary', { params })
      return data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Failed to fetch summary'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    error,
    getCostAnalytics,
    getWorkflowAnalytics,
    getStatusDistribution,
    getTokenUsage,
    getTopCosts,
    getActivityHeatmap,
    getSummary
  }
})
