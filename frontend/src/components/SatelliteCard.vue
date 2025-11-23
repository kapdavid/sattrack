<template>
  <div class="bg-white rounded-lg shadow-md hover:shadow-lg transition p-6">
    <div class="flex justify-between items-start mb-3">
      <div>
        <h3 class="text-xl font-bold text-slate-900">{{ satellite.name }}</h3>
        <span
          class="inline-block mt-2 px-3 py-1 text-xs font-semibold rounded-full"
          :class="categoryClass"
        >
          {{ categoryLabel }}
        </span>
      </div>

      <button
        v-if="showFavoriteButton"
        @click="toggleFavorite"
        class="text-2xl hover:scale-110 transition"
        :disabled="userStore.loading"
      >
        {{ isFavorited ? '⭐' : '☆' }}
      </button>
    </div>

    <div class="text-sm text-slate-600 space-y-1">
      <p><strong>NORAD ID:</strong> {{ satellite.norad_id }}</p>
      <p><strong>Last Updated:</strong> {{ formattedDate }}</p>
    </div>

    <router-link
      :to="`/satellites/${satellite.id}`"
      class="mt-4 inline-block px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition text-sm"
    >
      View Details
    </router-link>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useUserStore } from '../stores/user'
import { useAuthStore } from '../stores/auth'

const props = defineProps({
  satellite: {
    type: Object,
    required: true
  },
  showFavoriteButton: {
    type: Boolean,
    default: true
  }
})

const userStore = useUserStore()
const authStore = useAuthStore()

const isFavorited = computed(() => {
  if (!authStore.isAuthenticated) return false
  return userStore.isFavorite(props.satellite.id)
})

const categoryClass = computed(() => {
  const classes = {
    weather: 'bg-blue-100 text-blue-800',
    amateur_radio: 'bg-green-100 text-green-800',
    popular: 'bg-purple-100 text-purple-800'
  }
  return classes[props.satellite.category] || 'bg-gray-100 text-gray-800'
})

const categoryLabel = computed(() => {
  const labels = {
    weather: 'Weather',
    amateur_radio: 'Amateur Radio',
    popular: 'Popular'
  }
  return labels[props.satellite.category] || props.satellite.category
})

const formattedDate = computed(() => {
  return new Date(props.satellite.last_updated).toLocaleDateString()
})

const toggleFavorite = async () => {
  if (!authStore.isAuthenticated) {
    // Could show a toast or redirect to login
    alert('Please login to add favorites')
    return
  }

  try {
    if (isFavorited.value) {
      await userStore.removeFavorite(props.satellite.id)
    } else {
      await userStore.addFavorite(props.satellite.id)
    }
  } catch (error) {
    console.error('Error toggling favorite:', error)
  }
}
</script>
