<template>
  <div class="max-w-md mx-auto">
    <div class="bg-space-800/50 backdrop-blur-md border border-white/10 rounded-xl p-8 shadow-xl">
      <h1 class="text-3xl font-display font-bold text-white mb-6 tracking-tight">Login</h1>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label for="email" class="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">
            Email
          </label>
          <input
            id="email"
            v-model="email"
            type="email"
            required
            class="w-full px-4 py-3 bg-space-900/50 border border-white/10 rounded-lg text-white font-mono placeholder-slate-600 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            placeholder="commander@sattrack.com"
          />
        </div>

        <div>
          <label for="password" class="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">
            Password
          </label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            class="w-full px-4 py-3 bg-space-900/50 border border-white/10 rounded-lg text-white font-mono placeholder-slate-600 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            placeholder="••••••••"
          />
        </div>

        <div v-if="error" class="bg-red-500/10 border border-red-500/20 text-red-400 p-3 rounded-lg text-sm flex items-center gap-2">
          <span>⚠️</span> {{ error }}
        </div>

        <button
          type="submit"
          :disabled="authStore.loading"
          class="w-full bg-blue-600 hover:bg-blue-500 text-white py-3 px-4 rounded-lg shadow-[0_0_15px_rgba(37,99,235,0.4)] disabled:opacity-50 disabled:cursor-not-allowed transition-all font-medium"
        >
          {{ authStore.loading ? 'Authenticating...' : 'Login' }}
        </button>
      </form>

      <p class="mt-6 text-center text-slate-400 text-sm">
        Don't have an account?
        <router-link to="/register" class="text-blue-400 hover:text-blue-300 font-medium underline">
          Sign up
        </router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const error = ref(null)

const handleLogin = async () => {
  error.value = null
  try {
    await authStore.signIn(email.value, password.value)
    // Redirect to the page they were trying to access, or home
    const redirect = route.query.redirect || '/'
    router.push(redirect)
  } catch (err) {
    error.value = err.message || 'Failed to login. Please check your credentials.'
  }
}
</script>
