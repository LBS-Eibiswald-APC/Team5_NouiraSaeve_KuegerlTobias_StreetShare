import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import App from './App.vue'
import router from "./router";
import ToastPlugin from 'vue-toast-notification'
import 'vue-toast-notification/dist/theme-bootstrap.css'
import { BootstrapIconsPlugin } from "bootstrap-icons-vue";

const savedTheme = localStorage.getItem("theme");

if (savedTheme === "dark") {
    document.documentElement.classList.add("dark");
} else {
    document.documentElement.classList.remove("dark");
}
const app = createApp(App);
const pinia = createPinia();
app.use(ToastPlugin, {
    position: 'top-right',
    duration: 3000
})
app.use(pinia);
app.use(router);
app.use(BootstrapIconsPlugin);

app.mount("#app")

