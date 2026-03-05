<script setup>
import { useRouter } from "vue-router";
const router = useRouter();
</script>
<template>
  <nav class="flex justify-between items-center px-6 py-6 max-w-7xl mx-auto w-full">
    <h1
        class="text-2xl font-bold tracking-tight cursor-pointer"
        @click="router.push('/')"
    >
      Street<span class="text-lime-400">Share</span>
    </h1>
  </nav>
</template>