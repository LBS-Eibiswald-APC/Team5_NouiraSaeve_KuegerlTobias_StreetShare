import {defineStore} from "pinia";
import api from "@/services/api";

export const useToolsStore = defineStore("tools", {
    state: () => ({
        tools: [],
        filters: {city: "", zip: "", country: ""},
        loading: false,
        countries: ["Österreich", "Deutschland", "Schweiz", "Italien", "Frankreich"],
    }),
    actions: {
        async fetchTools() {
            this.loading = true;
            try {
                const response = await api.get("/tools", {params: this.filters});
                if (response.status === 200) {
                    this.tools = response.data.map(t => ({
                        ...t,
                        creator_display_name: t.creator_display_name ?? "N/A",
                        creator_city: t.creator_city ?? "Unbekannt",
                        creator_country: t.creator_country ?? "",
                    }));
                } else {
                    this.tools = [];
                }
            } catch (err) {
                console.error("API Fehler:", err);
                this.tools = [];
            } finally {
                this.loading = false;
            }
        },
    },
});