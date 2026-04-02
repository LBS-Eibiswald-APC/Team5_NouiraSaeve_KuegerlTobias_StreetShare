<script setup>
import {ref, computed, watch, onMounted} from "vue";
import {useToolsStore} from "@/store/toolsStore";
import ToolCreate from "@/components/PopUp/ToolCreate.vue";
import ToolEdit from "@/components/PopUp/ToolEdit.vue";
import {useTransactionsStore} from "@/store/transactionsStore.js";
import {useToast} from 'vue-toast-notification'
import ConfirmationPopUp from "@/components/PopUp/ConfirmationPopUp.vue";

const $toast = useToast()

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
const showDelete = ref();
const showDescriptionModal = ref(false);
const selectedDescription = ref("");
const page = ref(1);
const perPage = ref(5);
const totalPages = computed(() => Math.max(1, Math.ceil(myTools.value.length / perPage.value)));
const paginatedTools = computed(() => {
  const start = (page.value - 1) * perPage.value;
  return myTools.value.slice(start, start + perPage.value);
});

function openDescriptionModal(description) {
  selectedDescription.value = description || "Keine Beschreibung vorhanden";
  showDescriptionModal.value = true;
}

function closeDescriptionModal() {
  showDescriptionModal.value = false;
  selectedDescription.value = "";
}

async function loadMyTools(toolUpdated) {
  if (toolUpdated) {
    $toast.success("Erfolgreich die Tools aktualisiert!", {"position": "top-right"});
  }
  myTools.value = await toolStore.getUserTools();
  if (page.value > totalPages.value) {
    page.value = totalPages.value;
  }
}

function changePage(nextPage) {
  if (nextPage < 1 || nextPage > totalPages.value) {
    return;
  }

  page.value = nextPage;
}

function changePerPage() {
  page.value = 1;
}

async function clickedEdit(tool) {
  const req = await transactionsStore.getTransactionsByToolId(tool.id);
  if (req && req.length <= 0) {
    editTool.value = tool;
    showEdit.value = true;
  } else {
    $toast.warning('Es gibt schon eine Transaktion!', {"position": "top-right"});
  }
}

const deletedTool = ref();

async function deleteTool(tool) {
  const req = await transactionsStore.getTransactionsByToolId(tool.id);
  if (req && req.length <= 0) {
    showDelete.value = true;
    deletedTool.value = tool;
  } else {
    /* Hier müssen wir unterscheiden zwischen ob es eine akutelle Transaktion gibt oder nicht */
    /* Wenn es eine gibt kommt diese Error Message */
    $toast.warning('Es gibt schon eine Transaktion!', {"position": "top-right"});
    /* Wenn es eine Transaktion gibt aber die schon Vergangenheit ist einfach deleted True setzen */
  }
}

const showImageModal = ref(false);
const selectedImageUrl = ref("");

async function showImage(tool) {
  try {
    const req = await toolStore.getToolImage(tool.id);
    if (req) {
      if (selectedImageUrl.value && selectedImageUrl.value.startsWith("blob:")) {
        URL.revokeObjectURL(selectedImageUrl.value);
      }

      selectedImageUrl.value = URL.createObjectURL(req);
      showImageModal.value = true;
    } else {
      $toast.error("Tool hat kein Bild hinterlegt!", {"position": "top-right"});
    }
  } catch (e) {
    console.log(e);
  }
}

function closeImageModal() {
  if (selectedImageUrl.value && selectedImageUrl.value.startsWith("blob:")) {
    URL.revokeObjectURL(selectedImageUrl.value);
  }

  showImageModal.value = false;
  selectedImageUrl.value = "";
}

async function deleteToolEntry() {
  try {
    const req = await toolStore.deleteTool(deletedTool.value.id);
    if (req.status === 200) {
      showDelete.value = false;
      await loadMyTools(false);
      $toast.success("Erfolgreich den Eintrag gelöscht!", {"position": "top-right"});
    }
  } catch (error) {
    console.log(error);
  }
}

const myTools = ref([]);

onMounted(async () => {
  await loadMyTools(false);
});

watch(activeTab, async (newVal) => {
  if (newVal === "entries") {
    await loadMyTools(false);
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
      class="text-neutral-900 dark:text-white font-sans flex gap-6">
    <div class="flex-1 flex flex-col gap-6 w-full">
      <div
          class="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-3xl shadow-xl p-6"
      >
        <div class="flex items-center justify-between flex-wrap gap-4 mb-6">
          <div>
            <h1 class="text-3xl font-bold text-neutral-900 dark:text-white tracking-tight">
              Meine Einträge
            </h1>
            <p class="text-neutral-500 dark:text-neutral-400 mt-1">
              Verwalte deine eingestellten Tools zentral an einem Ort
            </p>
          </div>

          <div class="flex items-center gap-3">
            <div
                class="px-4 py-2 rounded-2xl bg-lime-100 dark:bg-lime-500/10 text-lime-700 dark:text-lime-400 font-semibold"
            >
              {{ myTools.length }} Tool<span v-if="myTools.length !== 1">s</span>
            </div>

            <button
                @click="showModal = true"
                class="flex items-center gap-2 bg-lime-500 hover:bg-lime-400 text-black rounded-xl px-4 py-3 font-semibold transition hover:scale-[1.02]"
            >
              <BIconPlusLg/>
              <span>Eintrag hinzufügen</span>
            </button>
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
                  <span>Name</span>
                </div>
              </th>

              <th class="py-4 px-5 font-semibold text-neutral-700 dark:text-neutral-300" width="10">
                <div class="flex items-center gap-2">
                  <BIconCardText/>
                  <span>Beschreibung</span>
                </div>
              </th>

              <th class="py-4 px-5 font-semibold text-neutral-700 dark:text-neutral-300">
                <div class="flex items-center gap-2">
                  <BIconCashStack/>
                  <span>Preis</span>
                </div>
              </th>

              <th class="py-4 px-5 font-semibold text-neutral-700 dark:text-neutral-300">
                <div class="flex items-center gap-2">
                  <BIconShieldLock/>
                  <span>Zustand</span>
                </div>
              </th>

              <th class="py-4 px-5 font-semibold text-neutral-700 dark:text-neutral-300">
                <div class="flex items-center gap-2">
                  <BIconShieldLock/>
                  <span>Pfand</span>
                </div>
              </th>

              <th class="py-4 px-5 font-semibold text-neutral-700 dark:text-neutral-300 text-center">
                Aktion
              </th>
            </tr>
            </thead>

            <tbody>
            <tr
                v-for="tool in paginatedTools"
                :key="tool.id"
                class="border-b border-neutral-200 dark:border-neutral-800 hover:bg-neutral-100 dark:hover:bg-neutral-800/60 transition"
            >
              <td class="py-4 px-5">
                <div class="font-semibold text-neutral-900 dark:text-white">
                  {{ tool.name }}
                </div>
              </td>

              <td class="px-5 py-4 text-neutral-700 dark:text-neutral-300 text-center">
                <button
                    type="button"
                    @click="openDescriptionModal(tool.description)"
                    class="inline-flex h-9 w-9 items-center justify-center rounded-lg text-neutral-500 transition hover:bg-neutral-100 hover:text-neutral-900 dark:text-neutral-400 dark:hover:bg-neutral-800 dark:hover:text-white"
                    title="Beschreibung anzeigen"
                    aria-label="Beschreibung anzeigen"
                >
                  <BIconCardText class="text-base" />
                </button>
              </td>

              <td class="py-4 px-5 text-neutral-900 dark:text-white font-medium">
                {{ euroFormat.format(tool.base_price) }}
              </td>

              <td class="py-4 px-5 text-neutral-700 dark:text-neutral-300">
                {{ tool.tool_condition }}
              </td>

              <td class="py-4 px-5 font-semibold text-lime-600 dark:text-lime-400">
                {{ euroFormat.format(tool.deposit) }}
              </td>

              <td class="py-4 px-5">
                <div class="flex items-center justify-center gap-3">
                  <button
                      @click="clickedEdit(tool)"
                      class="flex items-center text-sm gap-2 px-3 py-2 rounded-xl bg-neutral-200 dark:bg-neutral-800 hover:bg-neutral-300 dark:hover:bg-neutral-700 text-neutral-900 dark:text-white font-semibold transition hover:scale-105"
                  >
                    <BIconPencilSquare/>
                    <span>Bearbeiten</span>
                  </button>

                  <button
                      @click="deleteTool(tool)"
                      class="text-sm flex items-center gap-2 px-2 py-2 rounded-xl bg-red-500/90 hover:bg-red-500 text-white font-semibold transition hover:scale-105"
                  >
                    <BIconTrash/>
                    <span>Löschen</span>
                  </button>
                  <button
                      @click="showImage(tool)"
                      class="text-sm flex items-center gap-2 px-2 py-2 rounded-xl bg-blue-500/90 hover:bg-blue-500 text-white font-semibold transition hover:scale-105"
                  >
                    <BIconImage/>
                    <span>Bild</span>
                  </button>
                </div>
              </td>
            </tr>

            <tr v-if="myTools.length === 0">
              <td colspan="6" class="py-14 text-center">
                <div class="flex flex-col items-center justify-center gap-3 text-neutral-500 dark:text-neutral-400">
                  <div
                      class="w-16 h-16 rounded-2xl bg-neutral-200 dark:bg-neutral-800 flex items-center justify-center"
                  >
                    <BIconTools class="text-2xl"/>
                  </div>
                  <p class="text-lg font-medium">Keine Einträge vorhanden</p>
                  <p class="text-sm">Lege dein erstes Tool an, damit es hier erscheint.</p>
                </div>
              </td>
            </tr>
            </tbody>
          </table>
        </div>

        <div v-if="myTools.length > 0" class="mt-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div class="flex items-center gap-3 text-sm text-neutral-500 dark:text-neutral-400">
            <span>Pro Seite:</span>
            <select
                v-model="perPage"
                @change="changePerPage"
                class="rounded-xl border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-950 px-3 py-2 text-sm text-neutral-900 dark:text-white"
            >
              <option :value="5">5</option>
              <option :value="10">10</option>
              <option :value="25">25</option>
            </select>
          </div>

          <div class="flex items-center justify-center gap-3">
            <button
                @click="changePage(page - 1)"
                :disabled="page <= 1"
                class="px-4 py-2 rounded-xl border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-950 text-neutral-900 dark:text-white hover:bg-neutral-100 dark:hover:bg-neutral-800 transition disabled:opacity-50"
            >
              Zurück
            </button>

            <span class="text-sm text-neutral-500 dark:text-neutral-400">
              Seite {{ page }} von {{ totalPages }}
            </span>

            <button
                @click="changePage(page + 1)"
                :disabled="page >= totalPages"
                class="px-4 py-2 rounded-xl border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-950 text-neutral-900 dark:text-white hover:bg-neutral-100 dark:hover:bg-neutral-800 transition disabled:opacity-50"
            >
              Weiter
            </button>
          </div>
        </div>
      </div>

      <!-- Modal MyTools -->
      <ToolCreate :new-tool="newTool" :show-modal="showModal"
                  :tool-store="toolStore" @close="showModal = false"
                  @saved="loadMyTools(true)"/>
      <ToolEdit
          :edit-tool="editTool" :show-modal="showEdit"
          :tool-store="toolStore" @close="showEdit = false"
          @saved="loadMyTools(true)"
      />

    </div>
    <ConfirmationPopUp
        v-if="showDelete"
        title="Speichern?"
        message="Willst du den Eintrag löschen?"
        button-save-style="warning"
        @close="showDelete = false"
        @confirm="deleteToolEntry"
    />
    <div
        v-if="showImageModal"
        class="fixed inset-0 z-50 flex items-center justify-center p-4"
    >
      <div
          class="absolute inset-0 bg-black/70 backdrop-blur-sm"
          @click="closeImageModal"
      ></div>

      <div
          class="relative z-10 w-full max-w-3xl rounded-3xl border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-900 shadow-2xl p-6"
      >
        <button
            @click="closeImageModal"
            class="absolute top-4 right-4 text-3xl font-bold text-neutral-500 dark:text-neutral-400 hover:text-black dark:hover:text-white"
        >
          &times;
        </button>

        <div class="mb-4">
          <h1 class="text-xl text-black dark:text-white">
            Tool-Bild
          </h1>
        </div>

        <div
            class="flex items-center justify-center rounded-2xl bg-neutral-100 dark:bg-neutral-950/50 border border-neutral-200 dark:border-neutral-800 p-4"
        >
          <img
              :src="selectedImageUrl"
              class="max-h-[70vh] w-auto max-w-full rounded-2xl object-contain"
          />
        </div>
      </div>
    </div>
    <transition name="fade">
      <div
          v-if="showDescriptionModal"
          class="fixed inset-0 z-[60] flex items-center justify-center px-4"
      >
        <div
            class="absolute inset-0 bg-black/50"
            @click="closeDescriptionModal"
        ></div>

        <div
            class="relative z-10 w-full max-w-md rounded-2xl border border-neutral-200 bg-white p-6 shadow-xl dark:border-neutral-800 dark:bg-neutral-900"
        >
          <button
              @click="closeDescriptionModal"
              class="absolute right-4 top-4 flex h-9 w-9 items-center justify-center rounded-full text-neutral-500 transition hover:bg-neutral-100 dark:text-neutral-400 dark:hover:bg-neutral-800"
          >
            &times;
          </button>

          <h3 class="text-lg font-semibold text-neutral-900 dark:text-white">
            Beschreibung
          </h3>

          <p class="mt-4 whitespace-pre-line text-sm leading-6 text-neutral-600 dark:text-neutral-300">
            {{ selectedDescription }}
          </p>
        </div>
      </div>
    </transition>
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
