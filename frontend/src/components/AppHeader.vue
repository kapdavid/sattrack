<template>
  <header class="sticky top-0 z-50 bg-space-900/80 backdrop-blur-md border-b border-white/5 text-white">
    <nav class="container mx-auto px-4 py-4">
      <div class="flex items-center justify-between">
        <!-- Logo -->
        <router-link to="/" class="text-2xl font-bold flex items-center gap-2">
          🛰️ SatTrack
        </router-link>

        <!-- Desktop Navigation -->
        <div class="hidden md:flex items-center gap-6">
          <router-link to="/satellites" class="hover:text-blue-400 transition">
            Satellites
          </router-link>

          <router-link
            v-if="authStore.isAuthenticated"
            to="/favorites"
            class="hover:text-blue-400 transition"
          >
            Favorites
          </router-link>

          <router-link
            v-if="authStore.isAuthenticated"
            to="/settings"
            class="hover:text-blue-400 transition"
          >
            Settings
          </router-link>

          <!-- Auth buttons -->
          <div v-if="!authStore.isAuthenticated" class="flex gap-3">
            <router-link
              to="/login"
              class="px-4 py-2 hover:bg-slate-800 rounded transition"
            >
              Login
            </router-link>
            <router-link
              to="/register"
              class="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded transition"
            >
              Sign Up
            </router-link>
          </div>

          <button
            v-else
            @click="handleSignOut"
            class="px-4 py-2 hover:bg-slate-800 rounded transition"
          >
            Sign Out
          </button>
        </div>

        <!-- Mobile menu button -->
        <button
          @click="mobileMenuOpen = !mobileMenuOpen"
          class="md:hidden p-2 hover:bg-slate-800 rounded"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              v-if="!mobileMenuOpen"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 6h16M4 12h16M4 18h16"
            />
            <path
              v-else
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>

      <!-- Mobile menu -->
      <div
        v-if="mobileMenuOpen"
        class="md:hidden mt-4 pb-4 border-t border-slate-700 pt-4"
      >
        <div class="flex flex-col gap-3">
          <router-link
            to="/satellites"
            class="hover:text-blue-400 transition"
            @click="mobileMenuOpen = false"
          >
            Satellites
          </router-link>

          <router-link
            v-if="authStore.isAuthenticated"
            to="/favorites"
            class="hover:text-blue-400 transition"
            @click="mobileMenuOpen = false"
          >
            Favorites
          </router-link>

          <router-link
            v-if="authStore.isAuthenticated"
            to="/settings"
            class="hover:text-blue-400 transition"
            @click="mobileMenuOpen = false"
          >
            Settings
          </router-link>

          <div v-if="!authStore.isAuthenticated" class="flex flex-col gap-2 mt-2">
            <router-link
              to="/login"
              class="px-4 py-2 text-center hover:bg-slate-800 rounded transition"
              @click="mobileMenuOpen = false"
            >
              Login
            </router-link>
            <router-link
              to="/register"
              class="px-4 py-2 text-center bg-blue-600 hover:bg-blue-700 rounded transition"
              @click="mobileMenuOpen = false"
            >
              Sign Up
            </router-link>
          </div>

          <button
            v-else
            @click="handleSignOut"
            class="px-4 py-2 text-left hover:bg-slate-800 rounded transition"
          >
            Sign Out
          </button>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const mobileMenuOpen = ref(false)

const handleSignOut = async () => {
  try {
    await authStore.signOut()
    mobileMenuOpen.value = false
    router.push('/')
  } catch (error) {
    console.error('Sign out error:', error)
  }
}
</script>
