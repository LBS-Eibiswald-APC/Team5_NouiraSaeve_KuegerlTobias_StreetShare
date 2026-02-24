<script setup>
import { ref, computed } from "vue";
import router from "../../router/index.js";
import { useAuthStore } from "@/store/authStore";

const auth = useAuthStore();

const firstname = ref("");
const lastname = ref("");
const displayname = ref("");
const phone = ref("");
const adress = ref("");
const zip = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");

const errors = ref({});

const emailValid = computed(() =>
    /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)
);

const passwordValid = computed(() =>
    /^(?=.*\d).{8,}$/.test(password.value)
);

const passwordsMatch = computed(() =>
    password.value === confirmPassword.value
);

const formValid = computed(() =>
    firstname.value.trim() !== "" &&
    lastname.value.trim() !== "" &&
    displayname.value.trim() !== "" &&
    phone.value.trim() !== "" &&
    adress.value.trim() !== "" &&
    zip.value.trim() !== "" &&
    emailValid.value &&
    passwordValid.value &&
    passwordsMatch.value
);
const register = async () => {
  errors.value = {};
  if (!firstname.value.trim()) errors.value.firstname = "Vorname ist erforderlich.";
  if (!lastname.value.trim()) errors.value.lastname = "Nachname ist erforderlich.";
  if (!displayname.value.trim()) errors.value.displayname = "Displayname ist erforderlich.";
  if (!phone.value.trim()) errors.value.phone = "Telefonnummer ist erforderlich.";
  if (!adress.value.trim()) errors.value.adress = "Adresse ist erforderlich.";
  if (!zip.value.trim()) errors.value.zip = "PLZ ist erforderlich.";
  if (!emailValid.value) errors.value.email = "Bitte gültige E-Mail eingeben.";
  if (!passwordValid.value) errors.value.password = "Passwort muss mindestens 8 Zeichen und eine Zahl enthalten.";
  if (!passwordsMatch.value) errors.value.confirmPassword = "Passwörter stimmen nicht überein.";
  if (Object.keys(errors.value).length > 0) return;
  try {
    await auth.register({
      firstname: firstname.value,
      lastname: lastname.value,
      displayname: displayname.value,
      phone: phone.value,
      adress: adress.value,
      zip: zip.value,
      email: email.value,
      password: password.value,
      role_id: 2
    });

    await router.push("/main");
  } catch (e) {
    console.error(e);
  }
};
</script>

<template>
  <div class="min-h-screen bg-neutral-950 text-white font-sans flex flex-col">
    <div class="flex flex-1 justify-center px-6">
      <div class="w-full max-w-4xl bg-neutral-900 p-8 rounded-2xl shadow-xl border border-neutral-800">
        <h2 class="text-3xl font-bold mb-4">Konto erstellen</h2>
        <form @submit.prevent="register" class="space-y-5">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm mb-2 text-neutral-400">Vorname</label>
              <input v-model="firstname" type="text" required placeholder="Max"
                     class="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"/>
              <p v-if="errors.firstname" class="text-red-400 text-sm mt-1">{{ errors.firstname }}</p>
            </div>

            <div>
              <label class="block text-sm mb-2 text-neutral-400">Nachname</label>
              <input v-model="lastname" type="text" required placeholder="Mustermann"
                     class="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"/>
              <p v-if="errors.lastname" class="text-red-400 text-sm mt-1">{{ errors.lastname }}</p>
            </div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm mb-2 text-neutral-400">Displayname</label>
              <input v-model="displayname" type="text" required placeholder="MaxD"
                     class="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"/>
              <p v-if="errors.displayname" class="text-red-400 text-sm mt-1">{{ errors.displayname }}</p>
            </div>
            <div>
              <label class="block text-sm mb-2 text-neutral-400">Telefon</label>
              <input v-model="phone" type="text" required placeholder="+43 123456789"
                     class="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"/>
              <p v-if="errors.phone" class="text-red-400 text-sm mt-1">{{ errors.phone }}</p>
            </div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm mb-2 text-neutral-400">Adresse</label>
              <input v-model="adress" type="text" required placeholder="Musterstraße 1"
                     class="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"/>
              <p v-if="errors.adress" class="text-red-400 text-sm mt-1">{{ errors.adress }}</p>
            </div>
            <div>
              <label class="block text-sm mb-2 text-neutral-400">PLZ</label>
              <input v-model="zip" type="text" required placeholder="1234"
                     class="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"/>
              <p v-if="errors.zip" class="text-red-400 text-sm mt-1">{{ errors.zip }}</p>
            </div>
          </div>
          <div>
            <label class="block text-sm mb-2 text-neutral-400">E-Mail</label>
            <input v-model="email" type="email" required placeholder="max@email.com"
                   class="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"/>
            <p v-if="errors.email" class="text-red-400 text-sm mt-1">{{ errors.email }}</p>
          </div>
          <div>
            <label class="block text-sm mb-2 text-neutral-400">Passwort</label>
            <input v-model="password" type="password" required placeholder="••••••••"
                   class="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"/>
            <p v-if="errors.password" class="text-red-400 text-sm mt-1">{{ errors.password }}</p>
          </div>
          <div>
            <label class="block text-sm mb-2 text-neutral-400">Passwort bestätigen</label>
            <input v-model="confirmPassword" type="password" required placeholder="••••••••"
                   class="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"/>
            <p v-if="errors.confirmPassword" class="text-red-400 text-sm mt-1">{{ errors.confirmPassword }}</p>
          </div>
          <button type="submit"
                  :disabled="!formValid"
                  class="w-full cursor-pointer bg-lime-400 text-black py-3 rounded-lg font-semibold hover:scale-[1.02] transition disabled:opacity-50 disabled:cursor-not-allowed">
            Registrieren
          </button>
        </form>
        <p class="text-neutral-500 text-sm mt-6 text-center">
          Bereits ein Konto?
          <span @click="router.push('/login')" class="text-lime-400 cursor-pointer hover:underline">
            Jetzt einloggen
          </span>
        </p>

      </div>
    </div>

  </div>
</template>