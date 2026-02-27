import axios from "axios";
import { useAuthStore } from "@/store/authStore.js";

const baseUrl = "http://127.0.0.1:8000";

const api = axios.create({
    baseURL: baseUrl,
    headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use(config => {
    const token = localStorage.getItem("token");
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
});

api.interceptors.response.use(
    response => response,
    async error => {
        const authStore = useAuthStore();
        if (error.response?.status === 401) {
            authStore.logout();
            localStorage.removeItem("token");
            window.location.href = "/login";
        }
        return Promise.reject(error);
    }
);

export default api;