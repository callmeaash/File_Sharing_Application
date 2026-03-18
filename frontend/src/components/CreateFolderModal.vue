<script setup>
import { ref } from 'vue'
import api from '../api'

const props = defineProps({
  parentId: { type: Number, default: null },
})

const emit = defineEmits(['close', 'created'])

const folderName = ref('')
const loading = ref(false)
const error = ref('')

async function createFolder() {
  if (!folderName.value.trim()) return
  loading.value = true
  error.value = ''

  try {
    await api.post('/folders/', {
      name: folderName.value.trim(),
      parent_id: props.parentId,
    })
    emit('created')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to create folder'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <Teleport to="body">
    <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm" @click.self="emit('close')">
      <div class="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-2xl w-full max-w-md mx-4 shadow-xl">
        <div class="flex items-center justify-between px-6 py-4 border-b border-[var(--color-border)]">
          <h2 class="text-base font-semibold text-[var(--color-text)]">New Folder</h2>
          <button @click="emit('close')" class="p-1 hover:bg-[var(--color-surface-hover)] rounded-lg transition-colors">
            <svg class="w-5 h-5 text-[var(--color-text-muted)]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form @submit.prevent="createFolder" class="p-6">
          <div v-if="error" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-xl text-sm text-red-600">
            {{ error }}
          </div>

          <input
            v-model="folderName"
            type="text"
            placeholder="Folder name"
            autofocus
            class="w-full px-4 py-2.5 bg-[var(--color-bg)] border border-[var(--color-border)] rounded-xl text-sm text-[var(--color-text)] placeholder-[var(--color-text-muted)] outline-none focus:border-[var(--color-accent)] transition-colors"
          />

          <div class="flex justify-end gap-2 mt-5">
            <button
              type="button"
              @click="emit('close')"
              class="px-4 py-2 text-sm font-medium text-[var(--color-text-muted)] hover:text-[var(--color-text)] transition-colors rounded-xl hover:bg-[var(--color-surface-hover)]"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="!folderName.trim() || loading"
              class="px-5 py-2 text-sm font-medium bg-[var(--color-accent)] text-white rounded-xl hover:bg-[var(--color-accent-hover)] transition-colors disabled:opacity-50"
            >
              {{ loading ? 'Creating...' : 'Create' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </Teleport>
</template>
