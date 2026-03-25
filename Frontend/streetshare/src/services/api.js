import axios from "axios";
import { useAuthStore } from "@/store/authStore.js";

const api = axios.create({
    baseURL: "http://localhost:8000",
    withCredentials: true,
});

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const authStore = useAuthStore();

        const isLoginRoute = error.config?.url?.includes("/auth/login");

        if (error.response?.status === 401 && !isLoginRoute) {
            authStore.logout(false);
            window.location.href = "/login";
        }

        return Promise.reject(error);
    }
);

export default api;