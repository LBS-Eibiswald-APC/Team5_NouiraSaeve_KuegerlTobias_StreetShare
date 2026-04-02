<script setup>
import { BIconChatDots, BIconSearch } from "bootstrap-icons-vue";

defineProps({
  loading: {
    type: Boolean,
    default: false,
  },
  search: {
    type: String,
    default: "",
  },
  filteredChats: {
    type: Array,
    default: () => [],
  },
  selectedChatId: {
    type: Number,
    default: null,
  },
  getChatTitle: {
    type: Function,
    required: true,
  },
  getChatPartner: {
    type: Function,
    required: true,
  },
  getChatActivity: {
    type: Function,
    required: true,
  },
  getLastMessage: {
    type: Function,
    required: true,
  },
});

const emit = defineEmits(["update:search", "select"]);
</script>

<template>
  <aside class="flex h-full min-h-0 flex-col overflow-hidden rounded-[28px] border border-neutral-200 bg-neutral-50 shadow-xl dark:border-neutral-800 dark:bg-neutral-950 lg:rounded-none lg:border-0 lg:border-r lg:bg-neutral-50/80 lg:shadow-sm lg:dark:bg-neutral-950/40">
    <div class="border-b border-neutral-200 p-5 dark:border-neutral-800">
      <div class="flex items-center gap-3">
        <div class="flex h-11 w-11 items-center justify-center rounded-2xl bg-lime-500 text-black">
          <BIconChatDots class="text-lg" />
        </div>
        <div>
          <p class="text-xs font-semibold uppercase tracking-[0.18em] text-lime-500">
            Postfach
          </p>
          <h2 class="text-xl font-bold tracking-tight text-neutral-900 dark:text-white">
            Chats
          </h2>
        </div>
      </div>

      <div class="relative mt-5">
        <BIconSearch class="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-neutral-400" />
        <input
          :value="search"
          type="text"
          placeholder="Chats durchsuchen"
          class="w-full rounded-2xl border border-neutral-200 bg-neutral-50 py-3 pl-11 pr-4 text-sm text-neutral-700 placeholder:text-neutral-400 focus:outline-none focus:ring-2 focus:ring-lime-400 dark:border-neutral-700 dark:bg-neutral-950 dark:text-white dark:placeholder:text-neutral-500"
          @input="emit('update:search', $event.target.value)"
        />
      </div>
    </div>

    <div class="min-h-0 flex-1 overflow-y-auto p-3 overscroll-contain">
      <div v-if="loading" class="space-y-3">
        <div
          v-for="index in 4"
          :key="index"
          class="animate-pulse rounded-2xl border border-neutral-200 p-4 dark:border-neutral-800"
        >
          <div class="h-4 w-2/3 rounded bg-neutral-200 dark:bg-neutral-800"></div>
          <div class="mt-3 h-3 w-1/2 rounded bg-neutral-200 dark:bg-neutral-800"></div>
          <div class="mt-4 h-3 w-full rounded bg-neutral-200 dark:bg-neutral-800"></div>
        </div>
      </div>

      <div v-else-if="filteredChats.length === 0" class="flex min-h-[300px] flex-col items-center justify-center px-6 text-center">
        <div class="flex h-16 w-16 items-center justify-center rounded-3xl bg-neutral-100 dark:bg-neutral-800">
          <BIconChatDots class="text-2xl text-neutral-500 dark:text-neutral-300" />
        </div>
        <h3 class="mt-5 text-lg font-semibold text-neutral-900 dark:text-white">
          Noch keine Chats
        </h3>
        <p class="mt-2 max-w-xs text-sm leading-6 text-neutral-500 dark:text-neutral-400">
          Sobald eine Unterhaltung startet, erscheint sie hier in deiner Übersicht.
        </p>
      </div>

      <template v-else>
        <button
          v-for="chat in filteredChats"
          :key="chat.id"
          type="button"
          :class="selectedChatId === chat.id
            ? 'border-lime-400 bg-lime-50 dark:border-lime-500/70 dark:bg-lime-500/10'
            : chat.unread_count > 0
              ? 'border-red-200 bg-red-50/70 dark:border-red-900/60 dark:bg-red-950/20'
              : 'border-neutral-200 bg-white/70 hover:bg-white dark:border-neutral-800 dark:bg-neutral-900/40 dark:hover:bg-neutral-800/70'"
          class="mb-2 block w-full rounded-2xl border p-4 text-left transition"
          @click="emit('select', chat)"
        >
          <div class="flex items-start justify-between gap-3">
            <div class="min-w-0">
              <p class="truncate text-sm font-semibold text-neutral-900 dark:text-white">
                {{ getChatTitle(chat) }}
              </p>
              <p class="mt-1 truncate text-xs text-neutral-500 dark:text-neutral-400">
                {{ getChatPartner(chat) }}
              </p>
            </div>
            <div class="flex shrink-0 items-center gap-2">
              <span
                v-if="chat.unread_count > 0"
                class="inline-flex min-w-6 items-center justify-center rounded-full bg-red-500 px-2 py-1 text-[11px] font-bold text-white"
              >
                {{ chat.unread_count }}
              </span>
              <span class="rounded-full bg-neutral-100 px-2.5 py-1 text-[11px] font-medium text-neutral-600 dark:bg-neutral-800 dark:text-neutral-300">
                {{ getChatActivity(chat) }}
              </span>
            </div>
          </div>

          <p class="mt-3 line-clamp-2 text-sm leading-6 text-neutral-500 dark:text-neutral-400">
            {{ getLastMessage(chat) }}
          </p>
        </button>
      </template>
    </div>
  </aside>
</template>
