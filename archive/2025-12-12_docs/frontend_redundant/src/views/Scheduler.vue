<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Task Scheduler</h1>
        <p class="text-gray-600 mt-2">Automate your agent workflows with precise timing.</p>
      </div>
      <button @click="openCreateModal" class="btn btn-primary">
        + New Scheduled Task
      </button>
    </div>

    <!-- Task List -->
    <div v-if="loading" class="text-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
      <p class="mt-4 text-gray-500">Loading tasks...</p>
    </div>

    <div v-else-if="tasks.length === 0" class="text-center py-12 bg-white rounded-lg shadow">
      <div class="text-6xl mb-4">🕰️</div>
      <h3 class="text-xl font-medium text-gray-900">No Scheduled Tasks</h3>
      <p class="text-gray-500 mt-2">Create your first task to run agents automatically.</p>
      <button @click="openCreateModal" class="btn btn-primary mt-6">
        Create Task
      </button>
    </div>

    <div v-else class="grid grid-cols-1 gap-6">
      <div v-for="task in tasks" :key="task.id" class="card hover:shadow-lg transition-shadow">
        <div class="flex items-start justify-between">
          <div class="flex items-center gap-4">
            <div :class="['p-3 rounded-lg', task.isActive ? 'bg-green-100 text-green-600' : 'bg-gray-100 text-gray-500']">
              <span class="text-2xl">⏰</span>
            </div>
            <div>
              <h3 class="text-lg font-bold text-gray-900">{{ task.name }}</h3>
              <div class="flex items-center gap-2 text-sm text-gray-500 mt-1">
                <code class="bg-gray-100 px-2 py-0.5 rounded">{{ task.cronExpression }}</code>
                <span>•</span>
                <span>Workflow: {{ getWorkflowName(task.workflowId) }}</span>
              </div>
            </div>
          </div>
          
          <div class="flex items-center gap-2">
            <button 
              @click="toggleTask(task)" 
              :class="['btn btn-sm', task.isActive ? 'btn-warning' : 'btn-success']"
            >
              {{ task.isActive ? 'Pause' : 'Resume' }}
            </button>
            <button @click="runTaskNow(task)" class="btn btn-sm btn-secondary">
              Run Now
            </button>
            <button @click="deleteTask(task.id)" class="btn btn-sm btn-danger">
              Delete
            </button>
          </div>
        </div>

        <div class="mt-4 flex items-center gap-6 text-sm text-gray-500 border-t pt-4">
          <div>
            <span class="font-medium">Last Run:</span>
            {{ task.lastRunAt ? new Date(task.lastRunAt).toLocaleString() : 'Never' }}
          </div>
          <div>
            <span class="font-medium">Next Run:</span>
            {{ task.isActive ? 'Scheduled' : 'Paused' }}
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-xl w-full max-w-lg p-6">
        <h2 class="text-2xl font-bold mb-6">Create Scheduled Task</h2>
        
        <form @submit.prevent="createTask">
          <div class="mb-4">
            <label class="block text-sm font-medium mb-2">Task Name</label>
            <input v-model="form.name" type="text" class="input w-full" required placeholder="e.g., Daily Morning Briefing" />
          </div>

          <div class="mb-4">
            <label class="block text-sm font-medium mb-2">Workflow</label>
            <select v-model="form.workflowId" class="input w-full" required>
              <option value="" disabled>Select a workflow</option>
              <option v-for="wf in workflows" :key="wf.id" :value="wf.id">
                {{ wf.name }}
              </option>
            </select>
          </div>

          <div class="mb-4">
            <label class="block text-sm font-medium mb-2">Schedule (Cron Expression)</label>
            <div class="flex gap-2 mb-2">
              <input v-model="form.cronExpression" type="text" class="input w-full font-mono" required placeholder="* * * * *" />
              <a href="https://crontab.guru/" target="_blank" class="btn btn-secondary whitespace-nowrap">Help</a>
            </div>
            <div class="text-xs text-gray-500 flex gap-2">
              <button type="button" @click="form.cronExpression = '0 9 * * *'" class="hover:text-primary-600 underline">Daily 9AM</button>
              <button type="button" @click="form.cronExpression = '0 * * * *'" class="hover:text-primary-600 underline">Hourly</button>
              <button type="button" @click="form.cronExpression = '*/15 * * * *'" class="hover:text-primary-600 underline">Every 15m</button>
            </div>
          </div>

          <div class="flex justify-end gap-3 mt-8">
            <button type="button" @click="showModal = false" class="btn btn-secondary">Cancel</button>
            <button type="submit" class="btn btn-primary" :disabled="submitting">
              {{ submitting ? 'Creating...' : 'Create Task' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '../services/api'

interface Task {
  id: string
  name: string
  cronExpression: string
  workflowId: string
  isActive: boolean
  lastRunAt?: string
}

interface Workflow {
  id: string
  name: string
}

const tasks = ref<Task[]>([])
const workflows = ref<Workflow[]>([])
const loading = ref(true)
const showModal = ref(false)
const submitting = ref(false)

const form = ref({
  name: '',
  workflowId: '',
  cronExpression: ''
})

onMounted(async () => {
  await Promise.all([
    loadTasks(),
    loadWorkflows()
  ])
})

async function loadTasks() {
  loading.value = true
  try {
    const { data } = await api.get('/scheduler/tasks')
    tasks.value = data
  } catch (error) {
    console.error('Failed to load tasks:', error)
  } finally {
    loading.value = false
  }
}

async function loadWorkflows() {
  try {
    const { data } = await api.get('/workflows')
    workflows.value = data
  } catch (error) {
    console.error('Failed to load workflows:', error)
  }
}

function getWorkflowName(id: string) {
  return workflows.value.find(w => w.id === id)?.name || 'Unknown Workflow'
}

function openCreateModal() {
  form.value = { name: '', workflowId: '', cronExpression: '' }
  showModal.value = true
}

async function createTask() {
  submitting.value = true
  try {
    await api.post('/scheduler/tasks', form.value)
    await loadTasks()
    showModal.value = false
  } catch (error) {
    alert('Failed to create task')
  } finally {
    submitting.value = false
  }
}

async function toggleTask(task: Task) {
  try {
    await api.patch(`/scheduler/tasks/${task.id}`, {
      isActive: !task.isActive
    })
    await loadTasks()
  } catch (error) {
    alert('Failed to update task')
  }
}

async function deleteTask(id: string) {
  if (!confirm('Are you sure you want to delete this task?')) return
  try {
    await api.delete(`/scheduler/tasks/${id}`)
    await loadTasks()
  } catch (error) {
    alert('Failed to delete task')
  }
}

async function runTaskNow(task: Task) {
  try {
    await api.post(`/scheduler/tasks/${task.id}/run`)
    alert('Task started!')
  } catch (error) {
    alert('Failed to run task')
  }
}
</script>
