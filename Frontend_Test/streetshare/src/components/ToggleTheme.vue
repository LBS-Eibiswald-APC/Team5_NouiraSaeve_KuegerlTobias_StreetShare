<script setup>
import { useTheme } from "@/composables/useTheme";

const { isDark, toggleTheme } = useTheme();
</script>

<template>
  <button
      @click="toggleTheme"
      class="group relative flex h-11 w-11 items-center justify-center rounded-2xl border border-neutral-300 bg-white text-neutral-800 shadow-sm transition-all duration-300 hover:scale-105 hover:shadow-md hover:border-neutral-400 dark:border-neutral-700 dark:bg-neutral-900 dark:text-white dark:hover:border-neutral-500 cursor-pointer"
      :aria-label="isDark ? 'Zum Light Mode wechseln' : 'Zum Dark Mode wechseln'"
  >
    <span class="text-lg transition-transform duration-650 group-hover:rotate-360">
      {{ isDark ? "☀️" : "🌛" }}
    </span>
  </button>
</template>