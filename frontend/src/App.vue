<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <RouterView />
    
    <!-- Global Loading Overlay -->
    <div v-if="globalLoading" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded-xl shadow-2xl text-center">
        <div class="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
        <p class="text-gray-700 font-medium">Yuklanmoqda...</p>
      </div>
    </div>
    
    <!-- Global Error Modal -->
    <div v-if="globalError" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded-xl shadow-2xl max-w-sm mx-4">
        <div class="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <i class="fas fa-exclamation-triangle text-red-500 text-xl"></i>
        </div>
        <h3 class="text-lg font-bold text-gray-800 mb-2">Xatolik</h3>
        <p class="text-gray-600 mb-4">{{ globalError }}</p>
        <button @click="globalError = null" class="w-full bg-blue-600 text-white py-2 rounded-lg font-medium hover:bg-blue-700">
          OK
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, provide } from 'vue'
import { useUserStore } from '@/stores/user'

const globalLoading = ref(false)
const globalError = ref(null)

// Provide global functions
provide('showLoading', (show) => {
  globalLoading.value = show
})

provide('showError', (error) => {
  globalError.value = error
  setTimeout(() => {
    globalError.value = null
  }, 5000)
})

// Initialize user store
const userStore = useUserStore()

// Try to get user from Telegram
const initUser = async () => {
  if (window.Telegram?.WebApp?.initDataUnsafe?.user) {
    const tgUser = window.Telegram.WebApp.initDataUnsafe.user
    await userStore.setTelegramUser(tgUser)
  }
}

initUser()
</script>
