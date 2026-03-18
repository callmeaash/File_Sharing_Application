<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const token = route.params.token

const loading = ref(true)
const error = ref('')
const downloading = ref(false)

onMounted(async () => {
  loading.value = false
})

async function downloadFile() {
  downloading.value = true
  error.value = ''

  try {
    const response = await axios.get(`http://localhost:8000/share/file/${token}`, {
      responseType: 'blob',
    })

    const contentDisposition = response.headers['content-disposition']
    let filename = 'download'
    if (contentDisposition) {
      const match = contentDisposition.match(/filename="?(.+?)"?$/i)
      if (match) filename = match[1]
    }

    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', filename)
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
  } catch (err) {
    if (err.response?.status === 404) {
      error.value = 'This link is invalid or has expired.'
    } else {
      error.value = 'Something went wrong. Please try again.'
    }
  } finally {
    downloading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-[var(--color-bg)] px-4">
    <div class="w-full max-w-md text-center">
      <!-- Logo -->
      <div class="inline-flex items-center justify-center w-14 h-14 bg-[var(--color-text)] rounded-2xl mb-5">
        <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
            d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
        </svg>
      </div>
      <h1 class="text-2xl font-semibold text-[var(--color-text)] tracking-tight mb-1">FileVault</h1>
      <p class="text-sm text-[var(--color-text-muted)] mb-8">A file has been shared with you</p>

      <div class="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-2xl p-8 shadow-sm">
        <!-- Error state -->
        <div v-if="error" class="text-center">
          <div class="inline-flex items-center justify-center w-12 h-12 bg-red-50 rounded-xl mb-4">
            <svg class="w-6 h-6 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
          </div>
          <p class="text-sm text-[var(--color-text)]">{{ error }}</p>
          <button
            @click="error = ''"
            class="mt-4 px-4 py-2 text-sm font-medium text-[var(--color-text-muted)] hover:text-[var(--color-text)] transition-colors"
          >
            Try again
          </button>
        </div>

        <!-- Download ready -->
        <div v-else class="text-center">
          <div class="inline-flex items-center justify-center w-12 h-12 bg-[var(--color-bg)] border border-[var(--color-border)] rounded-xl mb-4">
            <svg class="w-6 h-6 text-[var(--color-text-muted)]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <p class="text-sm text-[var(--color-text)] mb-5">Click below to download the shared file</p>

          <button
            @click="downloadFile"
            :disabled="downloading"
            class="w-full py-2.5 bg-[var(--color-accent)] text-white rounded-xl text-sm font-medium hover:bg-[var(--color-accent-hover)] transition-colors disabled:opacity-50 disabled:cursor-not-allowed inline-flex items-center justify-center gap-2"
          >
            <template v-if="downloading">
              <svg class="animate-spin h-4 w-4" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              Downloading...
            </template>
            <template v-else>
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                  d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              Download File
            </template>
          </button>
        </div>
      </div>

      <p class="text-xs text-[var(--color-text-muted)] mt-6">
        Shared via <span class="font-medium text-[var(--color-text)]">FileVault</span>
      </p>
    </div>
  </div>
</template>
