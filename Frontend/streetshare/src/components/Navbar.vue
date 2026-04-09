<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { BIconList, BIconX } from "bootstrap-icons-vue";
import ToggleTheme from "@/components/ToggleTheme.vue";

const router = useRouter();
const mobileMenuOpen = ref(false);

const closeMobileMenu = () => {
  mobileMenuOpen.value = false;
};

const goLogin = () => {
  closeMobileMenu();
  router.push("/login");
};

const goRegister = () => {
  closeMobileMenu();
  router.push("/register");
};

</script>

<template>
  <nav class="sticky top-0 z-50 px-4 pt-4 sm:px-6">
    <div
        class="mx-auto max-w-7xl rounded-2xl border border-neutral-200/80 bg-white/90 backdrop-blur supports-[backdrop-filter]:bg-white/80 dark:border-neutral-800 dark:bg-neutral-900/85 shadow-sm"
    >
      <div class="flex items-center justify-between px-5 py-4">
        <button
            @click="router.push('/')"
            class="flex min-w-0 items-center gap-3 cursor-pointer group"
        >
          <div
              class="flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl bg-neutral-950 text-white dark:bg-white dark:text-black font-bold text-sm transition-transform group-hover:scale-[1.03]"
          >
            S
          </div>

          <div class="min-w-0 text-left">
            <h1 class="truncate text-xl sm:text-2xl font-bold tracking-tight text-black dark:text-white">
              Street<span class="text-lime-500">Share</span>
            </h1>
            <p class="truncate text-xs text-neutral-500 dark:text-neutral-400 -mt-0.5">
              Local tool sharing
            </p>
          </div>
        </button>

        <div class="hidden lg:flex items-center gap-8 dark:bg-neutral-950/30 bg-neutral-200 py-3 px-4 rounded-full">
          <a
              href="#features"
              class="text-sm font-medium text-neutral-800 rounded-full transition duration-200 hover:text-black hover:scale-105 dark:text-neutral-300 dark:hover:text-white py-1 px-2 hover:bg-neutral-400/30"
          >
            Features
          </a>
          <a
              href="#how"
              class="text-sm font-medium text-neutral-800 rounded-full transition hover:text-black hover:scale-105 dark:text-neutral-300 dark:hover:text-white py-1 px-2 hover:bg-neutral-400/30 duration-200"
          >
            So funktioniert's
          </a>
          <a
              href="#trust"
              class="text-sm font-medium text-neutral-800 rounded-full transition hover:text-black hover:scale-105 dark:text-neutral-300 dark:hover:text-white py-1 px-2 hover:bg-neutral-400/30 duration-200"
          >
            Vertrauen
          </a>
        </div>

        <div class="hidden lg:flex items-center gap-3">
          <button
              @click="router.push('/login')"
              class="px-5 py-2.5 rounded-full text-neutral-700 dark:text-neutral-200 hover:bg-neutral-100 dark:hover:bg-neutral-800 transition"
          >
            Login
          </button>

          <button
              @click="router.push('/register')"
              class="rounded-full bg-lime-500 px-5 py-2.5 text-sm font-semibold text-black hover:bg-lime-400 transition"
          >
            Jetzt starten
          </button>

          <div
              class="flex h-11 w-11 items-center justify-center rounded-full border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-900"
          >
            <ToggleTheme />
          </div>
        </div>

        <div class="flex lg:hidden items-center gap-2">
          <div
              class="flex h-11 w-11 items-center justify-center rounded-full border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-900"
          >
            <ToggleTheme />
          </div>

          <button
              @click="mobileMenuOpen = !mobileMenuOpen"
              class="flex h-11 w-11 items-center justify-center rounded-xl border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-900 text-black dark:text-white transition hover:bg-neutral-100 dark:hover:bg-neutral-800"
              aria-label="Navigation öffnen"
          >
            <BIconList v-if="!mobileMenuOpen" class="text-xl" />
            <BIconX v-else class="text-xl" />
          </button>
        </div>
      </div>

      <transition name="fade-slide">
        <div
            v-if="mobileMenuOpen"
            class="lg:hidden border-t border-neutral-200 dark:border-neutral-800 px-4 pb-4"
        >
          <div class="flex flex-col gap-2 pt-4">
            <a
                href="#features"
                @click="closeMobileMenu"
                class="rounded-xl px-4 py-3 text-sm font-medium text-neutral-700 transition hover:bg-neutral-100 dark:text-neutral-200 dark:hover:bg-neutral-800"
            >
              Features
            </a>

            <a
                href="#how"
                @click="closeMobileMenu"
                class="rounded-xl px-4 py-3 text-sm font-medium text-neutral-700 transition hover:bg-neutral-100 dark:text-neutral-200 dark:hover:bg-neutral-800"
            >
              So funktioniert's
            </a>

            <a
                href="#trust"
                @click="closeMobileMenu"
                class="rounded-xl px-4 py-3 text-sm font-medium text-neutral-700 transition hover:bg-neutral-100 dark:text-neutral-200 dark:hover:bg-neutral-800"
            >
              Vertrauen
            </a>

            <div class="my-2 h-px bg-neutral-200 dark:bg-neutral-800"></div>

            <button
                @click="goLogin"
                class="w-full rounded-xl px-4 py-3 text-left text-sm font-medium text-neutral-700 transition hover:bg-neutral-100 dark:text-neutral-200 dark:hover:bg-neutral-800"
            >
              Login
            </button>

            <button
                @click="goRegister"
                class="w-full rounded-xl bg-lime-500 px-4 py-3 text-left text-sm font-semibold text-black transition hover:bg-lime-400"
            >
              Jetzt starten
            </button>
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
