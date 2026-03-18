<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close'])

const navItems = [
  {
    name: 'My Drive',
    path: '/drive',
    icon: `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />`,
  },
  {
    name: 'Dashboard',
    path: '/dashboard',
    icon: `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 5a1 1 0 011-1h4a1 1 0 011 1v5a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM14 5a1 1 0 011-1h4a1 1 0 011 1v3a1 1 0 01-1 1h-4a1 1 0 01-1-1V5zM4 16a1 1 0 011-1h4a1 1 0 011 1v3a1 1 0 01-1 1H5a1 1 0 01-1-1v-3zM14 13a1 1 0 011-1h4a1 1 0 011 1v5a1 1 0 01-1 1h-4a1 1 0 01-1-1v-5z" />`,
  },
]

function isActive(path) {
  return route.path.startsWith(path)
}

function logout() {
  localStorage.removeItem('access_token')
  router.push('/login')
}
</script>

<template>
  <!-- Mobile Overlay -->
  <div
    v-if="isOpen"
    @click="emit('close')"
    class="fixed inset-0 bg-black/40 backdrop-blur-sm z-30 lg:hidden"
  ></div>

  <!-- Sidebar -->
  <aside 
    class="fixed left-0 top-0 bottom-0 w-64 bg-[var(--color-surface)] border-r border-[var(--color-border)] flex flex-col z-40 transition-transform duration-300 ease-in-out lg:translate-x-0"
    :class="isOpen ? 'translate-x-0' : '-translate-x-full'"
  >
    <!-- Logo -->
    <div class="px-6 py-6 flex items-center gap-3">
      <div class="w-9 h-9 bg-[var(--color-text)] rounded-xl flex items-center justify-center">
        <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
            d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
        </svg>
      </div>
      <span class="text-lg font-semibold text-[var(--color-text)] tracking-tight">FileVault</span>
    </div>

    <nav class="flex-1 px-3 mt-2">
      <router-link
        v-for="item in navItems"
        :key="item.path"
        :to="item.path"
        @click="emit('close')"
        class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium mb-1 transition-colors"
        :class="isActive(item.path)
          ? 'bg-[var(--color-bg)] text-[var(--color-text)]'
          : 'text-[var(--color-text-muted)] hover:bg-[var(--color-surface-hover)] hover:text-[var(--color-text)]'"
      >
        <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" v-html="item.icon" />
        {{ item.name }}
      </router-link>
    </nav>

    <!-- Logout -->
    <div class="px-3 pb-5">
      <button
        @click="logout"
        class="flex items-center gap-3 w-full px-3 py-2.5 rounded-xl text-sm font-medium text-[var(--color-text-muted)] hover:bg-[var(--color-surface-hover)] hover:text-[var(--color-text)] transition-colors"
      >
        <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
            d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
        </svg>
        Log out
      </button>
    </div>
  </aside>
</template>
