<script setup>
import {computed, ref, onMounted, onBeforeUnmount, watch, onBeforeMount} from "vue";
import Settings from "@/views/User/Settings.vue";
import Requests from "@/views/User/Requests.vue";
import Entries from "@/views/User/Entries.vue";
import SendedRequests from "@/views/User/SendedRequests.vue";

import {
  BIconGrid,
  BIconInbox,
  BIconArrowLeftRight,
  BIconGear,
  BIconList,
  BIconX
} from "bootstrap-icons-vue";

const activeTab = ref("entries");
const mobileNavOpen = ref(false);
const isMobile = ref(false);

const tabs = [
  {
    key: "entries",
    label: "Meine Einträge",
    icon: BIconGrid,
    view: Entries,
  },
  {
    key: "requests",
    label: "Meine Anfragen",
    icon: BIconInbox,
    view: Requests,
  },
  {
    key: "sendedRequests",
    label: "Gesendete Anfragen",
    icon: BIconInbox,
    view: SendedRequests,
  },
  {
    key: "transactions",
    label: "Meine Transaktionen",
    icon: BIconArrowLeftRight,
    view: "",
  },
  {
    key: "settings",
    label: "Einstellungen",
    icon: BIconGear,
    view: Settings,
  },
];

const activeTabObject = computed(() => {
  return tabs.find((tab) => tab.key === activeTab.value) ?? tabs[0];
});

const activeTitle = computed(() => {
  return activeTabObject.value.label;
});

const activeView = computed(() => {
  return activeTabObject.value.view;
});

function handleResize() {
  isMobile.value = window.innerWidth < 1024;
  if (!isMobile.value) {
    mobileNavOpen.value = false;
  }
}

function selectTab(tabKey) {
  activeTab.value = tabKey;
  localStorage.setItem("activeTab", activeTab.value);

  if (isMobile.value) {
    mobileNavOpen.value = false;
  }
}

function toggleMobileNav() {
  mobileNavOpen.value = !mobileNavOpen.value;
}

function closeMobileNav() {
  mobileNavOpen.value = false;
}

function handleEscape(e) {
  if (e.key === "Escape") {
    closeMobileNav();
  }
}

onBeforeMount(() => {
  const activeTabStorage = localStorage.getItem("activeTab");
  const tabExists = tabs.some((tab) => tab.key === activeTabStorage);

  if (activeTabStorage && tabExists) {
    activeTab.value = activeTabStorage;
  } else {
    localStorage.setItem("activeTab", activeTab.value);
  }
})

onMounted(() => {
  handleResize();
  window.addEventListener("resize", handleResize);
  window.addEventListener("keydown", handleEscape);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", handleResize);
  window.removeEventListener("keydown", handleEscape);
});

watch(activeTab, () => {
  if (isMobile.value) {
    closeMobileNav();
  }
});
</script>

<template>
  <div class="min-h-screen text-neutral-900 dark:text-white font-sans">
    <div class="mx-auto flex max-w-[1600px] gap-6 px-4 py-4 sm:px-6  lg:py-10">
      <!-- Desktop Sidebar -->
      <aside
          class="hidden h-screen lg:block lg:w-72 shrink-0 rounded-3xl border border-neutral-200 bg-white p-4 shadow-sm dark:border-neutral-800 dark:bg-neutral-900 sticky top-8"
      >
        <div class="mb-4 px-2">
          <p class="text-xs font-semibold uppercase tracking-[0.18em] text-lime-500">
            Übersicht
          </p>
          <h2 class="mt-2 text-2xl font-bold tracking-tight">
            Dashboard
          </h2>
          <p class="mt-1 text-sm text-neutral-500 dark:text-neutral-400">
            Verwalte deine Einträge, Anfragen und Einstellungen zentral.
          </p>
        </div>

        <nav class="flex flex-col gap-2">
          <button
              v-for="tab in tabs"
              :key="tab.key"
              @click="selectTab(tab.key)"
              :class="
              activeTab === tab.key
                ? 'bg-lime-500 text-black shadow-sm'
                : 'text-neutral-700 hover:bg-neutral-100 dark:text-neutral-200 dark:hover:bg-neutral-800'
            "
              class="flex items-center gap-3 rounded-2xl px-4 py-3 text-left text-sm font-medium transition"
          >
            <component :is="tab.icon" class="text-base shrink-0" />
            <span class="truncate">{{ tab.label }}</span>
          </button>
        </nav>
      </aside>

      <!-- Main Content -->
      <div class="flex-1 min-w-0 flex flex-col gap-4 lg:gap-6">
        <!-- Mobile Topbar -->
        <div
            class="lg:hidden sticky top-0 z-30 rounded-2xl border border-neutral-200 bg-white/90 backdrop-blur px-4 py-3 shadow-sm dark:border-neutral-800 dark:bg-neutral-900/90"
        >
          <div class="flex items-center justify-between gap-3">
            <div class="min-w-0">
              <p class="text-xs font-semibold uppercase tracking-[0.18em] text-lime-500">
                Dashboard
              </p>
              <h1 class="truncate text-lg font-bold">
                {{ activeTitle }}
              </h1>
            </div>

            <button
                @click="toggleMobileNav"
                class="inline-flex h-11 w-11 items-center justify-center rounded-2xl border border-neutral-200 bg-white text-neutral-800 shadow-sm transition hover:bg-neutral-100 dark:border-neutral-700 dark:bg-neutral-900 dark:text-white dark:hover:bg-neutral-800"
                aria-label="Menü öffnen"
            >
              <BIconList class="text-xl" />
            </button>
          </div>
        </div>

        <!-- Mobile Overlay -->
        <transition
            enter-active-class="transition duration-200 ease-out"
            enter-from-class="opacity-0"
            enter-to-class="opacity-100"
            leave-active-class="transition duration-150 ease-in"
            leave-from-class="opacity-100"
            leave-to-class="opacity-0"
        >
          <div
              v-if="mobileNavOpen"
              class="fixed inset-0 z-40 bg-black/50 lg:hidden"
              @click="closeMobileNav"
          />
        </transition>

        <!-- Mobile Drawer -->
        <transition
            enter-active-class="transition duration-300 ease-out"
            enter-from-class="-translate-x-full"
            enter-to-class="translate-x-0"
            leave-active-class="transition duration-200 ease-in"
            leave-from-class="translate-x-0"
            leave-to-class="-translate-x-full"
        >
          <aside
              v-if="mobileNavOpen"
              class="fixed left-0 top-0 z-50 flex h-full w-[85%] max-w-[320px] flex-col border-r border-neutral-200 bg-white p-4 shadow-2xl dark:border-neutral-800 dark:bg-neutral-900 lg:hidden"
          >
            <div class="mb-4 flex items-start justify-between gap-3 px-2">
              <div>
                <p class="text-xs font-semibold uppercase tracking-[0.18em] text-lime-500">
                  Übersicht
                </p>
                <h2 class="mt-2 text-2xl font-bold tracking-tight">
                  Dashboard
                </h2>
                <p class="mt-1 text-sm text-neutral-500 dark:text-neutral-400">
                  Verwalte alles mobil und schnell.
                </p>
              </div>

              <button
                  @click="closeMobileNav"
                  class="inline-flex h-10 w-10 items-center justify-center rounded-2xl border border-neutral-200 text-neutral-700 transition hover:bg-neutral-100 dark:border-neutral-700 dark:text-neutral-200 dark:hover:bg-neutral-800"
                  aria-label="Menü schließen"
              >
                <BIconX class="text-xl" />
              </button>
            </div>

            <nav class="flex flex-col gap-2">
              <button
                  v-for="tab in tabs"
                  :key="tab.key"
                  @click="selectTab(tab.key)"
                  :class="
                  activeTab === tab.key
                    ? 'bg-lime-500 text-black shadow-sm'
                    : 'text-neutral-700 hover:bg-neutral-100 dark:text-neutral-200 dark:hover:bg-neutral-800'
                "
                  class="flex items-center gap-3 rounded-2xl px-4 py-3 text-left text-sm font-medium transition"
              >
                <component :is="tab.icon" class="text-base shrink-0" />
                <span class="truncate">{{ tab.label }}</span>
              </button>
            </nav>
          </aside>
        </transition>

        <!-- Content Card -->
        <div class="min-w-0">
          <transition name="fade-slide" mode="out-in">
            <component :is="activeView" />
          </transition>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.35s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(15px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-15px);
}
</style>