import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './styles/main.css'

// Initialize Telegram Web App
let tg = null;
if (window.Telegram?.WebApp) {
  tg = window.Telegram.WebApp;
  tg.expand();
  tg.enableClosingConfirmation();
  tg.setHeaderColor('#2b6cb0');
  tg.setBackgroundColor('#f7fafc');
  
  // Set theme
  const theme = tg.colorScheme;
  document.documentElement.setAttribute('data-theme', theme);
}

const app = createApp(App);

// Provide Telegram instance
app.provide('telegram', tg);

app.use(createPinia());
app.use(router);

app.mount('#app');
