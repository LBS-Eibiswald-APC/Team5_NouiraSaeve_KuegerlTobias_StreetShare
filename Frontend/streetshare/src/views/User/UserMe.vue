<script setup>
import {ref, computed, watch, onMounted} from "vue";
import {useToolsStore} from "@/store/toolsStore";
import {useAuthStore} from "@/store/authStore.js";

const toolStore = useToolsStore();
const authStore = useAuthStore();
const showModal = ref(false);

const newTool = ref({
  name: "",
  description: "",
  base_price: 0,
  tool_condition: "Neu",
  deposit: 0,
});

const conditions = ["Neu", "Minimal abgenutzt", "Gebraucht", "Gut abgenutzt", "Defekt"];
const activeTab = ref("entries");

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

async function saveTool() {
  calcDeposit()
  if (await toolStore.createTool(newTool.value)) {
    myTools.value = await toolStore.getUserTools();
  }
  showModal.value = false;
  newTool.value = {name: "", description: "", base_price: 0, tool_condition: "Neu", deposit: 0};
}

const myTools = ref([]);

onMounted(async () => {
  myTools.value = await toolStore.getUserTools();
});

watch(activeTab, async (newVal) => {
  if (newVal === "entries") {
    myTools.value = await toolStore.getUserTools();
  }
});
watch(showModal, async (newVal) => {
  if (!newVal) {
    newTool.value = {name: "", description: "", base_price: 0, tool_condition: "Neu", deposit: 0};
  }
})
</script>

<template>
  <div class="min-h-screen bg-neutral-950 text-white font-sans px-6 py-10 flex gap-6">
    <!-- Sidebar -->
    <nav class="w-64 bg-neutral-900 rounded-2xl p-6 flex flex-col gap-4 ml-20 ">
      <h2 class="text-xl font-bold text-lime-400 mb-2">Dashboard</h2>
      <button @click="activeTab = 'entries'"
              :class="{'bg-lime-400 text-black': activeTab==='entries'}"
              class="text-white px-4 py-2 rounded-xl hover:bg-lime-500 transition text-left cursor-pointer">
        Meine Einträge
      </button>
      <button @click="activeTab = 'deposit'"
              :class="{'bg-lime-400 text-black': activeTab==='deposit'}"
              class="text-white px-4 py-2 rounded-xl hover:bg-lime-500 transition text-left cursor-pointer">
        Mein Pfand
      </button>
      <button @click="activeTab = 'transactions'"
              :class="{'bg-lime-400 text-black': activeTab==='transactions'}"
              class="text-white px-4 py-2 rounded-xl hover:bg-lime-500 transition text-left cursor-pointer">
        Meine Transaktionen
      </button>
    </nav>

    <!-- Content -->
    <div class="flex-1 flex flex-col gap-6">
      <!-- Einträge Tab -->
      <div v-if="activeTab === 'entries'" class="flex flex-col gap-4">
        <button @click="showModal = true"
                class="bg-lime-400 text-black rounded-xl px-4 py-2 font-semibold hover:scale-105 transition w-48">
          Eintrag hinzufügen
        </button>

        <!-- Tools Tabelle -->
        <div class="overflow-x-auto bg-neutral-900 rounded-2xl p-4">
          <table class="w-full text-left">
            <thead>
            <tr class="border-b border-neutral-700">
              <th class="py-2 px-4">Name</th>
              <th class="py-2 px-4">Beschreibung</th>
              <th class="py-2 px-4">Preis</th>
              <th class="py-2 px-4">Kondition</th>
              <th class="py-2 px-4">Pfand</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="tool in myTools" :key="tool.id" class="border-b border-neutral-700 hover:bg-neutral-800">
              <td class="py-2 px-4">{{ tool.name }}</td>
              <td class="py-2 px-4">{{ tool.description }}</td>
              <td class="py-2 px-4">{{ tool.base_price }} €</td>
              <td class="py-2 px-4">{{ tool.tool_condition }}</td>
              <td class="py-2 px-4">{{ tool.deposit }} €</td>
              <td class="py-2 px-4">
                <div class="w-9 h-9 flex items-center justify-center rounded-full
              hover:bg-neutral-700 transition cursor-pointer">
                  <svg xmlns="http://www.w3.org/2000/svg"
                       fill="none"
                       viewBox="0 0 24 24"
                       stroke-width="1.5"
                       stroke="currentColor"
                       class="w-5 h-5">
                    <path stroke-linecap="round"
                          stroke-linejoin="round"
                          d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L6.832 19.82a4.5 4.5 0 0 1-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 0 1 1.13-1.897L16.863 4.487Zm0 0L19.5 7.125"/>
                  </svg>
                </div>
              </td>
              <td class="py-2 px-4">
                <div class="w-9 h-9 flex items-center justify-center rounded-full
              hover:bg-red-600/20 hover:text-red-400
              transition cursor-pointer">
                  <svg xmlns="http://www.w3.org/2000/svg"
                       fill="none"
                       viewBox="0 0 24 24"
                       stroke-width="1.5"
                       stroke="currentColor"
                       class="w-5 h-5">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                         stroke="currentColor" class="size-6">
                      <path stroke-linecap="round" stroke-linejoin="round"
                            d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0"/>
                    </svg>
                  </svg>
                </div>
              </td>
            </tr>
            <tr v-if="myTools.length === 0">
              <td colspan="5" class="py-4 text-center text-neutral-400">Keine Einträge vorhanden</td>
            </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Mein Pfand -->
      <div v-if="activeTab === 'deposit'" class="text-neutral-400">
        Hier siehst du dein gesamtes Pfand. (Implementierung folgt)
      </div>

      <!-- Meine Transaktionen -->
      <div v-if="activeTab === 'transactions'" class="text-neutral-400">
        Hier siehst du deine Transaktionen. (Implementierung folgt)
      </div>
    </div>

    <!-- Modal -->
    <transition name="fade">
      <div v-if="showModal" class="fixed inset-0 z-50 flex justify-center items-center">
        <div class="absolute inset-0 bg-black bg-opacity-70 backdrop-blur-sm" @click="showModal = false"></div>
        <div @click.stop
             class="relative bg-neutral-900 text-white rounded-3xl p-8 w-11/12 max-w-lg shadow-2xl transition-all">
          <button @click="showModal = false"
                  class="absolute top-4 right-4 text-neutral-400 hover:text-white text-3xl font-bold">&times;
          </button>

          <h2 class="text-2xl font-bold text-lime-400 mb-4">Neues Tool</h2>

          <div class="flex flex-col gap-3">
            <p>Name:</p>
            <input v-model="newTool.name" placeholder="Name" class="px-4 py-2 rounded-xl bg-neutral-800 text-white"/>
            <p>Beschreibung:</p>
            <textarea rows="4" v-model="newTool.description" placeholder="Beschreibung"
                      class="px-4 py-2 rounded-xl bg-neutral-800 text-white"></textarea>
            <p>Preis:</p>
            <input v-model.number="newTool.base_price" @input="calcDeposit()" type="number" placeholder="Preis"
                   class="px-4 py-2 rounded-xl bg-neutral-800 text-white"/>
            <p>Kondition:</p>
            <select v-model="newTool.tool_condition" @change="calcDeposit()"
                    class="px-4 py-2 rounded-xl bg-neutral-800 text-white">
              <option v-for="c in conditions" :key="c">{{ c }}</option>
            </select>
            <p>Pfand:</p>
            <input v-model="newTool.deposit" readonly placeholder="Pfand"
                   class="px-4 py-2 rounded-xl bg-neutral-700 text-neutral-400"/>
            <button @click="saveTool"
                    class="bg-lime-400 text-black px-4 py-2 rounded-xl font-semibold hover:scale-105 transition">
              Speichern
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>