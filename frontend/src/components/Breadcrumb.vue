<script setup>
defineProps({
  items: {
    type: Array,
    required: true,
  },
})

const emit = defineEmits(['navigate'])
</script>

<template>
  <nav class="flex items-center gap-1 text-sm text-[var(--color-text-muted)] mb-6 mt-1">
    <template v-for="(item, index) in items" :key="index">
      <button
        v-if="index < items.length - 1"
        @click="emit('navigate', item.id)"
        class="hover:text-[var(--color-text)] transition-colors px-1 py-0.5 rounded hover:bg-[var(--color-surface-hover)]"
      >
        {{ item.name }}
      </button>
      <span v-else class="text-[var(--color-text)] font-medium px-1">{{ item.name }}</span>

      <svg v-if="index < items.length - 1" class="w-3.5 h-3.5 text-[var(--color-border)]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
      </svg>
    </template>
  </nav>
</template>
