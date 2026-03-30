import { defineStore } from "pinia";
import api from "@/services/api";
import { useAuthStore } from "@/store/authStore.js";

export const useToolsStore = defineStore("tools", {
    state: () => ({
        tools: [],
        loading: false,
        filters: {
            name: "",
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
        async getToolImage(tool_id) {
            try {
                const response = await api.get(`/tools/image/${tool_id}`, {
                    responseType: "blob",
                });
                return response.data;
            } catch (error) {
                console.log(error);
                return null
            }
        },
        async fetchTools() {
            this.loading = true;

            try {
                const params = {
                    skip: (this.page - 1) * this.perPage,
                    limit: this.perPage,
                };

                if (this.filters.name?.trim()) params.name = this.filters.name.trim();
                if (this.filters.city?.trim()) params.city = this.filters.city.trim();
                if (this.filters.zip?.trim()) params.zip = this.filters.zip.trim();
                if (this.filters.country?.trim()) params.country = this.filters.country.trim();

                const response = await api.get("/tools", { params });

                if (response.status === 200) {
                    const data = response.data;
                    this.tools = data.tools.map((t) => ({
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
            this.perPage = Number(newPerPage);
            this.page = 1;
            this.fetchTools();
        },

        resetFilters() {
            this.filters = {
                name: "",
                city: "",
                zip: "",
                country: "",
            };
            this.page = 1;
            this.fetchTools();
        },
        async createTool(tool) {
            try {
                const formData = new FormData();
                formData.append("name", tool.name);
                formData.append("description", tool.description ?? "");
                formData.append("base_price", String(tool.base_price));
                formData.append("tool_condition", tool.tool_condition);

                if (tool.tool_image) {
                    formData.append("tool_image", tool.tool_image);
                }

                await api.post("/tools/", formData);
                return true;
            } catch (err) {
                console.error("Fehler beim Erstellen:", err.response?.data || err);
                return false;
            }
        },
        async editTool(tool) {
            try {
                const formData = new FormData();
                formData.append("name", tool.name);
                formData.append("description", tool.description ?? "");
                formData.append("base_price", String(tool.base_price));
                formData.append("tool_condition", tool.tool_condition);

                if (tool.tool_image) {
                    formData.append("tool_image", tool.tool_image);
                }

                await api.put(`/tools/${tool.id}`, formData);

                return true;
            } catch (e) {
                console.log(e.response?.data || e);
                return false;
            }
        },

        async deleteTool(tool_id) {
            try {
                return await api.delete(`/tools/${tool_id}`);
            } catch (e) {
                console.log(e);
            }
        },
        async calculateDeposit(basePrice, toolCondition) {
            if (!basePrice || basePrice <= 0 || !toolCondition) {
                return 0;
            }

            try {
                const response = await api.get("/tools/calculate-deposit", {
                    params: {
                        base_price: basePrice,
                        tool_condition: toolCondition,
                    },
                });
                return response.data.deposit ?? 0;
            } catch (error) {
                console.error("Fehler beim Berechnen des Pfands:", error);
                return 0;
            }
        },
    },
});
