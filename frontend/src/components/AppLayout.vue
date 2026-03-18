<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Sidebar from './Sidebar.vue'

const router = useRouter()
const route = useRoute()

const isSidebarOpen = ref(false)
</script>

<template>
  <div class="flex min-h-screen bg-[var(--color-bg)]">
    <Sidebar :isOpen="isSidebarOpen" @close="isSidebarOpen = false" />
    
    <main class="flex-1 lg:ml-64 min-h-screen flex flex-col min-w-0">
      <!-- Mobile Header -->
      <div class="lg:hidden sticky top-0 z-20 flex items-center justify-between px-4 py-3 bg-[var(--color-surface)] border-b border-[var(--color-border)]">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 bg-[var(--color-text)] rounded-lg flex items-center justify-center">
            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
            </svg>
          </div>
          <span class="text-base font-semibold text-[var(--color-text)] tracking-tight">FileVault</span>
        </div>
        <button
          @click="isSidebarOpen = true"
          class="p-2 -mr-2 text-[var(--color-text-muted)] hover:bg-[var(--color-surface-hover)] hover:text-[var(--color-text)] rounded-lg transition-colors"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </div>

      <router-view />
    </main>
  </div>
</template>
