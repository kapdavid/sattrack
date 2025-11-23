<template>
  <footer class="bg-slate-900 text-slate-400 py-8 mt-auto">
    <div class="container mx-auto px-4 text-center">
      <p>&copy; {{ currentYear }} SatTrack. Built for satellite enthusiasts.</p>
      <p class="text-sm mt-2">
        Data from <a href="https://celestrak.org" target="_blank" class="text-blue-400 hover:text-blue-300">CelesTrak</a>
      </p>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue'

const currentYear = computed(() => new Date().getFullYear())
</script>
