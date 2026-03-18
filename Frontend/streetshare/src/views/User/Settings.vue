<script setup>
import {useAuthStore} from "@/store/authStore.js";
import {onMounted, ref} from "vue";
import ConfirmationPopUp from "@/components/PopUp/ConfirmationPopUp.vue";

const authStore = useAuthStore()

const user = ref({
  first_name: '',
  last_name: '',
  display_name: '',
  phone: '',
  street: '',
  house_nr: '',
  city: '',
  zip: ''
})

async function loadUser() {
  await authStore.getMe()
  user.value = authStore.user
}

onMounted(async () => {
  await loadUser();
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
                v-model="user.first_name"
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
                v-model="user.last_name"
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
                v-model="user.display_name"
                type="text"
                placeholder="max_mustermann"
                class="w-full bg-white text-neutral-900 placeholder:text-neutral-400 border border-neutral-300 dark:bg-neutral-800 dark:text-white dark:placeholder:text-neutral-500 dark:border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"
            />
          </div>
        </div>
        <div class="col-span-12 md:col-span-6">
          <div>
            <label class="block text-sm mb-2 text-neutral-700 dark:text-neutral-400">Telefon</label>
            <input
                v-model="user.phone"
                type="text"
                placeholder="+43 123456789"
                class="w-full bg-white text-neutral-900 placeholder:text-neutral-400 border border-neutral-300 dark:bg-neutral-800 dark:text-white dark:placeholder:text-neutral-500 dark:border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"
            />
          </div>
        </div>
        <div class="col-span-12 md:col-span-6">
          <div>
            <label class="block text-sm mb-2 text-neutral-700 dark:text-neutral-400">Straße</label>
            <input
                v-model="user.street"
                type="text"
                placeholder="Musterstraße"
                class="w-full bg-white text-neutral-900 placeholder:text-neutral-400 border border-neutral-300 dark:bg-neutral-800 dark:text-white dark:placeholder:text-neutral-500 dark:border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"
            />
          </div>
        </div>
        <div class="col-span-12 md:col-span-6">
          <div>
            <label class="block text-sm mb-2 text-neutral-700 dark:text-neutral-400">Hausnummer</label>
            <input
                v-model="user.house_nr"
                type="text"
                placeholder="1"
                class="w-full bg-white text-neutral-900 placeholder:text-neutral-400 border border-neutral-300 dark:bg-neutral-800 dark:text-white dark:placeholder:text-neutral-500 dark:border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"
            />
          </div>
        </div>
        <div class="col-span-12 md:col-span-6">
          <div>
            <label class="block text-sm mb-2 text-neutral-700 dark:text-neutral-400">Stadt</label>
            <input
                v-model="user.city"
                type="text"
                placeholder="Wien"
                class="w-full bg-white text-neutral-900 placeholder:text-neutral-400 border border-neutral-300 dark:bg-neutral-800 dark:text-white dark:placeholder:text-neutral-500 dark:border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"
            />
          </div>
        </div>
        <div class="col-span-12 md:col-span-6">
          <div>
            <label class="block text-sm mb-2 text-neutral-700 dark:text-neutral-400">PLZ</label>
            <input
                v-model="user.zip"
                type="text"
                placeholder="1010"
                class="w-full bg-white text-neutral-900 placeholder:text-neutral-400 border border-neutral-300 dark:bg-neutral-800 dark:text-white dark:placeholder:text-neutral-500 dark:border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"
            />
          </div>
        </div>
      </div>
      <h3 class="text-lime-500 dark:text-lime-400 font-bold">
        Private Daten
      </h3>
      <div class="grid grid-cols-12 gap-4">
        <div class="col-span-12 md:col-span-6">
          <div>
            <label class="block text-sm mb-2 text-neutral-700 dark:text-neutral-400">E-Mail</label>
            <input
                v-model="user.email"
                type="text"
                placeholder="max.mustermann@gmail.com"
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