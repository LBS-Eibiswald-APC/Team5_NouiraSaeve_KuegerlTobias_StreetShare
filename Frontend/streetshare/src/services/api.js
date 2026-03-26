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
        const isMeRoute = error.config?.url?.includes("/users/me");

        if (error.response?.status === 401 && !isLoginRoute && !isMeRoute) {
            authStore.logout(false);
            window.location.href = "/login";
        }

        return Promise.reject(error);
    }
);

export default api;
