<template>
  <div class="container mx-auto px-4 py-8">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="flex items-center justify-between mb-6">
        <h1 class="text-3xl font-bold">Analytics & Cost Tracking</h1>

        <!-- Time Range Selector -->
        <div class="flex items-center gap-3">
          <select
            v-model="timeRange"
            @change="loadAllData"
            class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
          >
            <option value="7d">Last 7 Days</option>
            <option value="14d">Last 14 Days</option>
            <option value="30d">Last 30 Days</option>
            <option value="60d">Last 60 Days</option>
            <option value="90d">Last 90 Days</option>
          </select>

          <button
            @click="loadAllData"
            :disabled="loading"
            class="btn btn-secondary"
          >
            🔄 Refresh
          </button>
        </div>
      </div>

      <!-- Summary Cards -->
      <div v-if="summary" class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="card bg-gradient-to-br from-blue-50 to-blue-100">
          <div class="text-sm text-blue-600 mb-1">Total Sessions</div>
          <div class="text-3xl font-bold text-blue-900">
            {{ summary.summary.total_sessions }}
          </div>
          <div v-if="summary.trends.sessions.change_percent !== null" class="text-xs mt-1">
            <span :class="summary.trends.sessions.change_percent >= 0 ? 'text-green-600' : 'text-red-600'">
              {{ summary.trends.sessions.change_percent >= 0 ? '↑' : '↓' }}
              {{ Math.abs(summary.trends.sessions.change_percent).toFixed(1) }}%
            </span>
            vs previous period
          </div>
        </div>

        <div class="card bg-gradient-to-br from-green-50 to-green-100">
          <div class="text-sm text-green-600 mb-1">Success Rate</div>
          <div class="text-3xl font-bold text-green-900">
            {{ summary.summary.success_rate }}%
          </div>
          <div class="text-xs mt-1 text-green-700">
            {{ summary.summary.completed_count }} completed
          </div>
        </div>

        <div class="card bg-gradient-to-br from-purple-50 to-purple-100">
          <div class="text-sm text-purple-600 mb-1">Total Cost</div>
          <div class="text-3xl font-bold text-purple-900">
            ${{ summary.summary.total_cost.toFixed(2) }}
          </div>
          <div v-if="summary.trends.cost.change_percent !== null" class="text-xs mt-1">
            <span :class="summary.trends.cost.change_percent >= 0 ? 'text-red-600' : 'text-green-600'">
              {{ summary.trends.cost.change_percent >= 0 ? '↑' : '↓' }}
              {{ Math.abs(summary.trends.cost.change_percent).toFixed(1) }}%
            </span>
            vs previous period
          </div>
        </div>

        <div class="card bg-gradient-to-br from-orange-50 to-orange-100">
          <div class="text-sm text-orange-600 mb-1">Total Tokens</div>
          <div class="text-3xl font-bold text-orange-900">
            {{ formatNumber(summary.summary.total_tokens) }}
          </div>
          <div class="text-xs mt-1 text-orange-700">
            {{ summary.summary.unique_workflows }} workflows
          </div>
        </div>
      </div>

      <!-- Charts Row 1: Cost & Token Usage -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <!-- Cost Over Time Chart -->
        <div class="card">
          <h3 class="text-lg font-semibold mb-4">Cost Trend</h3>
          <div v-if="costData" class="h-64">
            <Line :data="costChartData" :options="costChartOptions" />
          </div>
          <div v-else class="h-64 flex items-center justify-center text-gray-500">
            Loading chart data...
          </div>
        </div>

        <!-- Token Usage Chart -->
        <div class="card">
          <h3 class="text-lg font-semibold mb-4">Token Usage</h3>
          <div v-if="tokenData" class="h-64">
            <Bar :data="tokenChartData" :options="tokenChartOptions" />
          </div>
          <div v-else class="h-64 flex items-center justify-center text-gray-500">
            Loading chart data...
          </div>
        </div>
      </div>

      <!-- Charts Row 2: Status Distribution & Workflow Performance -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <!-- Status Distribution Pie Chart -->
        <div class="card">
          <h3 class="text-lg font-semibold mb-4">Session Status Distribution</h3>
          <div v-if="statusData" class="h-64 flex items-center justify-center">
            <Doughnut :data="statusChartData" :options="statusChartOptions" />
          </div>
          <div v-else class="h-64 flex items-center justify-center text-gray-500">
            Loading chart data...
          </div>
        </div>

        <!-- Top Workflows Table -->
        <div class="card">
          <h3 class="text-lg font-semibold mb-4">Top Workflows by Usage</h3>
          <div v-if="workflowData && workflowData.workflows.length > 0" class="overflow-auto max-h-64">
            <table class="w-full text-sm">
              <thead class="bg-gray-50 sticky top-0">
                <tr>
                  <th class="text-left p-2">Workflow</th>
                  <th class="text-right p-2">Sessions</th>
                  <th class="text-right p-2">Success</th>
                  <th class="text-right p-2">Cost</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="workflow in workflowData.workflows.slice(0, 5)"
                  :key="workflow.id"
                  class="border-t hover:bg-gray-50"
                >
                  <td class="p-2 font-medium">{{ workflow.name }}</td>
                  <td class="text-right p-2">{{ workflow.total_sessions }}</td>
                  <td class="text-right p-2">
                    <span :class="workflow.success_rate >= 80 ? 'text-green-600' : workflow.success_rate >= 50 ? 'text-yellow-600' : 'text-red-600'">
                      {{ workflow.success_rate }}%
                    </span>
                  </td>
                  <td class="text-right p-2">${{ workflow.total_cost.toFixed(2) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else class="h-64 flex items-center justify-center text-gray-500">
            No workflow data available
          </div>
        </div>
      </div>

      <!-- Top Costly Sessions -->
      <div class="card mb-6">
        <h3 class="text-lg font-semibold mb-4">Most Expensive Sessions</h3>
        <div v-if="topCosts && topCosts.sessions.length > 0" class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="bg-gray-50">
              <tr>
                <th class="text-left p-3">Session ID</th>
                <th class="text-left p-3">Workflow</th>
                <th class="text-center p-3">Status</th>
                <th class="text-right p-3">Input Tokens</th>
                <th class="text-right p-3">Output Tokens</th>
                <th class="text-right p-3">Duration</th>
                <th class="text-right p-3">Cost</th>
                <th class="text-left p-3">Started</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="session in topCosts.sessions"
                :key="session.id"
                class="border-t hover:bg-gray-50"
              >
                <td class="p-3 font-mono text-xs">
                  <router-link
                    :to="`/sessions/${session.id}`"
                    class="text-primary-600 hover:underline"
                  >
                    {{ session.id.substring(0, 8) }}...
                  </router-link>
                </td>
                <td class="p-3">{{ session.workflow_name }}</td>
                <td class="text-center p-3">
                  <span :class="['badge', getStatusClass(session.status)]">
                    {{ session.status }}
                  </span>
                </td>
                <td class="text-right p-3">{{ formatNumber(session.input_tokens) }}</td>
                <td class="text-right p-3">{{ formatNumber(session.output_tokens) }}</td>
                <td class="text-right p-3">{{ formatDuration(session.duration_seconds) }}</td>
                <td class="text-right p-3 font-semibold">${{ session.cost_usd.toFixed(4) }}</td>
                <td class="p-3 text-xs text-gray-500">{{ formatDate(session.started_at) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else class="py-8 text-center text-gray-500">
          No session data available
        </div>
      </div>

      <!-- Workflow Performance Details -->
      <div class="card">
        <h3 class="text-lg font-semibold mb-4">Workflow Performance Analysis</h3>
        <div v-if="workflowData && workflowData.workflows.length > 0" class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="bg-gray-50">
              <tr>
                <th class="text-left p-3">Workflow</th>
                <th class="text-right p-3">Total Sessions</th>
                <th class="text-right p-3">Completed</th>
                <th class="text-right p-3">Failed</th>
                <th class="text-right p-3">Stalled</th>
                <th class="text-right p-3">Success Rate</th>
                <th class="text-right p-3">Avg Duration</th>
                <th class="text-right p-3">Total Cost</th>
                <th class="text-right p-3">Avg Cost</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="workflow in workflowData.workflows"
                :key="workflow.id"
                class="border-t hover:bg-gray-50"
              >
                <td class="p-3">
                  <div class="font-medium">{{ workflow.name }}</div>
                  <div v-if="workflow.description" class="text-xs text-gray-500 mt-1">
                    {{ workflow.description.substring(0, 60) }}...
                  </div>
                </td>
                <td class="text-right p-3 font-semibold">{{ workflow.total_sessions }}</td>
                <td class="text-right p-3 text-green-600">{{ workflow.completed_sessions }}</td>
                <td class="text-right p-3 text-red-600">{{ workflow.failed_sessions }}</td>
                <td class="text-right p-3 text-yellow-600">{{ workflow.stalled_sessions }}</td>
                <td class="text-right p-3">
                  <div
                    :class="[
                      'inline-block px-2 py-1 rounded text-xs font-semibold',
                      workflow.success_rate >= 80 ? 'bg-green-100 text-green-800' :
                      workflow.success_rate >= 50 ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    ]"
                  >
                    {{ workflow.success_rate }}%
                  </div>
                </td>
                <td class="text-right p-3">{{ formatDuration(workflow.avg_duration_seconds) }}</td>
                <td class="text-right p-3 font-semibold">${{ workflow.total_cost.toFixed(2) }}</td>
                <td class="text-right p-3 text-gray-600">${{ workflow.avg_cost.toFixed(4) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else class="py-8 text-center text-gray-500">
          No workflow data available
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAnalyticsStore } from '../stores/analytics'
import { Line, Bar, Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  Filler
} from 'chart.js'
import { format } from 'date-fns'

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  Filler
)

const analyticsStore = useAnalyticsStore()

const timeRange = ref('7d')
const loading = ref(false)

// Data refs
const summary = ref<any>(null)
const costData = ref<any>(null)
const tokenData = ref<any>(null)
const statusData = ref<any>(null)
const workflowData = ref<any>(null)
const topCosts = ref<any>(null)

onMounted(() => {
  loadAllData()
})

async function loadAllData() {
  loading.value = true

  try {
    const [summaryRes, costRes, tokenRes, statusRes, workflowRes, topCostsRes] = await Promise.all([
      analyticsStore.getSummary({ timeRange: timeRange.value }),
      analyticsStore.getCostAnalytics({ timeRange: timeRange.value, granularity: 'day' }),
      analyticsStore.getTokenUsage({ timeRange: timeRange.value }),
      analyticsStore.getStatusDistribution({ timeRange: timeRange.value }),
      analyticsStore.getWorkflowAnalytics({ timeRange: timeRange.value }),
      analyticsStore.getTopCosts({ limit: 10, timeRange: timeRange.value })
    ])

    summary.value = summaryRes
    costData.value = costRes
    tokenData.value = tokenRes
    statusData.value = statusRes
    workflowData.value = workflowRes
    topCosts.value = topCostsRes
  } catch (error) {
    console.error('Failed to load analytics:', error)
  } finally {
    loading.value = false
  }
}

// Cost Chart Data
const costChartData = computed(() => {
  if (!costData.value) return null

  const labels = costData.value.timeSeries.map((d: any) =>
    format(new Date(d.time_bucket), 'MMM dd')
  )

  return {
    labels,
    datasets: [
      {
        label: 'Cost (USD)',
        data: costData.value.timeSeries.map((d: any) => parseFloat(d.total_cost)),
        borderColor: 'rgb(147, 51, 234)',
        backgroundColor: 'rgba(147, 51, 234, 0.1)',
        fill: true,
        tension: 0.4
      }
    ]
  }
})

const costChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      callbacks: {
        label: (context: any) => `Cost: $${context.parsed.y.toFixed(4)}`
      }
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        callback: (value: any) => `$${value.toFixed(2)}`
      }
    }
  }
}

// Token Chart Data
const tokenChartData = computed(() => {
  if (!tokenData.value) return null

  const labels = tokenData.value.timeSeries.map((d: any) =>
    format(new Date(d.date), 'MMM dd')
  )

  return {
    labels,
    datasets: [
      {
        label: 'Input Tokens',
        data: tokenData.value.timeSeries.map((d: any) => parseInt(d.input_tokens)),
        backgroundColor: 'rgba(59, 130, 246, 0.8)'
      },
      {
        label: 'Output Tokens',
        data: tokenData.value.timeSeries.map((d: any) => parseInt(d.output_tokens)),
        backgroundColor: 'rgba(168, 85, 247, 0.8)'
      }
    ]
  }
})

const tokenChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top' as const
    },
    tooltip: {
      callbacks: {
        label: (context: any) => `${context.dataset.label}: ${formatNumber(context.parsed.y)}`
      }
    }
  },
  scales: {
    y: {
      stacked: true,
      beginAtZero: true,
      ticks: {
        callback: (value: any) => formatNumber(value)
      }
    },
    x: {
      stacked: true
    }
  }
}

// Status Chart Data
const statusChartData = computed(() => {
  if (!statusData.value) return null

  const statusColors: Record<string, string> = {
    completed: 'rgba(34, 197, 94, 0.8)',
    failed: 'rgba(239, 68, 68, 0.8)',
    active: 'rgba(59, 130, 246, 0.8)',
    stalled: 'rgba(251, 191, 36, 0.8)',
    pending: 'rgba(156, 163, 175, 0.8)'
  }

  return {
    labels: statusData.value.distribution.map((d: any) =>
      d.status.charAt(0).toUpperCase() + d.status.slice(1)
    ),
    datasets: [
      {
        data: statusData.value.distribution.map((d: any) => d.count),
        backgroundColor: statusData.value.distribution.map((d: any) =>
          statusColors[d.status] || 'rgba(156, 163, 175, 0.8)'
        )
      }
    ]
  }
})

const statusChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'right' as const
    },
    tooltip: {
      callbacks: {
        label: (context: any) => {
          const item = statusData.value.distribution[context.dataIndex]
          return `${context.label}: ${item.count} (${item.percentage}%)`
        }
      }
    }
  }
}

function formatNumber(num: number): string {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}

function formatDuration(seconds: number): string {
  if (!seconds) return 'N/A'
  if (seconds < 60) return `${Math.round(seconds)}s`
  const minutes = Math.floor(seconds / 60)
  const secs = Math.round(seconds % 60)
  return `${minutes}m ${secs}s`
}

function formatDate(dateString: string): string {
  return format(new Date(dateString), 'MMM dd, HH:mm')
}

function getStatusClass(status: string): string {
  const classes: Record<string, string> = {
    completed: 'badge-success',
    active: 'badge-info',
    pending: 'badge-warning',
    failed: 'badge-error',
    stalled: 'badge-warning'
  }
  return classes[status] || 'badge-info'
}
</script>
