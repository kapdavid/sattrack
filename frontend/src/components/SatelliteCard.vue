<template>
  <div class="group relative bg-space-800/50 backdrop-blur-sm border border-white/10 rounded-xl p-6 transition-all duration-300 hover:border-blue-500/50 hover:shadow-[0_0_20px_rgba(59,130,246,0.15)]">
    <div class="flex justify-between items-start mb-4">
      <div>
        <h3 class="text-xl font-display font-bold text-white tracking-tight group-hover:text-blue-400 transition-colors">
          {{ satellite.name }}
        </h3>
        <div class="mt-2 flex items-center gap-2">
           <span class="w-2 h-2 rounded-full" :class="categoryColorDot"></span>
           <span class="text-xs font-medium text-slate-400 uppercase tracking-wider">{{ categoryLabel }}</span>
        </div>
      </div>

      <button
        v-if="showFavoriteButton"
        @click.stop="toggleFavorite"
        class="text-2xl transition-transform active:scale-95 text-slate-600 hover:text-yellow-400"
        :class="{ 'text-yellow-400': isFavorited }"
      >
        ★ </button>
    </div>

    <div class="grid grid-cols-2 gap-4 my-4 py-4 border-t border-white/5">
      <div>
        <p class="text-xs text-slate-500 uppercase">NORAD ID</p>
        <p class="font-mono text-slate-300">{{ satellite.norad_id }}</p>
      </div>
      <div class="text-right">
        <p class="text-xs text-slate-500 uppercase">Updated</p>
        <p class="text-slate-300 text-sm">{{ formattedDate }}</p>
      </div>
    </div>

    <router-link
      :to="`/satellites/${satellite.id}`"
      class="block w-full text-center py-2.5 rounded-lg bg-blue-600/10 text-blue-400 font-medium hover:bg-blue-600 hover:text-white transition-all duration-300"
    >
      View Telemetry
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
// Add this computed property for the dot color
const categoryColorDot = computed(() => {
  const map = {
    weather: 'bg-cyan-400 shadow-[0_0_8px_rgba(34,211,238,0.6)]',
    amateur_radio: 'bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.6)]',
    popular: 'bg-purple-400 shadow-[0_0_8px_rgba(192,132,252,0.6)]'
  }
  return map[props.satellite.category] || 'bg-slate-400'
})
</script>
