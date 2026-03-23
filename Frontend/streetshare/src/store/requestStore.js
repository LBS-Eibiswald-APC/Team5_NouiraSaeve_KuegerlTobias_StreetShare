import { defineStore } from "pinia";
import api from "@/services/api";

export const useRequestStore = defineStore("request", {
    state: () => ({
        states: {
            "Ausstehend":
                "bg-amber-100 text-amber-700 border border-amber-200 dark:bg-amber-500/15 dark:text-amber-300 dark:border-amber-500/20",
            "Abgelehnt":
                "bg-red-100 text-red-700 border border-red-200 dark:bg-red-500/15 dark:text-red-300 dark:border-red-500/20",
            "Akzeptiert":
                "bg-emerald-100 text-emerald-700 border border-emerald-200 dark:bg-emerald-500/15 dark:text-emerald-300 dark:border-emerald-500/20",
        },
    }),

    getters: {
        getStates: (state) => state.states,
    },

    actions: {
        async getMe() {
            const response = await api.get("/requests/me");
            return response.data;
        },

        async getSendedMe() {
            const response = await api.get("/requests/sending/me");
            return response.data;
        },

        async createRequest(request) {
            return await api.post("/requests/", request);
        },
    },
});