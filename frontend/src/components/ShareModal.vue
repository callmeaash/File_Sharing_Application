<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'

const props = defineProps({
  item: { type: Object, required: true },
  type: { type: String, required: true, validator: (v) => ['file', 'folder'].includes(v) },
})

const emit = defineEmits(['close'])

const accessType = ref('only_me')
const timeUnit = ref('hours')
const timeValue = ref(1)
const shareLink = ref('')
const loading = ref(false)
const error = ref('')
const copied = ref(false)
const fetching = ref(true)

const itemLabel = props.type === 'file' ? 'File' : 'Folder'

onMounted(async () => {
  try {
    const response = await api.get(`/share/${props.type}/${props.item.id}/access`)
    const data = response.data
    
    accessType.value = data.access_type
    if (data.share_token) {
      const routePrefix = props.type === 'file' ? 'shared' : 'shared-folder'
      shareLink.value = `${window.location.origin}/${routePrefix}/${data.share_token}`
    }
    
    // Attempt to map expiry_time back to relative time if needed (simplified here, in reality 
    // it's an absolute datetime, so time value is just kept at defaults if we can't reverse engineer easily)
    
  } catch (err) {
    console.error('Failed to load current sharing settings', err)
  } finally {
    fetching.value = false
  }
})

async function updateAccess() {
  loading.value = true
  error.value = ''
  shareLink.value = ''

  try {
    const payload = {
      access_type: accessType.value,
    }

    if (accessType.value === 'timed_access') {
      if (timeValue.value <= 0) {
        error.value = 'Time value must be greater than 0'
        loading.value = false
        return
      }
      payload.time_unit = timeUnit.value
      payload.time_value = timeValue.value
    }

    const response = await api.patch(`/share/${props.type}/${props.item.id}/access`, payload)

    if (response.data.share_token) {
      const routePrefix = props.type === 'file' ? 'shared' : 'shared-folder'
      shareLink.value = `${window.location.origin}/${routePrefix}/${response.data.share_token}`
    }
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to update access'
  } finally {
    loading.value = false
  }
}

function copyLink() {
  navigator.clipboard.writeText(shareLink.value)
  copied.value = true
  setTimeout(() => (copied.value = false), 2000)
}
</script>

<template>
  <Teleport to="body">
    <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm" @click.self="emit('close')">
      <div class="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-2xl w-full max-w-md mx-4 shadow-xl">
        <div class="flex items-center justify-between px-6 py-4 border-b border-[var(--color-border)]">
          <div>
            <h2 class="text-base font-semibold text-[var(--color-text)]">Share {{ itemLabel }}</h2>
            <p class="text-xs text-[var(--color-text-muted)] mt-0.5 truncate max-w-[280px]">{{ item.filename || item.name }}</p>
          </div>
          <button @click="emit('close')" class="p-1 hover:bg-[var(--color-surface-hover)] rounded-lg transition-colors">
            <svg class="w-5 h-5 text-[var(--color-text-muted)]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div class="p-6">
          <div v-if="fetching" class="flex justify-center py-6">
            <svg class="animate-spin h-6 w-6 text-[var(--color-text-muted)]" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" />
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
          </div>
          <template v-else>
            <div v-if="error" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-xl text-sm text-red-600">
              {{ error }}
            </div>

            <!-- Access type selector -->
          <label class="block text-sm font-medium text-[var(--color-text)] mb-2">Access</label>
          <div class="space-y-2 mb-5">
            <label
              v-for="option in [
                { value: 'only_me', label: 'Only me', desc: 'No one else can access' },
                { value: 'anyone_with_link', label: 'Anyone with link', desc: 'Share via link' },
                { value: 'timed_access', label: 'Timed access', desc: 'Link expires after set time' },
              ]"
              :key="option.value"
              class="flex items-start gap-3 p-3 rounded-xl border cursor-pointer transition-colors"
              :class="accessType === option.value
                ? 'border-[var(--color-accent)] bg-[var(--color-bg)]'
                : 'border-[var(--color-border)] hover:bg-[var(--color-surface-hover)]'"
            >
              <input
                type="radio"
                v-model="accessType"
                :value="option.value"
                class="mt-0.5 accent-[var(--color-accent)]"
              />
              <div>
                <p class="text-sm font-medium text-[var(--color-text)]">{{ option.label }}</p>
                <p class="text-xs text-[var(--color-text-muted)]">{{ option.desc }}</p>
              </div>
            </label>
          </div>

          <!-- Timed access options -->
          <div v-if="accessType === 'timed_access'" class="flex items-center gap-3 mb-5">
            <input
              v-model.number="timeValue"
              type="number"
              min="1"
              class="w-20 px-3 py-2 bg-[var(--color-bg)] border border-[var(--color-border)] rounded-xl text-sm text-[var(--color-text)] outline-none focus:border-[var(--color-accent)]"
            />
            <select
              v-model="timeUnit"
              class="px-3 py-2 bg-[var(--color-bg)] border border-[var(--color-border)] rounded-xl text-sm text-[var(--color-text)] outline-none focus:border-[var(--color-accent)]"
            >
              <option value="minutes">Minutes</option>
              <option value="hours">Hours</option>
              <option value="days">Days</option>
            </select>
          </div>

          <!-- Share link display -->
          <div v-if="shareLink" class="mb-5">
            <label class="block text-sm font-medium text-[var(--color-text)] mb-1.5">Share Link</label>
            <div class="flex items-center gap-2">
              <input
                :value="shareLink"
                readonly
                class="flex-1 px-3 py-2 bg-[var(--color-bg)] border border-[var(--color-border)] rounded-xl text-xs text-[var(--color-text-muted)] outline-none"
              />
              <button
                @click="copyLink"
                class="shrink-0 px-3 py-2 text-sm font-medium border border-[var(--color-border)] rounded-xl hover:bg-[var(--color-surface-hover)] transition-colors"
              >
                {{ copied ? '✓ Copied' : 'Copy' }}
              </button>
            </div>
          </div>

          <div class="flex justify-end gap-2">
            <button
              @click="emit('close')"
              class="px-4 py-2 text-sm font-medium text-[var(--color-text-muted)] hover:text-[var(--color-text)] transition-colors rounded-xl hover:bg-[var(--color-surface-hover)]"
            >
              Close
            </button>
            <button
              @click="updateAccess"
              :disabled="loading"
              class="px-5 py-2 text-sm font-medium bg-[var(--color-accent)] text-white rounded-xl hover:bg-[var(--color-accent-hover)] transition-colors disabled:opacity-50"
            >
              {{ loading ? 'Saving...' : 'Update Access' }}
            </button>
          </div>
          </template>
        </div>
      </div>
    </div>
  </Teleport>
</template>
