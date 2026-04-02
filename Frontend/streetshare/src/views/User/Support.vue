<script setup>
import { onMounted, ref } from "vue";
import { useToast } from "vue-toast-notification";
import { useTransactionsStore } from "@/store/transactionsStore.js";
import api from "@/services/api.js";

const transactionsStore = useTransactionsStore();
const toast = useToast();
const reviews = ref([]);
const loading = ref(false);
const actionLoading = ref(false);
const selectedReview = ref(null);
const showResolveModal = ref(false);
const showImageModal = ref(false);
const selectedImageUrl = ref("");
const selectedImageTitle = ref("");
const finalCondition = ref("Gebraucht");
const supportNote = ref("");

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

function getReviewStatusClass(status) {
  if (status === "Entschieden") {
    return "bg-emerald-100 text-emerald-700 border border-emerald-200 dark:bg-emerald-500/15 dark:text-emerald-300 dark:border-emerald-500/20";
  }

  return "bg-amber-100 text-amber-700 border border-amber-200 dark:bg-amber-500/15 dark:text-amber-300 dark:border-amber-500/20";
}

function getReviewPictureUrl(reviewId) {
  return `${api.defaults.baseURL}/transaction-reviews/${reviewId}/picture`;
}

function openImageModal(review) {
  selectedImageUrl.value = getReviewPictureUrl(review.id);
  selectedImageTitle.value = review.tool_name || `Tool #${review.tool_id}`;
  showImageModal.value = true;
}

function closeImageModal() {
  showImageModal.value = false;
  selectedImageUrl.value = "";
  selectedImageTitle.value = "";
}

async function loadReviews() {
  loading.value = true;

  try {
    reviews.value = await transactionsStore.getSupportReviews();
  } finally {
    loading.value = false;
  }
}

function openResolveModal(review) {
  selectedReview.value = review;
  finalCondition.value = review.support_decision_condition || review.lender_condition || review.borrower_condition || "Gebraucht";
  supportNote.value = review.support_note || "";
  showResolveModal.value = true;
}

function closeResolveModal(force = false) {
  if (force || !actionLoading.value) {
    showResolveModal.value = false;
    selectedReview.value = null;
    supportNote.value = "";
  }
}

async function submitResolution() {
  if (!selectedReview.value) {
    return;
  }

  actionLoading.value = true;

  try {
    await transactionsStore.resolveSupportReview(selectedReview.value.id, {
      finalCondition: finalCondition.value,
      supportNote: supportNote.value,
    });
    toast.success("Support-Fall wurde entschieden.", { position: "top-right" });
    closeResolveModal(true);
    await loadReviews();
  } catch (error) {
    toast.error(error.response?.data?.detail || "Support-Fall konnte nicht entschieden werden.", { position: "top-right" });
  } finally {
    actionLoading.value = false;
  }
}

onMounted(async () => {
  await loadReviews();
});
</script>

<template>
  <div class="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-3xl shadow-xl p-6">
    <div class="flex items-center justify-between flex-wrap gap-4 mb-6">
      <div>
        <h1 class="text-3xl tracking-tight font-bold text-neutral-900 dark:text-white">
          Support-Fälle
        </h1>
        <p class="text-neutral-500 dark:text-neutral-400 mt-1">
          Hier sieht das Support-Team alle Fälle, bei denen sich Leiher und Verleiher nicht einig sind.
        </p>
      </div>

      <div class="px-4 py-2 rounded-2xl bg-amber-100 dark:bg-amber-500/10 text-amber-700 dark:text-amber-400 font-semibold">
        {{ reviews.length }} Fälle
      </div>
    </div>

    <div class="overflow-x-auto bg-neutral-50 dark:bg-neutral-950/40 border border-neutral-200 dark:border-neutral-800 rounded-2xl">
      <table class="w-full text-left">
        <thead class="bg-neutral-100 dark:bg-neutral-900">
        <tr class="border-b border-neutral-200 dark:border-neutral-800 text-sm">
          <th class="py-4 px-5 font-semibold text-neutral-700 dark:text-neutral-300">Tool</th>
          <th class="py-4 px-5 font-semibold text-neutral-700 dark:text-neutral-300">Leiher</th>
          <th class="py-4 px-5 font-semibold text-neutral-700 dark:text-neutral-300">Verleiher</th>
          <th class="py-4 px-5 font-semibold text-neutral-700 dark:text-neutral-300">Konditionen</th>
          <th class="py-4 px-5 font-semibold text-neutral-700 dark:text-neutral-300">Status</th>
          <th class="py-4 px-5 font-semibold text-neutral-700 dark:text-neutral-300">Erstellt</th>
          <th class="py-4 px-5 font-semibold text-neutral-700 dark:text-neutral-300 text-center">Aktion</th>
        </tr>
        </thead>

        <tbody>
        <tr v-if="loading">
          <td colspan="7" class="py-14 text-center text-neutral-500 dark:text-neutral-400">
            Support-Fälle werden geladen...
          </td>
        </tr>

        <tr
          v-for="review in reviews"
          v-else
          :key="review.id"
          class="border-b border-neutral-200 dark:border-neutral-800 hover:bg-neutral-100 dark:hover:bg-neutral-800/60 transition align-top"
        >
          <td class="py-4 px-5 font-semibold text-neutral-900 dark:text-white">
            {{ review.tool_name || `Tool #${review.tool_id}` }}
          </td>
          <td class="py-4 px-5 text-neutral-700 dark:text-neutral-300">
            {{ review.borrower_name || "-" }}
          </td>
          <td class="py-4 px-5 text-neutral-700 dark:text-neutral-300">
            {{ review.lender_name || "-" }}
          </td>
          <td class="py-4 px-5 text-sm leading-6 text-neutral-700 dark:text-neutral-300">
            <div>Leiher: {{ review.borrower_condition || "-" }}</div>
            <div>Verleiher: {{ review.lender_condition || "-" }}</div>
            <div v-if="review.has_lender_picture" class="mt-3">
              <img
                :src="getReviewPictureUrl(review.id)"
                alt="Support-Foto"
                class="h-20 w-20 cursor-zoom-in rounded-2xl border border-neutral-200 object-cover dark:border-neutral-700"
                @click="openImageModal(review)"
              />
            </div>
            <div v-else>Foto: Kein Foto</div>
          </td>
          <td class="py-4 px-5 text-neutral-700 dark:text-neutral-300">
            <span :class="getReviewStatusClass(review.review_status)" class="inline-flex rounded-full px-3 py-1 text-xs font-semibold">
              {{ review.review_status }}
            </span>
          </td>
          <td class="py-4 px-5 text-neutral-700 dark:text-neutral-300">
            {{ formatDate(review.created_at) }}
          </td>
          <td class="py-4 px-5 text-center">
            <button
              v-if="review.review_status !== 'Entschieden'"
              type="button"
              class="rounded-xl bg-neutral-950 px-4 py-2 font-semibold text-white transition hover:opacity-90 dark:bg-white dark:text-black"
              @click="openResolveModal(review)"
            >
              Entscheiden
            </button>
            <span v-else class="text-sm text-neutral-500 dark:text-neutral-400">
              -
            </span>
          </td>
        </tr>

        <tr v-if="!loading && reviews.length === 0">
          <td colspan="7" class="py-14 text-center text-neutral-500 dark:text-neutral-400">
            Keine Support-Fälle vorhanden.
          </td>
        </tr>
        </tbody>
      </table>
    </div>

    <transition name="fade">
      <div v-if="showResolveModal" class="fixed inset-0 z-[70] flex items-center justify-center px-4">
        <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="closeResolveModal"></div>
        <div class="relative z-10 w-full max-w-lg rounded-[28px] border border-neutral-200 bg-white p-6 shadow-xl dark:border-neutral-800 dark:bg-neutral-900">
          <button
            @click="closeResolveModal"
            class="absolute right-4 top-4 flex h-10 w-10 items-center justify-center rounded-full text-neutral-500 transition hover:bg-neutral-100 dark:text-neutral-400 dark:hover:bg-neutral-800"
          >
            &times;
          </button>

          <h2 class="text-2xl font-bold text-neutral-900 dark:text-white">Support-Fall entscheiden</h2>

          <div class="mt-4 rounded-2xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm leading-6 text-amber-900 dark:border-amber-500/20 dark:bg-amber-500/10 dark:text-amber-100">
            <div>Leiher meldet: {{ selectedReview?.borrower_condition || "-" }}</div>
            <div>Verleiher meldet: {{ selectedReview?.lender_condition || "-" }}</div>
          </div>

          <div v-if="selectedReview?.has_lender_picture" class="mt-4">
            <p class="mb-2 text-sm font-medium text-neutral-700 dark:text-neutral-300">Hochgeladenes Foto</p>
            <img
              :src="getReviewPictureUrl(selectedReview.id)"
              alt="Support-Foto groß"
              class="max-h-72 w-full cursor-zoom-in rounded-2xl border border-neutral-200 object-contain dark:border-neutral-700"
              @click="openImageModal(selectedReview)"
            />
          </div>

          <label class="mt-5 block">
            <span class="mb-2 block text-sm font-medium text-neutral-700 dark:text-neutral-300">Finale Kondition</span>
            <select
              v-model="finalCondition"
              class="w-full rounded-2xl border border-neutral-300 bg-white px-4 py-3 text-neutral-900 focus:outline-none focus:ring-2 focus:ring-lime-400 dark:border-neutral-700 dark:bg-neutral-950 dark:text-white"
            >
              <option v-for="condition in conditions" :key="condition" :value="condition">{{ condition }}</option>
            </select>
          </label>

          <label class="mt-4 block">
            <span class="mb-2 block text-sm font-medium text-neutral-700 dark:text-neutral-300">Support-Notiz</span>
            <textarea
              v-model="supportNote"
              rows="4"
              class="w-full rounded-2xl border border-neutral-300 bg-white px-4 py-3 text-neutral-900 focus:outline-none focus:ring-2 focus:ring-lime-400 dark:border-neutral-700 dark:bg-neutral-950 dark:text-white"
            ></textarea>
          </label>

          <div class="mt-6 flex justify-end gap-3">
            <button
              type="button"
              class="rounded-xl border border-neutral-300 px-4 py-2 text-neutral-700 transition hover:bg-neutral-100 dark:border-neutral-700 dark:text-neutral-300 dark:hover:bg-neutral-800"
              :disabled="actionLoading"
              @click="closeResolveModal"
            >
              Abbrechen
            </button>
            <button
              type="button"
              class="rounded-xl bg-neutral-950 px-4 py-2 font-semibold text-white transition hover:opacity-90 disabled:opacity-60 dark:bg-white dark:text-black"
              :disabled="actionLoading"
              @click="submitResolution"
            >
              {{ actionLoading ? "Speichert..." : "Entscheidung speichern" }}
            </button>
          </div>
        </div>
      </div>
    </transition>

    <transition name="fade">
      <div v-if="showImageModal" class="fixed inset-0 z-[80] flex items-center justify-center px-4">
        <div class="absolute inset-0 bg-black/75 backdrop-blur-sm" @click="closeImageModal"></div>
        <div class="relative z-10 w-full max-w-5xl rounded-[28px] border border-neutral-200 bg-white p-4 shadow-xl dark:border-neutral-800 dark:bg-neutral-900">
          <button
            @click="closeImageModal"
            class="absolute right-4 top-4 flex h-10 w-10 items-center justify-center rounded-full text-neutral-500 transition hover:bg-neutral-100 dark:text-neutral-400 dark:hover:bg-neutral-800"
          >
            &times;
          </button>

          <div class="pr-12">
            <p class="text-sm text-neutral-500 dark:text-neutral-400">Support-Foto</p>
            <h3 class="mt-1 text-xl font-bold text-neutral-900 dark:text-white">
              {{ selectedImageTitle }}
            </h3>
          </div>

          <div class="mt-4 flex justify-center">
            <img
              :src="selectedImageUrl"
              alt="Support-Foto Vollansicht"
              class="max-h-[80vh] w-auto max-w-full rounded-2xl object-contain"
            />
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
