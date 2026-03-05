import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import App from './App.vue'
import router from "./router";

import PrimeVue from 'primevue/config';
import 'primeicons/primeicons.css';

const app = createApp(App);
const pinia = createPinia();
app.use(pinia);
app.use(router);
app.use(PrimeVue);

app.mount("#app");

