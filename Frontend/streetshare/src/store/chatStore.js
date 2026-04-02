import { defineStore } from "pinia";
import api from "@/services/api";

function getWebSocketBaseUrl() {
    const apiUrl = new URL(api.defaults.baseURL);
    apiUrl.protocol = apiUrl.protocol === "https:" ? "wss:" : "ws:";
    return apiUrl.origin;
}

export const useChatStore = defineStore("chat", {
    state: () => ({
        socket: null,
        connectedConversationId: null,
    }),
    actions: {
        async getChats() {
            const response = await api.get("/conversation/chats");
            return response.data;
        },

        async getMessages(conversationId) {
            const response = await api.get(`/messages/conversation/${conversationId}`);
            return response.data;
        },

        async readMessages(conversationId) {
            const response = await api.put(`/messages/read/conversation/${conversationId}`);
            return response.data;
        },

        async deleteChat(conversationId) {
            return await api.delete(`/conversation/${conversationId}`);
        },

        connectToConversation(conversationId, { onMessage, onOpen, onClose, onError } = {}) {
            this.disconnectSocket();

            const socket = new WebSocket(`${getWebSocketBaseUrl()}/messages/ws/${conversationId}`);

            socket.onopen = (event) => {
                this.socket = socket;
                this.connectedConversationId = conversationId;
                onOpen?.(event);
            };

            socket.onmessage = (event) => {
                try {
                    const parsed = JSON.parse(event.data);
                    onMessage?.(parsed);
                } catch (error) {
                    console.error("Failed to parse websocket message:", error);
                }
            };

            socket.onerror = (event) => {
                onError?.(event);
            };

            socket.onclose = (event) => {
                if (this.socket === socket) {
                    this.socket = null;
                    this.connectedConversationId = null;
                }
                onClose?.(event);
            };

            this.socket = socket;
            this.connectedConversationId = conversationId;
            return socket;
        },

        disconnectSocket() {
            if (this.socket) {
                this.socket.close();
            }
            this.socket = null;
            this.connectedConversationId = null;
        },

        sendMessage(content) {
            if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
                throw new Error("Chat connection is not active.");
            }

            this.socket.send(JSON.stringify({ content }));
        },
    },
});
