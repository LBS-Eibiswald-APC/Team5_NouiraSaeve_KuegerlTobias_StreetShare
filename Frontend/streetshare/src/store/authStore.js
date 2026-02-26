import {defineStore} from "pinia";
import api from "@/services/api";


export const useAuthStore = defineStore("auth", {

    state: () => ({
        user: null,
        token: localStorage.getItem("token") || null,
        isAuthenticated: !!localStorage.getItem("token"),
        loading: false,
        error: null
    }),


    actions: {
        async getMe() {
            try {
                const response = await api.get("/users/me");
                return response.data
            } catch (error) {
                return null
            }
        },
        async register(payload) {
            this.loading = true;
            this.error = null;
            try {
                const response = await api.post(
                    "/auth/register",
                    payload
                );
                this.token = response.data.access_token;
                this.user = response.data.user;
                this.isAuthenticated = true;

                localStorage.setItem(
                    "token",
                    this.token
                );
            } catch (error) {
                this.error =
                    error.response?.data?.detail ||
                    "Register failed";
                throw error;
            } finally {
                this.loading = false;
            }
        },

        async login(payload) {
            this.loading = true;
            this.error = null;
            try {
                const formData = new URLSearchParams();
                formData.append("username", payload.email);
                formData.append("password", payload.password);
                const response = await api.post(
                    "/auth/login",
                    formData,
                    {
                        headers: { "Content-Type": "application/x-www-form-urlencoded" },
                    }
                );
                this.token = response.data.access_token;
                this.user = response.data.user;
                this.isAuthenticated = true;
                localStorage.setItem(
                    "token",
                    this.token
                );
                return true
            } catch (error) {
                this.error =
                    error.response?.data?.detail ||
                    "Login failed";
                throw error;

            } finally {
                this.loading = false;
            }
            return false
        },


        async fetchUser() {
            if (!this.token) return;
            try {
                const response = await api.get(
                    "/auth/me"
                );
                this.user = response.data;
                this.isAuthenticated = true;
            } catch {
                this.logout();
            }
        },


        logout() {
            this.user = null;
            this.token = null;
            this.isAuthenticated = false;
            localStorage.removeItem("token");
        }

    }

});