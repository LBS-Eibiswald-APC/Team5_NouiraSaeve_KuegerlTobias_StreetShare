<script setup>
import { useRouter } from "vue-router";
import ToggleTheme from "@/components/ToggleTheme.vue";
const router = useRouter();

</script>
<template>
  <nav class="flex justify-between items-center px-6 py-6 max-w-7xl mx-auto w-full">
    <h1 class="text-2xl text-black dark:text-white font-bold tracking-tight" @click="router.push('/')">
      Street<span class="dark:text-lime-400 text-lime-500">Share</span>
    </h1>
    <ToggleTheme/>
  </nav>
</template>