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

        async requestReturn(transactionId, returnCondition) {
            const formData = new FormData();
            formData.append("return_condition", returnCondition);

            const response = await api.post(`/transactions/${transactionId}/return-request`, formData);
            return response.data;
        },

        async confirmReturn(transactionId, { finalCondition, pictureAfter }) {
            const formData = new FormData();
            formData.append("final_condition", finalCondition);
            formData.append("picture_after", pictureAfter);

            const response = await api.post(`/transactions/${transactionId}/confirm-return`, formData);
            return response.data;
        },

        async createSupportReview(transactionId, { lenderCondition, lenderPicture }) {
            const formData = new FormData();
            formData.append("lender_condition", lenderCondition);
            formData.append("lender_picture", lenderPicture);

            const response = await api.post(`/transaction-reviews/${transactionId}`, formData);
            return response.data;
        },

        async getSupportReviews() {
            const response = await api.get("/transaction-reviews/");
            return response.data;
        },

        async resolveSupportReview(reviewId, { finalCondition, supportNote }) {
            const formData = new FormData();
            formData.append("final_condition", finalCondition);
            if (supportNote?.trim()) {
                formData.append("support_note", supportNote.trim());
            }

            const response = await api.post(`/transaction-reviews/${reviewId}/resolve`, formData);
            return response.data;
        },
    },
});
