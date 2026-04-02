<script setup>
import { computed, onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/store/authStore.js";
import ToggleTheme from "@/components/ToggleTheme.vue";

const router = useRouter();
const auth = useAuthStore();
const mobileMenuOpen = ref(false);

const user = computed(() => auth.user);

onMounted(async () => {
  if (!auth.user) {
    try {
      await auth.getMe();
    } catch {
      //
    }
  }
});

const goLogin = () => {
  mobileMenuOpen.value = false;
  router.push("/login");
};

const goUserPage = () => {
  mobileMenuOpen.value = false;
  router.push("/dashboard");
};

const goMain = () => {
  mobileMenuOpen.value = false;
  router.push("/main");
};

const logout = () => {
  auth.logout();
  mobileMenuOpen.value = false;
  router.push("/login");
};

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value;
};
</script>

<template>
  <nav class="sticky top-0 z-50 px-4 pt-4 sm:px-6">
    <div
        class="mx-auto max-w-7xl rounded-2xl border border-neutral-200/80 bg-white/90 shadow-sm backdrop-blur supports-[backdrop-filter]:bg-white/80 dark:border-neutral-800 dark:bg-neutral-900/85"
    >
      <div class="flex items-center justify-between px-5 py-4">
        <button
            data-test="nav-main"
            @click="goMain"
            class="group flex min-w-0 items-center gap-3 cursor-pointer"
        >
          <div
              class="flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl bg-neutral-950 text-sm font-bold text-white transition-transform group-hover:scale-[1.03] dark:bg-white dark:text-black"
          >
            S
          </div>

          <div class="min-w-0 text-left">
            <h1
                class="truncate text-xl font-bold tracking-tight text-black dark:text-white sm:text-2xl"
            >
              Street<span class="text-lime-500">Share</span>
            </h1>
            <p class="-mt-0.5 truncate text-xs text-neutral-500 dark:text-neutral-400">
              Local tool sharing
            </p>
          </div>
        </button>

        <!-- Desktop -->
        <div class="hidden items-center gap-3 lg:flex">
          <template v-if="user">
            <div
                class="rounded-full bg-neutral-100 px-4 py-2 text-sm font-medium text-neutral-700 dark:bg-neutral-800 dark:text-neutral-200"
            >
              {{ user.first_name + " " + user.last_name }}
            </div>

            <button
                data-test="nav-dashboard"
                @click="goUserPage"
                class="rounded-full bg-lime-500 px-5 py-2.5 font-semibold text-black transition hover:bg-lime-400"
            >
              Dashboard
            </button>

            <button
                data-test="nav-logout"
                @click="logout"
                class="rounded-full px-4 py-2.5 text-neutral-700 transition hover:bg-neutral-100 dark:text-neutral-200 dark:hover:bg-neutral-800"
            >
              Abmelden
            </button>

            <div
                class="flex h-11 w-11 items-center justify-center rounded-full border border-neutral-200 bg-white dark:border-neutral-800 dark:bg-neutral-900"
            >
              <ToggleTheme />
            </div>
          </template>

          <template v-else>
            <button
                @click="goLogin"
                class="rounded-full px-5 py-2.5 text-neutral-700 transition hover:bg-neutral-100 dark:text-neutral-200 dark:hover:bg-neutral-800"
            >
              Login
            </button>

            <div
                class="flex h-11 w-11 items-center justify-center rounded-full border border-neutral-200 bg-white dark:border-neutral-800 dark:bg-neutral-900"
            >
              <ToggleTheme />
            </div>
          </template>
        </div>

        <!-- Mobile button -->
        <div class="flex items-center gap-2 lg:hidden">
          <div
              class="flex h-11 w-11 items-center justify-center rounded-full border border-neutral-200 bg-white dark:border-neutral-800 dark:bg-neutral-900"
          >
            <ToggleTheme />
          </div>

          <button
              @click="toggleMobileMenu"
              class="flex h-11 w-11 items-center justify-center rounded-xl border border-neutral-200 bg-white text-black dark:border-neutral-800 dark:bg-neutral-900 dark:text-white"
              :aria-expanded="mobileMenuOpen"
              aria-label="Menü öffnen"
          >
            <svg
                v-if="!mobileMenuOpen"
                xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
            >
              <path stroke-linecap="round" stroke-linejoin="round" d="M4 7h16M4 12h16M4 17h16" />
            </svg>

            <svg
                v-else
                xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
            >
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 6l12 12M18 6L6 18" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Mobile Menu -->
      <transition name="fade-slide">
        <div
            v-if="mobileMenuOpen"
            class="border-t border-neutral-200 px-4 pb-4 dark:border-neutral-800 lg:hidden"
        >
          <div class="flex flex-col gap-2 pt-4">
            <template v-if="user">
              <div class="rounded-2xl bg-neutral-100 px-4 py-3 dark:bg-neutral-800">
                <p class="text-xs text-neutral-500 dark:text-neutral-400">
                  Angemeldet als
                </p>
                <p class="mt-1 font-semibold text-black dark:text-white">
                  {{ user.first_name + " " + user.last_name }}
                </p>
              </div>

              <button
                  @click="goUserPage"
                  class="w-full rounded-xl bg-lime-500 px-4 py-3 text-left font-semibold text-black"
              >
                Dashboard
              </button>

              <button
                  @click="logout"
                  class="w-full rounded-xl px-4 py-3 text-left text-black transition hover:bg-neutral-100 dark:text-white dark:hover:bg-neutral-800"
              >
                Abmelden
              </button>
            </template>

            <template v-else>
              <button
                  @click="goLogin"
                  class="w-full rounded-xl px-4 py-3 text-left text-black transition hover:bg-neutral-100 dark:text-white dark:hover:bg-neutral-800"
              >
                Login
              </button>
            </template>
          </div>
        </div>
      </transition>
    </div>
  </nav>
</template>

<style scoped>
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.18s ease;
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>