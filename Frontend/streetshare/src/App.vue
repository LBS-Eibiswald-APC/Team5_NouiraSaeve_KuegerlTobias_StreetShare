<script setup>
import { useRoute } from "vue-router";
import Navbar from "@/components/Navbar.vue";

const route = useRoute();
</script>

<template>
  <div class="min-h-screen bg-neutral-950 text-white font-sans flex flex-col">
    <transition name="fade-slide">
      <Navbar v-if="route.meta.showNav" />
    </transition>
    <router-view v-slot="{ Component }">
      <transition name="fade-slide" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>

  </div>
</template>

<style scoped>
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.35s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(15px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-15px);
}
</style>