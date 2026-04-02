<script setup>
import {onMounted, ref} from "vue";
import ConfirmationPopUp from "@/components/PopUp/ConfirmationPopUp.vue";
import {useRequestStore} from "@/store/requestStore.js";

const requestStore = useRequestStore();
const requests = ref([]);
const showModal = ref(false);
const showMessageModal = ref(false);
const selectedRequest = ref(null);

async function loadRequests() {
  return await requestStore.getMe();
}

onMounted(async () => {
  requests.value = await loadRequests();
});

function openConfirmModal(request) {
  selectedRequest.value = request;
  showModal.value = true;
}

function openMessageModal(request) {
  selectedRequest.value = request;
  showMessageModal.value = true;
}

function onConfirm(result) {
  showModal.value = false;
  selectedRequest.value = null;
}
</script>

<template>
  <div
      class="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-3xl shadow-xl p-6"
  >

    <div class="flex items-center justify-between flex-wrap gap-4 mb-6">
      <div>
        <h1 class="text-3xl tracking-tight font-bold text-neutral-900 dark:text-white">
          Anfragen
        </h1>
        <p class="text-neutral-500 dark:text-neutral-400 mt-1">
          Verwalte eingehende Anfragen für deine Tools
        </p>
      </div>

      <div
          class="px-4 py-2 rounded-2xl bg-lime-100 dark:bg-lime-500/10 text-lime-700 dark:text-lime-400 font-semibold"
      >
        {{ requests.length }} Anfragen<span v-if="requests.length !== 1"></span>
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
              <span>Leiher</span>
            </div>
          </th>

          <th class="py-4 px-5 font-semibold text-neutral-700 dark:text-neutral-300 text-center">
            <div class="flex items-center justify-center gap-2">
              <BIconChatDots/>
              <span>Nachricht</span>
            </div>
          </th>

          <th class="py-4 px-5 font-semibold text-neutral-700 dark:text-neutral-300 text-center">
            Aktion
          </th>
        </tr>
        </thead>

        <tbody>
        <tr
            v-for="request in requests"
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
            <div class="flex justify-center">
              <button
                  @click="openMessageModal(request)"
                  class="flex items-center justify-center w-10 h-10 rounded-xl bg-neutral-200 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 hover:bg-lime-100 hover:text-lime-700 dark:hover:bg-lime-500/10 dark:hover:text-lime-400 transition"
              >
                <BIconChatDots class="text-lg"/>
              </button>
            </div>
          </td>

          <td class="py-4 px-5">
            <div class="flex items-center justify-center gap-3">
              <button
                  class="flex items-center gap-2 px-4 py-2 rounded-xl bg-lime-500 hover:bg-lime-400 text-black font-semibold transition hover:scale-105"
              >
                <BIconCheckCircle/>
                <span>Akzeptieren</span>
              </button>

              <button
                  @click="openConfirmModal(request)"
                  class="flex items-center gap-2 px-4 py-2 rounded-xl bg-red-500/90 hover:bg-red-500 text-white font-semibold transition hover:scale-105"
              >
                <BIconXCircle/>
                <span>Ablehnen</span>
              </button>

              <button
                  class="flex items-center gap-2 px-4 py-2 rounded-xl bg-neutral-200 dark:bg-neutral-800 hover:bg-neutral-300 dark:hover:bg-neutral-700 text-neutral-900 dark:text-white font-semibold transition hover:scale-105"
              >
                <BIconArrowLeftRight/>
                <span>Gegenangebot</span>
              </button>
            </div>
          </td>
        </tr>

        <tr v-if="requests.length === 0">
          <td colspan="4" class="py-14 text-center">
            <div class="flex flex-col items-center justify-center gap-3 text-neutral-500 dark:text-neutral-400">
              <div
                  class="w-16 h-16 rounded-2xl bg-neutral-200 dark:bg-neutral-800 flex items-center justify-center"
              >
                <BIconChatDots class="text-2xl"/>
              </div>
              <p class="text-lg font-medium">Keine Anfragen vorhanden</p>
              <p class="text-sm">Sobald jemand ein Tool anfragt, siehst du es hier.</p>
            </div>
          </td>
        </tr>
        </tbody>
      </table>
    </div>

    <transition name="fade">
      <div
          v-if="showMessageModal"
          class="fixed inset-0 z-[60] flex items-center justify-center px-4"
      >
        <!-- Overlay -->
        <div
            class="absolute inset-0 bg-black/50 backdrop-blur-sm"
            @click="showMessageModal = false"
        ></div>

        <!-- Modal -->
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