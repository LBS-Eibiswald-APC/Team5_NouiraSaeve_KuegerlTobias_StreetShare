<script setup>
import {computed, ref} from "vue";

const props = defineProps({
  showModal: {
    type: Boolean,
    default: false,
  },
  amount: {
    type: Number,
    default: 0,
  },
  toolName: {
    type: String,
    default: "",
  },
  loading: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["close", "confirm"]);

const paypalEmail = ref("");

const formattedAmount = computed(() => {
  return new Intl.NumberFormat("de-DE", {
    style: "currency",
    currency: "EUR",
  }).format(props.amount || 0);
});

function closeModal() {
  if (!props.loading) {
    emit("close");
    paypalEmail.value = "";
  }
}

function confirmPayment() {
  emit("confirm", {
    paypal_email: paypalEmail.value,
  });
}
</script>

<template>
  <transition name="fade">
    <div
        v-if="showModal"
        class="fixed inset-0 z-[70] flex items-center justify-center px-4"
    >
      <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="closeModal"></div>

      <div
          class="relative z-10 w-full max-w-md rounded-[28px] border border-neutral-200 bg-white p-6 shadow-xl dark:border-neutral-800 dark:bg-neutral-900"
      >
        <button
            @click="closeModal"
            class="absolute right-4 top-4 flex h-10 w-10 items-center justify-center rounded-full text-neutral-500 transition hover:bg-neutral-100 dark:text-neutral-400 dark:hover:bg-neutral-800"
        >
          &times;
        </button>

        <p class="text-sm font-semibold uppercase tracking-[0.18em] text-sky-500">
          Fake PayPal
        </p>
        <h2 class="mt-2 text-2xl font-bold text-neutral-900 dark:text-white">
          Zahlung bestätigen
        </h2>
        <p class="mt-2 text-sm text-neutral-500 dark:text-neutral-400">
          Du zahlst das Pfand für <span class="font-semibold text-neutral-900 dark:text-white">{{ toolName }}</span>.
        </p>

        <div class="mt-5 rounded-2xl bg-sky-50 px-4 py-4 dark:bg-sky-500/10">
          <p class="text-sm text-neutral-500 dark:text-neutral-400">Pfandbetrag</p>
          <p class="mt-1 text-3xl font-bold text-sky-600 dark:text-sky-300">
            {{ formattedAmount }}
          </p>
        </div>

        <div class="mt-5">
          <label class="mb-2 block text-sm font-medium text-neutral-700 dark:text-neutral-300">
            PayPal E-Mail
          </label>
          <input
              v-model="paypalEmail"
              type="email"
              placeholder="name@paypal.com"
              class="w-full rounded-2xl border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-950 px-4 py-3 text-neutral-900 dark:text-white placeholder-neutral-400 dark:placeholder-neutral-500 focus:outline-none focus:ring-2 focus:ring-sky-400"
          />
        </div>

        <div class="mt-6 flex justify-end gap-3">
          <button
              @click="closeModal"
              :disabled="loading"
              class="px-4 py-2 rounded-xl border border-neutral-300 dark:border-neutral-700 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-800 transition disabled:opacity-50"
          >
            Abbrechen
          </button>

          <button
              @click="confirmPayment"
              :disabled="loading || !paypalEmail.trim()"
              class="px-4 py-2 rounded-xl bg-sky-500 text-white font-semibold hover:bg-sky-400 transition disabled:opacity-50"
          >
            {{ loading ? "Zahle..." : "Jetzt bezahlen" }}
          </button>
        </div>
      </div>
    </div>
  </transition>
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
