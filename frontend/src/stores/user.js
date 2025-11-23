import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../services/api'

export const useUserStore = defineStore('user', () => {
  const profile = ref(null)
  const favorites = ref([])
  const loading = ref(false)
  const error = ref(null)

  const hasLocation = computed(() => {
    return profile.value?.location_lat != null && profile.value?.location_lon != null
  })

  const fetchProfile = async () => {
    loading.value = true
    error.value = null
    try {
      profile.value = await api.getUserProfile()
    } catch (err) {
      error.value = err.message
      console.error('Error fetching profile:', err)
    } finally {
      loading.value = false
    }
  }

  const updateLocation = async (latitude, longitude) => {
    loading.value = true
    error.value = null
    try {
      profile.value = await api.updateUserLocation(latitude, longitude)
    } catch (err) {
      error.value = err.message
      console.error('Error updating location:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchFavorites = async () => {
    loading.value = true
    error.value = null
    try {
      favorites.value = await api.getFavorites()
    } catch (err) {
      error.value = err.message
      console.error('Error fetching favorites:', err)
    } finally {
      loading.value = false
    }
  }

  const addFavorite = async (satelliteId) => {
    loading.value = true
    error.value = null
    try {
      await api.addFavorite(satelliteId)
      await fetchFavorites() // Refresh the list
    } catch (err) {
      error.value = err.message
      console.error('Error adding favorite:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const removeFavorite = async (satelliteId) => {
    loading.value = true
    error.value = null
    try {
      await api.removeFavorite(satelliteId)
      await fetchFavorites() // Refresh the list
    } catch (err) {
      error.value = err.message
      console.error('Error removing favorite:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const isFavorite = (satelliteId) => {
    return favorites.value.some(fav => fav.satellite_id === satelliteId)
  }

  return {
    profile,
    favorites,
    loading,
    error,
    hasLocation,
    fetchProfile,
    updateLocation,
    fetchFavorites,
    addFavorite,
    removeFavorite,
    isFavorite
  }
})
