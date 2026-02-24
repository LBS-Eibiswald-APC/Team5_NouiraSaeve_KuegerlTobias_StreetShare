
<template>
  <div class="bg-neutral-950 text-white font-sans flex flex-col justify-center py-12">
    <div class="flex flex-1 justify-center px-6">
      <div class="w-full max-w-md bg-neutral-900 p-8 rounded-2xl shadow-xl border border-neutral-800" >
        <h2 class="text-3xl font-bold mb-2">
          Login
        </h2>
        <form @submit.prevent="handleLogin" class="space-y-5">
          <div>
            <label class="block text-sm mb-2 text-neutral-400">E-Mail</label>
            <input
                v-model="email"
                type="email"
                required
                class="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"
                placeholder="max@email.com"
            />
          </div>
          <div class="mb-18">
            <label class="block text-sm mb-2 text-neutral-400">Passwort</label>
            <input
                v-model="password"
                type="password"
                required
                class="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"
                placeholder="••••••••"
            />
          </div>
          <button
              type="submit"
              class="w-full bg-lime-400 text-black py-3 rounded-lg font-semibold hover:scale-[1.02] transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Login
          </button>
        </form>
      </div>
    </div>

  </div>
</template>


<script setup>

import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/store/authStore";


const email = ref("");
const password = ref("");

const auth = useAuthStore();
const router = useRouter();


const handleLogin = async () => {

  try {
    await auth.login({

      email: email.value,
      password: password.value

    });
    await router.push("/main");
  } catch {}

};

</script>


<style scoped>

.login-container {

  max-width: 400px;
  margin: 100px auto;

  display: flex;
  flex-direction: column;
  gap: 10px;
}

.error {
  color: red;
}

</style>