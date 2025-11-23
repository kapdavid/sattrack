<template>
  <div class="max-w-4xl mx-auto">
    <div class="text-center mb-12">
      <h1 class="text-5xl font-bold text-slate-900 mb-4">
        Track Satellites in Real-Time
      </h1>
      <p class="text-xl text-slate-600 mb-8">
        Monitor weather satellites, amateur radio birds, and popular space stations.
        Get pass predictions for your location.
      </p>
      <div class="flex gap-4 justify-center">
        <router-link
          to="/satellites"
          class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-medium"
        >
          Browse Satellites
        </router-link>
        <router-link
          v-if="!authStore.isAuthenticated"
          to="/register"
          class="px-6 py-3 border-2 border-blue-600 text-blue-600 rounded-lg hover:bg-blue-50 transition font-medium"
        >
          Sign Up Free
        </router-link>
      </div>
    </div>

    <div class="grid md:grid-cols-3 gap-6 mt-12">
      <div class="bg-white p-6 rounded-lg shadow-md">
        <div class="text-3xl mb-3">🛰️</div>
        <h3 class="text-lg font-bold text-slate-900 mb-2">Weather Satellites</h3>
        <p class="text-slate-600">
          Track NOAA and Meteor-M satellites to receive weather imagery
        </p>
      </div>

      <div class="bg-white p-6 rounded-lg shadow-md">
        <div class="text-3xl mb-3">📡</div>
        <h3 class="text-lg font-bold text-slate-900 mb-2">Amateur Radio</h3>
        <p class="text-slate-600">
          Find pass times for amateur radio satellites like SO-50 and AO-91
        </p>
      </div>

      <div class="bg-white p-6 rounded-lg shadow-md">
        <div class="text-3xl mb-3">🚀</div>
        <h3 class="text-lg font-bold text-slate-900 mb-2">ISS & More</h3>
        <p class="text-slate-600">
          See when the International Space Station will pass overhead
        </p>
      </div>
    </div>

    <div class="mt-12 bg-blue-50 p-8 rounded-lg">
      <h2 class="text-2xl font-bold text-slate-900 mb-4">How it Works</h2>
      <ol class="space-y-3 text-slate-700">
        <li class="flex gap-3">
          <span class="font-bold text-blue-600">1.</span>
          <span>Set your observer location in settings</span>
        </li>
        <li class="flex gap-3">
          <span class="font-bold text-blue-600">2.</span>
          <span>Browse satellites and add your favorites</span>
        </li>
        <li class="flex gap-3">
          <span class="font-bold text-blue-600">3.</span>
          <span>Get pass predictions showing when satellites will be visible from your location</span>
        </li>
        <li class="flex gap-3">
          <span class="font-bold text-blue-600">4.</span>
          <span>Receive email notifications for upcoming passes</span>
        </li>
      </ol>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
</script>
