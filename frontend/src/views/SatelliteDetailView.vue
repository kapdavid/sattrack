<template>
  <div>
    <!-- Loading State -->
    <div v-if="satellitesStore.loading && !satellite" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      <p class="mt-4 text-slate-600">Loading satellite...</p>
    </div>

    <!-- Satellite Details -->
    <div v-else-if="satellite">
      <div class="flex justify-between items-start mb-6">
        <div>
          <h1 class="text-3xl font-bold text-slate-900">{{ satellite.name }}</h1>
          <span
            class="inline-block mt-2 px-3 py-1 text-sm font-semibold rounded-full"
            :class="categoryClass"
          >
            {{ categoryLabel }}
          </span>
        </div>

        <button
          v-if="authStore.isAuthenticated"
          @click="toggleFavorite"
          class="text-4xl hover:scale-110 transition"
          :disabled="userStore.loading"
        >
          {{ isFavorited ? '⭐' : '☆' }}
        </button>
      </div>

      <!-- Satellite Info -->
      <div class="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 class="text-xl font-bold text-slate-900 mb-4">Information</h2>
        <div class="grid md:grid-cols-2 gap-4 text-slate-700">
          <div>
            <p class="text-sm text-slate-500">NORAD ID</p>
            <p class="font-semibold">{{ satellite.norad_id }}</p>
          </div>
          <div>
            <p class="text-sm text-slate-500">Last TLE Update</p>
            <p class="font-semibold">{{ formattedDate }}</p>
          </div>
        </div>
      </div>

      <!-- Current Position -->
      <div class="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 class="text-xl font-bold text-slate-900 mb-4">Current Position</h2>

        <button
          @click="fetchPosition"
          :disabled="loadingPosition"
          class="mb-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition"
        >
          {{ loadingPosition ? 'Loading...' : 'Get Current Position' }}
        </button>

        <div v-if="position" class="grid md:grid-cols-3 gap-4 text-slate-700">
          <div>
            <p class="text-sm text-slate-500">Latitude</p>
            <p class="font-semibold">{{ position.latitude.toFixed(4) }}°</p>
          </div>
          <div>
            <p class="text-sm text-slate-500">Longitude</p>
            <p class="font-semibold">{{ position.longitude.toFixed(4) }}°</p>
          </div>
          <div>
            <p class="text-sm text-slate-500">Altitude</p>
            <p class="font-semibold">{{ position.altitude_km.toFixed(2) }} km</p>
          </div>
        </div>
      </div>

      <!-- Pass Predictions -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex justify-between items-start mb-4">
          <h2 class="text-xl font-bold text-slate-900">Pass Predictions</h2>
          <button
            @click="showQualityInfo = !showQualityInfo"
            class="text-sm text-blue-600 hover:text-blue-800 underline"
          >
            {{ showQualityInfo ? 'Hide' : 'What is quality?' }}
          </button>
        </div>

        <!-- Quality Score Explanation -->
        <div v-if="showQualityInfo" class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4 text-sm">
          <p class="font-semibold text-blue-900 mb-2">How Pass Quality is Calculated (0-100)</p>
          <ul class="space-y-1 text-blue-800">
            <li><strong>Elevation (70 points max):</strong> Higher passes are better. Passes above 45° get near-perfect elevation scores.</li>
            <li><strong>Duration (30 points max):</strong> Longer passes are better. Passes of 10+ minutes get full duration scores.</li>
            <li><strong>Score ranges:</strong> 70+ = Excellent (green), 40-69 = Good (yellow), &lt;40 = Fair (orange)</li>
          </ul>
        </div>

        <div v-if="!userStore.hasLocation" class="bg-yellow-50 border border-yellow-200 text-yellow-800 p-4 rounded-lg mb-4">
          <p class="font-semibold">Location Required</p>
          <p class="text-sm mt-1">Please set your observer location in settings to calculate pass predictions.</p>
          <router-link
            to="/settings"
            class="inline-block mt-3 px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 transition text-sm"
          >
            Go to Settings
          </router-link>
        </div>

        <div v-else>
          <button
            @click="calculatePasses"
            :disabled="loadingPasses"
            class="mb-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition"
          >
            {{ loadingPasses ? 'Calculating...' : 'Calculate Passes (7 days)' }}
          </button>

          <!-- Filter Controls -->
          <div v-if="passes && passes.length > 0" class="mb-4 p-4 bg-slate-50 rounded-lg">
            <p class="text-sm font-semibold text-slate-700 mb-3">Filter Passes:</p>
            <div class="grid md:grid-cols-2 gap-4">
              <div>
                <label for="minQuality" class="block text-sm text-slate-600 mb-1">
                  Min. Quality: {{ minQuality }}
                </label>
                <input
                  id="minQuality"
                  v-model.number="minQuality"
                  type="range"
                  min="0"
                  max="100"
                  step="5"
                  class="w-full"
                />
                <div class="flex justify-between text-xs text-slate-500 mt-1">
                  <span>0</span>
                  <span>50</span>
                  <span>100</span>
                </div>
              </div>
              <div>
                <label for="minDuration" class="block text-sm text-slate-600 mb-1">
                  Min. Duration: {{ Math.floor(minDuration / 60) }}m {{ minDuration % 60 }}s
                </label>
                <input
                  id="minDuration"
                  v-model.number="minDuration"
                  type="range"
                  min="0"
                  max="600"
                  step="30"
                  class="w-full"
                />
                <div class="flex justify-between text-xs text-slate-500 mt-1">
                  <span>0m</span>
                  <span>5m</span>
                  <span>10m</span>
                </div>
              </div>
            </div>
            <p class="text-xs text-slate-500 mt-2">
              Showing {{ filteredPasses.length }} of {{ passes.length }} passes
            </p>
          </div>

          <!-- Passes Table -->
          <div v-if="passes && passes.length > 0" class="overflow-x-auto">
<table class="w-full text-sm border-collapse">
  <thead>
    <tr class="border-b border-white/10 text-slate-400 uppercase text-xs tracking-wider">
      <th class="px-4 py-4 text-left font-medium">AOS Time</th>
      <th class="px-4 py-4 text-left font-medium">Max El</th>
      <th class="px-4 py-4 text-left font-medium">Duration</th>
      <th class="px-4 py-4 text-left font-medium">Quality</th>
    </tr>
  </thead>
  <tbody class="divide-y divide-white/5">
    <tr v-for="(pass, index) in filteredPasses" :key="index" class="hover:bg-white/5 transition-colors">
      <td class="px-4 py-4 font-mono text-slate-300">
        {{ formatDateTime(pass.aos_time) }}
      </td>
      <td class="px-4 py-4 text-slate-300">
        <div class="flex items-center gap-2">
           <div class="w-12 h-1.5 bg-slate-700 rounded-full overflow-hidden">
             <div class="h-full bg-blue-500" :style="`width: ${(pass.max_elevation / 90) * 100}%`"></div>
           </div>
           {{ pass.max_elevation.toFixed(0) }}°
        </div>
      </td>
      <td class="px-4 py-4 text-slate-300">{{ formatDuration(pass.duration) }}</td>
      <td class="px-4 py-4">
        <span class="px-2.5 py-1 rounded-md text-xs font-bold border" :class="qualityBadgeClass(pass.quality_score)">
          {{ pass.quality_score.toFixed(0) }}
        </span>
      </td>
    </tr>
  </tbody>
</table>
          </div>

          <div v-else-if="passes && filteredPasses.length === 0 && passes.length > 0" class="text-slate-600 text-center py-4">
            No passes match your filters. Try adjusting the quality or duration filters.
          </div>

          <div v-else-if="passes && passes.length === 0" class="text-slate-600 text-center py-4">
            No passes found in the next 7 days
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
const minQuality = ref(0)
const minDuration = ref(0)

const filteredPasses = computed(() => {
  if (!passes.value) return []
  return passes.value.filter(pass =>
    pass.quality_score >= minQuality.value &&
    pass.duration >= minDuration.value
  )
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

const qualityClass = (score) => {
  if (score >= 70) return 'bg-green-100 text-green-800'
  if (score >= 40) return 'bg-yellow-100 text-yellow-800'
  return 'bg-orange-100 text-orange-800'
}
const qualityBadgeClass = (score) => {
  if (score >= 70) return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
  if (score >= 40) return 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20'
  return 'bg-red-500/10 text-red-400 border-red-500/20'
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
