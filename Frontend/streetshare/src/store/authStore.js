import { defineStore } from "pinia";
import api from "@/services/api";

export const useAuthStore = defineStore("auth", {
    state: () => ({
        user: null,
        user_id: null,
        isAuthenticated: false,
        initialized: false,
        loading: false,
        error: null,
    }),

    actions: {
        async getMe() {
            try {
                const response = await api.get("/users/me");
                this.user = response.data;
                this.user_id = response.data.id;
                this.isAuthenticated = true;
                this.initialized = true;
                return response.data;
            } catch (error) {
                this.user = null;
                this.user_id = null;
                this.isAuthenticated = false;
                this.initialized = true;
                throw error;
            }
        },

        async updateProfile(user) {
            try {
                const response = await api.put("/users/settings/me", user);
                this.user = response.data;
                this.user_id = response.data.id;
                return response.data;
            } catch (error) {
                throw error;
            }
        },

        async changePassword(payload) {
            try {
                const response = await api.put("/users/password", payload);
                return response.data;
            } catch (error) {
                throw error;
            }
        },

        async register(payload) {
            this.loading = true;
            this.error = null;

            try {
                const response = await api.post("/auth/register", payload);
                return response.data;
            } catch (error) {
                const detail = error.response?.data?.detail;

                if (typeof detail === "object" && detail !== null) {
                    this.error = {
                        email: detail.email || "",
                        display_name: detail.display_name || "",
                        general: detail.general || "Registrierung fehlgeschlagen.",
                    };
                } else {
                    this.error = {
                        email: "",
                        display_name: "",
                        general: detail || "Registrierung fehlgeschlagen.",
                    };
                }

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

                await api.post("/auth/login", formData.toString(), {
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                });

                await this.getMe();
                this.isAuthenticated = true;

                return true;
            } catch (error) {
                this.user = null;
                this.user_id = null;
                this.isAuthenticated = false;
                this.error = error.response?.data?.detail || "Login fehlgeschlagen";
                return false;
            } finally {
                this.loading = false;
            }
        },

        async fetchUser() {
            try {
                await this.getMe();
            } catch {
                this.logout(false);
            } finally {
                this.initialized = true;
            }
        },

        async ensureInitialized() {
            if (this.initialized) {
                return;
            }

            await this.fetchUser();
        },

        async logout(callBackend = true) {
            try {
                if (callBackend) {
                    await api.post("/auth/logout");
                }
            } catch (error) {
                console.error("Logout error:", error);
            } finally {
                this.user = null;
                this.user_id = null;
                this.isAuthenticated = false;
                this.initialized = true;
                this.error = null;
            }
        },
    },
});
