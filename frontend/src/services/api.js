import { useAuthStore } from '../stores/auth'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

class ApiService {
  async request(endpoint, options = {}) {
    const authStore = useAuthStore()
    const token = authStore.getToken()

    const headers = {
      'Content-Type': 'application/json',
      ...options.headers
    }

    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }

    const config = {
      ...options,
      headers
    }

    const response = await fetch(`${API_URL}${endpoint}`, config)

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Request failed' }))
      throw new Error(error.detail || `HTTP ${response.status}`)
    }

    return response.json()
  }

  // Satellites
  async getSatellites(category = null) {
    const params = category ? `?category=${category}` : ''
    return this.request(`/satellites${params}`)
  }

  async searchSatellites(query) {
    return this.request(`/satellites/search?q=${encodeURIComponent(query)}`)
  }

  async getSatellite(id) {
    return this.request(`/satellites/${id}`)
  }

  async getSatellitePosition(id) {
    return this.request(`/satellites/${id}/position`)
  }

  async predictPasses(id, latitude, longitude, daysAhead = 7) {
    return this.request(`/satellites/${id}/predict`, {
      method: 'POST',
      body: JSON.stringify({
        latitude,
        longitude,
        days_ahead: daysAhead
      })
    })
  }

  // User
  async getUserProfile() {
    return this.request('/user/me')
  }

  async updateUserLocation(latitude, longitude) {
    return this.request('/user/location', {
      method: 'PUT',
      body: JSON.stringify({
        location_lat: latitude,
        location_lon: longitude
      })
    })
  }

  // Favorites
  async getFavorites() {
    return this.request('/favorites')
  }

  async addFavorite(satelliteId) {
    return this.request('/favorites', {
      method: 'POST',
      body: JSON.stringify({
        satellite_id: satelliteId
      })
    })
  }

  async removeFavorite(satelliteId) {
    return this.request(`/favorites/${satelliteId}`, {
      method: 'DELETE'
    })
  }

  async getFavoritePasses() {
    return this.request('/favorites/passes')
  }
}

export default new ApiService()
