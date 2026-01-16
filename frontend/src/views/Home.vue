<template>
  <div class="min-h-screen pb-20">
    <!-- Header -->
    <header class="bg-blue-600 text-white p-4 sticky top-0 z-40 shadow-lg">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-white rounded-full flex items-center justify-center text-blue-600">
            <i class="fas fa-robot text-xl"></i>
          </div>
          <div>
            <h1 class="font-bold text-lg">BAHODIR BRAT</h1>
            <p class="text-xs opacity-90">YouTube Lottery</p>
          </div>
        </div>
        <div class="flex items-center gap-3">
          <div class="text-right">
            <p class="text-xs opacity-80">Balans</p>
            <p class="font-bold">{{ userStore.balance }} ₽</p>
          </div>
          <button @click="router.push('/profile')" class="w-8 h-8 rounded-full bg-white/20 flex items-center justify-center">
            <i class="fas fa-user"></i>
          </button>
        </div>
      </div>
    </header>

    <!-- Live Banner -->
    <div v-if="lotteryStore.isLive" class="m-4 bg-gradient-to-r from-red-600 to-red-700 rounded-2xl p-4 text-white shadow-lg">
      <div class="flex items-center justify-between">
        <div>
          <div class="flex items-center gap-2 mb-1">
            <span class="w-2 h-2 bg-red-300 rounded-full animate-pulse"></span>
            <span class="text-xs font-bold uppercase">Jonli Efir</span>
          </div>
          <h3 class="font-bold text-lg">O'yin ketmoqda!</h3>
          <p class="text-sm opacity-90">YouTube kanalimizda tomosha qiling</p>
        </div>
        <a :href="lotteryStore.youtubeLink" target="_blank" class="bg-white text-red-600 px-4 py-2 rounded-full font-bold text-sm hover:bg-gray-100">
          <i class="fab fa-youtube mr-1"></i> Tomosha
        </a>
      </div>
    </div>

    <!-- Next Draw Banner -->
    <div v-else class="m-4 bg-gradient-to-r from-gray-900 to-blue-900 rounded-2xl p-4 text-white shadow-lg">
      <div class="flex items-center justify-between">
        <div>
          <p class="text-xs opacity-80 mb-1">Keyingi o'yin</p>
          <h3 class="font-bold text-xl">{{ formatDate(lotteryStore.nextDraw) }}</h3>
          <div class="flex gap-2 mt-2">
            <span class="bg-white/20 px-2 py-1 rounded text-xs">{{ lotteryStore.daysLeft }} kun</span>
            <span class="bg-white/20 px-2 py-1 rounded text-xs">{{ lotteryStore.hoursLeft }} soat</span>
          </div>
        </div>
        <div class="text-4xl opacity-30">
          <i class="fas fa-clock"></i>
        </div>
      </div>
    </div>

    <!-- Tickets Section -->
    <div class="p-4">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-bold text-gray-800">Biletlar</h2>
        <button @click="router.push('/winners')" class="text-blue-600 text-sm font-medium">
          G'oliblar <i class="fas fa-arrow-right ml-1"></i>
        </button>
      </div>

      <!-- Tickets Grid -->
      <div class="space-y-4">
        <TicketCard
          v-for="ticket in tickets"
          :key="ticket.id"
          :ticket="ticket"
          @select="selectTicket"
        />
      </div>
    </div>

    <!-- Info Section -->
    <div class="mx-4 mt-6 p-4 bg-white rounded-xl shadow-sm border border-gray-200">
      <div class="flex items-center gap-3 mb-3">
        <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center text-blue-600">
          <i class="fas fa-shield-alt"></i>
        </div>
        <div>
          <h4 class="font-bold text-gray-800">100% Himoyalangan</h4>
          <p class="text-xs text-gray-500">Barcha to'lovlar va o'yinlar shaffof</p>
        </div>
      </div>
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center text-green-600">
          <i class="fas fa-gift"></i>
        </div>
        <div>
          <h4 class="font-bold text-gray-800">Katta Sovg'alar</h4>
          <p class="text-xs text-gray-500">Har o'yinda yangi yutuqlar</p>
        </div>
      </div>
    </div>

    <!-- Quick Stats -->
    <div class="grid grid-cols-3 gap-3 m-4">
      <div class="bg-white p-3 rounded-xl shadow-sm border border-gray-100 text-center">
        <p class="text-xs text-gray-500 mb-1">Bugun</p>
        <p class="font-bold text-lg">{{ lotteryStore.todayParticipants }}</p>
      </div>
      <div class="bg-white p-3 rounded-xl shadow-sm border border-gray-100 text-center">
        <p class="text-xs text-gray-500 mb-1">Jami</p>
        <p class="font-bold text-lg">{{ lotteryStore.totalWinners }}</p>
      </div>
      <div class="bg-white p-3 rounded-xl shadow-sm border border-gray-100 text-center">
        <p class="text-xs text-gray-500 mb-1">Foyda</p>
        <p class="font-bold text-lg">{{ lotteryStore.totalWon }} ₽</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useLotteryStore } from '@/stores/lottery'
import TicketCard from '@/components/TicketCard.vue'
import api from '@/api'

const router = useRouter()
const userStore = useUserStore()
const lotteryStore = useLotteryStore()
const showLoading = inject('showLoading')
const showError = inject('showError')

const tickets = ref([])

onMounted(async () => {
  await loadTickets()
  await lotteryStore.loadLotteryInfo()
})

async function loadTickets() {
  try {
    showLoading(true)
    const response = await api.get('/tickets')
    tickets.value = response.data
  } catch (error) {
    showError('Biletlarni yuklashda xatolik')
  } finally {
    showLoading(false)
  }
}

function selectTicket(ticket) {
  router.push({
    path: '/payment',
    query: { ticketId: ticket.id }
  })
}

function formatDate(dateString) {
  const date = new Date(dateString)
  return date.toLocaleDateString('uz-UZ', {
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>
