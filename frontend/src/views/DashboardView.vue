<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'

const stats = ref({
  total_files: 0,
  total_storage: 0,
  total_downloads: 0,
})
const loading = ref(true)

function formatBytes(bytes) {
  if (!bytes || bytes === 0) return '0 B'
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(1024))
  return `${(bytes / Math.pow(1024, i)).toFixed(1)} ${sizes[i]}`
}

onMounted(async () => {
  try {
    const response = await api.get('/dashboard/dashboard')
    stats.value = response.data
  } catch (err) {
    console.error('Failed to load dashboard:', err)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="p-4 sm:p-6 lg:p-10 max-w-5xl">
    <h1 class="text-2xl font-semibold text-[var(--color-text)] mb-1">Dashboard</h1>
    <p class="text-sm text-[var(--color-text-muted)] mb-8">Overview of your storage</p>

    <div v-if="loading" class="flex items-center gap-3 text-[var(--color-text-muted)] text-sm">
      <svg class="animate-spin h-4 w-4" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" />
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
      </svg>
      Loading...
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-3 gap-5">
      <!-- Total Files -->
      <div class="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-2xl p-6 group hover:shadow-md transition-shadow">
        <div class="flex items-center gap-3 mb-4">
          <div class="w-10 h-10 rounded-xl bg-[var(--color-bg)] border border-[var(--color-border)] flex items-center justify-center">
            <svg class="w-5 h-5 text-[var(--color-text-muted)]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <span class="text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">Total Files</span>
        </div>
        <p class="text-3xl font-semibold text-[var(--color-text)]">{{ stats.total_files }}</p>
      </div>

      <!-- Storage Used -->
      <div class="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-2xl p-6 group hover:shadow-md transition-shadow">
        <div class="flex items-center gap-3 mb-4">
          <div class="w-10 h-10 rounded-xl bg-[var(--color-bg)] border border-[var(--color-border)] flex items-center justify-center">
            <svg class="w-5 h-5 text-[var(--color-text-muted)]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
            </svg>
          </div>
          <span class="text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">Storage Used</span>
        </div>
        <p class="text-3xl font-semibold text-[var(--color-text)]">{{ formatBytes(stats.total_storage) }}</p>
      </div>

      <!-- Total Downloads -->
      <div class="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-2xl p-6 group hover:shadow-md transition-shadow">
        <div class="flex items-center gap-3 mb-4">
          <div class="w-10 h-10 rounded-xl bg-[var(--color-bg)] border border-[var(--color-border)] flex items-center justify-center">
            <svg class="w-5 h-5 text-[var(--color-text-muted)]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
          </div>
          <span class="text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">Downloads</span>
        </div>
        <p class="text-3xl font-semibold text-[var(--color-text)]">{{ stats.total_downloads || 0 }}</p>
      </div>
    </div>
  </div>
</template>
