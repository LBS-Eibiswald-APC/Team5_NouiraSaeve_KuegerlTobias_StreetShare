<script setup>
import { onMounted, ref, nextTick } from "vue";
import { useToolsStore } from "@/store/toolsStore";

const toolStore = useToolsStore();
const selectedTool = ref(null);
const showModal = ref(false);

onMounted(() => {
  toolStore.fetchTools();
});

function openToolModal(tool) {
  selectedTool.value = tool;
  showModal.value = true;
}

function closeModal() {
  selectedTool.value = null;
  showModal.value = false;
}

function overlayClick(e) {
  if (e.target === e.currentTarget) closeModal();
}

async function goToPage(page) {
  if (page < 1 || page > toolStore.totalPages) return;
  toolStore.page = page;
  await toolStore.fetchTools();

  scrollToGrid();
}

function scrollToGrid() {
  nextTick(() => {
    const grid = document.querySelector(".md\\:w-3\\/4");
    if (grid) {
      grid.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  });
}

async function applyFilters() {
  toolStore.page = 1;
  await toolStore.fetchTools();
  scrollToGrid();
}
</script>

<template>
  <div class="min-h-screen bg-neutral-950 text-white font-sans px-6 py-10">
    <div class="max-w-7xl mx-auto flex flex-col md:flex-row gap-8 cursor-pointer">
      <div class="md:w-1/4 bg-neutral-900 p-6 rounded-2xl shadow-lg space-y-4 mt-12" style="height: 350px">
        <h2 class="text-xl font-bold text-lime-400 mb-4">Filter</h2>

        <input @keydown.enter="applyFilters" v-model="toolStore.filters.city" placeholder="Stadt"
               class="w-full border border-neutral-700 rounded-xl px-4 py-2 mb-5 bg-neutral-950 text-white placeholder-neutral-500"/>
        <input @keydown.enter="applyFilters" v-model="toolStore.filters.zip" placeholder="PLZ"
               class="w-full border border-neutral-700 rounded-xl px-4 py-2 mb-5 bg-neutral-950 text-white placeholder-neutral-500"/>
        <select @change="applyFilters" v-model="toolStore.filters.country"
                class="w-full border border-neutral-700 rounded-xl px-4 py-2 mb-5 bg-neutral-950 text-white placeholder-neutral-500">
          <option value="">Alle Länder</option>
          <option v-for="c in toolStore.countries" :key="c" :value="c">{{ c }}</option>
        </select>
        <button @click="applyFilters"
                class="w-full bg-lime-400 text-black rounded-xl px-4 py-2 font-semibold hover:scale-105 transition">
          Anwenden
        </button>
      </div>

      <div class="md:w-3/4 flex flex-col gap-4">
        <div class="flex justify-end items-center space-x-3">
          <span>Pro Seite:</span>
          <select v-model="toolStore.perPage" @change="toolStore.changePerPage(toolStore.perPage)"
                  class="bg-neutral-900 text-white rounded-xl px-3 py-1">
            <option value="25">25</option>
            <option value="50">50</option>
            <option value="100">100</option>
          </select>
          <span class="text-neutral-400">({{ toolStore.total }} Einträge)</span>
        </div>

        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-if="toolStore.loading" class="text-center text-neutral-400 text-lg col-span-full">
            Lädt...
          </div>
          <div v-else v-for="tool in toolStore.tools" :key="tool.id"
               class="bg-neutral-900 rounded-2xl shadow-lg p-6 flex flex-col justify-between hover:scale-105 transition cursor-pointer"
               @click="openToolModal(tool)">
            <div>
              <h3 class="text-2xl font-bold text-lime-400">{{ tool.name }}</h3>
              <p class="text-neutral-400 mt-1">{{ tool.tool_condition || 'Zustand unbekannt' }}</p>
            </div>
            <div class="flex justify-between items-center mt-2">
              <span class="font-bold text-lime-400">{{ tool.deposit ?? 0 }}€ Pfand</span>
            </div>
            <div class="flex justify-between items-center mt-2">
              <button
                  class="bg-lime-400 text-black px-4 py-2 rounded-xl font-semibold hover:scale-105 transition cursor-pointer">
                Anfragen
              </button>
            </div>
            <p class="text-xs text-neutral-500 mt-2">
              {{ tool.creator_city }}, {{ tool.creator_country }} - {{ tool.creator_display_name }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto mt-6 flex justify-center items-center space-x-3">
      <button @click="goToPage(toolStore.page - 1)"
              :disabled="toolStore.page <= 1"
              class="px-3 py-1 rounded-xl bg-neutral-800 hover:bg-neutral-700 transition">
        &lt; Zurück
      </button>
      <span class="text-neutral-400">Seite {{ toolStore.page }} von {{ toolStore.totalPages }}</span>
      <button @click="goToPage(toolStore.page + 1)"
              :disabled="toolStore.page >= toolStore.totalPages"
              class="px-3 py-1 rounded-xl bg-neutral-800 hover:bg-neutral-700 transition">
        Weiter &gt;
      </button>
    </div>

    <transition name="fade">
      <div v-if="showModal" class="fixed inset-0 z-50 flex justify-center items-center">
        <div class="absolute inset-0 bg-black bg-opacity-70 backdrop-blur-sm" @click="closeModal"></div>
        <div @click.stop
             class="relative bg-neutral-900 text-white rounded-3xl p-8 w-11/12 max-w-3xl shadow-2xl transform scale-105 transition-all">
          <button @click="closeModal"
                  class="absolute top-4 right-4 text-neutral-400 hover:text-white text-3xl font-bold">&times;
          </button>

          <h2 class="text-3xl font-bold text-lime-400">{{ selectedTool?.name }}</h2>
          <p class="text-neutral-400">Zustand: {{ selectedTool?.tool_condition || 'Unbekannt' }}</p>
          <p class="text-neutral-400">Pfand: {{ selectedTool?.deposit ?? 0 }}€</p>
          <p class="text-neutral-400 mb-2">Von: {{ selectedTool?.creator_display_name }}
            <span v-if="selectedTool.creator_city">({{ selectedTool?.creator_city }}, {{

                selectedTool?.creator_country }})</span>
          </p>
          <p class="text-neutral-400 mt-4">{{ selectedTool?.description || 'Keine Beschreibung vorhanden' }}</p>
          <button class="mt-6 bg-lime-400 text-black px-6 py-3 rounded-xl font-semibold hover:scale-105 transition">
            Anfragen
          </button>
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