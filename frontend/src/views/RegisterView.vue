<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const error = ref('')
const loading = ref(false)

async function handleRegister() {
  error.value = ''

  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match.'
    return
  }

  if (password.value.length < 8) {
    error.value = 'Password must be at least 8 characters long.'
    return
  }

  loading.value = true

  try {
    await api.post('/auth/register', {
      email: email.value,
      password: password.value,
    })
    router.push('/login')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Registration failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-[var(--color-bg)] px-4">
    <div class="w-full max-w-md">
      <!-- Logo -->
      <div class="text-center mb-10">
        <div class="inline-flex items-center justify-center w-14 h-14 bg-[var(--color-text)] rounded-2xl mb-5">
          <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
          </svg>
        </div>
        <h1 class="text-2xl font-semibold text-[var(--color-text)] tracking-tight">FileVault</h1>
        <p class="text-sm text-[var(--color-text-muted)] mt-1">Create your account</p>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleRegister" class="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-2xl p-8 shadow-sm">
        <div v-if="error" class="mb-5 p-3 bg-red-50 border border-red-200 rounded-xl text-sm text-red-600">
          {{ error }}
        </div>

        <div class="mb-5">
          <label class="block text-sm font-medium text-[var(--color-text)] mb-1.5">Email</label>
          <input
            v-model="email"
            type="email"
            required
            placeholder="you@example.com"
            class="w-full px-4 py-2.5 bg-[var(--color-bg)] border border-[var(--color-border)] rounded-xl text-sm text-[var(--color-text)] placeholder-[var(--color-text-muted)] outline-none focus:border-[var(--color-accent)] transition-colors"
          />
        </div>

        <div class="mb-5">
          <label class="block text-sm font-medium text-[var(--color-text)] mb-1.5">Password</label>
          <input
            v-model="password"
            type="password"
            required
            placeholder="••••••••"
            class="w-full px-4 py-2.5 bg-[var(--color-bg)] border border-[var(--color-border)] rounded-xl text-sm text-[var(--color-text)] placeholder-[var(--color-text-muted)] outline-none focus:border-[var(--color-accent)] transition-colors"
          />
        </div>

        <div class="mb-6">
          <label class="block text-sm font-medium text-[var(--color-text)] mb-1.5">Confirm Password</label>
          <input
            v-model="confirmPassword"
            type="password"
            required
            placeholder="••••••••"
            class="w-full px-4 py-2.5 bg-[var(--color-bg)] border border-[var(--color-border)] rounded-xl text-sm text-[var(--color-text)] placeholder-[var(--color-text-muted)] outline-none focus:border-[var(--color-accent)] transition-colors"
          />
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full py-2.5 bg-[var(--color-accent)] text-white rounded-xl text-sm font-medium hover:bg-[var(--color-accent-hover)] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="loading" class="inline-flex items-center gap-2">
            <svg class="animate-spin h-4 w-4" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" />
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
            Creating account...
          </span>
          <span v-else>Create account</span>
        </button>
      </form>

      <p class="text-center text-sm text-[var(--color-text-muted)] mt-6">
        Already have an account?
        <router-link to="/login" class="text-[var(--color-text)] font-medium hover:underline">Sign in</router-link>
      </p>
    </div>
  </div>
</template>
