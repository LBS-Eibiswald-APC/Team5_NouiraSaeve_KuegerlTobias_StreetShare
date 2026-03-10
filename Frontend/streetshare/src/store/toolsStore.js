import { defineStore } from "pinia";
import api from "@/services/api";
import {useAuthStore} from "@/store/authStore.js";

export const useToolsStore = defineStore("tools", {
    state: () => ({
        tools: [],
        loading: false,
        filters: {
            city: "",
            zip: "",
            country: "",
        },
        countries: ["Österreich", "Deutschland", "Schweiz", "Italien", "Frankreich"],
        page: 1,
        perPage: 25,
        total: 0,
    }),
    getters: {
        totalPages: (state) => Math.ceil(state.total / state.perPage) || 1,
    },
    actions: {
        async getUserTools() {
            const response = await api.get("/tools/user-tools");
            return response.data;
        },
        async fetchTools() {
            this.loading = true;
            try {
                const params = {
                    ...this.filters,
                    skip: (this.page - 1) * this.perPage,
                    limit: this.perPage,
                };
                const response = await api.get("/tools", { params });

                if (response.status === 200) {
                    const data = response.data;
                    this.tools = data.tools.map(t => ({
                        ...t,
                        creator_display_name: t.creator_display_name,
                        creator_city: t.creator_city,
                        creator_country: t.creator_country,
                    }));
                    this.total = data.total;
                } else {
                    this.tools = [];
                    this.total = 0;
                }
            } catch (err) {
                console.error("API Fehler:", err);
                this.tools = [];
                this.total = 0;
            } finally {
                this.loading = false;
            }
        },
        changePage(newPage) {
            if (newPage < 1 || newPage > this.totalPages) return;
            this.page = newPage;
            this.fetchTools();
        },
        changePerPage(newPerPage) {
            this.perPage = newPerPage;
            this.page = 1;
            this.fetchTools();
        },
        resetFilters() {
            this.filters = { city: "", zip: "", country: "" };
            this.page = 1;
            this.fetchTools();
        },
        async createTool(tool) {
            try {
                const authStore = useAuthStore();
                const userId = authStore.user_id ?? null;
                if (!userId) throw new Error("Kein eingeloggter User");
                await api.post("/tools", {
                    ...tool,
                    created_by: userId,
                });
                return true
            } catch (err) {
                console.error("Fehler beim Erstellen:", err);
                return false
            }
            return false
        },

    }
});