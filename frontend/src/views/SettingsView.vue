<template>
  <div class="max-w-2xl mx-auto">
    <h1 class="text-3xl font-bold text-slate-900 mb-6">Settings</h1>

    <!-- User Info -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
      <h2 class="text-xl font-bold text-slate-900 mb-4">Account</h2>
      <div v-if="userStore.profile">
        <p class="text-slate-700"><strong>Email:</strong> {{ userStore.profile.email }}</p>
        <p class="text-sm text-slate-500 mt-2">
          Member since {{ new Date(userStore.profile.created_at).toLocaleDateString() }}
        </p>
      </div>
    </div>

    <!-- Observer Location -->
    <div class="bg-white rounded-lg shadow-md p-6">
      <h2 class="text-xl font-bold text-slate-900 mb-4">Observer Location</h2>
      <p class="text-slate-600 mb-4">
        Set your location to calculate satellite pass predictions. You can use coordinates or a city name.
      </p>

      <form @submit.prevent="handleUpdateLocation" class="space-y-4">
        <div class="grid md:grid-cols-2 gap-4">
          <div>
            <label for="latitude" class="block text-sm font-medium text-slate-700 mb-1">
              Latitude
            </label>
            <input
              id="latitude"
              v-model.number="latitude"
              type="number"
              step="0.0001"
              min="-90"
              max="90"
              required
              class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="37.7749"
            />
            <p class="text-xs text-slate-500 mt-1">-90 to 90</p>
          </div>

          <div>
            <label for="longitude" class="block text-sm font-medium text-slate-700 mb-1">
              Longitude
            </label>
            <input
              id="longitude"
              v-model.number="longitude"
              type="number"
              step="0.0001"
              min="-180"
              max="180"
              required
              class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="-122.4194"
            />
            <p class="text-xs text-slate-500 mt-1">-180 to 180</p>
          </div>
        </div>

        <div v-if="error" class="bg-red-50 text-red-600 p-3 rounded-lg text-sm">
          {{ error }}
        </div>

        <div v-if="success" class="bg-green-50 text-green-600 p-3 rounded-lg text-sm">
          {{ success }}
        </div>

        <div class="flex gap-3">
          <button
            type="submit"
            :disabled="userStore.loading"
            class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition"
          >
            {{ userStore.loading ? 'Saving...' : 'Save Location' }}
          </button>

          <button
            type="button"
            @click="getGeolocation"
            class="px-6 py-2 border-2 border-blue-600 text-blue-600 rounded-lg hover:bg-blue-50 transition"
          >
            Use My Location
          </button>
        </div>
      </form>

      <!-- Common Locations (examples) -->
      <div class="mt-6 pt-6 border-t">
        <p class="text-sm font-medium text-slate-700 mb-3">Quick Select:</p>
        <div class="flex flex-wrap gap-2">
          <button
            @click="setLocation(37.7749, -122.4194, 'San Francisco')"
            class="px-3 py-1 text-sm bg-slate-100 hover:bg-slate-200 rounded transition"
          >
            San Francisco
          </button>
          <button
            @click="setLocation(40.7128, -74.0060, 'New York')"
            class="px-3 py-1 text-sm bg-slate-100 hover:bg-slate-200 rounded transition"
          >
            New York
          </button>
          <button
            @click="setLocation(51.5074, -0.1278, 'London')"
            class="px-3 py-1 text-sm bg-slate-100 hover:bg-slate-200 rounded transition"
          >
            London
          </button>
          <button
            @click="setLocation(35.6762, 139.6503, 'Tokyo')"
            class="px-3 py-1 text-sm bg-slate-100 hover:bg-slate-200 rounded transition"
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
    success.value = 'Location updated successfully!'
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
  success.value = `Location set to ${name}`
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
  success.value = 'Getting your location...'

  navigator.geolocation.getCurrentPosition(
    (position) => {
      // Round to 6 decimal places (~0.1m precision) to avoid form validation issues
      latitude.value = Math.round(position.coords.latitude * 1000000) / 1000000
      longitude.value = Math.round(position.coords.longitude * 1000000) / 1000000
      success.value = 'Location detected!'
      setTimeout(() => {
        success.value = null
      }, 2000)
    },
    (err) => {
      error.value = 'Unable to retrieve your location'
      success.value = null
    }
  )
}

onMounted(async () => {
  // Fetch user profile if not already loaded
  if (!userStore.profile) {
    await userStore.fetchProfile()
  }

  // Pre-fill form with current location if set
  if (userStore.profile) {
    latitude.value = userStore.profile.location_lat
    longitude.value = userStore.profile.location_lon
  }
})
</script>
