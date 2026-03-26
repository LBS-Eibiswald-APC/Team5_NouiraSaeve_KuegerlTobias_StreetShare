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
            "Bezahlt":
                "bg-sky-100 text-sky-700 border border-sky-200 dark:bg-sky-500/15 dark:text-sky-300 dark:border-sky-500/20",
            "Gegenangebot":
                "bg-blue-100 text-blue-700 border border-blue-200 dark:bg-blue-500/15 dark:text-blue-300 dark:border-blue-500/20",
        },
    }),

    getters: {
        getStates: (state) => state.states,
    },

    actions: {
        async getMe(params = {}) {
            const response = await api.get("/requests/me", { params });
            return response.data;
        },

        async getSendedMe(params = {}) {
            const response = await api.get("/requests/sending/me", { params });
            return response.data;
        },

        async createRequest(payload) {
            try {
                return await api.post("/requests/", payload);
            } catch (error) {
                const detail = error.response?.data?.detail;
                throw new Error(detail);
            }
        },
        async updateRequest(id, request) {
            return await api.put(`/requests/${id}`, request);
        },
        async acceptRequest(id) {
            return await api.put(`/requests/accept/${id}`);
        },
        async rejectRequest(id) {
            return await api.put(`/requests/reject/${id}`);
        },
        async payRequest(id) {
            return await api.post(`/transactions/pay-request/${id}`);
        },
    },
});
