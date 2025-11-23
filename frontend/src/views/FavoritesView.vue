<template>
  <div>
    <h1 class="text-3xl font-bold text-slate-900 mb-6">My Favorites</h1>

    <!-- Location Check -->
    <div v-if="!userStore.hasLocation" class="bg-yellow-50 border border-yellow-200 text-yellow-800 p-4 rounded-lg mb-6">
      <p class="font-semibold">Location Not Set</p>
      <p class="text-sm mt-1">Set your observer location in settings to see pass predictions for your favorites.</p>
      <router-link
        to="/settings"
        class="inline-block mt-3 px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 transition text-sm"
      >
        Go to Settings
      </router-link>
    </div>

    <!-- Loading State -->
    <div v-if="userStore.loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      <p class="mt-4 text-slate-600">Loading favorites...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="userStore.favorites.length === 0" class="text-center py-12">
      <p class="text-xl text-slate-600 mb-4">No favorites yet</p>
      <p class="text-slate-500 mb-6">Browse satellites and add your favorites to track them here</p>
      <router-link
        to="/satellites"
        class="inline-block px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
      >
        Browse Satellites
      </router-link>
    </div>

    <!-- Favorites Grid -->
    <div v-else>
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="favorite in userStore.favorites"
          :key="favorite.id"
          class="bg-white rounded-lg shadow-md hover:shadow-lg transition p-6"
        >
          <div class="flex justify-between items-start mb-3">
            <div>
              <h3 class="text-xl font-bold text-slate-900">{{ favorite.satellite.name }}</h3>
              <span
                class="inline-block mt-2 px-3 py-1 text-xs font-semibold rounded-full"
                :class="getCategoryClass(favorite.satellite.category)"
              >
                {{ getCategoryLabel(favorite.satellite.category) }}
              </span>
            </div>

            <button
              @click="removeFavorite(favorite.satellite_id)"
              class="text-2xl hover:scale-110 transition"
              title="Remove from favorites"
            >
              ⭐
            </button>
          </div>

          <div class="text-sm text-slate-600 space-y-1 mb-4">
            <p><strong>NORAD ID:</strong> {{ favorite.satellite.norad_id }}</p>
            <p class="text-xs text-slate-500">
              Added {{ new Date(favorite.created_at).toLocaleDateString() }}
            </p>
          </div>

          <router-link
            :to="`/satellites/${favorite.satellite_id}`"
            class="inline-block px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition text-sm"
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
    weather: 'bg-blue-100 text-blue-800',
    amateur_radio: 'bg-green-100 text-green-800',
    popular: 'bg-purple-100 text-purple-800'
  }
  return classes[category] || 'bg-gray-100 text-gray-800'
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
