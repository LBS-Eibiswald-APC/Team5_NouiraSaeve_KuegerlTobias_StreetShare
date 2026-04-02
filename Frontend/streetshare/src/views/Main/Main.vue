<script setup>
import { computed, nextTick, onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useToolsStore } from "@/store/toolsStore";
import { useDashboardStore } from "@/store/dashboardStore";
import api from "@/services/api";

const toolStore = useToolsStore();
const dashboardStore = useDashboardStore();
const router = useRouter();

const selectedTool = ref(null);
const showModal = ref(false);
const showImageModal = ref(false);

const euroFormat = new Intl.NumberFormat("de-DE", {
  style: "currency",
  currency: "EUR",
});

onMounted(() => {
  if (!toolStore.filters.name) {
    toolStore.filters.name = "";
  }
  toolStore.fetchTools();
});

const selectedToolImageUrl = computed(() => {
  if (!selectedTool.value?.id) {
    return "";
  }

  return `${api.defaults.baseURL}/tools/image/${selectedTool.value.id}`;
});

function getToolImageUrl(toolId) {
  if (!toolId) {
    return "";
  }

  return `${api.defaults.baseURL}/tools/image/${toolId}`;
}

function openToolModal(tool) {
  selectedTool.value = tool;
  showModal.value = true;
  showImageModal.value = false;
}

function closeModal() {
  selectedTool.value = null;
  showModal.value = false;
  showImageModal.value = false;
}

function openImageModal() {
  if (!selectedToolImageUrl.value) {
    return;
  }

  showImageModal.value = true;
}

function closeImageModal() {
  showImageModal.value = false;
}

async function goToPage(page) {
  if (page < 1 || page > toolStore.totalPages) {
    return;
  }

  toolStore.page = page;
  await toolStore.fetchTools();
  scrollToGrid();
}

function scrollToGrid() {
  nextTick(() => {
    const grid = document.querySelector("#tools-grid");
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

async function resetFilters() {
  toolStore.filters.name = "";
  toolStore.filters.city = "";
  toolStore.filters.zip = "";
  toolStore.filters.country = "";
  toolStore.page = 1;
  await toolStore.fetchTools();
  scrollToGrid();
}

function onSearchChange(event) {
  if (event.target.value.trim().length === 0) {
    applyFilters();
  }
}

async function startRequestInChat(tool) {
  if (!tool?.id) {
    return;
  }

  sessionStorage.setItem("pendingChatRequest", JSON.stringify({
    toolId: tool.id,
    toolName: tool.name,
    creatorName: tool.creator_display_name,
    deposit: tool.deposit,
  }));

  dashboardStore.startChatRequest(tool.id);
  showModal.value = false;
  showImageModal.value = false;

  await router.push({ name: "dashboard" });
}
</script>

<template>
  <div class="min-h-screen px-4 dark:text-white sm:px-6 xl:px-10 2xl:px-12">
    <div class="mx-auto w-full max-w-[1800px]">
      <div class="mt-5 grid grid-cols-1 gap-6 xl:grid-cols-[280px_minmax(0,1fr)] 2xl:grid-cols-[320px_minmax(0,1fr)]">
        <aside class="lg:self-start">
          <div class="h-fit rounded-[1.75rem] border border-neutral-200/80 bg-white/90 p-5 shadow-sm backdrop-blur-sm dark:border-neutral-800/80 dark:bg-neutral-900/85 xl:sticky xl:top-5 xl:p-6">
            <div class="mb-4 flex items-start justify-between gap-3">
              <h2 class="text-lg font-semibold text-black dark:text-white">Filter</h2>
              <button
                @click="resetFilters"
                class="text-sm text-neutral-500 transition hover:text-black dark:text-neutral-400 dark:hover:text-white"
              >
                Zurücksetzen
              </button>
            </div>

            <div class="space-y-3">
              <div>
                <label class="mb-2 block text-sm font-medium text-neutral-600 dark:text-neutral-300">
                  Stadt
                </label>
                <input
                  v-model="toolStore.filters.city"
                  @keydown.enter="applyFilters"
                  placeholder="z. B. Graz"
                  class="w-full rounded-2xl border border-neutral-300 bg-white px-4 py-3 text-neutral-900 placeholder-neutral-400 focus:outline-none focus:ring-2 focus:ring-lime-400 dark:border-neutral-700 dark:bg-neutral-950 dark:text-white dark:placeholder-neutral-500"
                />
              </div>

              <div>
                <label class="mb-2 block text-sm font-medium text-neutral-600 dark:text-neutral-300">
                  PLZ
                </label>
                <input
                  v-model="toolStore.filters.zip"
                  @keydown.enter="applyFilters"
                  placeholder="z. B. 8010"
                  class="w-full rounded-2xl border border-neutral-300 bg-white px-4 py-3 text-neutral-900 placeholder-neutral-400 focus:outline-none focus:ring-2 focus:ring-lime-400 dark:border-neutral-700 dark:bg-neutral-950 dark:text-white dark:placeholder-neutral-500"
                />
              </div>

              <div>
                <label class="mb-2 block text-sm font-medium text-neutral-600 dark:text-neutral-300">
                  Land
                </label>
                <select
                  v-model="toolStore.filters.country"
                  class="w-full rounded-2xl border border-neutral-300 bg-white px-4 py-3 text-neutral-900 focus:outline-none focus:ring-2 focus:ring-lime-400 dark:border-neutral-700 dark:bg-neutral-950 dark:text-white"
                >
                  <option value="">Alle Länder</option>
                  <option v-for="country in toolStore.countries" :key="country" :value="country">
                    {{ country }}
                  </option>
                </select>
              </div>

              <button
                @click="applyFilters"
                class="w-full rounded-2xl bg-neutral-950 px-4 py-3 font-semibold text-white transition hover:opacity-90 dark:bg-white dark:text-black"
              >
                Filter anwenden
              </button>
            </div>
          </div>
        </aside>

        <section id="tools-grid" class="space-y-4">
          <div class="overflow-hidden rounded-[1.75rem] border border-neutral-200/80 bg-white/90 shadow-sm backdrop-blur-sm dark:border-neutral-800/80 dark:bg-neutral-900/85">
            <div class="flex flex-col gap-3 p-4 sm:p-5 xl:flex-row xl:items-center">
              <div class="relative flex-1">
                <span class="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-neutral-400 dark:text-neutral-500">
                  <svg class="h-5 w-5" viewBox="0 0 20 20" fill="none" aria-hidden="true">
                    <path d="M14.1667 14.1667L17.5 17.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
                    <circle cx="8.75" cy="8.75" r="5.75" stroke="currentColor" stroke-width="1.8"/>
                  </svg>
                </span>

                <input
                  v-model="toolStore.filters.name"
                  @keydown.enter="applyFilters"
                  @input="onSearchChange"
                  type="search"
                  placeholder="Nach Tool suchen..."
                  class="w-full rounded-2xl border border-neutral-300 bg-white py-3 pl-12 pr-4 text-neutral-900 placeholder-neutral-400 focus:outline-none focus:ring-2 focus:ring-lime-400 dark:border-neutral-700 dark:bg-neutral-950 dark:text-white dark:placeholder-neutral-500"
                />
              </div>

              <div class="flex flex-col gap-3 sm:flex-row xl:flex-none xl:items-center">
                <div class="flex items-center justify-between gap-3 rounded-2xl border border-neutral-200 bg-neutral-50 px-4 py-3 dark:border-neutral-800 dark:bg-neutral-900">
                  <span class="text-sm font-medium text-neutral-600 dark:text-neutral-300">Pro Seite</span>
                  <select
                    v-model="toolStore.perPage"
                    @change="toolStore.changePerPage(toolStore.perPage)"
                    class="rounded-xl border border-neutral-300 bg-white px-3 py-2 text-sm text-neutral-900 dark:border-neutral-700 dark:bg-neutral-950 dark:text-white"
                  >
                    <option value="25">25</option>
                    <option value="50">50</option>
                    <option value="100">100</option>
                  </select>
                </div>
              </div>
            </div>
          </div>

          <div class="grid gap-6 lg:grid-cols-2 2xl:grid-cols-3">
            <div
              v-if="toolStore.loading"
              class="col-span-full rounded-[1.75rem] border border-dashed border-neutral-300 bg-white/90 p-10 text-center text-neutral-500 shadow-sm dark:border-neutral-700 dark:bg-neutral-900/85 dark:text-neutral-400"
            >
              Lädt...
            </div>

            <div
              v-else-if="toolStore.tools.length === 0"
              class="col-span-full rounded-[1.75rem] border border-dashed border-neutral-300 bg-white/90 p-10 text-center text-neutral-500 shadow-sm dark:border-neutral-700 dark:bg-neutral-900/85 dark:text-neutral-400"
            >
              Keine Tools gefunden.
            </div>

            <article
              v-else
              v-for="tool in toolStore.tools"
              :key="tool.id"
              @click="openToolModal(tool)"
              class="group cursor-pointer overflow-hidden rounded-[1.75rem] border border-neutral-200/80 bg-white/95 shadow-[0_18px_40px_rgba(0,0,0,0.08)] transition duration-300 hover:-translate-y-1.5 hover:shadow-[0_24px_50px_rgba(0,0,0,0.12)] dark:border-neutral-800/80 dark:bg-neutral-900/92"
            >
              <div class="relative h-60 overflow-hidden bg-neutral-100 dark:bg-neutral-950 xl:h-64">
                <img
                  :src="getToolImageUrl(tool.id)"
                  :alt="tool.name"
                  class="h-full w-full object-cover transition duration-500 group-hover:scale-105"
                />

                <div class="absolute inset-x-0 top-0 flex items-start justify-between gap-3 p-4">
                  <div class="rounded-full bg-black/60 px-3 py-1 text-xs font-medium text-white backdrop-blur">
                    {{ tool.tool_condition || "Zustand unbekannt" }}
                  </div>

                  <div
                    :class="tool.availability_status === 'Ausgeliehen'
                      ? 'bg-amber-100 text-amber-700 dark:bg-amber-500/20 dark:text-amber-300'
                      : 'bg-white/90 text-neutral-800 dark:bg-neutral-900/90 dark:text-neutral-200'"
                    class="rounded-full px-3 py-1 text-xs font-semibold whitespace-nowrap"
                  >
                    {{ tool.availability_status || "Verfügbar" }}
                  </div>
                </div>

                <div class="absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/70 via-black/10 to-transparent px-6 pb-5 pt-12">
                  <p class="mb-3 text-sm uppercase tracking-[0.22em] text-white/70">Pfand</p>
                  <p class="mt-1 text-3xl font-bold text-lime-400">
                    <span class="rounded-xl bg-neutral-900/60 px-2 py-1">{{ euroFormat.format(tool.deposit ?? 0) }}</span>
                  </p>
                </div>
              </div>

              <div class="p-6">
                <h3 class="text-xl font-semibold tracking-tight text-black dark:text-white">
                  {{ tool.name }}
                </h3>

                <p class="mt-2 line-clamp-2 text-sm leading-6 text-neutral-600 dark:text-neutral-300">
                  {{ tool.description || "Keine Beschreibung vorhanden." }}
                </p>

                <div class="mt-6 grid grid-cols-2 gap-4">
                  <div class="rounded-2xl bg-neutral-100/90 px-4 py-3 dark:bg-neutral-800/80">
                    <p class="text-xs uppercase tracking-[0.18em] text-neutral-500 dark:text-neutral-400">Stadt</p>
                    <p class="mt-1 font-semibold text-black dark:text-white">
                      {{ tool.creator_city || "-" }}
                    </p>
                  </div>

                  <div class="rounded-2xl bg-neutral-100/90 px-4 py-3 dark:bg-neutral-800/80">
                    <p class="text-xs uppercase tracking-[0.18em] text-neutral-500 dark:text-neutral-400">Land</p>
                    <p class="mt-1 font-semibold text-black dark:text-white">
                      {{ tool.creator_country || "-" }}
                    </p>
                  </div>
                </div>

                <div class="mt-6 flex items-center justify-between rounded-2xl border border-neutral-200 bg-neutral-50 px-4 py-3 dark:border-neutral-800 dark:bg-neutral-950/80">
                  <div>
                    <p class="text-xs uppercase tracking-[0.18em] text-neutral-500 dark:text-neutral-400">Anbieter</p>
                    <p class="mt-1 font-semibold text-black dark:text-white">
                      {{ tool.creator_display_name }}
                    </p>
                  </div>
                  <div class="rounded-full bg-lime-500/15 px-3 py-1 text-xs font-semibold text-lime-700 dark:text-lime-300">
                    Details
                  </div>
                </div>

                <div class="mt-6 flex items-center gap-3">
                  <button
                    @click.stop="startRequestInChat(tool)"
                    class="flex-1 rounded-2xl bg-lime-500 px-4 py-3 font-semibold text-black transition hover:bg-lime-400"
                  >
                    Anfragen
                  </button>

                  <button
                    @click.stop="openToolModal(tool)"
                    class="rounded-2xl border border-neutral-300 bg-white px-4 py-3 font-semibold text-neutral-800 transition hover:bg-neutral-100 dark:border-neutral-700 dark:bg-neutral-950 dark:text-white dark:hover:bg-neutral-800"
                  >
                    Öffnen
                  </button>
                </div>
              </div>
            </article>
          </div>

          <div class="rounded-[1.75rem] border border-neutral-200/80 bg-white/90 px-6 py-5 shadow-sm backdrop-blur-sm dark:border-neutral-800/80 dark:bg-neutral-900/85">
            <div class="flex flex-col items-center justify-center gap-3 sm:flex-row">
              <button
                @click="goToPage(toolStore.page - 1)"
                :disabled="toolStore.page <= 1"
                class="rounded-xl border border-neutral-300 bg-white px-4 py-2 text-neutral-900 transition hover:bg-neutral-100 disabled:opacity-50 dark:border-neutral-700 dark:bg-neutral-950 dark:text-white dark:hover:bg-neutral-800"
              >
                Zurück
              </button>

              <span class="text-sm text-neutral-500 dark:text-neutral-400">
                Seite {{ toolStore.page }} von {{ toolStore.totalPages }}
              </span>

              <button
                @click="goToPage(toolStore.page + 1)"
                :disabled="toolStore.page >= toolStore.totalPages"
                class="rounded-xl border border-neutral-300 bg-white px-4 py-2 text-neutral-900 transition hover:bg-neutral-100 disabled:opacity-50 dark:border-neutral-700 dark:bg-neutral-950 dark:text-white dark:hover:bg-neutral-800"
              >
                Weiter
              </button>
            </div>
          </div>
        </section>
      </div>
    </div>

    <transition name="fade">
      <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center px-4">
        <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="closeModal"></div>

        <div
          @click.stop
          class="relative w-full max-w-2xl rounded-[28px] border border-neutral-200 bg-white p-6 shadow-xl dark:border-neutral-800 dark:bg-neutral-900 sm:p-8"
        >
          <button
            @click="closeModal"
            class="absolute right-4 top-4 flex h-10 w-10 items-center justify-center rounded-full text-neutral-500 transition hover:bg-neutral-100 dark:text-neutral-400 dark:hover:bg-neutral-800"
          >
            &times;
          </button>

          <div class="pr-10">
            <p class="text-sm text-neutral-500 dark:text-neutral-400">Tool Details</p>
            <h2 class="mt-1 text-3xl font-bold tracking-tight text-black dark:text-white">
              {{ selectedTool?.name }}
            </h2>
          </div>

          <div
            v-if="selectedTool?.id"
            class="mt-6 overflow-hidden rounded-[24px] border border-neutral-200 bg-neutral-100 dark:border-neutral-800 dark:bg-neutral-950"
          >
            <button
              @click="openImageModal"
              class="group relative block h-56 w-full overflow-hidden sm:h-72"
            >
              <img
                :src="selectedToolImageUrl"
                :alt="selectedTool?.name || 'Tool Bild'"
                class="h-full w-full object-cover transition duration-300 group-hover:scale-105"
              />
              <div class="absolute inset-x-0 bottom-0 flex items-center justify-between bg-gradient-to-t from-black/70 to-transparent px-4 py-4 text-left text-white">
                <span class="text-sm font-medium">Bild vergrößern</span>
                <span class="rounded-full bg-white/15 px-3 py-1 text-xs backdrop-blur">Klick</span>
              </div>
            </button>
          </div>

          <div class="mt-6 grid gap-4 sm:grid-cols-2">
            <div class="rounded-2xl bg-neutral-100 p-4 dark:bg-neutral-800">
              <p class="text-sm text-neutral-500 dark:text-neutral-400">Zustand</p>
              <p class="mt-1 font-semibold">
                {{ selectedTool?.tool_condition || "Unbekannt" }}
              </p>
            </div>

            <div class="rounded-2xl bg-neutral-100 p-4 dark:bg-neutral-800">
              <p class="text-sm text-neutral-500 dark:text-neutral-400">Pfand</p>
              <p class="mt-1 font-semibold">
                {{ euroFormat.format(selectedTool?.deposit ?? 0) }}
              </p>
            </div>

            <div class="rounded-2xl bg-neutral-100 p-4 dark:bg-neutral-800 sm:col-span-2">
              <p class="text-sm text-neutral-500 dark:text-neutral-400">Anbieter</p>
              <p class="mt-1 font-semibold">
                {{ selectedTool?.creator_display_name }}
              </p>
              <p class="mt-1 text-sm text-neutral-500 dark:text-neutral-400">
                {{ selectedTool?.creator_city }}, {{ selectedTool?.creator_country }}
              </p>
            </div>
          </div>

          <div class="mt-6">
            <p class="text-sm text-neutral-500 dark:text-neutral-400">Beschreibung</p>
            <p class="mt-2 leading-7 text-neutral-700 dark:text-neutral-300">
              {{ selectedTool?.description || "Keine Beschreibung vorhanden" }}
            </p>
          </div>

          <button
            @click="startRequestInChat(selectedTool)"
            class="mt-8 w-full rounded-2xl bg-lime-500 px-6 py-3.5 font-semibold text-black transition hover:bg-lime-400"
          >
            Anfragen
          </button>
        </div>
      </div>
    </transition>

    <transition name="fade">
      <div v-if="showImageModal" class="fixed inset-0 z-[60] flex items-center justify-center p-4 sm:p-8">
        <div class="absolute inset-0 bg-black/80 backdrop-blur-sm" @click="closeImageModal"></div>

        <div @click.stop class="relative max-h-full w-full max-w-5xl">
          <button
            @click="closeImageModal"
            class="absolute right-3 top-3 z-10 flex h-11 w-11 items-center justify-center rounded-full bg-black/45 text-white transition hover:bg-black/60"
          >
            &times;
          </button>

          <img
            :src="selectedToolImageUrl"
            :alt="selectedTool?.name || 'Tool Bild groß'"
            class="max-h-[88vh] w-full rounded-[28px] bg-neutral-950 object-contain shadow-2xl"
          />
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
