<script setup>
import {useAuthStore} from "@/store/authStore.js";
import {onMounted, ref} from "vue";
import ConfirmationPopUp from "@/components/PopUp/ConfirmationPopUp.vue";

const authStore = useAuthStore()

const requests = ref({

})

async function loadRequests() {
  await authStore.getMe()
}

onMounted(async () => {
  await loadRequests();
});

const showModal = ref(false)

function onConfirm(result) {
  showModal.value = false
}
</script>

<template>
  <div class="min-h-screen dark:text-white flex justify-center overflow-auto">
    <div
        class="w-full mx-auto bg-white dark:bg-neutral-900 p-8 rounded-2xl shadow-xl border border-neutral-200 dark:border-neutral-800 space-y-6">
      <h3 class="text-lime-500 dark:text-lime-400 font-bold">
        Öffentliche Daten
      </h3>
      <div class="grid grid-cols-12 gap-4">
        <div class="col-span-12 md:col-span-6">
          <div>
            <label class="block text-sm mb-2 text-neutral-700 dark:text-neutral-400">Vorname</label>
            <input

                type="text"
                placeholder="Max"
                class="w-full bg-white text-neutral-900 placeholder:text-neutral-400 border border-neutral-300 dark:bg-neutral-800 dark:text-white dark:placeholder:text-neutral-500 dark:border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"
            />
          </div>
        </div>
        <div class="col-span-12 md:col-span-6">
          <div>
            <label class="block text-sm mb-2 text-neutral-700 dark:text-neutral-400">Nachname</label>
            <input
              
                type="text"
                placeholder="Mustermann"
                class="w-full bg-white text-neutral-900 placeholder:text-neutral-400 border border-neutral-300 dark:bg-neutral-800 dark:text-white dark:placeholder:text-neutral-500 dark:border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"
            />
          </div>
        </div>
        <div class="col-span-12 md:col-span-6">
          <div>
            <label class="block text-sm mb-2 text-neutral-700 dark:text-neutral-400">Anzeigename</label>
            <input

                type="text"
                placeholder="max_mustermann"
                class="w-full bg-white text-neutral-900 placeholder:text-neutral-400 border border-neutral-300 dark:bg-neutral-800 dark:text-white dark:placeholder:text-neutral-500 dark:border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"
            />
          </div>
        </div>
      </div>
      <div class="grid grid-cols-12 gap-4">
        <div class="col-span-12">
          <button @click="showModal = true" class="w-full bg-lime-400 text-black py-3 rounded-lg font-semibold hover:scale-[1.02] transition disabled:opacity-50 disabled:cursor-not-allowed">Speichern</button>
        </div>
      </div>
    </div>
    <ConfirmationPopUp
        v-if="showModal"
        title="Speichern?"
        message="Willst du die Änderungen speichern?"
        @close="showModal = false"
        @confirm="onConfirm"
    />
  </div>
</template>
<style scoped>
</style>