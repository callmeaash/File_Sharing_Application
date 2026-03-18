<script setup>
import { ref } from 'vue'
import api from '../api'

const props = defineProps({
  folderId: { type: Number, default: null },
})

const emit = defineEmits(['close', 'uploaded'])

const files = ref([])
const isDragging = ref(false)
const loading = ref(false)
const error = ref('')
const progress = ref(0)

function handleDrop(e) {
  isDragging.value = false
  const dropped = Array.from(e.dataTransfer.files)
  files.value = [...files.value, ...dropped]
}

function handleFileSelect(e) {
  const selected = Array.from(e.target.files)
  files.value = [...files.value, ...selected]
}

function removeFile(index) {
  files.value.splice(index, 1)
}

function formatBytes(bytes) {
  if (!bytes) return '0 B'
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(1024))
  return `${(bytes / Math.pow(1024, i)).toFixed(1)} ${sizes[i]}`
}

async function uploadFiles() {
  if (files.value.length === 0) return
  loading.value = true
  error.value = ''
  progress.value = 0

  try {
    for (let i = 0; i < files.value.length; i++) {
      const formData = new FormData()
      formData.append('file', files.value[i])

      const url = props.folderId ? `/files/?folder_id=${props.folderId}` : '/files/'
      await api.post(url, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      progress.value = Math.round(((i + 1) / files.value.length) * 100)
    }
    emit('uploaded')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Upload failed'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <Teleport to="body">
    <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm" @click.self="emit('close')">
      <div class="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-2xl w-full max-w-lg mx-4 shadow-xl">
        <div class="flex items-center justify-between px-6 py-4 border-b border-[var(--color-border)]">
          <h2 class="text-base font-semibold text-[var(--color-text)]">Upload Files</h2>
          <button @click="emit('close')" class="p-1 hover:bg-[var(--color-surface-hover)] rounded-lg transition-colors">
            <svg class="w-5 h-5 text-[var(--color-text-muted)]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div class="p-6">
          <div v-if="error" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-xl text-sm text-red-600">
            {{ error }}
          </div>

          <!-- Drop zone -->
          <div
            @dragover.prevent="isDragging = true"
            @dragleave="isDragging = false"
            @drop.prevent="handleDrop"
            :class="[
              'border-2 border-dashed rounded-xl p-8 text-center transition-colors cursor-pointer',
              isDragging
                ? 'border-[var(--color-accent)] bg-[var(--color-bg)]'
                : 'border-[var(--color-border)] hover:border-[var(--color-text-muted)]'
            ]"
            @click="$refs.fileInput.click()"
          >
            <svg class="w-10 h-10 text-[var(--color-text-muted)] mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
            <p class="text-sm text-[var(--color-text-muted)]">
              <span class="text-[var(--color-text)] font-medium">Click to browse</span> or drag and drop
            </p>
          </div>
          <input ref="fileInput" type="file" multiple class="hidden" @change="handleFileSelect" />

          <!-- Selected files -->
          <div v-if="files.length > 0" class="mt-4 max-h-40 overflow-y-auto space-y-2">
            <div
              v-for="(file, index) in files"
              :key="index"
              class="flex items-center justify-between px-3 py-2 bg-[var(--color-bg)] rounded-xl"
            >
              <div class="min-w-0 flex-1">
                <p class="text-sm text-[var(--color-text)] truncate">{{ file.name }}</p>
                <p class="text-xs text-[var(--color-text-muted)]">{{ formatBytes(file.size) }}</p>
              </div>
              <button @click="removeFile(index)" class="p-1 hover:bg-[var(--color-surface-hover)] rounded-lg ml-2">
                <svg class="w-4 h-4 text-[var(--color-text-muted)]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>

          <!-- Progress -->
          <div v-if="loading" class="mt-4">
            <div class="flex items-center justify-between text-xs text-[var(--color-text-muted)] mb-1">
              <span>Uploading...</span>
              <span>{{ progress }}%</span>
            </div>
            <div class="w-full bg-[var(--color-bg)] rounded-full h-1.5">
              <div class="bg-[var(--color-accent)] h-1.5 rounded-full transition-all" :style="{ width: progress + '%' }" />
            </div>
          </div>

          <div class="flex justify-end gap-2 mt-5">
            <button
              type="button"
              @click="emit('close')"
              class="px-4 py-2 text-sm font-medium text-[var(--color-text-muted)] hover:text-[var(--color-text)] transition-colors rounded-xl hover:bg-[var(--color-surface-hover)]"
            >
              Cancel
            </button>
            <button
              @click="uploadFiles"
              :disabled="files.length === 0 || loading"
              class="px-5 py-2 text-sm font-medium bg-[var(--color-accent)] text-white rounded-xl hover:bg-[var(--color-accent-hover)] transition-colors disabled:opacity-50"
            >
              {{ loading ? 'Uploading...' : `Upload ${files.length > 0 ? `(${files.length})` : ''}` }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>
