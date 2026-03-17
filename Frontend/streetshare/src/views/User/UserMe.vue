<script setup>
import {ref, computed, watch, onMounted} from "vue";
import {useToolsStore} from "@/store/toolsStore";
import {useAuthStore} from "@/store/authStore.js";
import ToolCreate from "@/components/PopUp/ToolCreate.vue";
import ToolEdit from "@/components/PopUp/ToolEdit.vue";
import {useTransactionsStore} from "@/store/transactionsStore.js";

const toolStore = useToolsStore();
const transactionsStore = useTransactionsStore();
const euroFormat = new Intl.NumberFormat('de-DE', {
  style: 'currency',
  currency: 'EUR',
});
const showModal = ref(false);
const showEdit = ref(false);

const newTool = ref({
  id: null,
  name: "",
  description: "",
  base_price: 0,
  tool_condition: "Neu",
  deposit: 0,
});

const activeTab = ref("entries");

const editTool = ref();

const usageFactor = {
  "Neu": 0.35,
  "Minimal abgenutzt": 0.30,
  "Gebraucht": 0.25,
  "Gut abgenutzt": 0.2,
  "Defekt": 0.1,
}

const week_multiplier = 1

function calcDeposit() {
  const factor = usageFactor[newTool.value.tool_condition]
  let deposit = newTool.value.base_price * factor * week_multiplier
  if (newTool.value.base_price < 100) {
    deposit *= 0.8
  } else {
    deposit *= 0.7
  }
  newTool.value.deposit = deposit.toFixed(2);
}

async function loadMyTools() {
  myTools.value = await toolStore.getUserTools();
}

import { useToast } from 'vue-toast-notification'
import Settings from "@/views/User/Settings.vue";

const $toast = useToast()

async function clickedEdit(tool) {
  const req = await transactionsStore.getTransactionsByToolId(tool.id);
  console.log(req)
  if (req && req.length <= 0) {
    editTool.value = tool;
    showEdit.value = true;
  } else {
    $toast.open({
      message: 'Es gibt schon eine Transaktion!',
      type: 'warning'
    })
  }
}

const myTools = ref([]);

onMounted(async () => {
  await loadMyTools();
});

watch(activeTab, async (newVal) => {
  if (newVal === "entries") {
    await loadMyTools();
  }
});
watch(showModal, async (newVal) => {
  if (!newVal) {
    newTool.value = {name: "", description: "", base_price: 0, tool_condition: "Neu", deposit: 0};
  }
})
</script>
<template>
  <div
      class="h-screen overflow-hidden text-neutral-900 dark:text-white font-sans px-6 flex gap-6">
    <!-- Sidebar -->
    <nav
        class="w-60 bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-2xl p-6 flex flex-col gap-y-2 ml-20">
      <h2 class="text-xl font-bold text-lime-600 dark:text-lime-400 mb-2">Dashboard</h2>

      <button
          @click="activeTab = 'entries'"
          :class="activeTab === 'entries'
      ? 'bg-lime-500 text-black'
      : 'bg-transparent text-neutral-800 dark:text-white hover:bg-neutral-100 dark:hover:bg-lime-500/20'"
          class="px-4 py-3 rounded-xl transition text-left cursor-pointer"
      >
        Meine Einträge
      </button>

      <button
          @click="activeTab = 'transactions'"
          :class="activeTab === 'transactions'
      ? 'bg-lime-500 text-black'
      : 'bg-transparent text-neutral-800 dark:text-white hover:bg-neutral-100 dark:hover:bg-lime-500/20'"
          class="px-4 py-3 rounded-xl transition text-left cursor-pointer"
      >
        Meine Transaktionen
      </button>

      <button
          @click="activeTab = 'settings'"
          :class="activeTab === 'settings'
      ? 'bg-lime-500 text-black'
      : 'bg-transparent text-neutral-800 dark:text-white hover:bg-neutral-100 dark:hover:bg-lime-500/20'"
          class="px-4 py-3 rounded-xl transition text-left cursor-pointer mt-auto"
      >
        Settings
      </button>
    </nav>

    <!-- Content -->
    <div class="flex-1 flex flex-col gap-6">
      <!-- Einträge Tab -->
      <div v-if="activeTab === 'entries'" class="flex flex-col gap-4">
        <button
            @click="showModal = true"
            class="bg-lime-500 hover:bg-lime-400 text-black rounded-xl px-4 py-2 font-semibold hover:scale-105 transition w-48"
        >
          Eintrag hinzufügen
        </button>

        <!-- Tools Tabelle -->
        <div
            class="overflow-x-auto bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-2xl p-4 shadow-lg">
          <table class="w-full text-left">
            <thead>
            <tr class="border-b border-neutral-300 dark:border-neutral-700">
              <th class="py-2 px-4">Name</th>
              <th class="py-2 px-4">Beschreibung</th>
              <th class="py-2 px-4">Preis</th>
              <th class="py-2 px-4">Kondition</th>
              <th class="py-2 px-4">Pfand</th>
            </tr>
            </thead>

            <tbody>
            <tr
                v-for="tool in myTools"
                :key="tool.id"
                class="border-b border-neutral-200 dark:border-neutral-700 hover:bg-neutral-100 dark:hover:bg-neutral-800 transition"
            >
              <td class="py-2 px-4">{{ tool.name }}</td>
              <td class="py-2 px-4 text-neutral-700 dark:text-neutral-300">{{ tool.description }}</td>
              <td class="py-2 px-4">{{ euroFormat.format(tool.base_price) }}</td>
              <td class="py-2 px-4 text-neutral-700 dark:text-neutral-300">{{ tool.tool_condition }}</td>
              <td class="py-2 px-4 font-medium text-lime-600 dark:text-lime-400">{{
                  euroFormat.format(tool.deposit)
                }}
              </td>

              <td class="py-2 px-4">
                <div
                    @click="clickedEdit(tool)"
                    class="w-9 h-9 flex items-center justify-center rounded-full hover:bg-neutral-200 dark:hover:bg-neutral-700 transition cursor-pointer"
                >
                  <svg
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke-width="1.5"
                      stroke="currentColor"
                      class="w-5 h-5"
                  >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L6.832 19.82a4.5 4.5 0 0 1-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 0 1 1.13-1.897L16.863 4.487Zm0 0L19.5 7.125"
                    />
                  </svg>
                </div>
              </td>

              <td class="py-2 px-4">
                <div
                    class="w-9 h-9 flex items-center justify-center rounded-full hover:bg-red-100 hover:text-red-600 dark:hover:bg-red-600/20 dark:hover:text-red-400 transition cursor-pointer"
                >
                  <svg
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke-width="1.5"
                      stroke="currentColor"
                      class="w-5 h-5"
                  >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0"
                    />
                  </svg>
                </div>
              </td>
            </tr>

            <tr v-if="myTools.length === 0">
              <td colspan="7" class="py-4 text-center text-neutral-500 dark:text-neutral-400">
                Keine Einträge vorhanden
              </td>
            </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Modal MyTools -->
      <ToolCreate :new-tool="newTool" :show-modal="showModal" :usage-factor="usageFactor"
                  :week_multiplier="week_multiplier" :tool-store="toolStore" @close="showModal = false"
                  @saved="loadMyTools"/>
      <ToolEdit
          :edit-tool="editTool" :show-modal="showEdit" :usage-factor="usageFactor"
          :week_multiplier="week_multiplier" :tool-store="toolStore" @close="showEdit = false"
          @saved="loadMyTools"
      />
      <!-- Meine Transaktionen -->
      <div v-if="activeTab === 'transactions'" class="text-neutral-600 dark:text-neutral-400">
        Hier siehst du deine Transaktionen. (Implementierung folgt)
      </div>

      <!-- Settings -->
      <div v-if="activeTab === 'settings'" class="text-neutral-600 dark:text-neutral-400">
        <Settings/>
      </div>

    </div>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>