<template>
  <div class="max-w-6xl mx-auto">
    <h1 class="text-3xl font-display font-bold text-white mb-8">Satellite Catalog</h1>

    <div class="bg-space-800/50 backdrop-blur-md border border-white/10 rounded-xl p-6 mb-8 shadow-lg">
      <div class="flex flex-col md:flex-row gap-6">
        <div class="flex-1 relative">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <span class="text-slate-500">🔍</span>
          </div>
          <input
            v-model="searchQuery"
            @input="handleSearch"
            type="text"
            placeholder="Search satellites (e.g., NOAA, ISS)..."
            class="w-full pl-10 pr-4 py-3 bg-space-900/50 border border-white/10 rounded-lg text-white placeholder-slate-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
          />
        </div>

        <div class="flex gap-2 flex-wrap">
          <button
            @click="selectCategory(null)"
            class="px-4 py-2 rounded-lg text-sm font-medium transition-all border"
            :class="selectedCategory === null 
              ? 'bg-blue-600 text-white border-blue-500 shadow-[0_0_10px_rgba(37,99,235,0.3)]' 
              : 'bg-white/5 text-slate-300 border-white/5 hover:bg-white/10 hover:border-white/10'"
          >
            All
          </button>
          
          <button
            @click="selectCategory('weather')"
            class="px-4 py-2 rounded-lg text-sm font-medium transition-all border"
            :class="selectedCategory === 'weather' 
              ? 'bg-cyan-600/20 text-cyan-300 border-cyan-500 shadow-[0_0_10px_rgba(6,182,212,0.3)]' 
              : 'bg-white/5 text-slate-300 border-white/5 hover:bg-white/10'"
          >
            Weather
          </button>
          
          <button
            @click="selectCategory('amateur_radio')"
            class="px-4 py-2 rounded-lg text-sm font-medium transition-all border"
            :class="selectedCategory === 'amateur_radio' 
              ? 'bg-emerald-600/20 text-emerald-300 border-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.3)]' 
              : 'bg-white/5 text-slate-300 border-white/5 hover:bg-white/10'"
          >
            Amateur Radio
          </button>
          
          <button
            @click="selectCategory('popular')"
            class="px-4 py-2 rounded-lg text-sm font-medium transition-all border"
            :class="selectedCategory === 'popular' 
              ? 'bg-purple-600/20 text-purple-300 border-purple-500 shadow-[0_0_10px_rgba(147,51,234,0.3)]' 
              : 'bg-white/5 text-slate-300 border-white/5 hover:bg-white/10'"
          >
            Popular
          </button>
        </div>
      </div>
    </div>

    <div v-if="satellitesStore.loading" class="text-center py-20">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 shadow-[0_0_15px_rgba(59,130,246,0.5)]"></div>
      <p class="mt-4 text-slate-400 font-mono text-sm">Scanning frequencies...</p>
    </div>

    <div v-else-if="satellitesStore.error" class="bg-red-500/10 border border-red-500/20 text-red-400 p-6 rounded-xl text-center">
      {{ satellitesStore.error }}
    </div>

    <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
      <SatelliteCard
        v-for="satellite in satellitesStore.satellites"
        :key="satellite.id"
        :satellite="satellite"
      />
    </div>
    
    <div v-if="!satellitesStore.loading && satellitesStore.satellites.length === 0" class="text-center py-20">
      <p class="text-slate-500 text-lg">No satellites found in orbit.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useSatellitesStore } from '../stores/satellites'
import { useUserStore } from '../stores/user'
import { useAuthStore } from '../stores/auth'
import SatelliteCard from '../components/SatelliteCard.vue'

const satellitesStore = useSatellitesStore()
const userStore = useUserStore()
const authStore = useAuthStore()

const searchQuery = ref('')
const selectedCategory = ref(null)
let searchTimeout = null

const selectCategory = async (category) => {
  selectedCategory.value = category
  searchQuery.value = '' // Clear search when changing category
  await satellitesStore.fetchSatellites(category)
}

const handleSearch = () => {
  // Debounce search
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(async () => {
    if (searchQuery.value.trim()) {
      await satellitesStore.searchSatellites(searchQuery.value)
      selectedCategory.value = null // Clear category when searching
    } else {
      await satellitesStore.fetchSatellites(selectedCategory.value)
    }
  }, 300)
}

onMounted(async () => {
  // Fetch satellites on mount
  await satellitesStore.fetchSatellites()

  // Fetch user favorites if authenticated
  if (authStore.isAuthenticated) {
    await userStore.fetchFavorites()
  }
})
</script>
