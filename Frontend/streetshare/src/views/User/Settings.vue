<script setup>
import { computed, onMounted, reactive, ref } from "vue";
import { useAuthStore } from "@/store/authStore.js";
import { useToast } from "vue-toast-notification";
import ConfirmationPopUp from "@/components/PopUp/ConfirmationPopUp.vue";
import {
  BIconEye,
  BIconEyeSlash,
  BIconCheckCircleFill,
  BIconXCircleFill,
} from "bootstrap-icons-vue";

const authStore = useAuthStore();
const $toast = useToast();

const countries = ["Österreich", "Deutschland", "Schweiz", "Italien", "Frankreich"];

const form = reactive({
  first_name: "",
  last_name: "",
  display_name: "",
  phone: "",
  street: "",
  house_nr: "",
  city: "",
  zip: "",
  country: "",
  email: "",
  currentPassword: "",
  newPassword: "",
  confirmNewPassword: "",
});

const errors = reactive({
  first_name: "",
  last_name: "",
  display_name: "",
  phone: "",
  street: "",
  house_nr: "",
  city: "",
  zip: "",
  country: "",
  email: "",
  currentPassword: "",
  newPassword: "",
  confirmNewPassword: "",
  general: "",
});

const showModal = ref(false);
const isSubmitting = ref(false);
const showCurrentPassword = ref(false);
const showNewPassword = ref(false);
const showConfirmNewPassword = ref(false);

const originalUser = ref(null);

async function loadUser() {
  await authStore.getMe();

  if (!authStore.user) return;

  const u = authStore.user;

  form.first_name = u.first_name ?? "";
  form.last_name = u.last_name ?? "";
  form.display_name = u.display_name ?? "";
  form.phone = u.phone ?? "";
  form.street = u.street ?? "";
  form.house_nr = u.house_nr ?? "";
  form.city = u.city ?? "";
  form.zip = u.zip ?? "";
  form.country = u.country ?? "";
  form.email = u.email ?? "";

  originalUser.value = JSON.parse(JSON.stringify({
    first_name: form.first_name,
    last_name: form.last_name,
    display_name: form.display_name,
    phone: form.phone,
    street: form.street,
    house_nr: form.house_nr,
    city: form.city,
    zip: form.zip,
    country: form.country,
    email: form.email,
  }));
}

onMounted(async () => {
  await loadUser();
});

const emailValid = computed(() => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email.trim()));
const newPasswordValid = computed(() => {
  if (!form.newPassword) return true;
  return /^(?=.*\d).{8,}$/.test(form.newPassword);
});
const newPasswordsMatch = computed(() => form.newPassword === form.confirmNewPassword);

const showPasswordMatchHint = computed(() => {
  return form.newPassword.length > 0 && form.confirmNewPassword.length > 0;
});

const wantsPasswordChange = computed(() => {
  return (
      form.currentPassword.trim().length > 0 ||
      form.newPassword.trim().length > 0 ||
      form.confirmNewPassword.trim().length > 0
  );
});

const profileChanged = computed(() => {
  if (!originalUser.value) return false;

  return JSON.stringify({
    first_name: form.first_name,
    last_name: form.last_name,
    display_name: form.display_name,
    phone: form.phone,
    street: form.street,
    house_nr: form.house_nr,
    city: form.city,
    zip: form.zip,
    country: form.country,
    email: form.email,
  }) !== JSON.stringify(originalUser.value);
});

function normalizePhone(phone) {
  return phone.trim().replace(/[()\-\s]/g, "");
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
  Object.keys(errors).forEach((k) => {
    errors[k] = "";
  });
}

function validate() {
  clearErrors();

  if (!form.first_name.trim()) errors.first_name = "Vorname ist erforderlich.";
  if (!form.last_name.trim()) errors.last_name = "Nachname ist erforderlich.";
  if (!form.display_name.trim()) errors.display_name = "Anzeigename ist erforderlich.";
  if (form.display_name.length < 4) errors.display_name = "Anzeigename muss länger als 3 Zeichen sein.";

  if (!phoneValid.value) {
    errors.phone = phoneValidation.value.message;
  }

  if (!form.street.trim()) errors.street = "Straße ist erforderlich.";
  if (!form.house_nr.trim()) errors.house_nr = "Hausnummer ist erforderlich.";
  if (!form.city.trim()) errors.city = "Stadt ist erforderlich.";
  if (!form.zip.trim()) errors.zip = "PLZ ist erforderlich.";
  if (!form.country) errors.country = "Land ist erforderlich.";

  if (!emailValid.value) {
    errors.email = "Bitte gültige E-Mail eingeben.";
  }

  if (wantsPasswordChange.value) {
    if (!form.currentPassword.trim()) {
      errors.currentPassword = "Aktuelles Passwort ist erforderlich.";
    }

    if (!form.newPassword.trim()) {
      errors.newPassword = "Neues Passwort ist erforderlich.";
    } else if (!newPasswordValid.value) {
      errors.newPassword = "Passwort muss mindestens 8 Zeichen und eine Zahl enthalten.";
    }

    if (!form.confirmNewPassword.trim()) {
      errors.confirmNewPassword = "Bitte neues Passwort bestätigen.";
    } else if (!newPasswordsMatch.value) {
      errors.confirmNewPassword = "Passwörter stimmen nicht überein.";
    }
  }

  return !Object.values(errors).some(Boolean);
}

const canSubmit = computed(() => {
  return profileChanged.value || wantsPasswordChange.value;
});

function openSaveModal() {
  errors.general = "";
  if (!validate()) return;
  showModal.value = true;
}
async function saveSettings() {
  showModal.value = false;
  clearErrors();

  if (!validate()) return;

  isSubmitting.value = true;

  try {
    if (profileChanged.value) {
      await authStore.updateProfile({
        first_name: form.first_name.trim(),
        last_name: form.last_name.trim(),
        display_name: form.display_name.trim(),
        phone: phoneValidation.value.normalized,
        street: form.street.trim(),
        house_nr: form.house_nr.trim(),
        city: form.city.trim(),
        zip: form.zip.trim(),
        country: form.country,
        email: form.email.trim().toLowerCase(),
      });
    }

    if (wantsPasswordChange.value) {
      await authStore.changePassword({
        current_password: form.currentPassword,
        new_password: form.newPassword,
      });

      form.currentPassword = "";
      form.newPassword = "";
      form.confirmNewPassword = "";
    }

    await loadUser();

    $toast.success("Einstellungen erfolgreich gespeichert.", {
      position: "top-right",
    });
  } catch (e) {
    const detail = e?.response?.data?.detail;

    clearErrors();

    if (typeof detail === "object" && detail !== null) {
      if (detail.email) errors.email = detail.email;
      if (detail.display_name) errors.display_name = detail.display_name;
      if (detail.current_password) errors.currentPassword = detail.current_password;
      if (detail.new_password) errors.newPassword = detail.new_password;
      if (detail.confirm_password) errors.confirmNewPassword = detail.confirm_password;

      if (
          !detail.email &&
          !detail.display_name &&
          !detail.current_password &&
          !detail.new_password &&
          !detail.confirm_password
      ) {
        errors.general =
            detail.general || "Speichern fehlgeschlagen. Bitte Daten prüfen.";
      }
    } else {
      errors.general =
          detail ||
          e?.response?.data?.message ||
          "Speichern fehlgeschlagen. Bitte Daten prüfen.";
    }

    console.error(e);
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<template>
  <div class="min-h-screen dark:text-white flex justify-center overflow-auto">
    <div
        class="w-full mx-auto rounded-2xl border border-neutral-200 bg-white p-8 shadow-xl dark:border-neutral-800 dark:bg-neutral-900"
    >
      <div class="mb-6">
        <h1 class="text-3xl font-bold tracking-tight text-neutral-900 dark:text-white">
          Einstellungen
        </h1>
        <p class="mt-2 text-sm text-neutral-500 dark:text-neutral-400">
          Hier kannst du deine Profildaten und dein Passwort ändern.
        </p>
      </div>

      <p
          v-if="errors.general"
          class="mb-4 rounded-lg border border-red-300 bg-red-50 px-4 py-3 text-sm text-red-700 dark:border-red-900 dark:bg-red-950/40 dark:text-red-400"
      >
        {{ errors.general }}
      </p>

      <div class="space-y-8">
        <!-- Öffentliche Daten -->
        <div>
          <h3 class="mb-4 font-bold text-lime-500 dark:text-lime-400">
            Öffentliche Daten
          </h3>

          <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12 md:col-span-6">
              <label class="mb-2 block text-sm text-neutral-700 dark:text-neutral-400">Vorname *</label>
              <input
                  v-model="form.first_name"
                  type="text"
                  placeholder="Max"
                  class="w-full rounded-lg border border-neutral-300 bg-white px-4 py-3 text-neutral-900 placeholder:text-neutral-400 transition focus:outline-none focus:ring-2 focus:ring-lime-400 dark:border-neutral-700 dark:bg-neutral-800 dark:text-white dark:placeholder:text-neutral-500"
              />
              <p v-if="errors.first_name" class="mt-1 text-sm text-red-500 dark:text-red-400">
                {{ errors.first_name }}
              </p>
            </div>

            <div class="col-span-12 md:col-span-6">
              <label class="mb-2 block text-sm text-neutral-700 dark:text-neutral-400">Nachname *</label>
              <input
                  v-model="form.last_name"
                  type="text"
                  placeholder="Mustermann"
                  class="w-full rounded-lg border border-neutral-300 bg-white px-4 py-3 text-neutral-900 placeholder:text-neutral-400 transition focus:outline-none focus:ring-2 focus:ring-lime-400 dark:border-neutral-700 dark:bg-neutral-800 dark:text-white dark:placeholder:text-neutral-500"
              />
              <p v-if="errors.last_name" class="mt-1 text-sm text-red-500 dark:text-red-400">
                {{ errors.last_name }}
              </p>
            </div>

            <div class="col-span-12 md:col-span-6">
              <label class="mb-2 block text-sm text-neutral-700 dark:text-neutral-400">Anzeigename *</label>
              <input
                  v-model="form.display_name"
                  type="text"
                  placeholder="max_mustermann"
                  class="w-full rounded-lg border border-neutral-300 bg-white px-4 py-3 text-neutral-900 placeholder:text-neutral-400 transition focus:outline-none focus:ring-2 focus:ring-lime-400 dark:border-neutral-700 dark:bg-neutral-800 dark:text-white dark:placeholder:text-neutral-500"
              />
              <p v-if="errors.display_name" class="mt-1 text-sm text-red-500 dark:text-red-400">
                {{ errors.display_name }}
              </p>
            </div>

            <div class="col-span-12 md:col-span-6">
              <label class="mb-2 block text-sm text-neutral-700 dark:text-neutral-400">Telefon *</label>
              <input
                  v-model="form.phone"
                  type="text"
                  placeholder="+43 123456789"
                  class="w-full rounded-lg border border-neutral-300 bg-white px-4 py-3 text-neutral-900 placeholder:text-neutral-400 transition focus:outline-none focus:ring-2 focus:ring-lime-400 dark:border-neutral-700 dark:bg-neutral-800 dark:text-white dark:placeholder:text-neutral-500"
              />
              <p v-if="errors.phone" class="mt-1 text-sm text-red-500 dark:text-red-400">
                {{ errors.phone }}
              </p>
            </div>

            <div class="col-span-12 md:col-span-6">
              <label class="mb-2 block text-sm text-neutral-700 dark:text-neutral-400">Straße *</label>
              <input
                  v-model="form.street"
                  type="text"
                  placeholder="Musterstraße"
                  class="w-full rounded-lg border border-neutral-300 bg-white px-4 py-3 text-neutral-900 placeholder:text-neutral-400 transition focus:outline-none focus:ring-2 focus:ring-lime-400 dark:border-neutral-700 dark:bg-neutral-800 dark:text-white dark:placeholder:text-neutral-500"
              />
              <p v-if="errors.street" class="mt-1 text-sm text-red-500 dark:text-red-400">
                {{ errors.street }}
              </p>
            </div>

            <div class="col-span-12 md:col-span-6">
              <label class="mb-2 block text-sm text-neutral-700 dark:text-neutral-400">Hausnummer *</label>
              <input
                  v-model="form.house_nr"
                  type="text"
                  placeholder="1"
                  class="w-full rounded-lg border border-neutral-300 bg-white px-4 py-3 text-neutral-900 placeholder:text-neutral-400 transition focus:outline-none focus:ring-2 focus:ring-lime-400 dark:border-neutral-700 dark:bg-neutral-800 dark:text-white dark:placeholder:text-neutral-500"
              />
              <p v-if="errors.house_nr" class="mt-1 text-sm text-red-500 dark:text-red-400">
                {{ errors.house_nr }}
              </p>
            </div>

            <div class="col-span-12 md:col-span-6">
              <label class="mb-2 block text-sm text-neutral-700 dark:text-neutral-400">Stadt *</label>
              <input
                  v-model="form.city"
                  type="text"
                  placeholder="Wien"
                  class="w-full rounded-lg border border-neutral-300 bg-white px-4 py-3 text-neutral-900 placeholder:text-neutral-400 transition focus:outline-none focus:ring-2 focus:ring-lime-400 dark:border-neutral-700 dark:bg-neutral-800 dark:text-white dark:placeholder:text-neutral-500"
              />
              <p v-if="errors.city" class="mt-1 text-sm text-red-500 dark:text-red-400">
                {{ errors.city }}
              </p>
            </div>

            <div class="col-span-12 md:col-span-6">
              <label class="mb-2 block text-sm text-neutral-700 dark:text-neutral-400">PLZ *</label>
              <input
                  v-model="form.zip"
                  type="text"
                  placeholder="1010"
                  class="w-full rounded-lg border border-neutral-300 bg-white px-4 py-3 text-neutral-900 placeholder:text-neutral-400 transition focus:outline-none focus:ring-2 focus:ring-lime-400 dark:border-neutral-700 dark:bg-neutral-800 dark:text-white dark:placeholder:text-neutral-500"
              />
              <p v-if="errors.zip" class="mt-1 text-sm text-red-500 dark:text-red-400">
                {{ errors.zip }}
              </p>
            </div>

            <div class="col-span-12">
              <label class="mb-2 block text-sm text-neutral-700 dark:text-neutral-400">Land *</label>
              <select
                  v-model="form.country"
                  class="w-full rounded-lg border border-neutral-300 bg-white px-4 py-3 text-neutral-900 transition focus:outline-none focus:ring-2 focus:ring-lime-400 dark:border-neutral-700 dark:bg-neutral-800 dark:text-white"
              >
                <option value="">Bitte wählen</option>
                <option v-for="c in countries" :key="c" :value="c">{{ c }}</option>
              </select>
              <p v-if="errors.country" class="mt-1 text-sm text-red-500 dark:text-red-400">
                {{ errors.country }}
              </p>
            </div>
          </div>
        </div>

        <!-- Private Daten -->
        <div>
          <h3 class="mb-4 font-bold text-lime-500 dark:text-lime-400">
            Private Daten
          </h3>

          <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12">
              <label class="mb-2 block text-sm text-neutral-700 dark:text-neutral-400">E-Mail *</label>
              <input
                  v-model="form.email"
                  type="email"
                  placeholder="max.mustermann@gmail.com"
                  class="w-full rounded-lg border border-neutral-300 bg-white px-4 py-3 text-neutral-900 placeholder:text-neutral-400 transition focus:outline-none focus:ring-2 focus:ring-lime-400 dark:border-neutral-700 dark:bg-neutral-800 dark:text-white dark:placeholder:text-neutral-500"
              />
              <p v-if="errors.email" class="mt-1 text-sm text-red-500 dark:text-red-400">
                {{ errors.email }}
              </p>
            </div>
          </div>
        </div>

        <!-- Passwort ändern -->
        <div>
          <h3 class="mb-4 font-bold text-lime-500 dark:text-lime-400">
            Passwort ändern
          </h3>

          <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12">
              <label class="mb-2 block text-sm text-neutral-700 dark:text-neutral-400">Aktuelles Passwort</label>
              <div class="relative">
                <input
                    v-model="form.currentPassword"
                    :type="showCurrentPassword ? 'text' : 'password'"
                    placeholder="••••••••"
                    class="w-full rounded-lg border border-neutral-300 bg-white px-4 py-3 pr-12 text-neutral-900 placeholder:text-neutral-400 transition focus:outline-none focus:ring-2 focus:ring-lime-400 dark:border-neutral-700 dark:bg-neutral-800 dark:text-white dark:placeholder:text-neutral-500"
                />
                <button
                    type="button"
                    @click="showCurrentPassword = !showCurrentPassword"
                    class="absolute inset-y-0 right-0 flex items-center px-4 text-neutral-500 hover:text-lime-500 dark:text-neutral-400 dark:hover:text-lime-400"
                >
                  <BIconEye v-if="!showCurrentPassword" />
                  <BIconEyeSlash v-else />
                </button>
              </div>
              <p v-if="errors.currentPassword" class="mt-1 text-sm text-red-500 dark:text-red-400">
                {{ errors.currentPassword }}
              </p>
            </div>

            <div class="col-span-12 md:col-span-6">
              <label class="mb-2 block text-sm text-neutral-700 dark:text-neutral-400">Neues Passwort</label>
              <div class="relative">
                <input
                    v-model="form.newPassword"
                    :type="showNewPassword ? 'text' : 'password'"
                    placeholder="••••••••"
                    class="w-full rounded-lg border border-neutral-300 bg-white px-4 py-3 pr-12 text-neutral-900 placeholder:text-neutral-400 transition focus:outline-none focus:ring-2 focus:ring-lime-400 dark:border-neutral-700 dark:bg-neutral-800 dark:text-white dark:placeholder:text-neutral-500"
                />
                <button
                    type="button"
                    @click="showNewPassword = !showNewPassword"
                    class="absolute inset-y-0 right-0 flex items-center px-4 text-neutral-500 hover:text-lime-500 dark:text-neutral-400 dark:hover:text-lime-400"
                >
                  <BIconEye v-if="!showNewPassword" />
                  <BIconEyeSlash v-else />
                </button>
              </div>
              <p v-if="errors.newPassword" class="mt-1 text-sm text-red-500 dark:text-red-400">
                {{ errors.newPassword }}
              </p>
            </div>

            <div class="col-span-12 md:col-span-6">
              <label class="mb-2 block text-sm text-neutral-700 dark:text-neutral-400">Neues Passwort bestätigen</label>
              <div class="relative">
                <input
                    v-model="form.confirmNewPassword"
                    :type="showConfirmNewPassword ? 'text' : 'password'"
                    placeholder="••••••••"
                    class="w-full rounded-lg border border-neutral-300 bg-white px-4 py-3 pr-12 text-neutral-900 placeholder:text-neutral-400 transition focus:outline-none focus:ring-2 focus:ring-lime-400 dark:border-neutral-700 dark:bg-neutral-800 dark:text-white dark:placeholder:text-neutral-500"
                />
                <button
                    type="button"
                    @click="showConfirmNewPassword = !showConfirmNewPassword"
                    class="absolute inset-y-0 right-0 flex items-center px-4 text-neutral-500 hover:text-lime-500 dark:text-neutral-400 dark:hover:text-lime-400"
                >
                  <BIconEye v-if="!showConfirmNewPassword" />
                  <BIconEyeSlash v-else />
                </button>
              </div>

              <div
                  v-if="showPasswordMatchHint"
                  class="mt-2 flex items-center gap-2 text-sm"
                  :class="newPasswordsMatch ? 'text-lime-600 dark:text-lime-400' : 'text-red-500 dark:text-red-400'"
              >
                <BIconCheckCircleFill v-if="newPasswordsMatch" />
                <BIconXCircleFill v-else />
                <span>
                  {{ newPasswordsMatch ? "Passwörter stimmen überein." : "Passwörter stimmen nicht überein." }}
                </span>
              </div>

              <p v-if="errors.confirmNewPassword" class="mt-1 text-sm text-red-500 dark:text-red-400">
                {{ errors.confirmNewPassword }}
              </p>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-12 gap-4">
          <div class="col-span-12">
            <button
                @click="openSaveModal"
                :disabled="!canSubmit || isSubmitting"
                class="w-full rounded-lg bg-lime-400 py-3 font-semibold text-black transition hover:scale-[1.02] disabled:cursor-not-allowed disabled:opacity-50"
            >
              {{ isSubmitting ? "Speichern..." : "Speichern" }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <ConfirmationPopUp
        v-if="showModal"
        title="Speichern?"
        message="Willst du die Änderungen speichern?"
        @close="showModal = false"
        @confirm="saveSettings"
    />
  </div>
</template>