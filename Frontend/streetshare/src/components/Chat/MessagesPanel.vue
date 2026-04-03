<script setup>
import { ref } from "vue";
import {
  BIconList,
  BIconChatDots,
  BIconCheck,
  BIconCheck2All,
  BIconXCircle,
  BIconCheckCircle,
} from "bootstrap-icons-vue";

const props = defineProps({
  selectedChat: {
    type: Object,
    default: null,
  },
  loadingMessages: {
    type: Boolean,
    default: false,
  },
  connectionStatus: {
    type: String,
    default: "",
  },
  draftMessage: {
    type: String,
    default: "",
  },
  requestDraft: {
    type: Object,
    default: null,
  },
  requestSubmitting: {
    type: Boolean,
    default: false,
  },
  selectedRequest: {
    type: Object,
    default: null,
  },
  canRespondToRequest: {
    type: Boolean,
    default: false,
  },
  requestActionLoading: {
    type: Boolean,
    default: false,
  },
  deletingChat: {
    type: Boolean,
    default: false,
  },
  canSendMessages: {
    type: Boolean,
    default: true,
  },
  canDeleteRejectedChat: {
    type: Boolean,
    default: false,
  },
  selectedTransaction: {
    type: Object,
    default: null,
  },
  paymentHint: {
    type: String,
    default: "",
  },
  canOpenPayment: {
    type: Boolean,
    default: false,
  },
  paymentLoading: {
    type: Boolean,
    default: false,
  },
  showConversationsToggle: {
    type: Boolean,
    default: false,
  },
  getChatTitle: {
    type: Function,
    required: true,
  },
  getChatPartner: {
    type: Function,
    required: true,
  },
  getMessages: {
    type: Function,
    required: true,
  },
  isOwnMessage: {
    type: Function,
    required: true,
  },
  getMessageAuthor: {
    type: Function,
    required: true,
  },
  getMessageText: {
    type: Function,
    required: true,
  },
});

const emit = defineEmits([
  "update:draftMessage",
  "update:requestDraft",
  "send",
  "create-request",
  "accept-request",
  "reject-request",
  "delete-chat",
  "open-payment",
  "cancel-request-draft",
  "toggle-conversations",
]);

const startDateInput = ref(null);
const endDateInput = ref(null);
function parseBackendDate(value) {
  if (!value) {
    return null;
  }

  if (value instanceof Date) {
    return value;
  }

  const normalizedValue =
    typeof value === "string"
      ? value.replace(" ", "T")
      : value;

  const date = new Date(normalizedValue);
  return Number.isNaN(date.getTime()) ? null : date;
}

function formatMessageTimestamp(value) {
  if (!value) {
    return "";
  }

  const date = parseBackendDate(value);
  if (!date) {
    return "";
  }

  const now = new Date();
  const isSameDay =
    date.getDate() === now.getDate() &&
    date.getMonth() === now.getMonth() &&
    date.getFullYear() === now.getFullYear();

  if (isSameDay) {
    return date.toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
  }

  return date.toLocaleString([], {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function getRequestStatusClass(status) {
  if (status === "Akzeptiert") {
    return "bg-emerald-100 text-emerald-700 dark:bg-emerald-500/15 dark:text-emerald-300";
  }

  if (status === "Abgelehnt") {
    return "bg-red-100 text-red-700 dark:bg-red-500/15 dark:text-red-300";
  }

  if (status === "Bezahlt") {
    return "bg-sky-100 text-sky-700 dark:bg-sky-500/15 dark:text-sky-300";
  }

  if (status === "Gegenangebot") {
    return "bg-blue-100 text-blue-700 dark:bg-blue-500/15 dark:text-blue-300";
  }

  return "bg-amber-100 text-amber-700 dark:bg-amber-500/15 dark:text-amber-300";
}

function formatDateTimeLocal(value) {
  if (!value) {
    return "-";
  }

  const date = parseBackendDate(value);
  if (!date) {
    return "-";
  }

  return date.toLocaleString([], {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function updateRequestDraft(field, value) {
  if (!props.requestDraft) {
    return;
  }

  emit("update:requestDraft", {
    ...props.requestDraft,
    [field]: value,
  });
}

function openDatePicker(inputRef) {
  const input = inputRef === "start" ? startDateInput.value : endDateInput.value;
  if (!input) {
    return;
  }

  if (typeof input.showPicker === "function") {
    input.showPicker();
    return;
  }

  input.focus();
}

function isReturnedEarly() {
  if (!props.selectedTransaction?.return_requested_at || !props.selectedRequest?.end_date) {
    return false;
  }

  const returnRequestedAt = parseBackendDate(props.selectedTransaction.return_requested_at);
  const requestEndDate = parseBackendDate(props.selectedRequest.end_date);

  if (!returnRequestedAt || !requestEndDate) {
    return false;
  }

  return returnRequestedAt < requestEndDate;
}
</script>

<template>
  <section class="flex h-full min-h-0 max-h-[110vh] flex-col overflow-hidden border-t border-neutral-200 bg-white dark:border-neutral-800 dark:bg-neutral-900 lg:max-h-none lg:border-l lg:border-t-0">
    <div
      v-if="selectedChat || requestDraft"
      class="flex h-full min-h-0 flex-col"
    >
      <!-- Header -->
      <div class="flex items-center justify-between border-b border-neutral-200 px-6 py-5 dark:border-neutral-800">
        <div class="flex items-start gap-3">
          <button
            v-if="showConversationsToggle"
            type="button"
            class="inline-flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl border border-neutral-200 text-neutral-700 transition hover:bg-neutral-100 dark:border-neutral-700 dark:text-white dark:hover:bg-neutral-800"
            @click="emit('toggle-conversations')"
          >
            <BIconList class="text-lg" />
          </button>

          <div>
            <h2 class="mt-1 text-2xl font-bold tracking-tight text-neutral-900 dark:text-white">
              {{ selectedChat ? getChatTitle(selectedChat) : requestDraft?.toolName || "Neue Anfrage" }}
            </h2>
            <p class="mt-1 text-sm text-neutral-500 dark:text-neutral-400">
              {{ selectedChat ? getChatPartner(selectedChat) : requestDraft?.creatorName || "Unbekannter Nutzer" }}
            </p>
            <p
              v-if="connectionStatus"
              class="mt-1 text-xs font-medium text-neutral-400 dark:text-neutral-500"
            >
              {{ connectionStatus }}
            </p>
          </div>
        </div>
      </div>
      <!-- Request -->
      <div data-chat-messages class="min-h-0 flex-1 space-y-4 overflow-y-auto overscroll-contain bg-neutral-50 px-4 py-5 sm:px-6 sm:py-6 dark:bg-neutral-950/60">
        <div
          v-if="requestDraft"
          class="rounded-3xl border border-lime-200 bg-white p-5 shadow-sm dark:border-lime-500/20 dark:bg-neutral-900"
        >
          <div class="flex items-start justify-between gap-4">
            <div>
              <p class="text-xs font-semibold uppercase tracking-[0.16em] text-lime-500">
                Anfrage starten
              </p>
              <h3 class="mt-1 text-lg font-semibold text-neutral-900 dark:text-white">
                {{ requestDraft.toolName }}
              </h3>
              <p class="mt-2 text-sm leading-6 text-neutral-500 dark:text-neutral-400">
                Deine Anfrage wird direkt als Chat gestartet. Die erste Nachricht erscheint gleich hier in der Unterhaltung.
              </p>
            </div>

            <button
              type="button"
              class="rounded-2xl border border-neutral-200 px-3 py-2 text-sm font-medium text-neutral-600 transition hover:bg-neutral-100 dark:border-neutral-700 dark:text-neutral-300 dark:hover:bg-neutral-800"
              @click="emit('cancel-request-draft')"
            >
              Abbrechen
            </button>
          </div>

          <div class="mt-5 grid gap-4 md:grid-cols-2">
            <label class="block">
              <span class="mb-2 block text-sm font-medium text-neutral-700 dark:text-neutral-300">Von</span>
              <div class="relative cursor-pointer" @click="openDatePicker('start')">
                <input
                  ref="startDateInput"
                  :value="requestDraft.start_date"
                  type="datetime-local"
                  class="w-full rounded-2xl border border-neutral-300 bg-white px-4 py-3 text-neutral-900 focus:outline-none focus:ring-2 focus:ring-lime-400 dark:border-neutral-700 dark:bg-neutral-950 dark:text-white"
                  @input="updateRequestDraft('start_date', $event.target.value)"
                />
              </div>
            </label>

            <label class="block">
              <span class="mb-2 block text-sm font-medium text-neutral-700 dark:text-neutral-300">Bis</span>
              <div class="relative cursor-pointer" @click="openDatePicker('end')">
                <input
                  ref="endDateInput"
                  :value="requestDraft.end_date"
                  :min="requestDraft.start_date"
                  type="datetime-local"
                  class="w-full rounded-2xl border border-neutral-300 bg-white px-4 py-3 text-neutral-900 focus:outline-none focus:ring-2 focus:ring-lime-400 dark:border-neutral-700 dark:bg-neutral-950 dark:text-white"
                  @input="updateRequestDraft('end_date', $event.target.value)"
                />
              </div>
            </label>
          </div>

          <label class="mt-4 block">
            <span class="mb-2 block text-sm font-medium text-neutral-700 dark:text-neutral-300">Nachricht</span>
            <textarea
              :value="requestDraft.message"
              rows="4"
              placeholder="Schreibe deine Anfrage..."
              class="w-full rounded-2xl border border-neutral-300 bg-white px-4 py-3 text-neutral-900 placeholder:text-neutral-400 focus:outline-none focus:ring-2 focus:ring-lime-400 dark:border-neutral-700 dark:bg-neutral-950 dark:text-white dark:placeholder:text-neutral-500"
              @input="updateRequestDraft('message', $event.target.value)"
            ></textarea>
          </label>

          <div class="mt-4 flex justify-end">
            <button
              type="button"
              class="rounded-2xl bg-lime-500 px-5 py-3 font-semibold text-black transition hover:bg-lime-400 disabled:cursor-not-allowed disabled:opacity-60"
              :disabled="requestSubmitting"
              @click="emit('create-request')"
            >
              {{ requestSubmitting ? "Wird gesendet..." : "Anfrage im Chat senden" }}
            </button>
          </div>
        </div>
        <div
          v-if="selectedRequest"
          class="rounded-3xl border border-neutral-200 bg-white p-5 shadow-sm dark:border-neutral-800 dark:bg-neutral-900"
        >
          <div class="flex flex-wrap items-center justify-between gap-3">
            <div>
              <p class="text-xs font-semibold uppercase tracking-[0.16em] text-lime-500">
                Anfrage
              </p>
              <h3 class="mt-1 text-lg font-semibold text-neutral-900 dark:text-white">
                {{ selectedRequest.tool_name }}
              </h3>
            </div>

            <span
              :class="getRequestStatusClass(selectedRequest.status)"
              class="inline-flex rounded-full px-3 py-1 text-xs font-semibold"
            >
              {{ selectedRequest.status }}
            </span>
          </div>

          <div class="mt-4 grid gap-4 md:grid-cols-2">
            <div class="rounded-2xl bg-neutral-50 px-4 py-3 dark:bg-neutral-950">
              <p class="text-xs font-semibold uppercase tracking-[0.12em] text-neutral-500 dark:text-neutral-400">
                Zeitraum
              </p>
              <p class="mt-2 text-sm leading-6 text-neutral-700 dark:text-neutral-300">
                {{ formatDateTimeLocal(selectedRequest.start_date) }}<br>
                bis {{ formatDateTimeLocal(selectedRequest.end_date) }}
              </p>
            </div>

            <div class="rounded-2xl bg-neutral-50 px-4 py-3 dark:bg-neutral-950">
              <p class="text-xs font-semibold uppercase tracking-[0.12em] text-neutral-500 dark:text-neutral-400">
                Nachricht
              </p>
              <p class="mt-2 text-sm leading-6 text-neutral-700 dark:text-neutral-300">
                {{ selectedRequest.message || "Keine Nachricht vorhanden." }}
              </p>
            </div>
          </div>

          <div
            v-if="paymentHint"
            class="mt-4 rounded-2xl border border-sky-200 bg-sky-50 px-4 py-3 text-sm leading-6 text-sky-800 dark:border-sky-500/20 dark:bg-sky-500/10 dark:text-sky-200"
          >
            {{ paymentHint }}
          </div>

          <div
            v-if="selectedTransaction?.return_requested_at"
            class="mt-4 rounded-2xl border border-lime-200 bg-lime-50 px-4 py-3 text-sm leading-6 text-lime-900 dark:border-lime-500/20 dark:bg-lime-500/10 dark:text-lime-100"
          >
            <span v-if="isReturnedEarly()">
              FrÃ¼hzeitig zurÃ¼ckgegeben am {{ formatDateTimeLocal(selectedTransaction.return_requested_at) }}.
            </span>
            <span v-else>
              RÃ¼ckgabe erfasst am {{ formatDateTimeLocal(selectedTransaction.return_requested_at) }}.
            </span>
          </div>

          <div
            v-if="canRespondToRequest"
            class="mt-4 flex flex-wrap justify-end gap-3"
          >
            <button
              type="button"
              class="inline-flex items-center gap-2 rounded-2xl bg-lime-500 px-4 py-3 font-semibold text-black transition hover:bg-lime-400 disabled:cursor-not-allowed disabled:opacity-60"
              :disabled="requestActionLoading"
              @click="emit('accept-request')"
            >
              <BIconCheckCircle />
              Akzeptieren
            </button>
            <button
              type="button"
              class="inline-flex items-center gap-2 rounded-2xl bg-red-500/90 px-4 py-3 font-semibold text-white transition hover:bg-red-500 disabled:cursor-not-allowed disabled:opacity-60"
              :disabled="requestActionLoading"
              @click="emit('reject-request')"
            >
              <BIconXCircle />
              Ablehnen
            </button>
          </div>

          <div
            v-else-if="canOpenPayment"
            class="mt-4 flex flex-wrap justify-end gap-3"
          >
            <button
              type="button"
              class="inline-flex items-center gap-2 rounded-2xl bg-sky-500 px-4 py-3 font-semibold text-white transition hover:bg-sky-400 disabled:cursor-not-allowed disabled:opacity-60"
              :disabled="paymentLoading"
              @click="emit('open-payment')"
            >
              {{ paymentLoading ? "Zahlung lÃ¤uft..." : "Jetzt bezahlen" }}
            </button>
          </div>

          <div
            v-else-if="canDeleteRejectedChat"
            class="mt-4 flex flex-wrap justify-end gap-3"
          >
            <button
              type="button"
              class="inline-flex items-center gap-2 rounded-2xl border border-neutral-300 px-4 py-3 font-semibold text-neutral-800 transition hover:bg-neutral-100 disabled:cursor-not-allowed disabled:opacity-60 dark:border-neutral-700 dark:text-white dark:hover:bg-neutral-800"
              :disabled="deletingChat"
              @click="emit('delete-chat')"
            >
              {{ deletingChat ? "LÃ¶scht..." : "Chat lÃ¶schen" }}
            </button>
          </div>
        </div>

        <div v-if="loadingMessages" class="space-y-3">
          <div
            v-for="index in 3"
            :key="index"
            class="h-20 animate-pulse rounded-3xl bg-white dark:bg-neutral-900"
          ></div>
        </div>

        <div v-else-if="selectedChat && getMessages(selectedChat).length === 0" class="flex h-full min-h-[240px] items-center justify-center">
          <div class="max-w-md rounded-3xl border border-dashed border-neutral-300 bg-white px-8 py-10 text-center dark:border-neutral-700 dark:bg-neutral-900">
            <p class="text-lg font-semibold text-neutral-900 dark:text-white">
              Noch keine Nachrichten
            </p>
            <p class="mt-2 text-sm leading-6 text-neutral-500 dark:text-neutral-400">
              Starte die Unterhaltung, um Details zu Anfrage, Abholung oder RÃ¼ckgabe zu klÃ¤ren.
            </p>
          </div>
        </div>
        <!-- Messages -->
        <template v-else-if="selectedChat">
          <div
            v-for="message in getMessages(selectedChat)"
            :key="message.id"
            :class="isOwnMessage(message) ? 'ml-auto bg-neutral-950 text-white dark:bg-white dark:text-black' : 'mr-auto bg-white text-neutral-900 dark:bg-neutral-900 dark:text-white'"
            class="max-w-xl rounded-3xl border border-neutral-200 px-4 py-2 shadow-sm dark:border-neutral-800"
          >
            <div class="flex items-start justify-between gap-4">
              <p
                :class="isOwnMessage(message) ? 'text-lime-300 dark:text-lime-600' : 'text-lime-500'"
                class="text-xs font-semibold uppercase tracking-[0.16em]"
              >
                {{ getMessageAuthor(message) }}
              </p>
              <span
                :class="isOwnMessage(message) ? 'text-white/70 dark:text-black/60' : 'text-neutral-400 dark:text-neutral-500'"
                class="shrink-0 text-[11px] font-medium"
              >
                {{ formatMessageTimestamp(message.created_at) }}
              </span>
            </div>
            <p
              :class="isOwnMessage(message) ? 'text-white dark:text-black' : 'text-neutral-700 dark:text-neutral-300'"
              class="mt-2 mb-1 whitespace-pre-wrap text-sm leading-7"
            >
              {{ getMessageText(message) }}
            </p>
            <div
              v-if="isOwnMessage(message)"
              class="flex justify-end"
            >
              <span
                :class="message.is_read ? 'text-sky-400 dark:text-sky-500' : 'text-white/70 dark:text-black/60'"
                class="inline-flex items-center"
              >
                <BIconCheck v-if="!message.is_read" class="text-sm" />
                <BIconCheck2All v-else class="text-sm" />
              </span>
            </div>
          </div>
        </template>
      </div>

      <div
        v-if="selectedChat"
        class="border-t border-neutral-200 bg-white px-4 py-4 sm:px-6 sm:py-5 dark:border-neutral-800 dark:bg-neutral-900"
      >
        <div class="flex items-end gap-3">
          <textarea
            :value="draftMessage"
            rows="3"
            :placeholder="canSendMessages ? 'Nachricht schreiben...' : 'Bei einer abgelehnten Anfrage sind keine weiteren Nachrichten mÃ¶glich.'"
            class="min-h-[84px] flex-1 resize-none rounded-2xl border border-neutral-200 bg-neutral-50 px-4 py-3 text-sm text-neutral-700 placeholder:text-neutral-400 focus:outline-none focus:ring-2 focus:ring-lime-400 dark:border-neutral-700 dark:bg-neutral-950 dark:text-white dark:placeholder:text-neutral-500"
            :disabled="!canSendMessages"
            @input="emit('update:draftMessage', $event.target.value)"
            @keydown.enter.exact.prevent="emit('send')"
          ></textarea>
          <button
            type="button"
            class="rounded-2xl bg-neutral-950 px-5 py-3 font-semibold text-white transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-60 dark:bg-white dark:text-black"
            :disabled="!canSendMessages || !draftMessage.trim()"
            @click="emit('send')"
          >
            Senden
          </button>
        </div>
      </div>
    </div>

    <div v-else class="flex h-full min-h-0 flex-col items-center justify-center px-6 text-center">
      <button
        v-if="showConversationsToggle"
        type="button"
        class="mb-6 inline-flex items-center gap-2 rounded-2xl border border-neutral-200 bg-white px-4 py-3 text-sm font-semibold text-neutral-700 transition hover:bg-neutral-100 dark:border-neutral-700 dark:bg-neutral-900 dark:text-white dark:hover:bg-neutral-800"
        @click="emit('toggle-conversations')"
      >
        <BIconList />
        Chats anzeigen
      </button>

      <div class="flex h-20 w-20 items-center justify-center rounded-[28px] bg-neutral-100 dark:bg-neutral-800">
        <BIconChatDots class="text-3xl text-neutral-500 dark:text-neutral-300" />
      </div>
      <h3 class="mt-6 text-2xl font-bold tracking-tight text-neutral-900 dark:text-white">
        WÃ¤hle einen Chat aus
      </h3>
      <p class="mt-3 max-w-md text-sm leading-7 text-neutral-500 dark:text-neutral-400">
        Sobald du links eine Konversation auswÃ¤hlst, erscheinen hier Nachrichten, Details und Aktionen.
      </p>
    </div>
  </section>
</template>


