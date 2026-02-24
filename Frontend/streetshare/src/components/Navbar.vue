<script setup>
import { useRouter } from "vue-router";
const router = useRouter();
</script>
<template>
  <nav class="flex justify-between items-center px-6 py-6 max-w-7xl mx-auto w-full">
    <h1
        class="text-2xl font-bold tracking-tight"
    >
      Street<span class="text-lime-400">Share</span>
    </h1>
    <div class="flex items-center space-x-4">
      <button
          @click="router.push('/login')"
          class="text-neutral-300 hover:text-lime-400 transition cursor-pointer"
      >
        Login
      </button>
    </div>
  </nav>
</template>