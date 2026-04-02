import { defineStore } from "pinia";
import api from "@/services/api";

export const useTransactionsStore = defineStore("transactionsStore", {
    state: () => ({}),

    actions: {
        async getTransactionsByToolId(tool_id) {
            try {
                const response = await api.get(`/transactions/tool/${tool_id}`);
                return response.data;
            } catch (error) {
                console.error("Fehler beim Laden der Transactions:", error);
                return [];
            }
        },
    },
});