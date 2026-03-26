<script setup>
import {computed, onMounted, ref, watch} from "vue";
import {useToast} from "vue-toast-notification";
import ConfirmationPopUp from "@/components/PopUp/ConfirmationPopUp.vue";
import FakePaypalPaymentPopUp from "@/components/PopUp/FakePaypalPaymentPopUp.vue";
import {useRequestStore} from "@/store/requestStore.js";

const requestStore = useRequestStore();
const toast = useToast();
const requests = ref([]);
const total = ref(0);
const loading = ref(false);
const showModal = ref(false);
const showMessageModal = ref(false);
const showPaymentModal = ref(false);
const paymentLoading = ref(false);
const selectedRequest = ref(null);
const filters = ref({
  search: "",
  status: "",
});
const page = ref(1);
const perPage = ref(10);

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / perPage.value)));
const hasActiveFilters = computed(() => Boolean(filters.value.search.trim() || filters.value.status));

async function loadRequests() {
  loading.value = true;

  try {
    const response = await requestStore.getSendedMe({
      search: filters.value.search?.trim() || undefined,
      status: filters.value.status || undefined,
      skip: (page.value - 1) * perPage.value,
      limit: perPage.value,
    });

    requests.value = response.requests;
    total.value = response.total;
  } finally {
    loading.value = false;
  }
}

onMounted(async () => {
  await loadRequests();
});

async function applyFilters() {
  page.value = 1;
  await loadRequests();
}

async function resetFilters() {
  filters.value.search = "";
  filters.value.status = "";
  page.value = 1;
  await loadRequests();
}

async function changePage(nextPage) {
  if (nextPage < 1 || nextPage > totalPages.value) {
    return;
  }

  page.value = nextPage;
  await loadRequests();
}

async function changePerPage() {
  page.value = 1;
  await loadRequests();
}

function openConfirmModal(request) {
  selectedRequest.value = request;
  showModal.value = true;
}

function openMessageModal(request) {
  selectedRequest.value = request;
  showMessageModal.value = true;
}

function onConfirm() {
  showModal.value = false;
  selectedRequest.value = null;
}

function onSearchChange(event) {
  if (event.target.value.trim().length === 0) {
    applyFilters();
  }
}

watch(
  () => filters.value.status,
  async () => {
    await changePerPage()
  }
);

async function checkForTransaction(request) {
  return request.has_transaction;
}

function openPaymentModal(request) {
  selectedRequest.value = request;
  showPaymentModal.value = true;
}

function closePaymentModal() {
  if (!paymentLoading.value) {
    showPaymentModal.value = false;
    selectedRequest.value = null;
  }
}

async function confirmPayment() {
  if (!selectedRequest.value) {
    return;
  }

  paymentLoading.value = true;

  try {
    await requestStore.payRequest(selectedRequest.value.id);
    toast.success("Zahlung erfolgreich durchgeführt.", {
      position: "top-right",
    });
    showPaymentModal.value = false;
    selectedRequest.value = null;
    await loadRequests();
  } catch (error) {
    toast.error(error.response?.data?.detail || "Zahlung fehlgeschlagen.", {
      position: "top-right",
    });
  } finally {
    paymentLoading.value = false;
  }
}
</script>

<template>
  <div
      class="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-3xl shadow-xl p-6"
  >
    <div class="flex items-center justify-between flex-wrap gap-4 mb-6">
      <div>
        <h1 class="text-3xl tracking-tight font-bold text-neutral-900 dark:text-white">
          Gesendete Anfragen
        </h1>
        <p class="text-neutral-500 dark:text-neutral-400 mt-1">
          Überblick über deine gesendeten Anfragen
        </p>
      </div>

      <div
          class="px-4 py-2 rounded-2xl bg-lime-100 dark:bg-lime-500/10 text-lime-700 dark:text-lime-400 font-semibold"
      >
        {{ total }} gesendet
      </div>
    </div>

    <div class="mb-6 rounded-2xl border border-neutral-200 dark:border-neutral-800 bg-neutral-50 dark:bg-neutral-950/40 p-4">
      <div class="grid gap-3 md:grid-cols-[minmax(0,1fr)_220px_auto_auto]">
        <input
            v-model="filters.search"
            @keydown.enter="applyFilters"
            @input="onSearchChange"
            type="search"
            placeholder="Nach Tool, Verleiher oder Nachricht suchen"
            class="w-full rounded-2xl border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-950 px-4 py-3 text-neutral-900 dark:text-white placeholder-neutral-400 dark:placeholder-neutral-500 focus:outline-none focus:ring-2 focus:ring-lime-400"
        />

        <select
            v-model="filters.status"
            class="w-full rounded-2xl border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-950 px-4 py-3 text-neutral-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-lime-400"
        >
          <option value="">Alle Status</option>
          <option value="Ausstehend">Ausstehend</option>
          <option value="Akzeptiert">Akzeptiert</option>
          <option value="Bezahlt">Bezahlt</option>
          <option value="Abgelehnt">Abgelehnt</option>
          <option value="Gegenangebot">Gegenangebot</option>
        </select>
      </div>
    </div>
    <div
        class="overflow-x-auto bg-neutral-50 dark:bg-neutral-950/40 border border-neutral-200 dark:border-neutral-800 rounded-2xl"
    >
      <table class="w-full text-left">
        <thead class="bg-neutral-100 dark:bg-neutral-900">
        <tr class="border-b border-neutral-200 dark:border-neutral-800 text-sm">
          <th class="py-4 px-5 font-semibold text-neutral-700 dark:text-neutral-300">
            <div class="flex items-center gap-2">
              <BIconTools/>
              <span>Tool</span>
            </div>
          </th>

          <th class="py-4 px-5 font-semibold text-neutral-700 dark:text-neutral-300">
            <div class="flex items-center gap-2">
              <BIconPerson/>
              <span>Ausleiher</span>
            </div>
          </th>

          <th class="py-4 px-5 font-semibold text-neutral-700 dark:text-neutral-300">
            <div class="flex items-center gap-2">
              <BIconPerson/>
              <span>Ihre Nachricht</span>
            </div>
          </th>

          <th class="py-4 px-5 font-semibold text-neutral-700 dark:text-neutral-300">
            <div class="flex items-center gap-2">
              <BIconPerson/>
              <span>Status</span>
            </div>
          </th>

          <th class="py-4 px-5 font-semibold text-neutral-700 dark:text-neutral-300 text-center">
            Aktion
          </th>
        </tr>
        </thead>

        <tbody>
        <tr v-if="loading">
          <td colspan="5" class="py-14 text-center text-neutral-500 dark:text-neutral-400">
            Gesendete Anfragen werden geladen...
          </td>
        </tr>

        <tr
            v-for="request in requests"
            v-else
            :key="request.id"
            class="border-b border-neutral-200 dark:border-neutral-800 hover:bg-neutral-100 dark:hover:bg-neutral-800/60 transition"
        >
          <td class="py-4 px-5">
            <div class="font-semibold text-neutral-900 dark:text-white">
              {{ request.tool_name }}
            </div>
          </td>

          <td class="py-4 px-5 text-neutral-700 dark:text-neutral-300">
            {{ request.borrower_username }}
          </td>

          <td class="py-4 px-5">
            <button
                @click="openMessageModal(request)"
                class="flex items-center justify-center w-10 h-10 rounded-xl bg-neutral-200 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 hover:bg-lime-100 hover:text-lime-700 dark:hover:bg-lime-500/10 dark:hover:text-lime-400 transition"
            >
              <BIconChatDots class="text-lg"/>
            </button>
          </td>

          <td class="py-4 px-5 text-neutral-700 dark:text-neutral-300">
            <span
                :class="requestStore.getStates[request.status]"
                class="inline-flex rounded-full px-3 py-1 text-xs font-semibold"
            >
              {{ request.status }}
            </span>
          </td>

          <td class="py-4 px-5">
            <div class="flex items-center justify-center gap-3" v-if="request.status === 'Akzeptiert'">
              <button
                  @click="openPaymentModal(request)"
                  class="bg-slate-200 dark:bg-slate-300 text-black py-2 px-3 rounded-xl hover:bg-slate-400 transition duration-300 hover:text-white font-semibold"
              >
                Zahlungsvorgang starten
              </button>
            </div>
    
          </td>
        </tr>

        <tr v-if="!loading && requests.length === 0">
          <td colspan="5" class="py-14 text-center">
            <div class="flex flex-col items-center justify-center gap-3 text-neutral-500 dark:text-neutral-400">
              <div
                  class="w-16 h-16 rounded-2xl bg-neutral-200 dark:bg-neutral-800 flex items-center justify-center"
              >
                <BIconChatDots class="text-2xl"/>
              </div>
              <p class="text-lg font-medium">Keine Anfragen gefunden</p>
              <p class="text-sm">
                {{ hasActiveFilters ? "Passe die Filter an, um mehr Ergebnisse zu sehen." : "Deine gesendeten Anfragen erscheinen hier." }}
              </p>
            </div>
          </td>
        </tr>
        </tbody>
      </table>
    </div>

    <div class="mt-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <div class="flex items-center gap-3 text-sm text-neutral-500 dark:text-neutral-400">
        <span>Pro Seite:</span>
        <select
            v-model="perPage"
            @change="changePerPage"
            class="rounded-xl border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-950 px-3 py-2 text-sm text-neutral-900 dark:text-white"
        >
          <option :value="5">5</option>
          <option :value="10">10</option>
          <option :value="25">25</option>
        </select>
      </div>

      <div class="flex items-center justify-center gap-3">
        <button
            @click="changePage(page - 1)"
            :disabled="page <= 1 || loading"
            class="px-4 py-2 rounded-xl border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-950 text-neutral-900 dark:text-white hover:bg-neutral-100 dark:hover:bg-neutral-800 transition disabled:opacity-50"
        >
          Zurück
        </button>

        <span class="text-sm text-neutral-500 dark:text-neutral-400">
          Seite {{ page }} von {{ totalPages }}
        </span>

        <button
            @click="changePage(page + 1)"
            :disabled="page >= totalPages || loading"
            class="px-4 py-2 rounded-xl border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-950 text-neutral-900 dark:text-white hover:bg-neutral-100 dark:hover:bg-neutral-800 transition disabled:opacity-50"
        >
          Weiter
        </button>
      </div>
    </div>

    <transition name="fade">
      <div
          v-if="showMessageModal"
          class="fixed inset-0 z-[60] flex items-center justify-center px-4"
      >
        <div
            class="absolute inset-0 bg-black/50 backdrop-blur-sm"
            @click="showMessageModal = false"
        ></div>

        <div
            class="relative z-10 w-full max-w-lg rounded-[28px] border border-neutral-200 bg-white p-6 shadow-xl dark:border-neutral-800 dark:bg-neutral-900"
        >
          <button
              @click="showMessageModal = false"
              class="absolute right-4 top-4 flex h-10 w-10 items-center justify-center rounded-full text-neutral-500 transition hover:bg-neutral-100 dark:text-neutral-400 dark:hover:bg-neutral-800"
          >
            &times;
          </button>

          <p class="text-lg font-semibold text-neutral-900 dark:text-white">
            Nachricht
          </p>

          <p
              v-if="selectedRequest?.message"
              class="mt-4 text-sm leading-6 text-neutral-600 dark:text-neutral-300"
          >
            {{ selectedRequest.message }}
          </p>

          <p
              v-else
              class="mt-4 text-sm text-neutral-500 dark:text-neutral-400"
          >
            Keine Nachricht vorhanden.
          </p>
        </div>
      </div>
    </transition>

    <ConfirmationPopUp
        v-if="showModal"
        title="Anfrage ablehnen?"
        message="Willst du diese Anfrage wirklich ablehnen?"
        @close="showModal = false"
        @confirm="onConfirm"
    />

    <FakePaypalPaymentPopUp
        :show-modal="showPaymentModal"
        :amount="selectedRequest?.tool_deposit || 0"
        :tool-name="selectedRequest?.tool_name || ''"
        :loading="paymentLoading"
        @close="closePaymentModal"
        @confirm="confirmPayment"
    />
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.18s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
