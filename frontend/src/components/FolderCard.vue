<script setup>
import { ref } from 'vue'

const props = defineProps({
  folder: { type: Object, required: true },
})

const emit = defineEmits(['open', 'delete', 'rename', 'share'])

const showMenu = ref(false)
const isRenaming = ref(false)
const newName = ref(props.folder.name)

function startRename() {
  isRenaming.value = true
  newName.value = props.folder.name
  showMenu.value = false
}

function submitRename() {
  const name = newName.value.trim()
  if (name && name !== props.folder.name) {
    if (name.length > 255) {
      alert('Folder name cannot exceed 255 characters')
      return
    }
    emit('rename', name)
  }
  isRenaming.value = false
}

function cancelRename() {
  isRenaming.value = false
  newName.value = props.folder.name
}
</script>

<template>
  <div
    class="group relative bg-[var(--color-surface)] border border-[var(--color-border)] rounded-xl p-4 cursor-pointer hover:shadow-md hover:border-[var(--color-text-muted)] transition-all"
    @dblclick="emit('open')"
  >
    <div class="flex items-start justify-between">
      <div class="flex items-center gap-3 min-w-0 flex-1" @click="emit('open')">
        <svg class="w-8 h-8 text-[var(--color-text-muted)] shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
            d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
        </svg>
        <div class="min-w-0">
          <div v-if="isRenaming" class="flex items-center gap-1" @click.stop>
            <input
              v-model="newName"
              @keyup.enter="submitRename"
              @keyup.escape="cancelRename"
              @blur="submitRename"
              ref="renameInput"
              class="text-sm font-medium bg-[var(--color-bg)] border border-[var(--color-border)] rounded-lg px-2 py-1 w-full outline-none focus:border-[var(--color-accent)]"
              autofocus
            />
          </div>
          <p v-else class="text-sm font-medium text-[var(--color-text)] truncate">{{ folder.name }}</p>
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
            @click="showMenu = false; emit('share')"
            class="w-full text-left px-3 py-2 text-sm text-[var(--color-text)] hover:bg-[var(--color-surface-hover)] transition-colors flex items-center gap-2"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
            </svg>
            Share
          </button>
          <button
            @click="startRename"
            class="w-full text-left px-3 py-2 text-sm text-[var(--color-text)] hover:bg-[var(--color-surface-hover)] transition-colors flex items-center gap-2"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            Rename
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

  <!-- Click-away to close menu -->
  <Teleport to="body">
    <div v-if="showMenu" class="fixed inset-0 z-10" @click="showMenu = false" />
  </Teleport>
</template>
