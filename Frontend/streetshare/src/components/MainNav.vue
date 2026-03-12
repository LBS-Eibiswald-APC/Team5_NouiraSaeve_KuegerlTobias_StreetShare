<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/store/authStore.js";
import ToggleTheme from "@/components/ToggleTheme.vue";

const router = useRouter();
const auth = useAuthStore();
const user = ref(null);

const fetchUser = async () => {
  try {
    const data = await auth.getMe();
    user.value = data;
  } catch {
    user.value = null;
  }
};

onMounted(fetchUser);

const goLogin = () => router.push("/login");
const goUserPage = () => router.push("/user/me");
const goMain = () => router.push("/main");

const logout = () => {
  auth.logout();
  user.value = null;
  router.push("/login");
};
</script>

<template>
  <nav class="flex justify-between items-center px-6 py-6 max-w-7xl mx-auto w-full">
    <h1
        @click="goMain"
        class="text-2xl font-bold tracking-tight cursor-pointer text-black dark:text-white"
    >
      Street<span class="text-lime-500">Share</span>
    </h1>
    <div class="flex items-center space-x-6">
      <template v-if="user">
        <span class="dark:text-white text-black font-medium">
          {{ user.first_name + " " + user.last_name }}
        </span>
        <button
            @click="goUserPage"
            class="bg-lime-500 text-black dark:text-white px-5 py-2 rounded-full font-semibold hover:scale-105 transition cursor-pointer"
        >
          Dashboard
        </button>
        <button
            @click="logout"
            class="dark:text-white text-black hover:text-lime-400 transition cursor-pointer"
        >
          Abmelden
        </button>
        <ToggleTheme/>
      </template>
      <template v-else>
        <button
            @click="goLogin"
            class="text-neutral-300 hover:text-lime-400 transition cursor-pointer"
        >
          Login
        </button>
      </template>
    </div>
  </nav>
</template>

<style scoped>
h1 span {
  transition: all 0.2s ease;
}

h1:hover span {
  color: #84cc16;
}
</style>
