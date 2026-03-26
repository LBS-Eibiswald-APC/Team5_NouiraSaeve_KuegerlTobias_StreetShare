<script setup>
import {onMounted, ref} from "vue";
import {useTransactionsStore} from "@/store/transactionsStore.js";
import {useAuthStore} from "@/store/authStore.js";

const transactionsStore = useTransactionsStore();
const authStore = useAuthStore();
const transactions = ref([]);
const loading = ref(false);

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

function getRoleLabel(transaction) {
  if (authStore.user_id === transaction.borrower_id) {
    return "Leiher";
  }

  if (authStore.user_id === transaction.lender_id) {
    return "Verleiher";
  }

  return "-";
}

async function loadTransactions() {
  loading.value = true;

  try {
    transactions.value = await transactionsStore.getMyTransactions();
  } finally {
    loading.value = false;
  }
}

onMounted(async () => {
  await loadTransactions();
});
</script>

<template>
  <div
      class="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-3xl shadow-xl p-6"
  >
    <div class="flex items-center justify-between flex-wrap gap-4 mb-6">
      <div>
        <h1 class="text-3xl tracking-tight font-bold text-neutral-900 dark:text-white">
          Meine Transaktionen
        </h1>
        <p class="text-neutral-500 dark:text-neutral-400 mt-1">
          Alle laufenden und vergangenen Ausleihen mit deiner Beteiligung
        </p>
      </div>

      <div
          class="px-4 py-2 rounded-2xl bg-lime-100 dark:bg-lime-500/10 text-lime-700 dark:text-lime-400 font-semibold"
      >
        {{ transactions.length }} Transaktionen
      </div>
    </div>

    <div
        class="overflow-x-auto bg-neutral-50 dark:bg-neutral-950/40 border border-neutral-200 dark:border-neutral-800 rounded-2xl"
    >
      <table class="w-full text-left">
        <thead class="bg-neutral-100 dark:bg-neutral-900">
        <tr class="border-b border-neutral-200 dark:border-neutral-800 text-sm">
          <th class="py-4 px-5 font-semibold text-neutral-700 dark:text-neutral-300">Tool</th>
          <th class="py-4 px-5 font-semibold text-neutral-700 dark:text-neutral-300">Rolle</th>
          <th class="py-4 px-5 font-semibold text-neutral-700 dark:text-neutral-300">Leiher</th>
          <th class="py-4 px-5 font-semibold text-neutral-700 dark:text-neutral-300">Verleiher</th>
          <th class="py-4 px-5 font-semibold text-neutral-700 dark:text-neutral-300">Von</th>
          <th class="py-4 px-5 font-semibold text-neutral-700 dark:text-neutral-300">Bis</th>
          <th class="py-4 px-5 font-semibold text-neutral-700 dark:text-neutral-300">Erstellt</th>
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
            class="border-b border-neutral-200 dark:border-neutral-800 hover:bg-neutral-100 dark:hover:bg-neutral-800/60 transition"
        >
          <td class="py-4 px-5 font-semibold text-neutral-900 dark:text-white">
            {{ transaction.tool_name || `Tool #${transaction.tool_id}` }}
          </td>
          <td class="py-4 px-5 text-neutral-700 dark:text-neutral-300">
            <span class="inline-flex rounded-full px-3 py-1 text-xs font-semibold bg-lime-100 text-lime-700 border border-lime-200 dark:bg-lime-500/15 dark:text-lime-300 dark:border-lime-500/20">
              {{ getRoleLabel(transaction) }}
            </span>
          </td>
          <td class="py-4 px-5 text-neutral-700 dark:text-neutral-300">
            {{ transaction.borrower_name || `User #${transaction.borrower_id}` }}
          </td>
          <td class="py-4 px-5 text-neutral-700 dark:text-neutral-300">
            {{ transaction.lender_name || `User #${transaction.lender_id}` }}
          </td>
          <td class="py-4 px-5 text-neutral-700 dark:text-neutral-300">
            {{ formatDate(transaction.start_date) }}
          </td>
          <td class="py-4 px-5 text-neutral-700 dark:text-neutral-300">
            {{ formatDate(transaction.end_date) }}
          </td>
          <td class="py-4 px-5 text-neutral-700 dark:text-neutral-300">
            {{ formatDate(transaction.created_at) }}
          </td>
        </tr>

        <tr v-if="!loading && transactions.length === 0">
          <td colspan="7" class="py-14 text-center">
            <div class="flex flex-col items-center justify-center gap-3 text-neutral-500 dark:text-neutral-400">
              <div
                  class="w-16 h-16 rounded-2xl bg-neutral-200 dark:bg-neutral-800 flex items-center justify-center"
              >
                <BIconArrowLeftRight class="text-2xl"/>
              </div>
              <p class="text-lg font-medium">Keine Transaktionen vorhanden</p>
              <p class="text-sm">Sobald du etwas verleihst oder ausleihst, erscheint es hier.</p>
            </div>
          </td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
