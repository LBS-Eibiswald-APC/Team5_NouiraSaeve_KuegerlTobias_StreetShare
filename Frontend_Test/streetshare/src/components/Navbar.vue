<script setup>
import { useRouter } from "vue-router";
import ToggleTheme from "@/components/ToggleTheme.vue";

const router = useRouter();
</script>

<template>
  <nav class="sticky top-0 z-50 px-4 pt-4 sm:px-6">
    <div
        class="mx-auto max-w-7xl rounded-2xl border border-neutral-200/80 bg-white/90 backdrop-blur supports-[backdrop-filter]:bg-white/80 dark:border-neutral-800 dark:bg-neutral-900/85 shadow-sm"
    >
      <div class="flex items-center justify-between px-5 py-4">
        <button
            @click="router.push('/')"
            class="flex items-center gap-3 cursor-pointer group"
        >
          <div
              class="flex h-10 w-10 items-center justify-center rounded-2xl bg-neutral-950 text-white dark:bg-white dark:text-black font-bold text-sm transition-transform group-hover:scale-[1.03]"
          >
            S
          </div>

          <div class="text-left">
            <h1 class="text-xl sm:text-2xl font-bold tracking-tight text-black dark:text-white">
              Street<span class="text-lime-500">Share</span>
            </h1>
            <p class="text-xs text-neutral-500 dark:text-neutral-400 -mt-0.5">
              Local tool sharing
            </p>
          </div>
        </button>

        <div
            class="flex h-11 w-11 items-center justify-center rounded-full border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-900"
        >
          <ToggleTheme />
        </div>
      </div>
    </div>
  </nav>
</template>