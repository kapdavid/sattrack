<template>
  <div class="max-w-6xl mx-auto">
    <h1 class="text-4xl font-display font-bold text-white mb-8 tracking-tight">Tracked Satellites</h1>

    <!-- Location Check -->
    <div v-if="!userStore.hasLocation" class="bg-yellow-500/10 border border-yellow-500/20 text-yellow-200 p-4 rounded-lg mb-6">
      <p class="font-semibold">Observer Location Required</p>
      <p class="text-sm mt-1 text-yellow-300">Configure your location to calculate pass predictions for your tracked satellites.</p>
      <router-link
        to="/settings"
        class="inline-block mt-3 px-4 py-2 bg-yellow-600 hover:bg-yellow-500 text-white rounded-lg transition text-sm font-medium"
      >
        Configure Location
      </router-link>
    </div>

    <!-- Loading State -->
    <div v-if="userStore.loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      <p class="mt-4 text-slate-400">Loading tracked satellites...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="userStore.favorites.length === 0" class="text-center py-16">
      <div class="text-6xl mb-4">📡</div>
      <p class="text-2xl font-display text-white mb-2">No Satellites Tracked</p>
      <p class="text-slate-400 mb-6">Explore the satellite catalog and start tracking your favorites</p>
      <router-link
        to="/satellites"
        class="inline-block px-6 py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-lg shadow-[0_0_15px_rgba(37,99,235,0.4)] transition font-medium"
      >
        Browse Catalog
      </router-link>
    </div>

    <!-- Favorites Grid -->
    <div v-else>
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="favorite in userStore.favorites"
          :key="favorite.id"
          class="bg-space-800/50 backdrop-blur-md border border-white/10 rounded-xl hover:border-blue-500/30 transition-all shadow-xl p-6 group"
        >
          <div class="flex justify-between items-start mb-4">
            <div>
              <h3 class="text-xl font-display font-bold text-white group-hover:text-blue-400 transition-colors">
                {{ favorite.satellite.name }}
              </h3>
              <span
                class="inline-block mt-2 px-3 py-1 text-xs font-bold tracking-wider uppercase rounded-full border"
                :class="getCategoryClass(favorite.satellite.category)"
              >
                {{ getCategoryLabel(favorite.satellite.category) }}
              </span>
            </div>

            <button
              @click="removeFavorite(favorite.satellite_id)"
              class="text-3xl hover:scale-110 transition-transform active:scale-95 text-yellow-400 drop-shadow-[0_0_8px_rgba(250,204,21,0.5)]"
              title="Remove from tracking"
            >
              ★
            </button>
          </div>

          <div class="text-sm space-y-2 mb-4">
            <div class="flex justify-between items-center">
              <span class="text-slate-400">NORAD ID</span>
              <span class="font-mono text-blue-400">{{ favorite.satellite.norad_id }}</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-slate-400">Tracked Since</span>
              <span class="text-slate-300 text-xs">{{ new Date(favorite.created_at).toLocaleDateString() }}</span>
            </div>
          </div>

          <router-link
            :to="`/satellites/${favorite.satellite_id}`"
            class="block w-full text-center px-4 py-2 bg-blue-600/20 hover:bg-blue-600/30 border border-blue-500/30 text-blue-300 rounded-lg transition-all text-sm font-medium"
          >
            View Details
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useUserStore } from '../stores/user'

const userStore = useUserStore()

const getCategoryClass = (category) => {
  const classes = {
    weather: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/20',
    amateur_radio: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
    popular: 'bg-purple-500/10 text-purple-400 border-purple-500/20'
  }
  return classes[category] || 'bg-slate-500/10 text-slate-400 border-slate-500/20'
}

const getCategoryLabel = (category) => {
  const labels = {
    weather: 'Weather',
    amateur_radio: 'Amateur Radio',
    popular: 'Popular'
  }
  return labels[category] || category
}

const removeFavorite = async (satelliteId) => {
  if (confirm('Remove this satellite from favorites?')) {
    try {
      await userStore.removeFavorite(satelliteId)
    } catch (error) {
      console.error('Error removing favorite:', error)
      alert('Failed to remove favorite')
    }
  }
}

onMounted(async () => {
  // Fetch favorites and profile on mount
  await userStore.fetchFavorites()
  if (!userStore.profile) {
    await userStore.fetchProfile()
  }
})
</script>
