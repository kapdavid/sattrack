<template>
  <div class="max-w-md mx-auto">
    <div class="bg-space-800/50 backdrop-blur-md border border-white/10 rounded-xl p-8 shadow-xl">
      <h1 class="text-3xl font-display font-bold text-white mb-6 tracking-tight">Create Account</h1>

      <form @submit.prevent="handleRegister" class="space-y-6">
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
            minlength="6"
            class="w-full px-4 py-3 bg-space-900/50 border border-white/10 rounded-lg text-white font-mono placeholder-slate-600 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            placeholder="••••••••"
          />
          <p class="text-xs text-slate-500 mt-1.5">Minimum 6 characters required</p>
        </div>

        <div>
          <label for="confirmPassword" class="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">
            Confirm Password
          </label>
          <input
            id="confirmPassword"
            v-model="confirmPassword"
            type="password"
            required
            class="w-full px-4 py-3 bg-space-900/50 border border-white/10 rounded-lg text-white font-mono placeholder-slate-600 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            placeholder="••••••••"
          />
        </div>

        <div v-if="error" class="bg-red-500/10 border border-red-500/20 text-red-400 p-3 rounded-lg text-sm flex items-center gap-2">
          <span>⚠️</span> {{ error }}
        </div>

        <div v-if="success" class="bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 p-3 rounded-lg text-sm flex items-center gap-2">
          <span>✓</span> {{ success }}
        </div>

        <button
          type="submit"
          :disabled="authStore.loading"
          class="w-full bg-blue-600 hover:bg-blue-500 text-white py-3 px-4 rounded-lg shadow-[0_0_15px_rgba(37,99,235,0.4)] disabled:opacity-50 disabled:cursor-not-allowed transition-all font-medium"
        >
          {{ authStore.loading ? 'Creating Account...' : 'Sign Up' }}
        </button>
      </form>

      <p class="mt-6 text-center text-slate-400 text-sm">
        Already have an account?
        <router-link to="/login" class="text-blue-400 hover:text-blue-300 font-medium underline">
          Login
        </router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const error = ref(null)
const success = ref(null)

const handleRegister = async () => {
  error.value = null
  success.value = null

  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match'
    return
  }

  try {
    await authStore.signUp(email.value, password.value)
    success.value = 'Account created! Please check your email to confirm your account.'
    // Optionally redirect to login after a delay
    setTimeout(() => {
      router.push('/login')
    }, 3000)
  } catch (err) {
    error.value = err.message || 'Failed to create account. Please try again.'
  }
}
</script>
