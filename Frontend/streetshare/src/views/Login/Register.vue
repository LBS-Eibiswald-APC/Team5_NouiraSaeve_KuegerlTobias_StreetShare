<script setup>
import { ref, computed } from "vue";
import router from "../../router/index.js";
import { useAuthStore } from "@/store/authStore";

const auth = useAuthStore();

// Formfelder
const firstname = ref("");
const lastname = ref("");
const displayname = ref("");
const phone = ref("");
const street = ref("");
const house_nr = ref("");
const zip = ref("");
const city = ref("");
const country = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");

// Fehlerobjekt
const errors = ref({});

// Liste Länder (ein paar als Beispiel)
const countries = ["Österreich", "Deutschland", "Schweiz", "Italien", "Frankreich"];

// Validierungen
const emailValid = computed(() =>
    /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)
);

const passwordValid = computed(() =>
    /^(?=.*\d).{8,}$/.test(password.value)
);

// Telefonnummer: +43 123456789 oder +49 1234567890 etc.
const phoneValid = computed(() =>
    /^\+\d{1,3}\s?\d{4,14}$/.test(phone.value)
);

const passwordsMatch = computed(() =>
    password.value === confirmPassword.value
);

const formValid = computed(() =>
    firstname.value.trim() &&
    lastname.value.trim() &&
    displayname.value.trim() &&
    phoneValid.value &&
    street.value.trim() &&
    house_nr.value.trim() &&
    zip.value.trim() &&
    city.value.trim() &&
    country.value &&
    emailValid.value &&
    passwordValid.value &&
    passwordsMatch.value
);

// Registrierung
const register = async () => {
  errors.value = {};

  if (!firstname.value.trim()) errors.value.firstname = "Vorname ist erforderlich.";
  if (!lastname.value.trim()) errors.value.lastname = "Nachname ist erforderlich.";
  if (!displayname.value.trim()) errors.value.displayname = "Displayname ist erforderlich.";
  if (!phone.value.trim()) errors.value.phone = "Telefonnummer ist erforderlich.";
  else if (!phoneValid.value) errors.value.phone = "Bitte gültige Telefonnummer mit Ländervorwahl eingeben.";

  if (!street.value.trim()) errors.value.street = "Straße ist erforderlich.";
  if (!house_nr.value.trim()) errors.value.house_nr = "Hausnummer ist erforderlich.";
  if (!zip.value.trim()) errors.value.zip = "PLZ ist erforderlich.";
  if (!city.value.trim()) errors.value.city = "Stadt ist erforderlich.";
  if (!country.value) errors.value.country = "Land ist erforderlich.";

  if (!emailValid.value) errors.value.email = "Bitte gültige E-Mail eingeben.";
  if (!passwordValid.value) errors.value.password = "Passwort muss mindestens 8 Zeichen und eine Zahl enthalten.";
  if (!passwordsMatch.value) errors.value.confirmPassword = "Passwörter stimmen nicht überein.";

  if (Object.keys(errors.value).length > 0) return;

  try {
    await auth.register({
      first_name: firstname.value,
      last_name: lastname.value,
      display_name: displayname.value,
      phone: phone.value,
      street: street.value,
      house_nr: house_nr.value,
      zip: zip.value,
      city: city.value,
      country: country.value,
      email: email.value,
      hashed_pw: password.value,
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

          <!-- Vorname / Nachname nebeneinander -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm mb-2 text-neutral-400">Vorname</label>
              <input v-model="firstname" type="text" placeholder="Max"
                     class="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"/>
              <p v-if="errors.firstname" class="text-red-400 text-sm mt-1">{{ errors.firstname }}</p>
            </div>

            <div>
              <label class="block text-sm mb-2 text-neutral-400">Nachname</label>
              <input v-model="lastname" type="text" placeholder="Mustermann"
                     class="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"/>
              <p v-if="errors.lastname" class="text-red-400 text-sm mt-1">{{ errors.lastname }}</p>
            </div>
          </div>

          <!-- Displayname / Telefon -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm mb-2 text-neutral-400">Displayname</label>
              <input v-model="displayname" type="text" placeholder="MaxD"
                     class="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"/>
              <p v-if="errors.displayname" class="text-red-400 text-sm mt-1">{{ errors.displayname }}</p>
            </div>
            <div>
              <label class="block text-sm mb-2 text-neutral-400">Telefon</label>
              <input v-model="phone" type="text" placeholder="+43 123456789"
                     class="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"/>
              <p v-if="errors.phone" class="text-red-400 text-sm mt-1">{{ errors.phone }}</p>
            </div>
          </div>

          <!-- Straße / Hausnummer -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm mb-2 text-neutral-400">Straße</label>
              <input v-model="street" type="text" placeholder="Musterstraße"
                     class="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"/>
              <p v-if="errors.street" class="text-red-400 text-sm mt-1">{{ errors.street }}</p>
            </div>
            <div>
              <label class="block text-sm mb-2 text-neutral-400">Hausnummer</label>
              <input v-model="house_nr" type="text" placeholder="1"
                     class="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"/>
              <p v-if="errors.house_nr" class="text-red-400 text-sm mt-1">{{ errors.house_nr }}</p>
            </div>
          </div>

          <!-- Stadt / PLZ -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm mb-2 text-neutral-400">Stadt</label>
              <input v-model="city" type="text" placeholder="Wien"
                     class="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"/>
              <p v-if="errors.city" class="text-red-400 text-sm mt-1">{{ errors.city }}</p>
            </div>
            <div>
              <label class="block text-sm mb-2 text-neutral-400">PLZ</label>
              <input v-model="zip" type="text" placeholder="1010"
                     class="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"/>
              <p v-if="errors.zip" class="text-red-400 text-sm mt-1">{{ errors.zip }}</p>
            </div>
          </div>

          <!-- Country Dropdown -->
          <div>
            <label class="block text-sm mb-2 text-neutral-400">Land</label>
            <select v-model="country" class="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition">
              <option value="">Bitte wählen</option>
              <option v-for="c in countries" :key="c" :value="c">{{ c }}</option>
            </select>
            <p v-if="errors.country" class="text-red-400 text-sm mt-1">{{ errors.country }}</p>
          </div>

          <!-- E-Mail -->
          <div>
            <label class="block text-sm mb-2 text-neutral-400">E-Mail</label>
            <input v-model="email" type="email" placeholder="max@email.com"
                   class="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"/>
            <p v-if="errors.email" class="text-red-400 text-sm mt-1">{{ errors.email }}</p>
          </div>

          <!-- Passwort -->
          <div>
            <label class="block text-sm mb-2 text-neutral-400">Passwort</label>
            <input v-model="password" type="password" placeholder="••••••••"
                   class="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"/>
            <p v-if="errors.password" class="text-red-400 text-sm mt-1">{{ errors.password }}</p>
          </div>

          <!-- Passwort bestätigen -->
          <div>
            <label class="block text-sm mb-2 text-neutral-400">Passwort bestätigen</label>
            <input v-model="confirmPassword" type="password" placeholder="••••••••"
                   class="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"/>
            <p v-if="errors.confirmPassword" class="text-red-400 text-sm mt-1">{{ errors.confirmPassword }}</p>
          </div>

          <!-- Submit -->
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