<script setup>
import { useRouter, useRoute } from 'vue-router'
import Sidebar from './Sidebar.vue'

const router = useRouter()
const route = useRoute()
</script>

<template>
  <div class="flex min-h-screen bg-[var(--color-bg)]">
    <Sidebar />
    <main class="flex-1 ml-64 min-h-screen">
      <router-view />
    </main>
  </div>
</template>
