<template>
  <div class="max-w-4xl mx-auto">
    <div v-if="satellitesStore.loading && !satellite" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      <p class="mt-4 text-slate-400">Acquiring signal...</p>
    </div>

    <div v-else-if="satellite">
      <div class="flex justify-between items-start mb-8">
        <div>
          <h1 class="text-4xl font-display font-bold text-white tracking-tight">{{ satellite.name }}</h1>
          <span
            class="inline-block mt-3 px-3 py-1 text-xs font-bold tracking-wider uppercase rounded-full border"
            :class="categoryBadgeClass"
          >
            {{ categoryLabel }}
          </span>
        </div>

        <button
          v-if="authStore.isAuthenticated"
          @click="toggleFavorite"
          class="text-3xl hover:scale-110 transition-transform active:scale-95"
          :class="isFavorited ? 'text-yellow-400 drop-shadow-[0_0_8px_rgba(250,204,21,0.5)]' : 'text-slate-600 hover:text-yellow-400'"
        >
          ★
        </button>
      </div>

      <div class="grid md:grid-cols-2 gap-6 mb-6">
        <div class="bg-space-800/50 backdrop-blur-md border border-white/10 rounded-xl p-6 shadow-xl">
          <h2 class="text-lg font-display font-bold text-white mb-4 border-b border-white/10 pb-2">Mission Data</h2>
          <div class="space-y-4">
            <div>
              <p class="text-xs text-slate-500 uppercase tracking-wider font-semibold">NORAD ID</p>
              <p class="font-mono text-xl text-blue-400">{{ satellite.norad_id }}</p>
            </div>
            <div>
              <p class="text-xs text-slate-500 uppercase tracking-wider font-semibold">Last TLE Update</p>
              <p class="font-mono text-slate-300">{{ formattedDate }}</p>
            </div>
          </div>
        </div>

        <div class="bg-space-800/50 backdrop-blur-md border border-white/10 rounded-xl p-6 shadow-xl">
          <h2 class="text-lg font-display font-bold text-white mb-4 border-b border-white/10 pb-2">Live Telemetry</h2>

          <button
            @click="fetchPosition"
            :disabled="loadingPosition"
            class="mb-6 w-full py-2 bg-blue-600/20 hover:bg-blue-600/30 border border-blue-500/30 text-blue-300 rounded-lg transition-all text-sm font-medium disabled:opacity-50"
          >
            {{ loadingPosition ? 'Triangulating...' : 'Refresh Coordinates' }}
          </button>

          <div v-if="position" class="grid grid-cols-3 gap-2">
            <div class="text-center p-2 bg-space-900/50 rounded-lg border border-white/5">
              <p class="text-[10px] text-slate-500 uppercase">Lat</p>
              <p class="font-mono text-sm text-white">{{ position.latitude.toFixed(2) }}°</p>
            </div>
            <div class="text-center p-2 bg-space-900/50 rounded-lg border border-white/5">
              <p class="text-[10px] text-slate-500 uppercase">Lon</p>
              <p class="font-mono text-sm text-white">{{ position.longitude.toFixed(2) }}°</p>
            </div>
            <div class="text-center p-2 bg-space-900/50 rounded-lg border border-white/5">
              <p class="text-[10px] text-slate-500 uppercase">Alt</p>
              <p class="font-mono text-sm text-emerald-400">{{ position.altitude_km.toFixed(0) }} km</p>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-space-800/50 backdrop-blur-md border border-white/10 rounded-xl p-6 shadow-xl">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-xl font-display font-bold text-white">Pass Predictions</h2>
          
          <div v-if="userStore.hasLocation">
             <button
              @click="calculatePasses"
              :disabled="loadingPasses"
              class="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg shadow-[0_0_15px_rgba(37,99,235,0.4)] transition-all text-sm font-medium disabled:opacity-50"
            >
              {{ loadingPasses ? 'Calculating...' : 'Calculate (7 Days)' }}
            </button>
          </div>
        </div>

        <!-- Not authenticated -->
        <div v-if="!authStore.isAuthenticated" class="bg-blue-500/10 border border-blue-500/20 text-blue-200 p-4 rounded-lg text-center">
          <p class="font-medium">Login Required</p>
          <p class="text-sm mt-1 text-blue-300">Sign in to calculate pass predictions</p>
          <router-link to="/login" class="inline-block mt-3 px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg transition text-sm font-medium">
            Login
          </router-link>
        </div>

        <!-- Authenticated but no location -->
        <div v-else-if="!userStore.hasLocation" class="bg-yellow-500/10 border border-yellow-500/20 text-yellow-200 p-4 rounded-lg text-center">
          <p class="font-medium">Location Required</p>
          <p class="text-sm mt-1 text-yellow-300">Configure your observer location to calculate passes</p>
          <router-link to="/settings" class="inline-block mt-3 px-4 py-2 bg-yellow-600 hover:bg-yellow-500 text-white rounded-lg transition text-sm font-medium">
            Configure Location
          </router-link>
        </div>

        <div v-else>
           <div v-if="passes && passes.length > 0" class="mb-6 p-4 bg-space-900/50 rounded-lg border border-white/5">
             <div class="flex items-center justify-between mb-4">
               <p class="text-xs font-bold text-slate-400 uppercase tracking-wider">Filter Passes</p>
               <button @click="resetFilters" class="text-xs text-blue-400 hover:text-blue-300 underline">
                 Reset
               </button>
             </div>

             <div class="grid md:grid-cols-3 gap-4 mb-4">
               <!-- Quality Filter -->
               <div>
                 <label for="qualityFilter" class="block text-xs text-slate-400 mb-2 uppercase tracking-wide">
                   Quality
                 </label>
                 <select
                   id="qualityFilter"
                   v-model="qualityFilter"
                   class="w-full px-3 py-2 bg-space-800 border border-white/10 rounded-lg text-white text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                 >
                   <option value="all">All Quality</option>
                   <option value="excellent">Excellent (70+)</option>
                   <option value="good">Good (40+)</option>
                   <option value="fair">Fair (0+)</option>
                 </select>
               </div>

               <!-- Duration Filter -->
               <div>
                 <label for="durationFilter" class="block text-xs text-slate-400 mb-2 uppercase tracking-wide">
                   Min Duration
                 </label>
                 <select
                   id="durationFilter"
                   v-model.number="durationFilter"
                   class="w-full px-3 py-2 bg-space-800 border border-white/10 rounded-lg text-white text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                 >
                   <option :value="0">Any Duration</option>
                   <option :value="60">1+ minutes</option>
                   <option :value="180">3+ minutes</option>
                   <option :value="300">5+ minutes</option>
                   <option :value="600">10+ minutes</option>
                 </select>
               </div>

               <!-- Time of Day Filter -->
               <div>
                 <label class="block text-xs text-slate-400 mb-2 uppercase tracking-wide">
                   Time of Day
                 </label>
                 <div class="grid grid-cols-2 gap-2">
                   <label class="flex items-center gap-2 text-xs text-slate-300 cursor-pointer">
                     <input type="checkbox" v-model="timeFilters.morning" class="rounded bg-space-800 border-white/10 text-blue-600 focus:ring-blue-500">
                     <span>Morning</span>
                   </label>
                   <label class="flex items-center gap-2 text-xs text-slate-300 cursor-pointer">
                     <input type="checkbox" v-model="timeFilters.afternoon" class="rounded bg-space-800 border-white/10 text-blue-600 focus:ring-blue-500">
                     <span>Afternoon</span>
                   </label>
                   <label class="flex items-center gap-2 text-xs text-slate-300 cursor-pointer">
                     <input type="checkbox" v-model="timeFilters.evening" class="rounded bg-space-800 border-white/10 text-blue-600 focus:ring-blue-500">
                     <span>Evening</span>
                   </label>
                   <label class="flex items-center gap-2 text-xs text-slate-300 cursor-pointer">
                     <input type="checkbox" v-model="timeFilters.night" class="rounded bg-space-800 border-white/10 text-blue-600 focus:ring-blue-500">
                     <span>Night</span>
                   </label>
                 </div>
               </div>
             </div>

             <p class="text-xs text-slate-500">
               Showing {{ filteredPasses.length }} of {{ passes.length }} passes
             </p>
           </div>

           <div v-if="passes && passes.length > 0" class="overflow-x-auto">
             <table class="w-full text-sm border-collapse">
               <thead>
                 <tr class="border-b border-white/10 text-slate-400 uppercase text-xs tracking-wider">
                   <th class="px-4 py-3 text-left font-medium">AOS Time</th>
                   <th class="px-4 py-3 text-left font-medium">Max El</th>
                   <th class="px-4 py-3 text-left font-medium">Duration</th>
                   <th class="px-4 py-3 text-left font-medium">Quality</th>
                 </tr>
               </thead>
               <tbody class="divide-y divide-white/5">
                 <tr v-for="(pass, index) in filteredPasses" :key="index" class="hover:bg-white/5 transition-colors group">
                   <td class="px-4 py-3 font-mono text-slate-300 group-hover:text-white">
                     {{ formatDateTime(pass.aos_time) }}
                   </td>
                   <td class="px-4 py-3 text-slate-300">
                     <div class="flex items-center gap-2">
                        <div class="w-16 h-1 bg-slate-700 rounded-full overflow-hidden">
                          <div class="h-full bg-blue-500" :style="`width: ${(pass.max_elevation / 90) * 100}%`"></div>
                        </div>
                        {{ pass.max_elevation.toFixed(0) }}°
                     </div>
                   </td>
                   <td class="px-4 py-3 text-slate-300">{{ formatDuration(pass.duration) }}</td>
                   <td class="px-4 py-3">
                     <span class="px-2 py-0.5 rounded text-[10px] font-bold border uppercase tracking-wider" :class="qualityBadgeClass(pass.quality_score)">
                       {{ pass.quality_score.toFixed(0) }}
                     </span>
                   </td>
                 </tr>
               </tbody>
             </table>
           </div>
           
           <div v-else-if="passes" class="text-slate-500 text-center py-8 italic">
             No passes found matching your filters.
           </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useSatellitesStore } from '../stores/satellites'
import { useUserStore } from '../stores/user'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

const route = useRoute()
const satellitesStore = useSatellitesStore()
const userStore = useUserStore()
const authStore = useAuthStore()

const satellite = computed(() => satellitesStore.currentSatellite)
const position = ref(null)
const loadingPosition = ref(false)
const passes = ref(null)
const loadingPasses = ref(false)
const showQualityInfo = ref(false)

// Filter controls
const qualityFilter = ref('all')
const durationFilter = ref(0)
const timeFilters = ref({
  morning: false,   // 5am - 12pm
  afternoon: false, // 12pm - 5pm
  evening: false,   // 5pm - 9pm
  night: false      // 9pm - 5am
})

const getTimeOfDay = (dateStr) => {
  const date = new Date(dateStr)
  const hour = date.getHours()

  if (hour >= 5 && hour < 12) return 'morning'
  if (hour >= 12 && hour < 17) return 'afternoon'
  if (hour >= 17 && hour < 21) return 'evening'
  return 'night'
}

const resetFilters = () => {
  qualityFilter.value = 'all'
  durationFilter.value = 0
  timeFilters.value = {
    morning: false,
    afternoon: false,
    evening: false,
    night: false
  }
}

// Helper for dynamic classes
const categoryBadgeClass = computed(() => {
  if (!satellite.value) return ''
  const map = {
    weather: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/20',
    amateur_radio: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
    popular: 'bg-purple-500/10 text-purple-400 border-purple-500/20'
  }
  return map[satellite.value.category] || 'bg-slate-500/10 text-slate-400'
})

const qualityBadgeClass = (score) => {
  if (score >= 70) return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20 shadow-[0_0_10px_rgba(52,211,153,0.2)]'
  if (score >= 40) return 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20'
  return 'bg-red-500/10 text-red-400 border-red-500/20'
}

const filteredPasses = computed(() => {
  if (!passes.value) return []

  return passes.value.filter(pass => {
    // Quality filter
    if (qualityFilter.value === 'excellent' && pass.quality_score < 70) return false
    if (qualityFilter.value === 'good' && pass.quality_score < 40) return false

    // Duration filter
    if (pass.duration < durationFilter.value) return false

    // Time of day filter - if any are selected, only show those times
    const anyTimeSelected = timeFilters.value.morning || timeFilters.value.afternoon ||
                           timeFilters.value.evening || timeFilters.value.night

    if (anyTimeSelected) {
      const timeOfDay = getTimeOfDay(pass.aos_time)
      if (!timeFilters.value[timeOfDay]) return false
    }

    return true
  })
})

const isFavorited = computed(() => {
  if (!authStore.isAuthenticated || !satellite.value) return false
  return userStore.isFavorite(satellite.value.id)
})

const categoryClass = computed(() => {
  if (!satellite.value) return ''
  const classes = {
    weather: 'bg-blue-100 text-blue-800',
    amateur_radio: 'bg-green-100 text-green-800',
    popular: 'bg-purple-100 text-purple-800'
  }
  return classes[satellite.value.category] || 'bg-gray-100 text-gray-800'
})

const categoryLabel = computed(() => {
  if (!satellite.value) return ''
  const labels = {
    weather: 'Weather',
    amateur_radio: 'Amateur Radio',
    popular: 'Popular'
  }
  return labels[satellite.value.category] || satellite.value.category
})

const formattedDate = computed(() => {
  if (!satellite.value) return ''
  return new Date(satellite.value.last_updated).toLocaleString()
})

const fetchPosition = async () => {
  loadingPosition.value = true
  try {
    position.value = await api.getSatellitePosition(satellite.value.id)
  } catch (error) {
    console.error('Error fetching position:', error)
    alert('Failed to fetch satellite position')
  } finally {
    loadingPosition.value = false
  }
}

const calculatePasses = async () => {
  if (!userStore.profile) {
    await userStore.fetchProfile()
  }

  loadingPasses.value = true
  try {
    const result = await api.predictPasses(
      satellite.value.id,
      userStore.profile.location_lat,
      userStore.profile.location_lon,
      7
    )
    passes.value = result.passes
  } catch (error) {
    console.error('Error calculating passes:', error)
    alert('Failed to calculate passes')
  } finally {
    loadingPasses.value = false
  }
}

const toggleFavorite = async () => {
  try {
    if (isFavorited.value) {
      await userStore.removeFavorite(satellite.value.id)
    } else {
      await userStore.addFavorite(satellite.value.id)
    }
  } catch (error) {
    console.error('Error toggling favorite:', error)
  }
}

const formatDateTime = (dateStr) => {
  return new Date(dateStr).toLocaleString()
}

const formatDuration = (seconds) => {
  const minutes = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${minutes}m ${secs}s`
}

onMounted(async () => {
  const satelliteId = route.params.id
  await satellitesStore.fetchSatellite(satelliteId)

  if (authStore.isAuthenticated) {
    await userStore.fetchFavorites()
    if (!userStore.profile) {
      await userStore.fetchProfile()
    }
  }
})
</script>
