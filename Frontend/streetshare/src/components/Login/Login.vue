<template>

  <div class="login-container">

    <h1>Login</h1>

    <form @submit.prevent="handleLogin">

      <input
          v-model="email"
          type="email"
          placeholder="Email"
          required
      />

      <input
          v-model="password"
          type="password"
          placeholder="Password"
          required
      />

      <button type="submit" :disabled="auth.loading">

        {{ auth.loading ? "Loading..." : "Login" }}

      </button>

      <p v-if="auth.error" class="error">
        {{ auth.error }}
      </p>

    </form>

  </div>

</template>


<script setup>

import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/store//authStore";


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

    router.push("/dashboard");

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