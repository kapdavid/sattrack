import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../services/api'

export const useSatellitesStore = defineStore('satellites', () => {
  const satellites = ref([])
  const currentSatellite = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const fetchSatellites = async (category = null) => {
    loading.value = true
    error.value = null
    try {
      satellites.value = await api.getSatellites(category)
    } catch (err) {
      error.value = err.message
      console.error('Error fetching satellites:', err)
    } finally {
      loading.value = false
    }
  }

  const searchSatellites = async (query) => {
    loading.value = true
    error.value = null
    try {
      satellites.value = await api.searchSatellites(query)
    } catch (err) {
      error.value = err.message
      console.error('Error searching satellites:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchSatellite = async (id) => {
    loading.value = true
    error.value = null
    try {
      currentSatellite.value = await api.getSatellite(id)
    } catch (err) {
      error.value = err.message
      console.error('Error fetching satellite:', err)
    } finally {
      loading.value = false
    }
  }

  return {
    satellites,
    currentSatellite,
    loading,
    error,
    fetchSatellites,
    searchSatellites,
    fetchSatellite
  }
})
