<template>
  <div class="min-h-screen flex flex-col bg-slate-50">
    <AppHeader />

    <main class="flex-1 container mx-auto px-4 py-8">
      <router-view />
    </main>

    <AppFooter />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import AppHeader from './components/AppHeader.vue'
import AppFooter from './components/AppFooter.vue'
import { useAuthStore } from './stores/auth'

const authStore = useAuthStore()

onMounted(async () => {
  // Initialize authentication state
  await authStore.initialize()
})
</script>
