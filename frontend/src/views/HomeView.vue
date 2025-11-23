<template>
  <div class="max-w-6xl mx-auto pt-10 pb-20">
    <div class="text-center mb-20 relative">
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-blue-600/20 rounded-full blur-3xl -z-10"></div>
      
      <span class="inline-block py-1 px-3 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-sm font-medium mb-6 animate-fade-in">
        Real-time Orbital Tracking
      </span>
      
      <h1 class="text-6xl md:text-7xl font-display font-bold text-transparent bg-clip-text bg-gradient-to-r from-white via-blue-100 to-slate-400 mb-6 tracking-tight">
        Look Up. <br />
        <span class="text-white">See the Future.</span>
      </h1>
      
      <p class="text-xl text-slate-400 max-w-2xl mx-auto mb-10 font-light leading-relaxed">
        Monitor weather satellites, track the ISS, and predict radio passes with precision accuracy. Your personal mission control center.
      </p>
      
      <div class="flex gap-4 justify-center">
        <router-link
          to="/satellites"
          class="px-8 py-4 bg-blue-600 hover:bg-blue-500 text-white rounded-xl font-medium transition-all shadow-[0_0_20px_rgba(37,99,235,0.3)] hover:shadow-[0_0_30px_rgba(37,99,235,0.5)] hover:-translate-y-1"
        >
          Launch Tracker
        </router-link>
        <router-link
          v-if="!authStore.isAuthenticated"
          to="/register"
          class="px-8 py-4 bg-white/5 border border-white/10 hover:bg-white/10 text-white rounded-xl font-medium transition-all hover:-translate-y-1"
        >
          Create Account
        </router-link>
      </div>
    </div>

    <div class="grid md:grid-cols-3 gap-6">
       </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
</script>
