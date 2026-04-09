<script setup>
import {computed, defineEmits, defineProps} from 'vue'

const props = defineProps({
  title: {
    type: String,
    default: 'Bestätigen'
  },
  message: {
    type: String,
    default: 'Bist du sicher?'
  },
  buttonSaveStyle: {
    type: String,
    default: 'success',
  }
})

const emit = defineEmits(['close', 'confirm'])

function handleClose() {
  emit('close')
}

function handleConfirm() {
  emit('confirm', true)
}

const buttonClasses = computed(() => {
  switch (props.buttonSaveStyle) {
    case 'success':
      return 'bg-green-500 hover:bg-green-600 text-white'
    case 'warning':
      return 'bg-yellow-500 hover:bg-yellow-600 text-black'
    case 'danger':
      return 'bg-red-500 hover:bg-red-600 text-white'
    case 'info':
      return 'bg-blue-500 hover:bg-blue-600 text-white'
    default:
      return 'bg-lime-400 hover:bg-lime-500 text-black'
  }
})
</script>

<template>
  <div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 backdrop-blur-sm">
    <div class="w-full max-w-md bg-white dark:bg-neutral-900 rounded-xl p-6 shadow-xl space-y-4">
      <h2 class="text-lg font-bold text-neutral-900 dark:text-white">
        {{ title }}
      </h2>
      <p class="text-sm text-neutral-600 dark:text-neutral-400">
        {{ message }}
      </p>
      <div class="flex justify-end gap-3 pt-4">

        <button
            @click="handleClose"
            class="px-4 py-2 rounded-lg border border-neutral-300 dark:border-neutral-700 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-800 transition"
        >
          Abbrechen
        </button>

        <button
            @click="handleConfirm"
            class="px-4 py-2 rounded-lg font-semibold transition"
            :class="buttonClasses"
        >
          Speichern
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>