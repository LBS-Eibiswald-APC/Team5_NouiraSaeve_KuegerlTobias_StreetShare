<script setup>
import { reactive, computed, ref } from "vue";
import router from "../../router/index.js";
import { useAuthStore } from "@/store/authStore";
import { useToast } from "vue-toast-notification";

const auth = useAuthStore();
const $toast = useToast();

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
const showPassword = ref(false);
const showConfirmPassword = ref(false);

const emailValid = computed(() => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email.trim()));
const passwordValid = computed(() => /^(?=.*\d).{8,}$/.test(form.password));
const passwordsMatch = computed(() => form.password === form.confirmPassword);

const showPasswordMatchHint = computed(() => {
  return form.password.length > 0 && form.confirmPassword.length > 0;
});

function normalizePhone(phone) {
  return phone
      .trim()
      .replace(/[()\-\s]/g, "");
}

function validatePhone(phone) {
  const raw = phone.trim();
  const normalized = normalizePhone(phone);

  if (!raw) {
    return {
      valid: false,
      message: "Telefonnummer ist erforderlich.",
      normalized: "",
    };
  }

  if (!raw.startsWith("+")) {
    return {
      valid: false,
      message: "Telefonnummer muss mit + und Ländervorwahl beginnen.",
      normalized: "",
    };
  }

  if ((raw.match(/\+/g) || []).length > 1) {
    return {
      valid: false,
      message: "Es ist nur ein + am Anfang erlaubt.",
      normalized: "",
    };
  }

  if (!/^\+[\d()\-\s]+$/.test(raw)) {
    return {
      valid: false,
      message: "Telefonnummer darf nur +, Zahlen, Leerzeichen, Klammern und Bindestriche enthalten.",
      normalized: "",
    };
  }

  if (!/^\+\d+$/.test(normalized)) {
    return {
      valid: false,
      message: "Nach dem + dürfen nur Ziffern stehen.",
      normalized: "",
    };
  }

  const digits = normalized.slice(1);

  if (digits.length < 7) {
    return {
      valid: false,
      message: "Telefonnummer ist zu kurz.",
      normalized: "",
    };
  }

  if (digits.length > 15) {
    return {
      valid: false,
      message: "Telefonnummer ist zu lang.",
      normalized: "",
    };
  }

  const countryCodeMatch = digits.match(/^(\d{1,3})(\d+)$/);

  if (!countryCodeMatch) {
    return {
      valid: false,
      message: "Ungültige Ländervorwahl.",
      normalized: "",
    };
  }

  const nationalNumber = countryCodeMatch[2];

  if (nationalNumber.length < 4) {
    return {
      valid: false,
      message: "Nach der Ländervorwahl müssen noch genügend Ziffern folgen.",
      normalized: "",
    };
  }

  return {
    valid: true,
    message: "",
    normalized,
  };
}

const phoneValidation = computed(() => validatePhone(form.phone));
const phoneValid = computed(() => phoneValidation.value.valid);

function clearErrors() {
  Object.keys(errors).forEach((k) => (errors[k] = ""));
}

function validate() {
  clearErrors();

  if (!form.firstname.trim()) errors.firstname = "Vorname ist erforderlich.";
  if (!form.lastname.trim()) errors.lastname = "Nachname ist erforderlich.";
  if (!form.displayname.trim()) errors.displayname = "Anzeigename ist erforderlich.";
  if (form.displayname.length < 4) errors.displayname = "Anzeigename muss länger als 4 Zeichen sein.";

  if (!phoneValid.value) {
    errors.phone = phoneValidation.value.message;
  }

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
      phone: phoneValidation.value.normalized,
      street: form.street.trim(),
      house_nr: form.house_nr.trim(),
      zip: form.zip.trim(),
      city: form.city.trim(),
      country: form.country,
      email: form.email.trim().toLowerCase(),
      hashed_pw: form.password,
      role_id: 2,
    });

    $toast.success("Konto erfolgreich erstellt! Bitte jetzt einloggen.", {
      position: "top-right",
    });

    setTimeout(() => {
      router.push("/login");
    }, 1400);
  } catch (e) {
    const detail = e?.response?.data?.detail;

    if (typeof detail === "object" && detail !== null) {
      errors.general =
          detail.email ||
          detail.display_name ||
          detail.general ||
          "Registrierung fehlgeschlagen. Bitte Daten prüfen.";
    } else {
      errors.general =
          detail ||
          e?.response?.data?.message ||
          "Registrierung fehlgeschlagen. Bitte Daten prüfen.";
    }

    console.error(e);
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<template>
  <div class="min-h-screen dark:text-white font-sans flex flex-col pt-5">
    <div class="flex flex-1 justify-center px-6 mb-5">
      <div
          class="w-full max-w-4xl bg-white dark:bg-neutral-900 p-8 rounded-2xl shadow-xl border border-neutral-200 dark:border-neutral-800"
      >
        <h2 class="text-3xl font-bold text-neutral-900 dark:text-white">
          Konto erstellen
        </h2>
        <p class="text-sm mb-4 text-neutral-400 dark:text-white-900">
          Pflichtfelder sind mit * gekennzeichnet.
        </p>

        <p
            v-if="errors.general"
            class="mb-4 rounded-lg border border-red-300 bg-red-50 px-4 py-3 text-sm text-red-700 dark:border-red-900 dark:bg-red-950/40 dark:text-red-400"
        >
          {{ errors.general }}
        </p>

        <form @submit.prevent="register" class="space-y-5">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm mb-2 text-neutral-700 dark:text-neutral-400">Vorname *</label>
              <input
                  v-model="form.firstname"
                  type="text"
                  placeholder="Max"
                  class="w-full bg-white text-neutral-900 placeholder:text-neutral-400 border border-neutral-300 dark:bg-neutral-800 dark:text-white dark:placeholder:text-neutral-500 dark:border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"
              />
              <p v-if="errors.firstname" class="text-red-500 dark:text-red-400 text-sm mt-1">{{ errors.firstname }}</p>
            </div>

            <div>
              <label class="block text-sm mb-2 text-neutral-700 dark:text-neutral-400">Nachname *</label>
              <input
                  v-model="form.lastname"
                  type="text"
                  placeholder="Mustermann"
                  class="w-full bg-white text-neutral-900 placeholder:text-neutral-400 border border-neutral-300 dark:bg-neutral-800 dark:text-white dark:placeholder:text-neutral-500 dark:border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"
              />
              <p v-if="errors.lastname" class="text-red-500 dark:text-red-400 text-sm mt-1">{{ errors.lastname }}</p>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm mb-2 text-neutral-700 dark:text-neutral-400">Anzeigename *</label>
              <input
                  v-model="form.displayname"
                  type="text"
                  placeholder="MaxD"
                  class="w-full bg-white text-neutral-900 placeholder:text-neutral-400 border border-neutral-300 dark:bg-neutral-800 dark:text-white dark:placeholder:text-neutral-500 dark:border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"
              />
              <p v-if="errors.displayname" class="text-red-500 dark:text-red-400 text-sm mt-1">{{
                  errors.displayname
                }}</p>
            </div>

            <div>
              <label class="block text-sm mb-2 text-neutral-700 dark:text-neutral-400">Telefon *</label>
              <input
                  v-model="form.phone"
                  type="text"
                  placeholder="+43 123456789"
                  class="w-full bg-white text-neutral-900 placeholder:text-neutral-400 border border-neutral-300 dark:bg-neutral-800 dark:text-white dark:placeholder:text-neutral-500 dark:border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"
              />
              <p v-if="errors.phone" class="text-red-500 dark:text-red-400 text-sm mt-1">{{ errors.phone }}</p>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm mb-2 text-neutral-700 dark:text-neutral-400">Straße *</label>
              <input
                  v-model="form.street"
                  type="text"
                  placeholder="Musterstraße"
                  class="w-full bg-white text-neutral-900 placeholder:text-neutral-400 border border-neutral-300 dark:bg-neutral-800 dark:text-white dark:placeholder:text-neutral-500 dark:border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"
              />
              <p v-if="errors.street" class="text-red-500 dark:text-red-400 text-sm mt-1">{{ errors.street }}</p>
            </div>

            <div>
              <label class="block text-sm mb-2 text-neutral-700 dark:text-neutral-400">Hausnummer *</label>
              <input
                  v-model="form.house_nr"
                  type="text"
                  placeholder="1"
                  class="w-full bg-white text-neutral-900 placeholder:text-neutral-400 border border-neutral-300 dark:bg-neutral-800 dark:text-white dark:placeholder:text-neutral-500 dark:border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"
              />
              <p v-if="errors.house_nr" class="text-red-500 dark:text-red-400 text-sm mt-1">{{ errors.house_nr }}</p>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm mb-2 text-neutral-700 dark:text-neutral-400">Stadt *</label>
              <input
                  v-model="form.city"
                  type="text"
                  placeholder="Wien"
                  class="w-full bg-white text-neutral-900 placeholder:text-neutral-400 border border-neutral-300 dark:bg-neutral-800 dark:text-white dark:placeholder:text-neutral-500 dark:border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"
              />
              <p v-if="errors.city" class="text-red-500 dark:text-red-400 text-sm mt-1">{{ errors.city }}</p>
            </div>

            <div>
              <label class="block text-sm mb-2 text-neutral-700 dark:text-neutral-400">PLZ *</label>
              <input
                  v-model="form.zip"
                  type="text"
                  placeholder="1010"
                  class="w-full bg-white text-neutral-900 placeholder:text-neutral-400 border border-neutral-300 dark:bg-neutral-800 dark:text-white dark:placeholder:text-neutral-500 dark:border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"
              />
              <p v-if="errors.zip" class="text-red-500 dark:text-red-400 text-sm mt-1">{{ errors.zip }}</p>
            </div>
          </div>

          <div>
            <label class="block text-sm mb-2 text-neutral-700 dark:text-neutral-400">Land *</label>
            <select
                v-model="form.country"
                class="w-full bg-white text-neutral-900 border border-neutral-300 dark:bg-neutral-800 dark:text-white dark:border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"
            >
              <option value="">Bitte wählen</option>
              <option v-for="c in countries" :key="c" :value="c">{{ c }}</option>
            </select>
            <p v-if="errors.country" class="text-red-500 dark:text-red-400 text-sm mt-1">{{ errors.country }}</p>
          </div>

          <div>
            <label class="block text-sm mb-2 text-neutral-700 dark:text-neutral-400">E-Mail *</label>
            <input
                v-model="form.email"
                type="email"
                placeholder="max@email.com"
                class="w-full bg-white text-neutral-900 placeholder:text-neutral-400 border border-neutral-300 dark:bg-neutral-800 dark:text-white dark:placeholder:text-neutral-500 dark:border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"
            />
            <p v-if="errors.email" class="text-red-500 dark:text-red-400 text-sm mt-1">{{ errors.email }}</p>
          </div>

          <div>
            <label class="block text-sm mb-2 text-neutral-700 dark:text-neutral-400">Passwort *</label>

            <div class="relative">
              <input
                  v-model="form.password"
                  :type="showPassword ? 'text' : 'password'"
                  placeholder="••••••••"
                  class="w-full bg-white text-neutral-900 placeholder:text-neutral-400 border border-neutral-300 dark:bg-neutral-800 dark:text-white dark:placeholder:text-neutral-500 dark:border-neutral-700 rounded-lg px-4 py-3 pr-12 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"
              />

              <button
                  type="button"
                  @click="showPassword = !showPassword"
                  :aria-label="showPassword ? 'Passwort verbergen' : 'Passwort anzeigen'"
                  class="absolute inset-y-0 right-0 flex items-center px-4 text-sm text-neutral-500 hover:text-lime-500 dark:text-neutral-400 dark:hover:text-lime-400"
              >
                <BIconEye v-if="!showPassword"/>
                <BIconEyeSlash v-else/>
              </button>
            </div>

            <p v-if="errors.password" class="text-red-500 dark:text-red-400 text-sm mt-1">
              {{ errors.password }}
            </p>
          </div>

          <div>
            <label class="block text-sm mb-2 text-neutral-700 dark:text-neutral-400">Passwort bestätigen *</label>

            <div class="relative">
              <input
                  v-model="form.confirmPassword"
                  :type="showConfirmPassword ? 'text' : 'password'"
                  placeholder="••••••••"
                  class="w-full bg-white text-neutral-900 placeholder:text-neutral-400 border border-neutral-300 dark:bg-neutral-800 dark:text-white dark:placeholder:text-neutral-500 dark:border-neutral-700 rounded-lg px-4 py-3 pr-12 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"
              />

              <button
                  type="button"
                  @click="showConfirmPassword = !showConfirmPassword"
                  :aria-label="showConfirmPassword ? 'Passwort verbergen' : 'Passwort anzeigen'"
                  class="absolute inset-y-0 right-0 flex items-center px-4 text-sm text-neutral-500 hover:text-lime-500 dark:text-neutral-400 dark:hover:text-lime-400"
              >
                <BIconEye v-if="!showConfirmPassword"/>
                <BIconEyeSlash v-else/>
              </button>
            </div>

            <div
                v-if="showPasswordMatchHint"
                class="mt-2 flex items-center gap-2 text-sm"
                :class="passwordsMatch ? 'text-lime-600 dark:text-lime-400' : 'text-red-500 dark:text-red-400'"
            >
              <BIconCheckCircleFill v-if="passwordsMatch"/>
              <BIconXCircleFill v-else/>
              <span>
                {{ passwordsMatch ? 'Passwörter stimmen überein.' : 'Passwörter stimmen nicht überein.' }}
              </span>
            </div>

            <p v-if="errors.confirmPassword" class="text-red-500 dark:text-red-400 text-sm mt-1">
              {{ errors.confirmPassword }}
            </p>
          </div>

          <button
              type="submit"
              :disabled="!formValid || isSubmitting"
              class="w-full cursor-pointer bg-lime-500 text-black py-3 rounded-lg font-semibold hover:scale-[1.02] hover:bg-lime-400 transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ isSubmitting ? "Registrieren..." : "Registrieren" }}
          </button>
        </form>

        <p class="text-neutral-600 dark:text-neutral-500 text-sm mt-6 text-center">
          Bereits ein Konto?
          <span
              @click="router.push('/login')"
              class="text-lime-600 dark:text-lime-400 cursor-pointer hover:underline"
          >
            Jetzt einloggen
          </span>
        </p>
      </div>
    </div>
  </div>
</template>