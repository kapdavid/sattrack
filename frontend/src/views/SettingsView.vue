<template>
  <div class="max-w-2xl mx-auto">
    <h1 class="text-3xl font-display font-bold text-white mb-8">Mission Configuration</h1>

    <div class="bg-space-800/50 backdrop-blur-md border border-white/10 rounded-xl p-6 mb-6 shadow-xl">
      <h2 class="text-lg font-display font-bold text-white mb-4 border-b border-white/10 pb-2">Commander Profile</h2>
      <div v-if="userStore.profile" class="flex items-center gap-4">
        <div class="w-12 h-12 rounded-full bg-blue-500/20 border border-blue-500/30 flex items-center justify-center text-blue-400 text-xl font-bold">
          {{ userStore.profile.email.charAt(0).toUpperCase() }}
        </div>
        <div>
          <p class="text-white font-medium">{{ userStore.profile.email }}</p>
          <p class="text-xs text-slate-400 mt-0.5 font-mono">
            ID: {{ userStore.profile.supabase_id.substring(0, 8) }}... • Joined {{ new Date(userStore.profile.created_at).toLocaleDateString() }}
          </p>
        </div>
      </div>
    </div>

    <div class="bg-space-800/50 backdrop-blur-md border border-white/10 rounded-xl p-6 shadow-xl">
      <div class="mb-6">
        <h2 class="text-lg font-display font-bold text-white mb-2 border-b border-white/10 pb-2">Observer Coordinates</h2>
        <p class="text-slate-400 text-sm">
          Precise latitude and longitude are required for accurate pass predictions and azimuth calculations.
        </p>
      </div>

<form @submit.prevent="handleUpdateLocation" class="space-y-6">
  <div class="grid md:grid-cols-2 gap-6">
<div class="space-y-2">
  <label for="latitude" class="block text-xs font-bold text-slate-400 uppercase tracking-wider">
    Latitude
  </label>
  <div class="relative group">
    <input
      id="latitude"
      v-model.number="latitude"
      type="number"
      step="0.0001"
      min="-90"
      max="90"
      required
      class="w-full pl-4 pr-12 py-3 bg-space-900/50 border border-white/10 rounded-lg text-white font-mono placeholder-slate-600 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
      placeholder="37.7749"
    />
    <span class="absolute right-4 top-3 text-slate-500 text-xs font-medium pointer-events-none select-none">deg</span>
  </div>
</div>

<div class="space-y-2">
  <label for="longitude" class="block text-xs font-bold text-slate-400 uppercase tracking-wider">
    Longitude
  </label>
  <div class="relative group">
    <input
      id="longitude"
      v-model.number="longitude"
      type="number"
      step="0.0001"
      min="-180"
      max="180"
      required
      class="w-full pl-4 pr-12 py-3 bg-space-900/50 border border-white/10 rounded-lg text-white font-mono placeholder-slate-600 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
      placeholder="-122.4194"
    />
    <span class="absolute right-4 top-3 text-slate-500 text-xs font-medium pointer-events-none select-none">deg</span>
  </div>
</div>
  </div>

        <div v-if="error" class="bg-red-500/10 border border-red-500/20 text-red-400 p-3 rounded-lg text-sm flex items-center gap-2">
          <span>⚠️</span> {{ error }}
        </div>

        <div v-if="success" class="bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 p-3 rounded-lg text-sm flex items-center gap-2">
          <span>✓</span> {{ success }}
        </div>

        <div class="flex flex-col sm:flex-row gap-3 pt-2">
          <button
            type="submit"
            :disabled="userStore.loading"
            class="px-6 py-2.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg shadow-[0_0_15px_rgba(37,99,235,0.4)] transition-all font-medium disabled:opacity-50 disabled:cursor-not-allowed flex-1 sm:flex-none justify-center"
          >
            {{ userStore.loading ? 'Updating...' : 'Update Coordinates' }}
          </button>

          <button
            type="button"
            @click="getGeolocation"
            class="px-6 py-2.5 bg-blue-600/10 hover:bg-blue-600/20 border border-blue-500/30 text-blue-300 rounded-lg transition-all font-medium flex items-center justify-center gap-2"
          >
            <span>📍</span> Detect Location
          </button>
        </div>
      </form>

      <div class="mt-8 pt-6 border-t border-white/5">
        <p class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-4">Quick Calibration</p>
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <button
            @click="setLocation(37.7749, -122.4194, 'San Francisco')"
            class="px-3 py-2 text-xs bg-space-900/80 hover:bg-blue-600/20 border border-white/5 hover:border-blue-500/30 text-slate-300 hover:text-blue-300 rounded transition-all"
          >
            San Francisco
          </button>
          <button
            @click="setLocation(40.7128, -74.0060, 'New York')"
            class="px-3 py-2 text-xs bg-space-900/80 hover:bg-blue-600/20 border border-white/5 hover:border-blue-500/30 text-slate-300 hover:text-blue-300 rounded transition-all"
          >
            New York
          </button>
          <button
            @click="setLocation(51.5074, -0.1278, 'London')"
            class="px-3 py-2 text-xs bg-space-900/80 hover:bg-blue-600/20 border border-white/5 hover:border-blue-500/30 text-slate-300 hover:text-blue-300 rounded transition-all"
          >
            London
          </button>
          <button
            @click="setLocation(35.6762, 139.6503, 'Tokyo')"
            class="px-3 py-2 text-xs bg-space-900/80 hover:bg-blue-600/20 border border-white/5 hover:border-blue-500/30 text-slate-300 hover:text-blue-300 rounded transition-all"
          >
            Tokyo
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '../stores/user'

const userStore = useUserStore()

const latitude = ref(null)
const longitude = ref(null)
const error = ref(null)
const success = ref(null)

const handleUpdateLocation = async () => {
  error.value = null
  success.value = null

  try {
    await userStore.updateLocation(latitude.value, longitude.value)
    success.value = 'Coordinates updated successfully.'
    setTimeout(() => {
      success.value = null
    }, 3000)
  } catch (err) {
    error.value = err.message || 'Failed to update location'
  }
}

const setLocation = (lat, lon, name) => {
  latitude.value = lat
  longitude.value = lon
  success.value = `Calibrated to ${name}`
  setTimeout(() => {
    success.value = null
  }, 2000)
}

const getGeolocation = () => {
  if (!navigator.geolocation) {
    error.value = 'Geolocation is not supported by your browser'
    return
  }

  error.value = null
  success.value = 'Acquiring GPS signal...'

  navigator.geolocation.getCurrentPosition(
    (position) => {
      // Round to 6 decimal places (~0.1m precision)
      latitude.value = Math.round(position.coords.latitude * 1000000) / 1000000
      longitude.value = Math.round(position.coords.longitude * 1000000) / 1000000
      success.value = 'GPS signal acquired.'
      setTimeout(() => {
        success.value = null
      }, 2000)
    },
    (err) => {
      error.value = 'Unable to retrieve location signal.'
      success.value = null
    }
  )
}

onMounted(async () => {
  if (!userStore.profile) {
    await userStore.fetchProfile()
  }

  if (userStore.profile) {
    latitude.value = userStore.profile.location_lat
    longitude.value = userStore.profile.location_lon
  }
})
</script>