<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { BIconArrowLeft, BIconEye, BIconEyeSlash } from "bootstrap-icons-vue";
import { useAuthStore } from "@/store/authStore";

const email = ref("");
const password = ref("");
const showPassword = ref(false);
const error = ref("");

const auth = useAuthStore();
const router = useRouter();

const handleLogin = async () => {
  error.value = "";

  const success = await auth.login({
    email: email.value,
    password: password.value,
  });

  if (success) {
    await router.push("/main");
  } else {
    error.value = auth.error;
  }
};
</script>

<template>
  <div class="min-h-screen px-4 text-neutral-900 dark:text-white flex items-center justify-center">
    <div class="flex justify-center w-full">
      <div
          class="w-full max-w-4xl rounded-[28px] border border-neutral-200 bg-white p-8 shadow-md dark:border-neutral-800 dark:bg-neutral-900 sm:p-10"
      >
      <div class="grid grid-cols-1 gap-8 md:grid-cols-2 md:gap-10 md:divide-x md:divide-neutral-200 dark:md:divide-neutral-800">
        <div class="col-span-1">
          <div class="flex h-full p-7">
            <div class="flex-col">
              <button
                type="button"
                @click="router.push('/')"
                class="inline-flex w-fit items-center gap-2 rounded-full px-3 py-2 text-sm font-medium text-neutral-600 transition hover:bg-neutral-200 hover:text-neutral-900 dark:text-neutral-300 dark:hover:bg-neutral-800 dark:hover:text-white"
            >
              <BIconArrowLeft />
              Zurück zur Homepage
              </button>
              <div class="space-y-4 mt-2">
                <p class="text-2xl font-semibold tracking-tight text-neutral-900 dark:text-white">
                  Schön, dass du wieder da bist.
                </p>
                <p class="max-w-sm text-sm leading-7 text-neutral-500 dark:text-neutral-400">
                  Melde dich an, um Werkzeuge in deiner Umgebung sicher zu verleihen oder auszuleihen.
                </p>
                <p class="max-w-sm text-sm leading-7 text-neutral-500 dark:text-neutral-400">
                  StreetShare hält Anfragen, Ausleihen und Rückgaben für dich übersichtlich an einem Ort.
                </p>
              </div>
            </div>
          </div>
        </div>
        <div class="col-span-1">
          <div class="mb-8">
          <p class="text-sm font-medium text-neutral-500 dark:text-neutral-400">
            Willkommen zurück
          </p>
          <h1 class="mt-2 text-3xl font-bold tracking-tight text-black dark:text-white">
            Login
          </h1>
        </div>

        <p
            v-if="error"
            class="mb-5 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-700 dark:border-red-900/60 dark:bg-red-950/30 dark:text-red-400"
        >
          {{ error }}
        </p>

        <form @submit.prevent="handleLogin" class="space-y-5">
          <div>
            <label class="mb-2 block text-sm font-medium text-neutral-700 dark:text-neutral-300">
              E-Mail
            </label>
            <input
                v-model="email"
                type="email"
                required
                autocomplete="email"
                placeholder="max@email.com"
                class="w-full rounded-2xl border border-neutral-300 bg-white px-4 py-3 text-neutral-900 placeholder:text-neutral-400 focus:outline-none focus:ring-2 focus:ring-lime-400 dark:border-neutral-700 dark:bg-neutral-950 dark:text-white dark:placeholder:text-neutral-500"
            />
          </div>

          <div>
            <label class="mb-2 block text-sm font-medium text-neutral-700 dark:text-neutral-300">
              Passwort
            </label>

            <div class="relative">
              <input
                  v-model="password"
                  :type="showPassword ? 'text' : 'password'"
                  required
                  autocomplete="current-password"
                  placeholder="••••••••"
                  class="w-full rounded-2xl border border-neutral-300 bg-white px-4 py-3 pr-12 text-neutral-900 placeholder:text-neutral-400 focus:outline-none focus:ring-2 focus:ring-lime-400 dark:border-neutral-700 dark:bg-neutral-950 dark:text-white dark:placeholder:text-neutral-500"
              />

              <button
                  type="button"
                  @click="showPassword = !showPassword"
                  :aria-label="showPassword ? 'Passwort verbergen' : 'Passwort anzeigen'"
                  class="absolute inset-y-0 right-0 flex items-center px-4 text-neutral-500 transition hover:text-neutral-900 dark:text-neutral-400 dark:hover:text-white"
              >
                <BIconEye v-if="!showPassword" />
                <BIconEyeSlash v-else />
              </button>
            </div>
          </div>

          <button
              type="submit"
              :disabled="auth.loading"
              class="w-full rounded-2xl bg-neutral-950 px-4 py-3.5 font-semibold text-white transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-60 dark:bg-white dark:text-black"
          >
            {{ auth.loading ? "Logge ein..." : "Login" }}
          </button>
        </form>

        <p class="mt-6 text-center text-sm text-neutral-500 dark:text-neutral-400">
          Noch kein Konto?
          <span
              @click="router.push('/register')"
              class="cursor-pointer font-medium text-lime-600 transition hover:underline dark:text-lime-400"
          >
            Jetzt registrieren
          </span>
        </p>
      </div>
    </div>
      </div>
    </div>
  </div>
</template>
