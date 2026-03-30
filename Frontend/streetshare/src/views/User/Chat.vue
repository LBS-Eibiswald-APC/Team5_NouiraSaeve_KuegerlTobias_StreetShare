<script setup>
import { computed, nextTick, onBeforeMount, onBeforeUnmount, ref, watch } from "vue";
import { useToast } from "vue-toast-notification";
import { useChatStore } from "@/store/chatStore";
import { useRequestStore } from "@/store/requestStore";
import { useAuthStore } from "@/store/authStore";
import { useTransactionsStore } from "@/store/transactionsStore";
import { useDashboardStore } from "@/store/dashboardStore";
import ConversationsPanel from "@/components/Chat/ConversationsPanel.vue";
import MessagesPanel from "@/components/Chat/MessagesPanel.vue";
import FakePaypalPaymentPopUp from "@/components/PopUp/FakePaypalPaymentPopUp.vue";

const chatStore = useChatStore();
const requestStore = useRequestStore();
const authStore = useAuthStore();
const transactionsStore = useTransactionsStore();
const dashboardStore = useDashboardStore();
const toast = useToast();

const chats = ref([]);
const allRequests = ref([]);
const transactions = ref([]);
const selectedChat = ref(null);
const pendingRequestDraft = ref(null);
const loading = ref(true);
const loadingMessages = ref(false);
const requestSubmitting = ref(false);
const requestActionLoading = ref(false);
const deletingChat = ref(false);
const paymentLoading = ref(false);
const showPaymentModal = ref(false);
const search = ref("");
const draftMessage = ref("");
const connectionStatus = ref("Verbinde...");
const blockedDraftNoticeToolId = ref(null);
let activeConversationRefreshInterval = null;
let conversationsRefreshInterval = null;
let requestsRefreshInterval = null;

function getLocalDateTimeValue(date = new Date()) {
  const pad = (value) => String(value).padStart(2, "0");

  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}`;
}

function addDays(date = new Date(), days = 1) {
  const nextDate = new Date(date);
  nextDate.setDate(nextDate.getDate() + days);
  return nextDate;
}

function buildRequestDraft(baseData = {}) {
  const now = new Date();

  return {
    toolId: Number(baseData.toolId),
    toolName: baseData.toolName || "Tool",
    creatorName: baseData.creatorName || "Unbekannter Nutzer",
    deposit: baseData.deposit ?? null,
    message: "",
    start_date: getLocalDateTimeValue(now),
    end_date: getLocalDateTimeValue(addDays(now, 1)),
  };
}

function getChatTitle(chat) {
  return chat?.tool?.name || chat?.title || "Unbenannter Chat";
}

function getChatPartner(chat) {
  return chat?.user?.display_name || chat?.partner?.display_name || "Unbekannter Nutzer";
}

function getLastMessage(chat) {
  return chat?.last_message || "Noch keine Nachrichten vorhanden.";
}

function getMessages(chat) {
  return chat?.messages || [];
}

function getChatActivity(chat) {
  if (!chat?.last_message_created_at) {
    return "Kein Verlauf";
  }

  return new Date(chat.last_message_created_at).toLocaleString();
}

function getMessageText(message) {
  return message?.message || message?.content || "";
}

function isOwnMessage(message) {
  return Number(message?.sender_id) === Number(authStore.user_id);
}

function getMessageAuthor(message) {
  if (isOwnMessage(message)) {
    return "Du";
  }

  return getChatPartner(selectedChat.value);
}

function isSameChatRequest(chat, request) {
  if (!chat || !request) {
    return false;
  }

  if (request.conversation_id) {
    return Number(request.conversation_id) === Number(chat.id);
  }

  if (!chat.tool_id) {
    return false;
  }

  if (Number(request.tool_id) !== Number(chat.tool_id)) {
    return false;
  }

  const currentUserId = Number(authStore.user_id);
  const chatPartnerId = Number(chat.user_id);
  const participants = [Number(request.borrower_id), Number(request.lender_id)];

  return participants.includes(currentUserId) && participants.includes(chatPartnerId);
}

function getChatRequest(chat) {
  const relevantRequests = allRequests.value
    .filter((request) => isSameChatRequest(chat, request))
    .sort((left, right) => {
      const leftActionable = left.status === "Ausstehend" || left.status === "Gegenangebot" ? 1 : 0;
      const rightActionable = right.status === "Ausstehend" || right.status === "Gegenangebot" ? 1 : 0;

      if (leftActionable !== rightActionable) {
        return rightActionable - leftActionable;
      }

      return new Date(right.created_at || 0) - new Date(left.created_at || 0);
    });

  return relevantRequests[0] || null;
}

function getTransactionForRequest(request) {
  if (!request?.id) {
    return null;
  }

  return transactions.value.find((transaction) => Number(transaction.request_id) === Number(request.id)) || null;
}

const selectedChatRequest = computed(() => {
  if (!selectedChat.value) {
    return null;
  }

  return getChatRequest(selectedChat.value);
});

const visiblePendingRequestDraft = computed(() => {
  const draft = pendingRequestDraft.value;

  if (!draft) {
    return null;
  }

  if (!selectedChat.value) {
    return draft;
  }

  return Number(selectedChat.value.tool_id) === Number(draft.toolId) ? draft : null;
});

const canRespondToSelectedRequest = computed(() => {
  const request = selectedChatRequest.value;

  if (!request) {
    return false;
  }

  return (
    Number(request.to_respond_id) === Number(authStore.user_id) &&
    (request.status === "Ausstehend" || request.status === "Gegenangebot")
  );
});

const canSendMessages = computed(() => {
  return selectedChatRequest.value?.status !== "Abgelehnt";
});

const canDeleteRejectedChat = computed(() => {
  return Boolean(selectedChat.value && selectedChatRequest.value?.status === "Abgelehnt");
});

const selectedTransaction = computed(() => getTransactionForRequest(selectedChatRequest.value));

const canOpenPayment = computed(() => {
  const request = selectedChatRequest.value;

  return Boolean(
    request &&
    Number(request.borrower_id) === Number(authStore.user_id) &&
    request.status === "Akzeptiert" &&
    !request.has_transaction
  );
});

const paymentHint = computed(() => {
  const request = selectedChatRequest.value;
  const transaction = selectedTransaction.value;

  if (!request) {
    return "";
  }

  if (request.status === "Akzeptiert" && Number(request.borrower_id) === Number(authStore.user_id) && !request.has_transaction) {
    return "Die Anfrage wurde akzeptiert. Du musst jetzt zahlen, sonst passiert nichts weiter.";
  }

  if (request.status === "Akzeptiert" && Number(request.lender_id) === Number(authStore.user_id) && !request.has_transaction) {
    return "Die Anfrage ist akzeptiert. Der Leiher muss zuerst zahlen, bevor die Ausleihe starten kann.";
  }

  if (request.status === "Bezahlt" && transaction?.status === "Bezahlt") {
    return "Die Zahlung ist bestätigt. Jetzt darf das Tool ausgeliehen werden.";
  }

  if (transaction?.status === "Rueckgabe ausstehend") {
    return "Die Rückgabe wurde erfasst. Jetzt muss der Leiher mit Foto und finaler Kondition bestätigen.";
  }

  if (transaction?.status === "Abgeschlossen") {
    return "Die Rückgabe ist abgeschlossen. Die Auszahlung wurde bereits berechnet.";
  }

  return "";
});

const filteredChats = computed(() => {
  const query = search.value.trim().toLowerCase();

  if (!query) {
    return chats.value;
  }

  return chats.value.filter((chat) => {
    return [
      getChatTitle(chat),
      getChatPartner(chat),
      getLastMessage(chat),
      getChatRequest(chat)?.status,
    ].some((value) => value?.toLowerCase().includes(query));
  });
});

function clearPendingRequestDraft() {
  pendingRequestDraft.value = null;
  sessionStorage.removeItem("pendingChatRequest");
  dashboardStore.clearChatState();
}

function hydratePendingRequestDraft() {
  if (!dashboardStore.chatState.composeRequest) {
    return;
  }

  const storedDraft = sessionStorage.getItem("pendingChatRequest");
  if (!storedDraft) {
    return;
  }

  try {
    const parsedDraft = JSON.parse(storedDraft);
    const routeToolId = Number(dashboardStore.chatState.toolId || parsedDraft.toolId);

    if (
      pendingRequestDraft.value &&
      Number(pendingRequestDraft.value.toolId) === routeToolId
    ) {
      return;
    }

    pendingRequestDraft.value = buildRequestDraft({
      ...parsedDraft,
      toolId: routeToolId,
    });
    syncPendingRequestDraftState();
  } catch (error) {
    console.error("Failed to read pending request draft:", error);
  }
}

function updateChatPreview(conversationId, message) {
  const chat = chats.value.find((entry) => entry.id === conversationId);
  if (!chat) {
    return;
  }

  chat.last_message = message.content;
  chat.last_message_created_at = message.created_at;

  const existingMessages = chat.messages || [];
  const alreadyExists = existingMessages.some((entry) => entry.id === message.id);
  if (!alreadyExists) {
    chat.messages = [...existingMessages, message];
  }

  chats.value = [
    chat,
    ...chats.value.filter((entry) => entry.id !== conversationId),
  ];

  if (selectedChat.value?.id === conversationId) {
    selectedChat.value = chat;
  }
}

async function scrollToBottom() {
  await nextTick();
  const container = document.querySelector("[data-chat-messages]");
  if (container) {
    container.scrollTop = container.scrollHeight;
  }
}

function mergeChats(nextChats) {
  const existingMessagesByConversation = new Map(
    chats.value.map((chat) => [chat.id, chat.messages || []])
  );

  chats.value = nextChats.map((chat) => ({
    ...chat,
    messages: existingMessagesByConversation.get(chat.id) || chat.messages || [],
  }));

  if (selectedChat.value) {
    selectedChat.value = chats.value.find((entry) => entry.id === selectedChat.value.id) || null;
  }
}

async function refreshConversations() {
  const nextChats = await chatStore.getChats();
  mergeChats(nextChats);
}

async function loadRequests() {
  const [incoming, outgoing] = await Promise.all([
    requestStore.getMe({ limit: 100 }),
    requestStore.getSendedMe({ limit: 100 }),
  ]);

  allRequests.value = [...incoming.requests, ...outgoing.requests];
}

async function loadTransactions() {
  transactions.value = await transactionsStore.getMyTransactions();
}

async function refreshMessages(conversationId, { markRead = false } = {}) {
  const chat = chats.value.find((entry) => entry.id === conversationId);
  if (!chat) {
    return;
  }

  const messages = await chatStore.getMessages(conversationId);
  chat.messages = messages;

  if (markRead) {
    await chatStore.readMessages(conversationId);
  }

  await refreshConversations();
  await loadRequests();
  await loadTransactions();
  await scrollToBottom();
}

function stopRefreshTimers() {
  if (activeConversationRefreshInterval) {
    window.clearInterval(activeConversationRefreshInterval);
    activeConversationRefreshInterval = null;
  }

  if (conversationsRefreshInterval) {
    window.clearInterval(conversationsRefreshInterval);
    conversationsRefreshInterval = null;
  }

  if (requestsRefreshInterval) {
    window.clearInterval(requestsRefreshInterval);
    requestsRefreshInterval = null;
  }
}

function findChatByConversationId(conversationId) {
  return chats.value.find((chat) => chat.id === Number(conversationId)) || null;
}

function findChatByToolId(toolId) {
  return chats.value.find((chat) => chat.tool_id === Number(toolId)) || null;
}

function hasRejectedRequestChatForTool(toolId) {
  const relatedChat = findChatByToolId(toolId);
  if (!relatedChat) {
    return false;
  }

  return allRequests.value.some((request) => {
    return request.status === "Abgelehnt" && isSameChatRequest(relatedChat, request);
  });
}

function syncPendingRequestDraftState() {
  const toolId = Number(pendingRequestDraft.value?.toolId || dashboardStore.chatState.toolId);

  if (!toolId || !hasRejectedRequestChatForTool(toolId)) {
    blockedDraftNoticeToolId.value = null;
    return;
  }

  pendingRequestDraft.value = null;
  sessionStorage.removeItem("pendingChatRequest");

  if (blockedDraftNoticeToolId.value !== toolId) {
    toast.error("Für dieses bereits abgelehnte Tool kannst du keine neue Anfrage starten.", {
      position: "top-right",
    });
    blockedDraftNoticeToolId.value = toolId;
  }
}

async function openConversation(chat) {
  if (!chat) {
    return;
  }

  selectedChat.value = chat;
  loadingMessages.value = true;
  connectionStatus.value = "Verbinde...";
  dashboardStore.openChatConversation(chat.id);

  if (activeConversationRefreshInterval) {
    window.clearInterval(activeConversationRefreshInterval);
    activeConversationRefreshInterval = null;
  }

  try {
    await refreshMessages(chat.id, { markRead: true });

    chatStore.connectToConversation(chat.id, {
      onOpen: async () => {
        connectionStatus.value = "";
        await scrollToBottom();
      },
      onMessage: async (message) => {
        updateChatPreview(chat.id, message);
        await chatStore.readMessages(chat.id);
        await refreshConversations();
        await loadRequests();
        await loadTransactions();
        await scrollToBottom();
      },
      onClose: () => {
        connectionStatus.value = "";
      },
      onError: () => {
        connectionStatus.value = "Verbindungsfehler";
      },
    });

    activeConversationRefreshInterval = window.setInterval(async () => {
      if (selectedChat.value?.id === chat.id) {
        await refreshMessages(chat.id);
      }
    }, 4000);

    await scrollToBottom();
  } catch (error) {
    console.error("Failed to open conversation:", error);
    connectionStatus.value = "Chat konnte nicht geladen werden";
  } finally {
    loadingMessages.value = false;
  }
}

async function restoreConversationFromRoute() {
  const conversationId = dashboardStore.chatState.conversationId;
  if (conversationId) {
    const chat = findChatByConversationId(conversationId);
    if (chat && selectedChat.value?.id !== chat.id) {
      await openConversation(chat);
      return;
    }
  }

  if (dashboardStore.chatState.composeRequest && dashboardStore.chatState.toolId) {
    const chat = findChatByToolId(dashboardStore.chatState.toolId);
    if (chat && selectedChat.value?.id !== chat.id) {
      await openConversation(chat);
    }
  }
}

async function sendCurrentMessage() {
  if (!canSendMessages.value) {
    connectionStatus.value = "Bei einer abgelehnten Anfrage können keine Nachrichten mehr gesendet werden";
    return;
  }

  const content = draftMessage.value.trim();
  if (!content) {
    return;
  }

  try {
    chatStore.sendMessage(content);
    draftMessage.value = "";
  } catch (error) {
    console.error("Failed to send message:", error);
    connectionStatus.value = error?.message || "Nachricht konnte nicht gesendet werden";
  }
}

async function createRequestFromDraft() {
  const draft = pendingRequestDraft.value;

  if (!draft?.toolId) {
    return;
  }

  if (!draft.message?.trim() || !draft.start_date || !draft.end_date) {
    toast.error("Bitte fülle alle Felder für die Anfrage aus.", {
      position: "top-right",
    });
    return;
  }

  if (new Date(draft.end_date) <= new Date(draft.start_date)) {
    toast.error("Das Enddatum muss nach dem Startdatum liegen.", {
      position: "top-right",
    });
    return;
  }

  if (hasRejectedRequestChatForTool(draft.toolId)) {
    syncPendingRequestDraftState();
    return;
  }

  requestSubmitting.value = true;

  try {
    const response = await requestStore.createRequest({
      tool_id: draft.toolId,
      message: draft.message.trim(),
      start_date: draft.start_date,
      end_date: draft.end_date,
    });

    toast.success("Anfrage wurde im Chat erstellt.", {
      position: "top-right",
    });

    await refreshConversations();
    await loadRequests();
    await loadTransactions();

    const conversationId = response.data?.conversation_id;
    clearPendingRequestDraft();

    if (conversationId) {
      const chat = findChatByConversationId(conversationId);
      if (chat) {
        await openConversation(chat);
      }
    }
  } catch (error) {
    toast.error(error.message || "Anfrage konnte nicht erstellt werden.", {
      position: "top-right",
    });
  } finally {
    requestSubmitting.value = false;
  }
}

function closePaymentModal() {
  if (!paymentLoading.value) {
    showPaymentModal.value = false;
  }
}

async function confirmPayment() {
  const request = selectedChatRequest.value;
  if (!request) {
    return;
  }

  paymentLoading.value = true;

  try {
    await requestStore.payRequest(request.id);
    toast.success("Zahlung erfolgreich durchgeführt.", {
      position: "top-right",
    });
    showPaymentModal.value = false;
    await loadRequests();
    await loadTransactions();
  } catch (error) {
    toast.error(error.response?.data?.detail || "Zahlung fehlgeschlagen.", {
      position: "top-right",
    });
  } finally {
    paymentLoading.value = false;
  }
}

async function respondToRequest(action) {
  const request = selectedChatRequest.value;
  if (!request) {
    return;
  }

  requestActionLoading.value = true;

  try {
    if (action === "accept") {
      await requestStore.acceptRequest(request.id);
      toast.success("Anfrage wurde akzeptiert.", {
        position: "top-right",
      });
    } else {
      await requestStore.rejectRequest(request.id);
      toast.success("Anfrage wurde abgelehnt.", {
        position: "top-right",
      });
    }

    await loadRequests();
    await refreshConversations();
  } catch (error) {
    toast.error(error.response?.data?.detail || "Anfrage konnte nicht aktualisiert werden.", {
      position: "top-right",
    });
  } finally {
    requestActionLoading.value = false;
  }
}

async function deleteRejectedChat() {
  if (!selectedChat.value || !canDeleteRejectedChat.value) {
    return;
  }

  deletingChat.value = true;

  try {
    await chatStore.deleteChat(selectedChat.value.id);
    toast.success("Abgelehnter Chat wurde gelöscht.", {
      position: "top-right",
    });

    const deletedChatId = selectedChat.value.id;
    chats.value = chats.value.filter((chat) => chat.id !== deletedChatId);
    selectedChat.value = null;
    draftMessage.value = "";
    connectionStatus.value = chats.value.length === 0 ? "Keine Chats vorhanden" : "";

    dashboardStore.clearChatState();
  } catch (error) {
    toast.error(error.response?.data?.detail || "Chat konnte nicht gelöscht werden.", {
      position: "top-right",
    });
  } finally {
    deletingChat.value = false;
  }
}

onBeforeMount(async () => {
  try {
    hydratePendingRequestDraft();
    await Promise.all([
      refreshConversations(),
      loadRequests(),
      loadTransactions(),
    ]);
    syncPendingRequestDraftState();
    await restoreConversationFromRoute();

    if (chats.value.length === 0 && !pendingRequestDraft.value) {
      connectionStatus.value = "Keine Chats vorhanden";
    }

    conversationsRefreshInterval = window.setInterval(async () => {
      await refreshConversations();
    }, 8000);

    requestsRefreshInterval = window.setInterval(async () => {
      await loadRequests();
    }, 8000);
  } finally {
    loading.value = false;
  }
});

onBeforeUnmount(() => {
  stopRefreshTimers();
  chatStore.disconnectSocket();
});

watch(
  () => selectedChat.value?.id,
  async () => {
    await scrollToBottom();
  }
);

watch(
  () => [dashboardStore.chatState.composeRequest, dashboardStore.chatState.toolId, dashboardStore.chatState.conversationId],
  async () => {
    hydratePendingRequestDraft();
    syncPendingRequestDraftState();
    await restoreConversationFromRoute();
  }
);
</script>

<template>
  <div class="grid h-[calc(100vh-9rem)] min-h-0 gap-6 lg:h-[calc(100vh-7rem)] lg:grid-cols-[340px_minmax(0,1fr)]">
    <ConversationsPanel
      :loading="loading"
      :search="search"
      :filtered-chats="filteredChats"
      :selected-chat-id="selectedChat?.id ?? null"
      :get-chat-title="getChatTitle"
      :get-chat-partner="getChatPartner"
      :get-chat-activity="getChatActivity"
      :get-last-message="getLastMessage"
      @update:search="search = $event"
      @select="openConversation"
    />

    <MessagesPanel
      :selected-chat="selectedChat"
      :loading-messages="loadingMessages"
      :connection-status="connectionStatus"
      :draft-message="draftMessage"
      :request-draft="visiblePendingRequestDraft"
      :request-submitting="requestSubmitting"
      :selected-request="selectedChatRequest"
      :can-respond-to-request="canRespondToSelectedRequest"
      :request-action-loading="requestActionLoading"
      :deleting-chat="deletingChat"
      :can-send-messages="canSendMessages"
      :can-delete-rejected-chat="canDeleteRejectedChat"
      :selected-transaction="selectedTransaction"
      :payment-hint="paymentHint"
      :can-open-payment="canOpenPayment"
      :payment-loading="paymentLoading"
      :get-chat-title="getChatTitle"
      :get-chat-partner="getChatPartner"
      :get-messages="getMessages"
      :is-own-message="isOwnMessage"
      :get-message-author="getMessageAuthor"
      :get-message-text="getMessageText"
      @update:draft-message="draftMessage = $event"
      @update:request-draft="pendingRequestDraft = $event"
      @send="sendCurrentMessage"
      @create-request="createRequestFromDraft"
      @accept-request="respondToRequest('accept')"
      @reject-request="respondToRequest('reject')"
      @delete-chat="deleteRejectedChat"
      @open-payment="showPaymentModal = true"
      @cancel-request-draft="clearPendingRequestDraft"
    />

    <FakePaypalPaymentPopUp
      :show-modal="showPaymentModal"
      :amount="selectedChatRequest?.tool_deposit || 0"
      :tool-name="selectedChatRequest?.tool_name || getChatTitle(selectedChat)"
      :loading="paymentLoading"
      @close="closePaymentModal"
      @confirm="confirmPayment"
    />
  </div>
</template>
