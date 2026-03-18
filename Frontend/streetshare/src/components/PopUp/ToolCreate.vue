<script setup>
import { reactive, watch } from "vue";

const props = defineProps({
  showModal: Boolean,
  newTool: Object,
  usageFactor: Object,
  week_multiplier: Number,
  toolStore: Object
});

const emit = defineEmits(["close", "saved"]);

const conditions = ["Neu", "Minimal abgenutzt", "Gebraucht", "Gut abgenutzt", "Defekt"];

const localTool = reactive({
  name: "",
  description: "",
  base_price: 0,
  tool_condition: "Neu",
  deposit: 0
});

watch(
    () => props.newTool,
    (newVal) => {
      if (newVal) {
        Object.assign(localTool, newVal);
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

async function saveTool() {
  calcDeposit();

  const success = await props.toolStore.createTool({...localTool});

  if (success) {
    emit("saved");
    emit("close");

    Object.assign(localTool, {
      name: "",
      description: "",
      base_price: 0,
      tool_condition: "Neu",
      deposit: 0
    });
  }
}
</script>

<template>
  <transition name="fade">
    <div v-if="showModal" class="fixed inset-0 z-50 flex justify-center items-center">
      <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="emit('close')"></div>

      <div
          @click.stop
          class="relative bg-white dark:bg-neutral-900 text-neutral-900 dark:text-white border border-neutral-200 dark:border-neutral-800 rounded-3xl p-8 w-11/12 max-w-lg shadow-2xl transition-all"
      >
        <button
            @click="emit('close')"
            class="absolute top-4 right-4 text-neutral-500 dark:text-neutral-400 hover:text-black dark:hover:text-white text-3xl font-bold"
        >
          &times;
        </button>

        <h2 class="text-2xl font-bold text-lime-600 dark:text-lime-400 mb-4">Neues Tool</h2>

        <div class="flex flex-col gap-3">
          <p class="text-neutral-700 dark:text-neutral-300">Name:</p>
          <input
              v-model="localTool.name"
              placeholder="Name"
              class="px-4 py-2 rounded-xl bg-white dark:bg-neutral-800 text-neutral-900 dark:text-white border border-neutral-300 dark:border-neutral-700"
          />

          <p class="text-neutral-700 dark:text-neutral-300">Beschreibung:</p>
          <textarea
              rows="4"
              v-model="localTool.description"
              placeholder="Beschreibung"
              class="px-4 py-2 rounded-xl bg-white dark:bg-neutral-800 text-neutral-900 dark:text-white border border-neutral-300 dark:border-neutral-700"
          ></textarea>

          <p class="text-neutral-700 dark:text-neutral-300">Preis:</p>
          <input
              v-model.number="localTool.base_price"
              @input="calcDeposit"
              type="number"
              placeholder="Preis"
              class="px-4 py-2 rounded-xl bg-white dark:bg-neutral-800 text-neutral-900 dark:text-white border border-neutral-300 dark:border-neutral-700"
          />

          <p class="text-neutral-700 dark:text-neutral-300">Kondition:</p>
          <select
              v-model="localTool.tool_condition"
              @change="calcDeposit"
              class="px-4 py-2 rounded-xl bg-white dark:bg-neutral-800 text-neutral-900 dark:text-white border border-neutral-300 dark:border-neutral-700"
          >
            <option v-for="c in conditions" :key="c">{{ c }}</option>
          </select>

          <p class="text-neutral-700 dark:text-neutral-300">Pfand:</p>
          <input
              v-model="localTool.deposit"
              readonly
              placeholder="Pfand"
              class="px-4 py-2 rounded-xl bg-neutral-100 dark:bg-neutral-700 text-neutral-600 dark:text-neutral-300 border border-neutral-300 dark:border-neutral-600"
          />

          <button
              @click="saveTool"
              class="bg-lime-500 hover:bg-lime-400 text-black px-4 py-2 rounded-xl font-semibold hover:scale-105 transition"
          >
            Speichern
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>