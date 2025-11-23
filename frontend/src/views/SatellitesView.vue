<template>
  <div>
    <h1 class="text-3xl font-bold text-slate-900 mb-6">Browse Satellites</h1>

    <!-- Search and Filter Bar -->
    <div class="bg-white rounded-lg shadow-md p-4 mb-6">
      <div class="flex flex-col md:flex-row gap-4">
        <!-- Search -->
        <div class="flex-1">
          <input
            v-model="searchQuery"
            @input="handleSearch"
            type="text"
            placeholder="Search satellites..."
            class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        <!-- Category Filter -->
        <div class="flex gap-2">
          <button
            @click="selectCategory(null)"
            :class="[
              'px-4 py-2 rounded-lg transition',
              selectedCategory === null
                ? 'bg-blue-600 text-white'
                : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
            ]"
          >
            All
          </button>
          <button
            @click="selectCategory('weather')"
            :class="[
              'px-4 py-2 rounded-lg transition',
              selectedCategory === 'weather'
                ? 'bg-blue-600 text-white'
                : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
            ]"
          >
            Weather
          </button>
          <button
            @click="selectCategory('amateur_radio')"
            :class="[
              'px-4 py-2 rounded-lg transition',
              selectedCategory === 'amateur_radio'
                ? 'bg-blue-600 text-white'
                : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
            ]"
          >
            Amateur Radio
          </button>
          <button
            @click="selectCategory('popular')"
            :class="[
              'px-4 py-2 rounded-lg transition',
              selectedCategory === 'popular'
                ? 'bg-blue-600 text-white'
                : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
            ]"
          >
            Popular
          </button>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="satellitesStore.loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      <p class="mt-4 text-slate-600">Loading satellites...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="satellitesStore.error" class="bg-red-50 text-red-600 p-4 rounded-lg">
      {{ satellitesStore.error }}
    </div>

    <!-- No Results -->
    <div v-else-if="satellitesStore.satellites.length === 0" class="text-center py-12">
      <p class="text-slate-600 text-lg">No satellites found</p>
    </div>

    <!-- Satellite Grid -->
    <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
      <SatelliteCard
        v-for="satellite in satellitesStore.satellites"
        :key="satellite.id"
        :satellite="satellite"
      />
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
