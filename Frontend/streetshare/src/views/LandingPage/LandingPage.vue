<template>
  <div class="min-h-screen dark:text-white font-sans">
    <nav class="flex justify-between items-center px-8 py-6 max-w-7xl mx-auto">
      <h1 class="text-2xl text-black dark:text-white font-bold tracking-tight">
        Street<span class="dark:text-lime-400 text-lime-500">Share</span>
      </h1>
      <div class="space-x-6 flex">
        <button @click="router.push('/register')" class="bg-lime-400 text-black px-5 py-2 rounded-full font-semibold hover:scale-105 transition cursor-pointer">
          Jetzt starten
        </button>
        <button @click="router.push('/login')" class="bg-lime-400 text-black px-5 py-2 rounded-full font-semibold hover:scale-105 transition cursor-pointer">
          Login
        </button>
        <ToggleTheme/>
      </div>
    </nav>
    <section class="text-center py-28 px-6">
      <h2 class="text-5xl text-black dark:text-white md:text-6xl font-bold leading-tight max-w-4xl mx-auto">
        Werkzeuge leihen.
        <span class="dark:text-lime-400 text-lime-500">Gemeinschaft stärken.</span>
      </h2>
      <p class="mt-6 dark:text-neutral-400 text-neutral-800 max-w-xl mx-auto text-lg">
        StreetShare verbindet Nachbarinnen und Nachbarn, damit Werkzeuge und Geräte
        sicher innerhalb der Gemeinde verliehen werden können – mit einem
        transparenten digitalen Pfandsystem.
      </p>
      <div class="mt-10 flex justify-center gap-4">
        <button @click="router.push('/register')" class="bg-lime-400 text-black px-8 py-3 rounded-full font-semibold hover:scale-105 transition">
          Deiner Gemeinde beitreten
        </button>
      </div>
    </section>
    <section id="features" class="py-24 px-6 bg-lime-400">
      <div class="max-w-6xl mx-auto grid md:grid-cols-3 gap-12 text-center">
        <div class="p-6 bg-neutral-200 dark:bg-neutral-800 rounded-2xl hover:-translate-y-2 transition">
          <h3 class="text-xl font-semibold mb-4 text-black dark:text-white">
            Intelligentes Pfandsystem
          </h3>
          <p class="dark:text-neutral-400 text-neutral-800">
            Jeder Verleih ist durch ein digitales und transparentes Pfand abgesichert.
          </p>
        </div>
        <div class="p-6 bg-neutral-200 dark:bg-neutral-800 rounded-2xl hover:-translate-y-2 transition">
          <h3 class="text-xl font-semibold mb-4 text-black dark:text-white">
            Nur lokal
          </h3>
          <p class="dark:text-neutral-400 text-neutral-800">
            Verbinde dich ausschließlich mit verifizierten Personen aus deiner Gemeinde.
          </p>
        </div>
        <div class="p-6 bg-neutral-200 dark:bg-neutral-800 rounded-2xl hover:-translate-y-2 transition">
          <h3 class="text-xl font-semibold mb-4 text-black dark:text-white">
            Vertrauen & Bewertungen
          </h3>
          <p class="dark:text-neutral-400 text-neutral-800">
            Ein Reputationssystem sorgt für Sicherheit, Transparenz und Zuverlässigkeit.
          </p>
        </div>
      </div>
    </section>
    <section id="how" class="py-24 px-6">
      <div class="max-w-5xl mx-auto text-center">
        <h2 class="text-4xl font-bold mb-16 text-black dark:text-white">
          So funktioniert StreetShare
        </h2>
        <div class="grid md:grid-cols-3 gap-12">
          <div>
            <div class="dark:text-lime-400 text-lime-500 text-4xl font-bold mb-4">1</div>
            <p class="dark:text-neutral-400 text-neutral-800">
              Stelle dein Werkzeug ein oder finde Geräte in deiner Nähe.
            </p>
          </div>
          <div>
            <div class="dark:text-lime-400 text-lime-500 text-4xl font-bold mb-4">2</div>
            <p class="dark:text-neutral-400 text-neutral-800">
              Sichere den Verleih mit einem digitalen Pfandbetrag ab.
            </p>
          </div>

          <div>
            <div class="dark:text-lime-400 text-lime-500 text-4xl font-bold mb-4">3</div>
            <p class="dark:text-neutral-400 text-neutral-800">
              Gib das Gerät unbeschädigt zurück und erhalte dein Pfand automatisch zurückerstattet.
            </p>
          </div>
        </div>
      </div>
    </section>
    <section class="py-24 px-6 bg-lime-400 text-black text-center">
      <h2 class="text-4xl font-bold mb-6">
        Starte noch heute mit dem Teilen.
      </h2>
      <button @click="router.push('/register')" class="bg-black text-white px-8 py-3 rounded-full font-semibold hover:scale-105 transition">
        Konto erstellen
      </button>
    </section>
    <footer class="py-10 text-center dark:text-neutral-500 text-neutral-800 text-sm">
      © 2026 StreetShare. Für starke Gemeinden entwickelt.
    </footer>
  </div>
</template>

<script setup>
import router from "../../router/index.js";
import ToggleTheme from "@/components/ToggleTheme.vue";
</script>