import { defineStore } from "pinia";

const ACTIVE_TAB_KEY = "dashboardActiveTab";
const CHAT_STATE_KEY = "dashboardChatState";

function readActiveTab() {
  return localStorage.getItem(ACTIVE_TAB_KEY) || "entries";
}

function readChatState() {
  const rawValue = sessionStorage.getItem(CHAT_STATE_KEY);
  if (!rawValue) {
    return {
      conversationId: null,
      toolId: null,
      composeRequest: false,
    };
  }

  try {
    const parsed = JSON.parse(rawValue);
    return {
      conversationId: parsed.conversationId ? Number(parsed.conversationId) : null,
      toolId: parsed.toolId ? Number(parsed.toolId) : null,
      composeRequest: parsed.composeRequest === true,
    };
  } catch {
    return {
      conversationId: null,
      toolId: null,
      composeRequest: false,
    };
  }
}

export const useDashboardStore = defineStore("dashboard", {
  state: () => ({
    activeTab: readActiveTab(),
    chatState: readChatState(),
  }),

  actions: {
    setActiveTab(tab) {
      this.activeTab = tab;
      localStorage.setItem(ACTIVE_TAB_KEY, tab);
    },

    openChatConversation(conversationId) {
      this.chatState = {
        conversationId: Number(conversationId),
        toolId: null,
        composeRequest: false,
      };
      sessionStorage.setItem(CHAT_STATE_KEY, JSON.stringify(this.chatState));
      this.setActiveTab("chat");
    },

    startChatRequest(toolId) {
      this.chatState = {
        conversationId: null,
        toolId: Number(toolId),
        composeRequest: true,
      };
      sessionStorage.setItem(CHAT_STATE_KEY, JSON.stringify(this.chatState));
      this.setActiveTab("chat");
    },

    clearChatState() {
      this.chatState = {
        conversationId: null,
        toolId: null,
        composeRequest: false,
      };
      sessionStorage.removeItem(CHAT_STATE_KEY);
    },
  },
});
