<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const token = route.params.token

const loading = ref(true)
const error = ref('')
const folderData = ref(null)

function formatBytes(bytes) {
  if (!bytes || bytes === 0) return '0 B'
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(1024))
  return `${(bytes / Math.pow(1024, i)).toFixed(1)} ${sizes[i]}`
}

onMounted(async () => {
  try {
    const response = await axios.get(`http://localhost:8000/share/folder/${token}`)
    folderData.value = response.data
  } catch (err) {
    if (err.response?.status === 404) {
      error.value = err.response?.data?.detail || 'This link is invalid or has expired.'
    } else {
      error.value = 'Something went wrong. Please try again.'
    }
  } finally {
    loading.value = false
  }
})

async function downloadFile(file) {
  try {
    const response = await axios.get(`http://localhost:8000/share/folder/${token}/file/${file.id}`, {
      responseType: 'blob',
    })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', file.filename)
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
  } catch (err) {
    alert('Failed to download file')
  }
}
</script>

<template>
  <div class="min-h-screen bg-[var(--color-bg)] px-4 py-10">
    <div class="max-w-2xl mx-auto">
      <!-- Logo -->
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-12 h-12 bg-[var(--color-text)] rounded-2xl mb-4">
          <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
          </svg>
        </div>
        <h1 class="text-xl font-semibold text-[var(--color-text)] tracking-tight">FileVault</h1>
        <p class="text-sm text-[var(--color-text-muted)] mt-1">A folder has been shared with you</p>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="flex items-center justify-center py-16">
        <svg class="animate-spin h-6 w-6 text-[var(--color-text-muted)]" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" />
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
        </svg>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-2xl p-8 text-center">
        <div class="inline-flex items-center justify-center w-12 h-12 bg-red-50 rounded-xl mb-4">
          <svg class="w-6 h-6 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
        </div>
        <p class="text-sm text-[var(--color-text)]">{{ error }}</p>
      </div>

      <!-- Folder contents -->
      <div v-else-if="folderData" class="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-2xl overflow-hidden">
        <div class="px-6 py-4 border-b border-[var(--color-border)] flex items-center gap-3">
          <svg class="w-6 h-6 text-[var(--color-text-muted)]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
          </svg>
          <h2 class="text-base font-semibold text-[var(--color-text)]">{{ folderData.folder_name }}</h2>
          <span class="text-xs text-[var(--color-text-muted)] ml-auto">{{ folderData.files.length }} files</span>
        </div>

        <div v-if="folderData.files.length === 0" class="px-6 py-10 text-center">
          <p class="text-sm text-[var(--color-text-muted)]">This folder is empty</p>
        </div>

        <div v-else>
          <div
            v-for="file in folderData.files"
            :key="file.id"
            class="flex items-center justify-between px-6 py-3 border-b border-[var(--color-border)] last:border-b-0 hover:bg-[var(--color-surface-hover)] transition-colors"
          >
            <div class="flex items-center gap-3 min-w-0 flex-1">
              <svg class="w-5 h-5 text-[var(--color-text-muted)] shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <div class="min-w-0">
                <p class="text-sm text-[var(--color-text)] truncate">{{ file.filename }}</p>
                <p class="text-xs text-[var(--color-text-muted)]">{{ formatBytes(file.filesize) }}</p>
              </div>
            </div>
            <button
              @click="downloadFile(file)"
              class="shrink-0 p-2 hover:bg-[var(--color-bg)] rounded-lg transition-colors"
              title="Download"
            >
              <svg class="w-4 h-4 text-[var(--color-text-muted)]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                  d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <p class="text-center text-xs text-[var(--color-text-muted)] mt-6">
        Shared via <span class="font-medium text-[var(--color-text)]">FileVault</span>
      </p>
    </div>
  </div>
</template>
