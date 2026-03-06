<script setup>
import { reactive, computed, ref } from "vue";
import router from "../../router/index.js";
import { useAuthStore } from "@/store/authStore";

const auth = useAuthStore();

const countries = ["Österreich", "Deutschland", "Schweiz", "Italien", "Frankreich"];

const form = reactive({
  firstname: "",
  lastname: "",
  displayname: "",
  phone: "",
  street: "",
  house_nr: "",
  zip: "",
  city: "",
  country: "",
  email: "",
  password: "",
  confirmPassword: "",
});

const errors = reactive({
  firstname: "",
  lastname: "",
  displayname: "",
  phone: "",
  street: "",
  house_nr: "",
  zip: "",
  city: "",
  country: "",
  email: "",
  password: "",
  confirmPassword: "",
  general: "",
});

const isSubmitting = ref(false);

const emailValid = computed(() => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email.trim()));

const passwordValid = computed(() => /^(?=.*\d).{8,}$/.test(form.password));

// Spaces/Hyphens tolerieren
const phoneValid = computed(() => {
  const normalized = form.phone.replace(/\s|-/g, "");
  return /^\+\d{6,15}$/.test(normalized);
});

const passwordsMatch = computed(() => form.password === form.confirmPassword);

function clearErrors() {
  Object.keys(errors).forEach((k) => (errors[k] = ""));
}

function validate() {
  clearErrors();

  if (!form.firstname.trim()) errors.firstname = "Vorname ist erforderlich.";
  if (!form.lastname.trim()) errors.lastname = "Nachname ist erforderlich.";
  if (!form.displayname.trim()) errors.displayname = "Displayname ist erforderlich.";

  if (!form.phone.trim()) errors.phone = "Telefonnummer ist erforderlich.";
  else if (!phoneValid.value) errors.phone = "Bitte gültige Telefonnummer mit Ländervorwahl eingeben.";

  if (!form.street.trim()) errors.street = "Straße ist erforderlich.";
  if (!form.house_nr.trim()) errors.house_nr = "Hausnummer ist erforderlich.";
  if (!form.zip.trim()) errors.zip = "PLZ ist erforderlich.";
  if (!form.city.trim()) errors.city = "Stadt ist erforderlich.";
  if (!form.country) errors.country = "Land ist erforderlich.";

  if (!emailValid.value) errors.email = "Bitte gültige E-Mail eingeben.";
  if (!passwordValid.value) errors.password = "Passwort muss mindestens 8 Zeichen und eine Zahl enthalten.";
  if (!passwordsMatch.value) errors.confirmPassword = "Passwörter stimmen nicht überein.";

  return !Object.values(errors).some(Boolean);
}

const formValid = computed(() => {
  return (
      form.firstname.trim() &&
      form.lastname.trim() &&
      form.displayname.trim() &&
      phoneValid.value &&
      form.street.trim() &&
      form.house_nr.trim() &&
      form.zip.trim() &&
      form.city.trim() &&
      form.country &&
      emailValid.value &&
      passwordValid.value &&
      passwordsMatch.value
  );
});

const register = async () => {
  errors.general = "";
  if (!validate()) return;

  isSubmitting.value = true;
  try {
    await auth.register({
      first_name: form.firstname.trim(),
      last_name: form.lastname.trim(),
      display_name: form.displayname.trim(),
      phone: form.phone.replace(/\s|-/g, ""),
      street: form.street.trim(),
      house_nr: form.house_nr.trim(),
      zip: form.zip.trim(),
      city: form.city.trim(),
      country: form.country,
      email: form.email.trim().toLowerCase(),
      hashed_pw: form.password,
      role_id: 2,
    });

    router.push("/main");
  } catch (e) {
    const msg =
        e?.response?.data?.detail ||
        e?.response?.data?.message ||
        "Registrierung fehlgeschlagen. Bitte Daten prüfen.";

    errors.general = msg;
    console.error(e);
  } finally {
    isSubmitting.value = false;
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
              <input v-model="form.firstname" type="text" placeholder="Max"
                     class="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"/>
              <p v-if="errors.firstname" class="text-red-400 text-sm mt-1">{{ errors.firstname }}</p>
            </div>
            <div>
              <label class="block text-sm mb-2 text-neutral-400">Nachname</label>
              <input v-model="form.lastname" type="text" placeholder="Mustermann"
                     class="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"/>
              <p v-if="errors.lastname" class="text-red-400 text-sm mt-1">{{ errors.lastname }}</p>
            </div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm mb-2 text-neutral-400">Displayname</label>
              <input v-model="form.displayname" type="text" placeholder="MaxD"
                     class="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"/>
              <p v-if="errors.displayname" class="text-red-400 text-sm mt-1">{{ errors.displayname }}</p>
            </div>
            <div>
              <label class="block text-sm mb-2 text-neutral-400">Telefon</label>
              <input v-model="form.phone" type="text" placeholder="+43 123456789"
                     class="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"/>
              <p v-if="errors.phone" class="text-red-400 text-sm mt-1">{{ errors.phone }}</p>
            </div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm mb-2 text-neutral-400">Straße</label>
              <input v-model="form.street" type="text" placeholder="Musterstraße"
                     class="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"/>
              <p v-if="errors.street" class="text-red-400 text-sm mt-1">{{ errors.street }}</p>
            </div>
            <div>
              <label class="block text-sm mb-2 text-neutral-400">Hausnummer</label>
              <input v-model="form.house_nr" type="text" placeholder="1"
                     class="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"/>
              <p v-if="errors.house_nr" class="text-red-400 text-sm mt-1">{{ errors.house_nr }}</p>
            </div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm mb-2 text-neutral-400">Stadt</label>
              <input v-model="form.city" type="text" placeholder="Wien"
                     class="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"/>
              <p v-if="errors.city" class="text-red-400 text-sm mt-1">{{ errors.city }}</p>
            </div>
            <div>
              <label class="block text-sm mb-2 text-neutral-400">PLZ</label>
              <input v-model="form.zip" type="text" placeholder="1010"
                     class="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"/>
              <p v-if="errors.zip" class="text-red-400 text-sm mt-1">{{ errors.zip }}</p>
            </div>
          </div>
          <div>
            <label class="block text-sm mb-2 text-neutral-400">Land</label>
            <select v-model="form.country" class="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition">
              <option value="">Bitte wählen</option>
              <option v-for="c in countries" :key="c" :value="c">{{ c }}</option>
            </select>
            <p v-if="errors.country" class="text-red-400 text-sm mt-1">{{ errors.country }}</p>
          </div>
          <div>
            <label class="block text-sm mb-2 text-neutral-400">E-Mail</label>
            <input v-model="form.email" type="email" placeholder="max@email.com"
                   class="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"/>
            <p v-if="errors.email" class="text-red-400 text-sm mt-1">{{ errors.email }}</p>
          </div>
          <div>
            <label class="block text-sm mb-2 text-neutral-400">Passwort</label>
            <input v-model="form.password" type="password" placeholder="••••••••"
                   class="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"/>
            <p v-if="errors.password" class="text-red-400 text-sm mt-1">{{ errors.password }}</p>
          </div>
          <div>
            <label class="block text-sm mb-2 text-neutral-400">Passwort bestätigen</label>
            <input v-model="form.confirmPassword" type="password" placeholder="••••••••"
                   class="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"/>
            <p v-if="errors.confirmPassword" class="text-red-400 text-sm mt-1">{{ errors.confirmPassword }}</p>
          </div>
          <button
              type="submit"
              :disabled="!formValid || isSubmitting"
              class="w-full cursor-pointer bg-lime-400 text-black py-3 rounded-lg font-semibold hover:scale-[1.02] transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ isSubmitting ? "Registrieren..." : "Registrieren" }}
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