<template>
  <div class="min-h-screen flex flex-col bg-space-900 text-slate-300 bg-[radial-gradient(circle_at_50%_0%,#1e293b_0%,#0B0C15_75%)]">
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
  await authStore.initialize()
})
</script>