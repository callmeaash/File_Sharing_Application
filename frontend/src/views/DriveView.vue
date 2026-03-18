<script setup>
import { ref, watch, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../api'
import Breadcrumb from '../components/Breadcrumb.vue'
import FolderCard from '../components/FolderCard.vue'
import FileCard from '../components/FileCard.vue'
import CreateFolderModal from '../components/CreateFolderModal.vue'
import UploadModal from '../components/UploadModal.vue'
import ShareModal from '../components/ShareModal.vue'

const route = useRoute()
const router = useRouter()

const folders = ref([])
const files = ref([])
const allFolders = ref([])
const loading = ref(true)
const showCreateFolder = ref(false)
const showUpload = ref(false)
const shareItem = ref(null)
const shareType = ref('file')

const currentFolderId = computed(() => {
  return route.params.folderId ? parseInt(route.params.folderId) : null
})

// Build breadcrumb trail
const breadcrumbs = computed(() => {
  const crumbs = [{ id: null, name: 'My Drive' }]
  if (!currentFolderId.value) return crumbs

  // Walk up the parent chain
  const buildPath = (folderId) => {
    const folder = allFolders.value.find(f => f.id === folderId)
    if (folder) {
      if (folder.parent_id) buildPath(folder.parent_id)
      crumbs.push({ id: folder.id, name: folder.name })
    }
  }
  buildPath(currentFolderId.value)
  return crumbs
})

async function loadContent() {
  loading.value = true
  try {
    // Load all folders for breadcrumb navigation
    const foldersRes = await api.get('/folders/')
    allFolders.value = foldersRes.data

    // Filter folders for current view
    folders.value = allFolders.value.filter(
      f => f.parent_id === currentFolderId.value
    )

    // Load files
    if (currentFolderId.value) {
      const filesRes = await api.get(`/files/${currentFolderId.value}/files`)
      files.value = filesRes.data
    } else {
      const filesRes = await api.get('/files/')
      // Show only root-level files (no folder)
      files.value = filesRes.data.filter(f => !f.folder_id)
    }
  } catch (err) {
    console.error('Failed to load content:', err)
  } finally {
    loading.value = false
  }
}

function navigateToFolder(folderId) {
  if (folderId) {
    router.push(`/drive/${folderId}`)
  } else {
    router.push('/drive')
  }
}

async function handleDeleteFolder(folderId) {
  if (!confirm('Delete this folder and all its contents?')) return
  try {
    await api.delete(`/folders/${folderId}`)
    loadContent()
  } catch (err) {
    alert(err.response?.data?.detail || 'Failed to delete folder')
  }
}

async function handleRenameFolder(folderId, newName) {
  try {
    await api.patch(`/folders/${folderId}`, { name: newName })
    loadContent()
  } catch (err) {
    alert(err.response?.data?.detail || 'Failed to rename folder')
  }
}

async function handleDownloadFile(fileId, filename) {
  try {
    const response = await api.get(`/files/${fileId}`, { responseType: 'blob' })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', filename)
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
  } catch (err) {
    alert(err.response?.data?.detail || 'Failed to download file')
  }
}

async function handleDeleteFile(fileId) {
  if (!confirm('Delete this file permanently?')) return
  try {
    await api.delete(`/files/${fileId}`)
    loadContent()
  } catch (err) {
    alert(err.response?.data?.detail || 'Failed to delete file')
  }
}

function handleShareFile(file) {
  shareItem.value = file
  shareType.value = 'file'
}

function handleShareFolder(folder) {
  shareItem.value = folder
  shareType.value = 'folder'
}

function onFolderCreated() {
  showCreateFolder.value = false
  loadContent()
}

function onFileUploaded() {
  showUpload.value = false
  loadContent()
}

watch(() => route.params.folderId, loadContent)
onMounted(loadContent)
</script>

<template>
  <div class="p-6 lg:p-10 max-w-6xl">
    <!-- Header -->
    <div class="flex items-center justify-between mb-2">
      <h1 class="text-2xl font-semibold text-[var(--color-text)]">My Drive</h1>
      <div class="flex items-center gap-2">
        <button
          @click="showCreateFolder = true"
          class="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium border border-[var(--color-border)] rounded-xl hover:bg-[var(--color-surface-hover)] transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M9 13h6m-3-3v6m-9 1V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
          </svg>
          New Folder
        </button>
        <button
          @click="showUpload = true"
          class="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium bg-[var(--color-accent)] text-white rounded-xl hover:bg-[var(--color-accent-hover)] transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
          </svg>
          Upload
        </button>
      </div>
    </div>

    <!-- Breadcrumb -->
    <Breadcrumb :items="breadcrumbs" @navigate="navigateToFolder" />

    <!-- Loading -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <svg class="animate-spin h-6 w-6 text-[var(--color-text-muted)]" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" />
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
      </svg>
    </div>

    <template v-else>
      <!-- Empty state -->
      <div v-if="folders.length === 0 && files.length === 0" class="text-center py-20">
        <div class="inline-flex items-center justify-center w-16 h-16 bg-[var(--color-bg)] border border-[var(--color-border)] rounded-2xl mb-4">
          <svg class="w-7 h-7 text-[var(--color-text-muted)]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
          </svg>
        </div>
        <p class="text-[var(--color-text-muted)] text-sm">This folder is empty</p>
        <p class="text-[var(--color-text-muted)] text-xs mt-1">Upload files or create a folder to get started</p>
      </div>

      <!-- Folders -->
      <div v-if="folders.length > 0" class="mb-6">
        <p class="text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider mb-3">Folders</p>
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3">
          <FolderCard
            v-for="folder in folders"
            :key="folder.id"
            :folder="folder"
            @open="navigateToFolder(folder.id)"
            @delete="handleDeleteFolder(folder.id)"
            @rename="(name) => handleRenameFolder(folder.id, name)"
            @share="handleShareFolder(folder)"
          />
        </div>
      </div>

      <!-- Files -->
      <div v-if="files.length > 0">
        <p class="text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider mb-3">Files</p>
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3">
          <FileCard
            v-for="file in files"
            :key="file.id"
            :file="file"
            @download="handleDownloadFile(file.id, file.filename)"
            @delete="handleDeleteFile(file.id)"
            @share="handleShareFile(file)"
          />
        </div>
      </div>
    </template>

    <!-- Modals -->
    <CreateFolderModal
      v-if="showCreateFolder"
      :parentId="currentFolderId"
      @close="showCreateFolder = false"
      @created="onFolderCreated"
    />

    <UploadModal
      v-if="showUpload"
      :folderId="currentFolderId"
      @close="showUpload = false"
      @uploaded="onFileUploaded"
    />

    <ShareModal
      v-if="shareItem"
      :item="shareItem"
      :type="shareType"
      @close="shareItem = null"
    />
  </div>
</template>
