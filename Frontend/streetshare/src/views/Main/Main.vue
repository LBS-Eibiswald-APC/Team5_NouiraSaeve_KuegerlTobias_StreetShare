<script setup>
import {onMounted, ref, nextTick} from "vue";
import {useToolsStore} from "@/store/toolsStore";
import {useRouter} from "vue-router";
import { useDashboardStore } from "@/store/dashboardStore";

const toolStore = useToolsStore();
const selectedTool = ref(null);
const showModal = ref(false);
const router = useRouter();
const dashboardStore = useDashboardStore();

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

function openToolModal(tool) {
  selectedTool.value = tool;
  showModal.value = true;
}

function closeModal() {
  selectedTool.value = null;
  showModal.value = false;
}

async function goToPage(page) {
  if (page < 1 || page > toolStore.totalPages) return;
  toolStore.page = page;
  await toolStore.fetchTools();
  scrollToGrid();
}

function scrollToGrid() {
  nextTick(() => {
    const grid = document.querySelector("#tools-grid");
    if (grid) {
      grid.scrollIntoView({behavior: "smooth", block: "start"});
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

  await router.push({ name: "dashboard" });
}
</script>

<template>
  <div class="min-h-screen px-4 py-5 sm:px-6 lg:px-8 text-neutral-900 dark:text-white">
    <div class="mx-auto max-w-7xl">
      <div class="mb-4">
        <div
            class="rounded-3xl border border-neutral-200 bg-white dark:bg-neutral-900 dark:border-neutral-800 shadow-sm p-4 sm:p-5"
        >
          <div class="flex flex-col sm:flex-row gap-3 w-full lg:w-auto lg:min-w-[460px]">
            <input
                v-model="toolStore.filters.name"
                @keydown.enter="applyFilters"
                @input="onSearchChange"
                type="search"
                placeholder="Nach Tool suchen..."
                class="w-full rounded-2xl border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-950 px-4 py-3 text-neutral-900 dark:text-white placeholder-neutral-400 dark:placeholder-neutral-500 focus:outline-none focus:ring-2 focus:ring-lime-400"
            />

            <button
                @click="applyFilters"
                class="rounded-2xl bg-lime-500 px-5 py-3 font-semibold text-black hover:bg-lime-400 transition"
            >
              Suchen
            </button>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 gap-4 lg:grid-cols-[260px_minmax(0,1fr)]">
        <aside class="lg:self-start">
          <div
              class="h-fit rounded-3xl border border-neutral-200 bg-white dark:bg-neutral-900 dark:border-neutral-800 shadow-sm p-4 lg:sticky lg:top-5"
          >
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-lg font-semibold">Filter</h2>
              <button
                  @click="resetFilters"
                  class="text-sm text-neutral-500 hover:text-black dark:hover:text-white dark:text-neutral-400 transition"
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
                    @keydown.enter="applyFilters"
                    v-model="toolStore.filters.city"
                    placeholder="z. B. Graz"
                    class="w-full rounded-2xl border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-950 px-4 py-3 text-neutral-900 dark:text-white placeholder-neutral-400 dark:placeholder-neutral-500 focus:outline-none focus:ring-2 focus:ring-lime-400"
                />
              </div>

              <div>
                <label class="mb-2 block text-sm font-medium text-neutral-600 dark:text-neutral-300">
                  PLZ
                </label>
                <input
                    @keydown.enter="applyFilters"
                    v-model="toolStore.filters.zip"
                    placeholder="z. B. 8010"
                    class="w-full rounded-2xl border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-950 px-4 py-3 text-neutral-900 dark:text-white placeholder-neutral-400 dark:placeholder-neutral-500 focus:outline-none focus:ring-2 focus:ring-lime-400"
                />
              </div>

              <div>
                <label class="mb-2 block text-sm font-medium text-neutral-600 dark:text-neutral-300">
                  Land
                </label>
                <select
                    v-model="toolStore.filters.country"
                    class="w-full rounded-2xl border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-950 px-4 py-3 text-neutral-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-lime-400"
                >
                  <option value="">Alle Länder</option>
                  <option v-for="c in toolStore.countries" :key="c" :value="c">
                    {{ c }}
                  </option>
                </select>
              </div>

              <button
                  @click="applyFilters"
                  class="w-full rounded-2xl bg-neutral-950 dark:bg-white dark:text-black text-white px-4 py-3 font-semibold hover:opacity-90 transition"
              >
                Filter anwenden
              </button>
            </div>
          </div>
        </aside>

        <section id="tools-grid" class="space-y-4">
          <div
              class="rounded-3xl border border-neutral-200 bg-white dark:bg-neutral-900 dark:border-neutral-800 shadow-sm px-5 py-3"
          >
            <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <div class="text-sm text-neutral-500 dark:text-neutral-400">
                {{ toolStore.total }} Einträge gefunden
              </div>

              <div class="flex items-center gap-3">
                <span class="text-sm text-neutral-600 dark:text-neutral-300">Pro Seite:</span>

                <select
                    v-model="toolStore.perPage"
                    @change="toolStore.changePerPage(toolStore.perPage)"
                    class="rounded-xl border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-950 px-3 py-2 text-sm text-neutral-900 dark:text-white"
                >
                  <option value="25">25</option>
                  <option value="50">50</option>
                  <option value="100">100</option>
                </select>
              </div>
            </div>
          </div>

          <div class="grid sm:grid-cols-2 xl:grid-cols-3 gap-4">
            <div
                v-if="toolStore.loading"
                class="col-span-full rounded-3xl border border-dashed border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-900 p-10 text-center text-neutral-500 dark:text-neutral-400"
            >
              Lädt...
            </div>

            <div
                v-else-if="toolStore.tools.length === 0"
                class="col-span-full rounded-3xl border border-dashed border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-900 p-10 text-center text-neutral-500 dark:text-neutral-400"
            >
              Keine Tools gefunden.
            </div>

            <article
                v-else
                v-for="tool in toolStore.tools"
                :key="tool.id"
                @click="openToolModal(tool)"
                class="group rounded-3xl border border-neutral-200 bg-white dark:bg-neutral-900 dark:border-neutral-800 shadow-sm p-5 cursor-pointer transition hover:-translate-y-1 hover:shadow-md"
            >
              <div class="flex items-start justify-between gap-3">
                <div>
                  <h3 class="text-xl font-semibold tracking-tight text-black dark:text-white">
                    {{ tool.name }}
                  </h3>
                  <p class="mt-1 text-sm text-neutral-500 dark:text-neutral-400">
                    {{ tool.tool_condition || "Zustand unbekannt" }}
                  </p>
                </div>

                <div
                    :class="tool.availability_status === 'Ausgeliehen'
                      ? 'bg-amber-100 text-amber-700 dark:bg-amber-500/15 dark:text-amber-300'
                      : 'bg-neutral-100 text-neutral-700 dark:bg-neutral-800 dark:text-neutral-300'"
                    class="rounded-full px-3 py-1 text-xs font-medium whitespace-nowrap"
                >
                  {{ tool.availability_status || "Verfügbar" }}
                </div>
              </div>

              <div class="mt-6">
                <p class="text-sm text-neutral-500 dark:text-neutral-400">Pfand</p>
                <p class="mt-1 text-2xl font-bold text-lime-600 dark:text-lime-400">
                  {{ euroFormat.format(tool.deposit ?? 0) }}
                </p>
              </div>

              <div class="mt-6 pt-4 border-t border-neutral-200 dark:border-neutral-800">
                <p class="text-sm text-neutral-600 dark:text-neutral-400">
                  {{ tool.creator_city }}, {{ tool.creator_country }}
                </p>
                <p class="mt-1 text-sm font-medium text-black dark:text-white">
                  {{ tool.creator_display_name }}
                </p>
              </div>

              <button
                  @click.stop="startRequestInChat(tool)"
                  class="mt-5 w-full rounded-2xl bg-lime-500 px-4 py-3 font-semibold text-black hover:bg-lime-400 transition"
              >
                Anfragen
              </button>
            </article>
          </div>

          <div
              class="rounded-3xl border border-neutral-200 bg-white dark:bg-neutral-900 dark:border-neutral-800 shadow-sm px-5 py-4"
          >
            <div class="flex items-center justify-center gap-3">
              <button
                  @click="goToPage(toolStore.page - 1)"
                  :disabled="toolStore.page <= 1"
                  class="px-4 py-2 rounded-xl border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-950 text-neutral-900 dark:text-white hover:bg-neutral-100 dark:hover:bg-neutral-800 transition disabled:opacity-50"
              >
                Zurück
              </button>

              <span class="text-sm text-neutral-500 dark:text-neutral-400">
                Seite {{ toolStore.page }} von {{ toolStore.totalPages }}
              </span>

              <button
                  @click="goToPage(toolStore.page + 1)"
                  :disabled="toolStore.page >= toolStore.totalPages"
                  class="px-4 py-2 rounded-xl border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-950 text-neutral-900 dark:text-white hover:bg-neutral-100 dark:hover:bg-neutral-800 transition disabled:opacity-50"
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
        <div
            class="absolute inset-0 bg-black/50 backdrop-blur-sm"
            @click="closeModal"
        ></div>

        <div
            @click.stop
            class="relative w-full max-w-2xl rounded-[28px] border border-neutral-200 bg-white dark:bg-neutral-900 dark:border-neutral-800 shadow-xl p-6 sm:p-8"
        >
          <button
              @click="closeModal"
              class="absolute right-4 top-4 flex h-10 w-10 items-center justify-center rounded-full text-neutral-500 hover:bg-neutral-100 dark:hover:bg-neutral-800 dark:text-neutral-400 transition"
          >
            &times;
          </button>

          <div class="pr-10">
            <p class="text-sm text-neutral-500 dark:text-neutral-400">Tool Details</p>
            <h2 class="mt-1 text-3xl font-bold tracking-tight text-black dark:text-white">
              {{ selectedTool?.name }}
            </h2>
          </div>

          <div class="mt-6 grid gap-4 sm:grid-cols-2">
            <div class="rounded-2xl bg-neutral-100 dark:bg-neutral-800 p-4">
              <p class="text-sm text-neutral-500 dark:text-neutral-400">Zustand</p>
              <p class="mt-1 font-semibold">
                {{ selectedTool?.tool_condition || "Unbekannt" }}
              </p>
            </div>

            <div class="rounded-2xl bg-neutral-100 dark:bg-neutral-800 p-4">
              <p class="text-sm text-neutral-500 dark:text-neutral-400">Pfand</p>
              <p class="mt-1 font-semibold">
                {{ euroFormat.format(selectedTool?.deposit ?? 0) }}
              </p>
            </div>

            <div class="rounded-2xl bg-neutral-100 dark:bg-neutral-800 p-4 sm:col-span-2">
              <p class="text-sm text-neutral-500 dark:text-neutral-400">Anbieter</p>
              <p class="mt-1 font-semibold">
                {{ selectedTool?.creator_display_name }}
              </p>
              <p class="text-sm text-neutral-500 dark:text-neutral-400 mt-1">
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
              class="mt-8 w-full rounded-2xl bg-lime-500 px-6 py-3.5 font-semibold text-black hover:bg-lime-400 transition"
          >
            Anfragen
          </button>
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
