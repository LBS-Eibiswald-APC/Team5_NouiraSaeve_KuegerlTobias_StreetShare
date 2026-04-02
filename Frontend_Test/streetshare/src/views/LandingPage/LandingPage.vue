<template>
  <div
      class="min-h-screen bg-neutral-50 text-neutral-900 dark:bg-neutral-950 dark:text-white font-sans"
  >
    <!-- Subtle background -->
    <div class="pointer-events-none absolute inset-0 overflow-hidden">
      <div
          class="absolute inset-0 bg-[linear-gradient(to_right,rgba(0,0,0,0.025)_1px,transparent_1px),linear-gradient(to_bottom,rgba(0,0,0,0.025)_1px,transparent_1px)] bg-[size:48px_48px] dark:bg-[linear-gradient(to_right,rgba(255,255,255,0.07)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.07)_1px,transparent_1px)]"
      />
    </div>

    <!-- Navigation -->
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

          <!-- Desktop Nav -->
          <div class="hidden lg:flex items-center gap-8">
            <a
                href="#features"
                class="text-sm font-medium text-neutral-600 transition hover:text-black dark:text-neutral-300 dark:hover:text-white"
            >
              Features
            </a>
            <a
                href="#how"
                class="text-sm font-medium text-neutral-600 transition hover:text-black dark:text-neutral-300 dark:hover:text-white"
            >
              So funktioniert’s
            </a>
            <a
                href="#trust"
                class="text-sm font-medium text-neutral-600 transition hover:text-black dark:text-neutral-300 dark:hover:text-white"
            >
              Vertrauen
            </a>
          </div>

          <!-- Desktop Actions -->
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

          <!-- Mobile Actions -->
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

        <!-- Mobile Menu -->
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
                So funktioniert’s
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

    <!-- Hero -->
    <section class="relative pt-7 z-10 px-6 pb-16 md:px-8 md:pb-24">
      <div class="mx-auto flex max-w-7xl justify-center">
        <div class="max-w-4xl text-center">
          <div
              class="inline-flex items-center gap-2 rounded-full border border-neutral-200 bg-white px-4 py-2 text-sm font-medium text-neutral-700 dark:border-neutral-800 dark:bg-neutral-900 dark:text-neutral-300"
          >
            <span class="h-2 w-2 rounded-full bg-lime-500"></span>
            Lokal teilen. Digital absichern.
          </div>

          <h2
              class="mt-6 text-5xl font-bold leading-tight tracking-tight md:text-6xl"
          >
            Werkzeuge leihen.
            <span class="text-lime-500">Einfach. Sicher. Lokal.</span>
          </h2>

          <p
              class="mx-auto mt-6 max-w-2xl text-lg leading-8 text-neutral-600 dark:text-neutral-300"
          >
            StreetShare verbindet Nachbarinnen und Nachbarn, damit Werkzeuge und
            Geräte sicher innerhalb der Gemeinde verliehen werden können — mit
            digitalem Pfandsystem und transparentem Vertrauensmodell.
          </p>

          <div class="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
            <button
                @click="router.push('/register')"
                class="rounded-full bg-neutral-950 px-8 py-4 text-base font-semibold text-white transition hover:opacity-90 dark:bg-white dark:text-black"
            >
              Deiner Gemeinde beitreten
            </button>

            <button
                @click="router.push('/login')"
                class="rounded-full border border-neutral-300 bg-white px-8 py-4 text-base font-semibold text-neutral-900 transition hover:bg-neutral-100 dark:border-neutral-700 dark:bg-neutral-900 dark:text-white dark:hover:bg-neutral-800"
            >
              Bereits dabei? Login
            </button>
          </div>

          <div class="mx-auto mt-12 grid max-w-3xl gap-4 sm:grid-cols-3">
            <div
                class="rounded-3xl border border-neutral-200 bg-white p-5 shadow-sm dark:border-neutral-800 dark:bg-neutral-900"
            >
              <p class="text-2xl font-bold">Lokal</p>
              <p class="mt-2 text-sm text-neutral-500 dark:text-neutral-400">
                Nur in deiner Umgebung
              </p>
            </div>

            <div
                class="rounded-3xl border border-neutral-200 bg-white p-5 shadow-sm dark:border-neutral-800 dark:bg-neutral-900"
            >
              <p class="text-2xl font-bold">Digital</p>
              <p class="mt-2 text-sm text-neutral-500 dark:text-neutral-400">
                Pfand und Nachweis klar geregelt
              </p>
            </div>

            <div
                class="rounded-3xl border border-neutral-200 bg-white p-5 shadow-sm dark:border-neutral-800 dark:bg-neutral-900"
            >
              <p class="text-2xl font-bold">Verlässlich</p>
              <p class="mt-2 text-sm text-neutral-500 dark:text-neutral-400">
                Mehr Vertrauen durch Bewertungen
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section id="features" class="relative z-10 px-6 py-20 md:px-8">
      <div class="mx-auto max-w-7xl">
        <div class="mb-12 text-center">
          <p class="font-semibold uppercase tracking-[0.18em] text-lime-500">
            Features
          </p>
          <h2 class="mt-3 text-4xl font-bold tracking-tight md:text-5xl">
            Alles, was sicheres Teilen braucht
          </h2>
          <p class="mx-auto mt-4 max-w-2xl text-neutral-600 dark:text-neutral-300">
            Weniger Risiko, klarere Abläufe und mehr Vertrauen innerhalb der Gemeinde.
          </p>
        </div>

        <div class="grid gap-6 md:grid-cols-3">
          <div
              class="rounded-3xl border border-neutral-200 bg-white p-8 shadow-sm dark:border-neutral-800 dark:bg-neutral-900"
          >
            <div
                class="mb-6 flex h-12 w-12 items-center justify-center rounded-2xl bg-lime-500 text-lg font-bold text-black"
            >
              €
            </div>
            <h3 class="text-2xl font-semibold">Digitales Pfandsystem</h3>
            <p class="mt-4 leading-7 text-neutral-600 dark:text-neutral-300">
              Jeder Verleih wird transparent abgesichert. Klar verständlich und
              einfach für beide Seiten.
            </p>
          </div>

          <div
              class="rounded-3xl border border-neutral-200 bg-white p-8 shadow-sm dark:border-neutral-800 dark:bg-neutral-900"
          >
            <div
                class="mb-6 flex h-12 w-12 items-center justify-center rounded-2xl bg-neutral-100 text-lg font-bold text-neutral-900 dark:bg-neutral-800 dark:text-white"
            >
              ◎
            </div>
            <h3 class="text-2xl font-semibold">Nur lokal</h3>
            <p class="mt-4 leading-7 text-neutral-600 dark:text-neutral-300">
              Fokus auf echte Nähe statt anonymem Marktplatz. Das macht Teilen
              sicherer und persönlicher.
            </p>
          </div>

          <div
              class="rounded-3xl border border-neutral-200 bg-white p-8 shadow-sm dark:border-neutral-800 dark:bg-neutral-900"
          >
            <div
                class="mb-6 flex h-12 w-12 items-center justify-center rounded-2xl bg-neutral-100 text-lg font-bold text-neutral-900 dark:bg-neutral-800 dark:text-white"
            >
              ★
            </div>
            <h3 class="text-2xl font-semibold">Bewertungen & Vertrauen</h3>
            <p class="mt-4 leading-7 text-neutral-600 dark:text-neutral-300">
              Ein nachvollziehbares Reputationssystem stärkt Zuverlässigkeit und
              schafft Sicherheit für alle Beteiligten.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- How -->
    <section id="how" class="relative z-10 px-6 py-0 md:px-8">
      <div class="mx-auto max-w-6xl">
        <div class="mb-14 text-center">
          <p class="font-semibold uppercase tracking-[0.18em] text-lime-500">
            So funktioniert’s
          </p>
          <h2 class="mt-3 text-4xl font-bold tracking-tight md:text-5xl">
            In drei klaren Schritten
          </h2>
        </div>

        <div class="grid gap-6 md:grid-cols-3">
          <div
              class="rounded-3xl border border-neutral-200 bg-white p-8 shadow-sm dark:border-neutral-800 dark:bg-neutral-900"
          >
            <div
                class="mb-5 flex h-11 w-11 items-center justify-center rounded-2xl bg-neutral-950 text-white dark:bg-white dark:text-black font-semibold"
            >
              1
            </div>
            <h3 class="text-2xl font-semibold">Tool finden oder anbieten</h3>
            <p class="mt-4 leading-7 text-neutral-600 dark:text-neutral-300">
              Stelle dein Werkzeug ein oder entdecke verfügbare Geräte direkt in
              deiner Nähe.
            </p>
          </div>

          <div
              class="rounded-3xl border border-neutral-200 bg-white p-8 shadow-sm dark:border-neutral-800 dark:bg-neutral-900"
          >
            <div
                class="mb-5 flex h-11 w-11 items-center justify-center rounded-2xl bg-neutral-950 text-white dark:bg-white dark:text-black font-semibold"
            >
              2
            </div>
            <h3 class="text-2xl font-semibold">Pfand digital absichern</h3>
            <p class="mt-4 leading-7 text-neutral-600 dark:text-neutral-300">
              Der Verleih wird mit einem klar definierten Pfandbetrag abgesichert —
              ohne unnötigen Aufwand.
            </p>
          </div>

          <div
              class="rounded-3xl border border-neutral-200 bg-white p-8 shadow-sm dark:border-neutral-800 dark:bg-neutral-900"
          >
            <div
                class="mb-5 flex h-11 w-11 items-center justify-center rounded-2xl bg-neutral-950 text-white dark:bg-white dark:text-black font-semibold"
            >
              3
            </div>
            <h3 class="text-2xl font-semibold">Zurückgeben & abschließen</h3>
            <p class="mt-4 leading-7 text-neutral-600 dark:text-neutral-300">
              Nach ordentlicher Rückgabe wird der Vorgang sauber abgeschlossen und
              das Pfand freigegeben.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Trust -->
    <section id="trust" class="relative z-10 px-6 py-20 md:px-8">
      <div
          class="mx-auto max-w-7xl rounded-[2rem] border border-neutral-200 bg-white p-8 shadow-sm dark:border-neutral-800 dark:bg-neutral-900 md:p-10"
      >
        <div class="max-w-3xl">
          <p class="font-semibold uppercase tracking-[0.18em] text-lime-500">
            Vertrauen
          </p>
          <h2 class="mt-3 text-4xl font-bold tracking-tight md:text-5xl">
            Warum StreetShare funktioniert
          </h2>
          <p class="mt-5 text-lg leading-8 text-neutral-600 dark:text-neutral-300">
            StreetShare kombiniert lokale Verifizierung, digitale Absicherung und
            transparente Rückmeldung zu einem System, das Teilen planbar und sicher macht.
          </p>
        </div>

        <div class="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <div class="rounded-3xl bg-neutral-100 dark:bg-neutral-800 p-6">
            <p class="text-2xl font-bold">Transparent</p>
            <p class="mt-2 text-neutral-500 dark:text-neutral-400">
              Jeder Schritt bleibt nachvollziehbar.
            </p>
          </div>

          <div class="rounded-3xl bg-neutral-100 dark:bg-neutral-800 p-6">
            <p class="text-2xl font-bold">Sicher</p>
            <p class="mt-2 text-neutral-500 dark:text-neutral-400">
              Pfand und Prozesse reduzieren Risiko.
            </p>
          </div>

          <div class="rounded-3xl bg-neutral-100 dark:bg-neutral-800 p-6">
            <p class="text-2xl font-bold">Lokal</p>
            <p class="mt-2 text-neutral-500 dark:text-neutral-400">
              Nähe schafft echte Verlässlichkeit.
            </p>
          </div>

          <div class="rounded-3xl bg-neutral-100 dark:bg-neutral-800 p-6">
            <p class="text-2xl font-bold">Fair</p>
            <p class="mt-2 text-neutral-500 dark:text-neutral-400">
              Gute Nutzer werden sichtbar gestärkt.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="relative z-10 px-6 py-10 md:px-8">
      <div
          class="mx-auto max-w-5xl rounded-[2rem] border border-neutral-200 bg-white px-8 py-14 text-center shadow-sm dark:border-neutral-800 dark:bg-neutral-900"
      >
        <p class="font-semibold uppercase tracking-[0.2em] text-lime-500">
          Jetzt loslegen
        </p>
        <h2 class="mt-4 text-4xl font-bold tracking-tight md:text-5xl">
          Starte noch heute mit dem Teilen
        </h2>
        <p class="mx-auto mt-4 max-w-2xl text-neutral-600 dark:text-neutral-300">
          Mach aus Werkzeugen in deiner Umgebung eine funktionierende Community.
        </p>

        <div class="mt-8 flex flex-col justify-center gap-4 sm:flex-row">
          <button
              @click="router.push('/register')"
              class="rounded-full bg-neutral-950 dark:bg-white dark:text-black px-8 py-4 font-semibold text-white hover:opacity-90 transition"
          >
            Konto erstellen
          </button>

          <button
              @click="router.push('/login')"
              class="rounded-full border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-900 px-8 py-4 font-semibold text-neutral-900 dark:text-white hover:bg-neutral-100 dark:hover:bg-neutral-800 transition"
          >
            Zum Login
          </button>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer
        class="relative z-10 border-t border-neutral-200 px-6 py-10 text-center text-sm text-neutral-500 dark:border-neutral-800 dark:text-neutral-400"
    >
      © 2026 StreetShare. Für starke Gemeinden entwickelt.
    </footer>
  </div>
</template>

<script setup>
import {ref} from "vue";
import router from "../../router/index.js";
import ToggleTheme from "@/components/ToggleTheme.vue";

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