import { defineStore } from "pinia";
import api from "@/services/api";

export const useTransactionsStore = defineStore("transactionsStore", {
    state: () => ({}),

    actions: {
        async getMyTransactions() {
            try {
                const response = await api.get("/transactions/me");
                return response.data;
            } catch (error) {
                console.error("Fehler beim Laden der eigenen Transactions:", error);
                return [];
            }
        },

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
