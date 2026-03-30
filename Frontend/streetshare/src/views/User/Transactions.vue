<script setup>
import { computed, onMounted, ref } from "vue";
import { useToast } from "vue-toast-notification";
import { useTransactionsStore } from "@/store/transactionsStore.js";
import { useAuthStore } from "@/store/authStore.js";

const transactionsStore = useTransactionsStore();
const authStore = useAuthStore();
const toast = useToast();
const transactions = ref([]);
const loading = ref(false);
const actionLoading = ref(false);
const disputeLoading = ref(false);
const showReturnRequestModal = ref(false);
const showReturnConfirmModal = ref(false);
const selectedTransaction = ref(null);
const lenderReturnCondition = ref("Gebraucht");
const borrowerReturnCondition = ref("Gebraucht");
const returnPhoto = ref(null);

const conditions = ["Neu", "Minimal abgenutzt", "Gebraucht", "Gut abgenutzt", "Defekt"];

const dateFormat = new Intl.DateTimeFormat("de-DE", {
  dateStyle: "medium",
  timeStyle: "short",
});

function formatDate(value) {
  if (!value) {
    return "-";
  }

  return dateFormat.format(new Date(value));
}

function formatMoney(value) {
  return new Intl.NumberFormat("de-DE", {
    style: "currency",
    currency: "EUR",
  }).format(Number(value || 0));
}

function getStatusLabel(status) {
  if (status === "Rueckgabe ausstehend") {
    return "Rückgabe ausstehend";
  }

  if (status === "In Review") {
    return "In Review";
  }

  return status || "-";
}

function getRoleLabel(transaction) {
  if (Number(authStore.user_id) === Number(transaction.borrower_id)) {
    return "Leiher";
  }

  if (Number(authStore.user_id) === Number(transaction.lender_id)) {
    return "Verleiher";
  }

  return "-";
}

function getStatusClass(status) {
  if (status === "Abgeschlossen") {
    return "bg-emerald-100 text-emerald-700 border border-emerald-200 dark:bg-emerald-500/15 dark:text-emerald-300 dark:border-emerald-500/20";
  }

  if (status === "Rueckgabe ausstehend") {
    return "bg-amber-100 text-amber-700 border border-amber-200 dark:bg-amber-500/15 dark:text-amber-300 dark:border-amber-500/20";
  }

  if (status === "In Review") {
    return "bg-rose-100 text-rose-700 border border-rose-200 dark:bg-rose-500/15 dark:text-rose-300 dark:border-rose-500/20";
  }

  return "bg-sky-100 text-sky-700 border border-sky-200 dark:bg-sky-500/15 dark:text-sky-300 dark:border-sky-500/20";
}

function isLender(transaction) {
  return Number(authStore.user_id) === Number(transaction.lender_id);
}

function isBorrower(transaction) {
  return Number(authStore.user_id) === Number(transaction.borrower_id);
}

function canRequestReturn(transaction) {
  return isBorrower(transaction) && transaction.status === "Bezahlt";
}

function canConfirmReturn(transaction) {
  return isLender(transaction) && transaction.status === "Rueckgabe ausstehend";
}

const selectedPhotoName = computed(() => returnPhoto.value?.name || "");

async function loadTransactions() {
  loading.value = true;

  try {
    transactions.value = await transactionsStore.getMyTransactions();
  } finally {
    loading.value = false;
  }
}

function openReturnRequestModal(transaction) {
  selectedTransaction.value = transaction;
  lenderReturnCondition.value = transaction.borrower_return_condition || transaction.final_condition || "Gebraucht";
  showReturnRequestModal.value = true;
}

function openReturnConfirmModal(transaction) {
  selectedTransaction.value = transaction;
  borrowerReturnCondition.value = transaction.lender_return_condition || transaction.borrower_return_condition || transaction.final_condition || "Gebraucht";
  returnPhoto.value = null;
  showReturnConfirmModal.value = true;
}

function closeReturnRequestModal(force = false) {
  if (force || !actionLoading.value) {
    showReturnRequestModal.value = false;
    selectedTransaction.value = null;
  }
}

function closeReturnConfirmModal(force = false) {
  if (force || (!actionLoading.value && !disputeLoading.value)) {
    showReturnConfirmModal.value = false;
    selectedTransaction.value = null;
    returnPhoto.value = null;
  }
}

function onPhotoChange(event) {
  returnPhoto.value = event.target.files?.[0] ?? null;
}

async function submitReturnRequest() {
  if (!selectedTransaction.value) {
    return;
  }

  actionLoading.value = true;

  try {
    await transactionsStore.requestReturn(selectedTransaction.value.id, lenderReturnCondition.value);
    toast.success("Rückgabe wurde erfasst.", { position: "top-right" });
    closeReturnRequestModal(true);
    await loadTransactions();
  } catch (error) {
    toast.error(error.response?.data?.detail || "Rückgabe konnte nicht erfasst werden.", { position: "top-right" });
  } finally {
    actionLoading.value = false;
  }
}

async function submitReturnConfirm() {
  if (!selectedTransaction.value || !returnPhoto.value) {
    toast.error("Bitte Foto und Kondition angeben.", { position: "top-right" });
    return;
  }

  actionLoading.value = true;

  try {
    await transactionsStore.confirmReturn(selectedTransaction.value.id, {
      finalCondition: borrowerReturnCondition.value,
      pictureAfter: returnPhoto.value,
    });
    toast.success("Rückgabe wurde bestätigt.", { position: "top-right" });
    closeReturnConfirmModal(true);
    await loadTransactions();
  } catch (error) {
    toast.error(error.response?.data?.detail || "Rückgabe konnte nicht bestätigt werden.", { position: "top-right" });
  } finally {
    actionLoading.value = false;
  }
}

async function sendToSupportReview() {
  if (!selectedTransaction.value || !returnPhoto.value) {
    toast.error("Bitte Foto und Kondition angeben.", { position: "top-right" });
    return;
  }

  disputeLoading.value = true;

  try {
    await transactionsStore.createSupportReview(selectedTransaction.value.id, {
      lenderCondition: borrowerReturnCondition.value,
      lenderPicture: returnPhoto.value,
    });
    toast.success("Fall wurde an den Support weitergegeben.", { position: "top-right" });
    closeReturnConfirmModal(true);
    await loadTransactions();
  } catch (error) {
    toast.error(error.response?.data?.detail || "Support-Fall konnte nicht erstellt werden.", { position: "top-right" });
  } finally {
    disputeLoading.value = false;
  }
}

onMounted(async () => {
  await loadTransactions();
});
</script>

<template>
  <div class="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-3xl shadow-xl p-6">
    <div class="flex items-center justify-between flex-wrap gap-4 mb-6">
      <div>
        <h1 class="text-3xl tracking-tight font-bold text-neutral-900 dark:text-white">
          Meine Transaktionen
        </h1>
        <p class="text-neutral-500 dark:text-neutral-400 mt-1">
          Zahlung, Ausleihe und Rückgabe laufen hier zusammen, auch bei vorzeitiger Rückgabe.
        </p>
      </div>

      <div class="px-4 py-2 rounded-2xl bg-lime-100 dark:bg-lime-500/10 text-lime-700 dark:text-lime-400 font-semibold">
        {{ transactions.length }} Transaktionen
      </div>
    </div>

    <div class="mb-6 rounded-2xl border border-sky-200 bg-sky-50 p-4 text-sm leading-6 text-sky-900 dark:border-sky-500/20 dark:bg-sky-500/10 dark:text-sky-100">
      5% Plattformgebühr, 5% Grundanteil für den Verleiher, je schlechtere Kondition +10% für den Verleiher, bei Defekt geht 95% an den Verleiher.
    </div>

    <div class="overflow-x-auto bg-neutral-50 dark:bg-neutral-950/40 border border-neutral-200 dark:border-neutral-800 rounded-2xl">
      <table class="w-full text-left">
        <thead class="bg-neutral-100 dark:bg-neutral-900">
        <tr class="border-b border-neutral-200 dark:border-neutral-800 text-sm">
          <th class="py-4 px-5 font-semibold text-neutral-700 dark:text-neutral-300">Tool</th>
          <th class="py-4 px-5 font-semibold text-neutral-700 dark:text-neutral-300">Rolle</th>
          <th class="py-4 px-5 font-semibold text-neutral-700 dark:text-neutral-300">Status</th>
          <th class="py-4 px-5 font-semibold text-neutral-700 dark:text-neutral-300">Von</th>
          <th class="py-4 px-5 font-semibold text-neutral-700 dark:text-neutral-300">Bis</th>
          <th class="py-4 px-5 font-semibold text-neutral-700 dark:text-neutral-300">Ergebnis</th>
          <th class="py-4 px-5 font-semibold text-neutral-700 dark:text-neutral-300 text-center">Aktion</th>
        </tr>
        </thead>

        <tbody>
        <tr v-if="loading">
          <td colspan="7" class="py-14 text-center text-neutral-500 dark:text-neutral-400">
            Transaktionen werden geladen...
          </td>
        </tr>

        <tr
          v-for="transaction in transactions"
          v-else
          :key="transaction.id"
          class="border-b border-neutral-200 dark:border-neutral-800 hover:bg-neutral-100 dark:hover:bg-neutral-800/60 transition align-top"
        >
          <td class="py-4 px-5 font-semibold text-neutral-900 dark:text-white">
            {{ transaction.tool_name || `Tool #${transaction.tool_id}` }}
          </td>
          <td class="py-4 px-5 text-neutral-700 dark:text-neutral-300">
            {{ getRoleLabel(transaction) }}
          </td>
          <td class="py-4 px-5 text-neutral-700 dark:text-neutral-300">
            <span :class="getStatusClass(transaction.status)" class="inline-flex rounded-full px-3 py-1 text-xs font-semibold">
              {{ getStatusLabel(transaction.status) }}
            </span>
          </td>
          <td class="py-4 px-5 text-neutral-700 dark:text-neutral-300">
            {{ formatDate(transaction.start_date) }}
          </td>
          <td class="py-4 px-5 text-neutral-700 dark:text-neutral-300">
            {{ formatDate(transaction.end_date) }}
          </td>
          <td class="py-4 px-5 text-sm leading-6 text-neutral-700 dark:text-neutral-300">
            <div v-if="transaction.status === 'Abgeschlossen'">
              <div>Finale Kondition: {{ transaction.final_condition || "-" }}</div>
              <div>Plattform: {{ formatMoney(transaction.platform_fee) }}</div>
              <div>Verleiher: {{ formatMoney(transaction.lender_payout) }}</div>
              <div>Leiher zurück: {{ formatMoney(transaction.borrower_refund) }}</div>
            </div>
            <div v-else-if="transaction.status === 'Rueckgabe ausstehend'">
              Vom Leiher gemeldet:
              {{ transaction.borrower_return_condition || "-" }}
            </div>
            <div v-else-if="transaction.status === 'In Review'">
              Uneinig. Der Fall liegt aktuell beim Support-Team.
            </div>
            <div v-else-if="getStatusLabel(transaction.status) === 'In Review'">
              Uneinig. Der Fall liegt aktuell beim Support-Team.
            </div>
            <div v-else>
              Bezahlt. Die Ausleihe kann stattfinden und die Rückgabe kann bei Bedarf auch früher erfasst werden.
            </div>
          </td>
          <td class="py-4 px-5 text-center">
            <button
              v-if="canRequestReturn(transaction)"
              type="button"
              class="rounded-xl bg-neutral-950 px-4 py-2 font-semibold text-white transition hover:opacity-90 dark:bg-white dark:text-black"
              @click="openReturnRequestModal(transaction)"
            >
              Rückgabe melden
            </button>

            <button
              v-else-if="canConfirmReturn(transaction)"
              type="button"
              class="rounded-xl bg-sky-500 px-4 py-2 font-semibold text-white transition hover:bg-sky-400"
              @click="openReturnConfirmModal(transaction)"
            >
              Rückgabe bestätigen
            </button>

            <span v-else class="text-sm text-neutral-500 dark:text-neutral-400">
              -
            </span>
          </td>
        </tr>

        <tr v-if="!loading && transactions.length === 0">
          <td colspan="7" class="py-14 text-center text-neutral-500 dark:text-neutral-400">
            Noch keine Transaktionen vorhanden.
          </td>
        </tr>
        </tbody>
      </table>
    </div>

    <transition name="fade">
      <div v-if="showReturnRequestModal" class="fixed inset-0 z-[70] flex items-center justify-center px-4">
        <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="closeReturnRequestModal"></div>
        <div class="relative z-10 w-full max-w-lg rounded-[28px] border border-neutral-200 bg-white p-6 shadow-xl dark:border-neutral-800 dark:bg-neutral-900">
          <button
            @click="closeReturnRequestModal"
            class="absolute right-4 top-4 flex h-10 w-10 items-center justify-center rounded-full text-neutral-500 transition hover:bg-neutral-100 dark:text-neutral-400 dark:hover:bg-neutral-800"
          >
            &times;
          </button>

          <h2 class="text-2xl font-bold text-neutral-900 dark:text-white">Rückgabe melden</h2>
          <p class="mt-2 text-sm text-neutral-500 dark:text-neutral-400">
            Du bestätigst, dass du das Tool zurückgegeben hast. Das geht auch früher als geplant. Danach muss der Verleiher mit Foto und finaler Kondition bestätigen.
          </p>

          <label class="mt-5 block">
            <span class="mb-2 block text-sm font-medium text-neutral-700 dark:text-neutral-300">Deine Kondition bei Rückgabe</span>
            <select
              v-model="lenderReturnCondition"
              class="w-full rounded-2xl border border-neutral-300 bg-white px-4 py-3 text-neutral-900 focus:outline-none focus:ring-2 focus:ring-lime-400 dark:border-neutral-700 dark:bg-neutral-950 dark:text-white"
            >
              <option v-for="condition in conditions" :key="condition" :value="condition">{{ condition }}</option>
            </select>
          </label>

          <div class="mt-6 flex justify-end gap-3">
            <button
              type="button"
              class="rounded-xl border border-neutral-300 px-4 py-2 text-neutral-700 transition hover:bg-neutral-100 dark:border-neutral-700 dark:text-neutral-300 dark:hover:bg-neutral-800"
              :disabled="actionLoading"
              @click="closeReturnRequestModal"
            >
              Abbrechen
            </button>
            <button
              type="button"
              class="rounded-xl bg-neutral-950 px-4 py-2 font-semibold text-white transition hover:opacity-90 disabled:opacity-60 dark:bg-white dark:text-black"
              :disabled="actionLoading"
              @click="submitReturnRequest"
            >
              {{ actionLoading ? "Speichert..." : "Rückgabe senden" }}
            </button>
          </div>
        </div>
      </div>
    </transition>

    <transition name="fade">
      <div v-if="showReturnConfirmModal" class="fixed inset-0 z-[70] flex items-center justify-center px-4">
        <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="closeReturnConfirmModal"></div>
        <div class="relative z-10 w-full max-w-lg rounded-[28px] border border-neutral-200 bg-white p-6 shadow-xl dark:border-neutral-800 dark:bg-neutral-900">
          <button
            @click="closeReturnConfirmModal"
            class="absolute right-4 top-4 flex h-10 w-10 items-center justify-center rounded-full text-neutral-500 transition hover:bg-neutral-100 dark:text-neutral-400 dark:hover:bg-neutral-800"
          >
            &times;
          </button>

          <h2 class="text-2xl font-bold text-neutral-900 dark:text-white">Rückgabe bestätigen</h2>
          <p class="mt-2 text-sm text-neutral-500 dark:text-neutral-400">
            Bestätige als Verleiher die finale Kondition und lade ein Foto hoch.
          </p>

          <div
            v-if="selectedTransaction?.borrower_return_condition"
            class="mt-4 rounded-2xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm leading-6 text-amber-900 dark:border-amber-500/20 dark:bg-amber-500/10 dark:text-amber-100"
          >
            Leiher gemeldet: {{ selectedTransaction.borrower_return_condition }}
          </div>

          <label class="mt-5 block">
            <span class="mb-2 block text-sm font-medium text-neutral-700 dark:text-neutral-300">Finale Kondition</span>
            <select
              v-model="borrowerReturnCondition"
              class="w-full rounded-2xl border border-neutral-300 bg-white px-4 py-3 text-neutral-900 focus:outline-none focus:ring-2 focus:ring-sky-400 dark:border-neutral-700 dark:bg-neutral-950 dark:text-white"
            >
              <option v-for="condition in conditions" :key="condition" :value="condition">{{ condition }}</option>
            </select>
          </label>

          <label class="mt-4 block">
            <span class="mb-2 block text-sm font-medium text-neutral-700 dark:text-neutral-300">Foto *</span>
            <input
              type="file"
              accept="image/*"
              class="w-full rounded-2xl border border-neutral-300 bg-white px-4 py-3 text-neutral-900 file:mr-4 file:rounded-lg file:border-0 file:bg-sky-500 file:px-4 file:py-2 file:font-semibold file:text-white dark:border-neutral-700 dark:bg-neutral-950 dark:text-white"
              @change="onPhotoChange"
            />
            <p v-if="selectedPhotoName" class="mt-2 text-sm text-neutral-500 dark:text-neutral-400">
              Ausgewählt: {{ selectedPhotoName }}
            </p>
          </label>

          <div class="mt-6 flex justify-end gap-3">
            <button
              type="button"
              class="rounded-xl border border-neutral-300 px-4 py-2 text-neutral-700 transition hover:bg-neutral-100 dark:border-neutral-700 dark:text-neutral-300 dark:hover:bg-neutral-800"
              :disabled="actionLoading || disputeLoading"
              @click="closeReturnConfirmModal"
            >
              Abbrechen
            </button>
            <button
              type="button"
              class="rounded-xl border border-rose-300 px-4 py-2 font-semibold text-rose-700 transition hover:bg-rose-50 disabled:opacity-60 dark:border-rose-500/30 dark:text-rose-300 dark:hover:bg-rose-500/10"
              :disabled="actionLoading || disputeLoading || !returnPhoto"
              @click="sendToSupportReview"
            >
              {{ disputeLoading ? "Sendet..." : "Nicht einverstanden" }}
            </button>
            <button
              type="button"
              class="rounded-xl bg-sky-500 px-4 py-2 font-semibold text-white transition hover:bg-sky-400 disabled:opacity-60"
              :disabled="actionLoading || disputeLoading || !returnPhoto"
              @click="submitReturnConfirm"
            >
              {{ actionLoading ? "Bestätigt..." : "Jetzt bestätigen" }}
            </button>
          </div>
        </div>
      </div>
    </transition>
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
