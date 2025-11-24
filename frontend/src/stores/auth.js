import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { createClient } from '@supabase/supabase-js'
import { useUserStore } from './user'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseKey = import.meta.env.VITE_SUPABASE_ANON_KEY

const supabase = createClient(supabaseUrl, supabaseKey)

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const session = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const initialized = ref(false)
  let initPromise = null

  const isAuthenticated = computed(() => !!session.value)

  // Get current session token for API requests
  const getToken = () => {
    return session.value?.access_token || null
  }

  // Initialize auth state
  const initialize = async () => {
    // If already initialized or currently initializing, return the existing promise
    if (initialized.value) return
    if (initPromise) return initPromise

    loading.value = true
    initPromise = (async () => {
      try {
        const { data } = await supabase.auth.getSession()
        session.value = data.session
        user.value = data.session?.user || null
      } catch (err) {
        console.error('Error initializing auth:', err)
        error.value = err.message
      } finally {
        loading.value = false
        initialized.value = true
      }

      // Listen for auth changes (only set up once)
      supabase.auth.onAuthStateChange((event, newSession) => {
        session.value = newSession
        user.value = newSession?.user || null
      })
    })()

    return initPromise
  }

  // Sign up
  const signUp = async (email, password) => {
    loading.value = true
    error.value = null
    try {
      const { data, error: signUpError } = await supabase.auth.signUp({
        email,
        password
      })
      if (signUpError) throw signUpError
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // Sign in
  const signIn = async (email, password) => {
    loading.value = true
    error.value = null
    try {
      const { data, error: signInError } = await supabase.auth.signInWithPassword({
        email,
        password
      })
      if (signInError) throw signInError
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // Sign out
  const signOut = async () => {
    loading.value = true
    error.value = null
    try {
      const { error: signOutError } = await supabase.auth.signOut()
      if (signOutError) throw signOutError
      user.value = null
      session.value = null

      // Clear user store data
      const userStore = useUserStore()
      userStore.clearUserData()
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    user,
    session,
    loading,
    error,
    isAuthenticated,
    getToken,
    initialize,
    signUp,
    signIn,
    signOut
  }
})
