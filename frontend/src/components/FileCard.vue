<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  file: { type: Object, required: true },
})

const emit = defineEmits(['download', 'delete', 'share'])
const showMenu = ref(false)

function formatBytes(bytes) {
  if (!bytes || bytes === 0) return '0 B'
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(1024))
  return `${(bytes / Math.pow(1024, i)).toFixed(1)} ${sizes[i]}`
}

const fileIcon = computed(() => {
  const mime = props.file.mime_type || ''
  if (mime.startsWith('image/')) return 'image'
  if (mime.startsWith('video/')) return 'video'
  if (mime.startsWith('audio/')) return 'audio'
  if (mime.includes('pdf')) return 'pdf'
  if (mime.includes('zip') || mime.includes('rar') || mime.includes('tar') || mime.includes('gzip')) return 'archive'
  if (mime.includes('sheet') || mime.includes('excel') || mime.includes('csv')) return 'spreadsheet'
  if (mime.includes('document') || mime.includes('msword')) return 'doc'
  if (mime.includes('presentation') || mime.includes('powerpoint')) return 'presentation'
  if (mime.includes('text/') || mime.includes('json') || mime.includes('xml') || mime.includes('javascript')) return 'code'
  return 'file'
})

const iconPaths = {
  image: 'M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z',
  video: 'M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z',
  audio: 'M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2z',
  pdf: 'M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z',
  archive: 'M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4',
  spreadsheet: 'M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z',
  doc: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
  presentation: 'M7 21l5-5 5 5M7 3v11a1 1 0 001 1h8a1 1 0 001-1V3',
  code: 'M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4',
  file: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
}
</script>

<template>
  <div class="group relative bg-[var(--color-surface)] border border-[var(--color-border)] rounded-xl p-4 hover:shadow-md hover:border-[var(--color-text-muted)] transition-all">
    <div class="flex items-start justify-between">
      <div class="flex items-center gap-3 min-w-0 flex-1">
        <svg class="w-8 h-8 text-[var(--color-text-muted)] shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" :d="iconPaths[fileIcon]" />
        </svg>
        <div class="min-w-0">
          <p class="text-sm font-medium text-[var(--color-text)] truncate" :title="file.filename">{{ file.filename }}</p>
          <p class="text-xs text-[var(--color-text-muted)] mt-0.5">{{ formatBytes(file.filesize) }}</p>
        </div>
      </div>

      <!-- Action menu -->
      <div class="relative" @click.stop>
        <button
          @click="showMenu = !showMenu"
          class="opacity-0 group-hover:opacity-100 p-1 hover:bg-[var(--color-bg)] rounded-lg transition-all"
        >
          <svg class="w-4 h-4 text-[var(--color-text-muted)]" fill="currentColor" viewBox="0 0 24 24">
            <circle cx="12" cy="6" r="1.5" />
            <circle cx="12" cy="12" r="1.5" />
            <circle cx="12" cy="18" r="1.5" />
          </svg>
        </button>

        <div
          v-if="showMenu"
          class="absolute right-0 top-8 w-40 bg-[var(--color-surface)] border border-[var(--color-border)] rounded-xl shadow-lg py-1 z-20"
        >
          <button
            @click="showMenu = false; emit('download')"
            class="w-full text-left px-3 py-2 text-sm text-[var(--color-text)] hover:bg-[var(--color-surface-hover)] transition-colors flex items-center gap-2"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            Download
          </button>
          <button
            @click="showMenu = false; emit('share')"
            class="w-full text-left px-3 py-2 text-sm text-[var(--color-text)] hover:bg-[var(--color-surface-hover)] transition-colors flex items-center gap-2"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
            </svg>
            Share
          </button>
          <div class="border-t border-[var(--color-border)] my-1" />
          <button
            @click="showMenu = false; emit('delete')"
            class="w-full text-left px-3 py-2 text-sm text-[var(--color-danger)] hover:bg-red-50 transition-colors flex items-center gap-2"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            Delete
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Click-away -->
  <Teleport to="body">
    <div v-if="showMenu" class="fixed inset-0 z-10" @click="showMenu = false" />
  </Teleport>
</template>
