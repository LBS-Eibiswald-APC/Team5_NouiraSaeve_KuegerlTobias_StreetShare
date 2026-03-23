import {defineStore} from "pinia";
import api from "@/services/api";


export const useAuthStore = defineStore("auth", {

    state: () => ({
        user: null,
        user_id: null,
        token: localStorage.getItem("token") || null,
        isAuthenticated: !!localStorage.getItem("token"),
        loading: false,
        error: null
    }),


    actions: {
        async getMe() {
            try {
                const response = await api.get("/users/me");
                this.user = response.data;
                this.user_id = response.data.id;
                return response.data
            } catch (error) {
                throw error;
            }
        },
        async updateProfile(user) {
            try {
                const response = await api.put("/users/settings/me", user);
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

                this.token = response.data.access_token;
                this.user = response.data.user;
                this.isAuthenticated = true;

                localStorage.setItem("token", this.token);

                return response.data;
            } catch (error) {
                const detail = error.response?.data?.detail;

                if (typeof detail === "object" && detail !== null) {
                    this.error = {
                        email: detail.email || "",
                        display_name: detail.display_name || "",
                        general: detail.general || "Registrierung fehlgeschlagen."
                    };
                } else {
                    this.error = {
                        email: "",
                        display_name: "",
                        general: detail || "Register failed"
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

                const response = await api.post(
                    "/auth/login",
                    formData.toString(),
                    {
                        headers: {
                            "Content-Type": "application/x-www-form-urlencoded",
                        },
                    }
                );

                this.token = response.data.access_token;
                this.user = response.data.user;
                this.isAuthenticated = true;

                localStorage.setItem("token", this.token);

                return true;
            } catch (error) {
                console.log(error.response?.data);
                this.error = error.response?.data?.detail || "Login failed";
                return false;
            } finally {
                this.loading = false;
            }
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