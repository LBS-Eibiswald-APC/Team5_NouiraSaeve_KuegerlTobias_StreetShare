<script setup>
import { reactive, watch, ref } from "vue";
import {useToast} from "vue-toast-notification";

const props = defineProps({
  showModal: Boolean,
  newTool: Object,
  usageFactor: Object,
  week_multiplier: Number,
  toolStore: Object
});

const emit = defineEmits(["close", "saved"]);
const $toast = useToast()

const conditions = ["Neu", "Minimal abgenutzt", "Gebraucht", "Gut abgenutzt", "Defekt"];
const imagePreview = ref(null);
const imageError = ref("");

const localTool = reactive({
  name: "",
  description: "",
  base_price: 0,
  tool_condition: "Neu",
  deposit: 0,
  tool_image: null
});

watch(
    () => props.newTool,
    (newVal) => {
      if (newVal) {
        Object.assign(localTool, {
          name: newVal.name ?? "",
          description: newVal.description ?? "",
          base_price: newVal.base_price ?? 0,
          tool_condition: newVal.tool_condition ?? "Neu",
          deposit: newVal.deposit ?? 0,
          tool_image: null
        });

        if (imagePreview.value?.startsWith("blob:")) {
          URL.revokeObjectURL(imagePreview.value);
        }

        imagePreview.value = null;
        imageError.value = "";
      }
    },
    { immediate: true, deep: true }
);

function calcDeposit() {
  const factor = props.usageFactor[localTool.tool_condition];
  let deposit = localTool.base_price * factor * props.week_multiplier;

  if (localTool.base_price < 100) {
    deposit *= 0.8;
  } else {
    deposit *= 0.7;
  }

  localTool.deposit = Number(deposit.toFixed(2));
}

async function onImageChange(event) {
  const file = event.target.files?.[0] ?? null;
  imageError.value = "";

  if (!file) {
    localTool.tool_image = null;

    if (imagePreview.value?.startsWith("blob:")) {
      URL.revokeObjectURL(imagePreview.value);
    }

    imagePreview.value = null;
    return;
  }

  try {
    localTool.tool_image = file;

    if (imagePreview.value?.startsWith("blob:")) {
      URL.revokeObjectURL(imagePreview.value);
    }

    imagePreview.value = URL.createObjectURL(file);
  } catch (error) {
    console.error(error);
    imageError.value = "Bild konnte nicht verarbeitet werden.";
    localTool.tool_image = null;

    if (imagePreview.value?.startsWith("blob:")) {
      URL.revokeObjectURL(imagePreview.value);
    }

    imagePreview.value = null;
  }
}

async function saveTool() {
  calcDeposit();
  if (localTool.name && localTool.description && localTool.base_price && localTool.base_price > 0 && localTool.tool_image) {
    const success = await props.toolStore.createTool({ ...localTool });

    if (success) {
      emit("saved");
      emit("close");

      if (imagePreview.value?.startsWith("blob:")) {
        URL.revokeObjectURL(imagePreview.value);
      }

      Object.assign(localTool, {
        name: "",
        description: "",
        base_price: 0,
        tool_condition: "Neu",
        deposit: 0,
        tool_image: null
      });

      imagePreview.value = null;
      imageError.value = "";
    }
  } else {
    $toast.error("Alle Pflichtfelder ausfüllen!", {"position": "top-right"});
  }
}
</script>
<template>
    <div v-if="showModal" class="fixed inset-0 z-50 flex justify-center items-center p-4">
      <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="emit('close')"></div>

      <div
          @click.stop
          class="relative z-10 bg-white dark:bg-neutral-900 text-neutral-900 dark:text-white border border-neutral-200 dark:border-neutral-800 rounded-3xl w-11/12 max-w-lg h-[95vh] shadow-2xl flex flex-col"
      >
        <button
            @click="emit('close')"
            class="absolute top-4 right-4 text-neutral-500 dark:text-neutral-400 hover:text-black dark:hover:text-white text-3xl font-bold z-20"
        >
          &times;
        </button>

        <div class="p-8 overflow-y-auto flex-1">
          <h2 class="text-2xl font-bold text-lime-600 dark:text-lime-400 mb-4">Neues Tool</h2>

          <div class="flex flex-col gap-3">
            <p class="text-neutral-700 dark:text-neutral-300">Name *</p>
            <input
                v-model="localTool.name"
                placeholder="Name"
                class="px-4 py-2 rounded-xl bg-white dark:bg-neutral-800 text-neutral-900 dark:text-white border border-neutral-300 dark:border-neutral-700"
            />

            <p class="text-neutral-700 dark:text-neutral-300">Beschreibung *</p>
            <textarea
                rows="4"
                v-model="localTool.description"
                placeholder="Beschreibung"
                class="px-4 py-2 rounded-xl bg-white dark:bg-neutral-800 text-neutral-900 dark:text-white border border-neutral-300 dark:border-neutral-700"
            ></textarea>

            <p class="text-neutral-700 dark:text-neutral-300">Preis *</p>
            <input
                v-model.number="localTool.base_price"
                @input="calcDeposit"
                type="number"
                placeholder="Preis"
                class="px-4 py-2 rounded-xl bg-white dark:bg-neutral-800 text-neutral-900 dark:text-white border border-neutral-300 dark:border-neutral-700"
            />

            <p class="text-neutral-700 dark:text-neutral-300">Kondition *</p>
            <select
                v-model="localTool.tool_condition"
                @change="calcDeposit"
                class="px-4 py-2 rounded-xl bg-white dark:bg-neutral-800 text-neutral-900 dark:text-white border border-neutral-300 dark:border-neutral-700"
            >
              <option v-for="c in conditions" :key="c" :value="c">{{ c }}</option>
            </select>

            <p class="text-neutral-700 dark:text-neutral-300">Bild *</p>
            <input
                type="file"
                accept="image/*"
                @change="onImageChange"
                class="px-4 py-2 rounded-xl bg-white dark:bg-neutral-800 text-neutral-900 dark:text-white border border-neutral-300 dark:border-neutral-700 file:mr-4 file:px-4 file:py-2 file:rounded-lg file:border-0 file:bg-lime-500 file:text-black file:font-semibold hover:file:bg-lime-400"
            />

            <p v-if="imageError" class="text-sm text-red-600 dark:text-red-400">
              {{ imageError }}
            </p>

            <div
                v-if="imagePreview"
                class="mt-2 border border-neutral-200 dark:border-neutral-700 rounded-2xl p-3 bg-neutral-50 dark:bg-neutral-800"
            >
              <img
                  :src="imagePreview"
                  alt="Vorschau"
                  class="w-full max-h-64 object-contain rounded-xl"
              />
            </div>

            <p class="text-neutral-700 dark:text-neutral-300">Pfand:</p>
            <input
                v-model="localTool.deposit"
                readonly
                placeholder="Pfand"
                class="px-4 py-2 rounded-xl bg-neutral-100 dark:bg-neutral-700 text-neutral-600 dark:text-neutral-300 border border-neutral-300 dark:border-neutral-600"
            />

            <button
                @click="saveTool"
                class="bg-lime-500 hover:bg-lime-400 text-black px-4 py-2 rounded-xl font-semibold hover:scale-105 transition mt-2"
            >
              Speichern
            </button>
          </div>
        </div>
      </div>
    </div>
</template>