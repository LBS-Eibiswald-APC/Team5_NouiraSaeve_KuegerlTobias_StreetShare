<script setup>
import { ref, watch } from "vue";
import {useRequestStore} from "@/store/requestStore.js";
import {useToast} from "vue-toast-notification";
const $toast = useToast()
const requestStore = useRequestStore()

const props = defineProps({
  showModal: {
    type: Boolean,
    default: false
  },
  tool: {
    type: Object,
    default: null
  }
});

const emit = defineEmits(["closeModal", "submit"]);

function getLocalDateTimeValue(date = new Date()) {
  const pad = (n) => String(n).padStart(2, "0");

  const year = date.getFullYear();
  const month = pad(date.getMonth() + 1);
  const day = pad(date.getDate());
  const hours = pad(date.getHours());
  const minutes = pad(date.getMinutes());

  return `${year}-${month}-${day}T${hours}:${minutes}`;
}

const request = ref({
  message: "",
  tool_id: null,
  start_date: getLocalDateTimeValue(),
  end_date: getLocalDateTimeValue()
});

watch(
    () => props.showModal,
    (isOpen) => {
      if (isOpen) {
        request.value = {
          message: "",
          tool_id: props.tool?.id ?? null,
          start_date: getLocalDateTimeValue(),
          end_date: getLocalDateTimeValue()
        };
      }
    }
);

function close() {
  emit("closeModal");
}

async function submitRequest() {
  if (!props.tool?.id) return;
  if (request.value.message && request.value.start_date && request.value.end_date) {
    const payload = {
      tool_id: props.tool.id,
      message: request.value.message,
      start_date: request.value.start_date,
      end_date: request.value.end_date
    };

    const resp = await requestStore.createRequest(payload)
    emit("submit", resp);
    emit("closeModal");
  } else {
    $toast.error("Alle Pflichtfelder ausfüllen!", {"position": "top-right"})
  }


}
</script>

<template>
  <transition name="fade">
    <div v-if="showModal" class="fixed inset-0 z-[60] flex items-center justify-center px-4">
      <div
          class="absolute inset-0 bg-black/50 backdrop-blur-sm"
          @click="close"
      ></div>

      <div
          @click.stop
          class="relative w-full max-w-lg rounded-[28px] border border-neutral-200 bg-white p-6 shadow-xl dark:border-neutral-800 dark:bg-neutral-900"
      >
        <button
            @click="close"
            class="absolute right-4 top-4 flex h-10 w-10 items-center justify-center rounded-full text-neutral-500 hover:bg-neutral-100 dark:text-neutral-400 dark:hover:bg-neutral-800 transition"
        >
          &times;
        </button>

        <div class="pr-10">
          <p class="text-sm text-neutral-500 dark:text-neutral-400">Neue Anfrage</p>
          <h2 class="mt-1 text-2xl font-bold tracking-tight text-black dark:text-white">
            {{ tool?.name || "Tool" }}
          </h2>
          <p class="mt-2 text-sm text-neutral-600 dark:text-neutral-400">
            Anbieter: {{ tool?.creator_display_name || "-" }}
          </p>
        </div>

        <div class="mt-6 grid grid-cols-2 gap-6">
          <div>
            <label class="mb-2 block text-sm font-medium text-neutral-700 dark:text-neutral-300">
              Ausleihen beginnen *
            </label>
            <input
                v-model="request.start_date"
                class="w-full rounded-2xl border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-950 px-4 py-3 text-neutral-900 dark:text-white placeholder-neutral-400 dark:placeholder-neutral-500 focus:outline-none focus:ring-2 focus:ring-lime-400"
                type="datetime-local"
            />
          </div>

          <div>
            <label class="mb-2 block text-sm font-medium text-neutral-700 dark:text-neutral-300">
              Ausleihen bis *
            </label>
            <input
                v-model="request.end_date"
                class="w-full rounded-2xl border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-950 px-4 py-3 text-neutral-900 dark:text-white placeholder-neutral-400 dark:placeholder-neutral-500 focus:outline-none focus:ring-2 focus:ring-lime-400"
                type="datetime-local"
            />
          </div>
        </div>

        <div class="mt-6">
          <label class="mb-2 block text-sm font-medium text-neutral-700 dark:text-neutral-300">
            Nachricht (Treffpunkt) *
          </label>
          <textarea
              v-model="request.message"
              rows="5"
              placeholder="Schreibe deine Anfrage..."
              class="w-full rounded-2xl border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-950 px-4 py-3 text-neutral-900 dark:text-white placeholder-neutral-400 dark:placeholder-neutral-500 focus:outline-none focus:ring-2 focus:ring-lime-400"
          />
        </div>

        <div class="mt-6 flex gap-3">
          <button
              @click="close"
              class="flex-1 rounded-2xl border border-neutral-300 dark:border-neutral-700 px-4 py-3 font-semibold text-neutral-900 dark:text-white hover:bg-neutral-100 dark:hover:bg-neutral-800 transition"
          >
            Abbrechen
          </button>

          <button
              @click="submitRequest"
              class="flex-1 rounded-2xl bg-lime-500 px-4 py-3 font-semibold text-black hover:bg-lime-400 transition"
          >
            Anfrage senden
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