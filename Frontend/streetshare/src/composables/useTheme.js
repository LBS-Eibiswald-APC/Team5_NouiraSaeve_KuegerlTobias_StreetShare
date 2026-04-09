import { ref } from "vue";

const isDark = ref(localStorage.getItem("theme") === "dark");

function applyTheme() {
    if (isDark.value) {
        document.documentElement.classList.add("dark");
        localStorage.setItem("theme", "dark");
    } else {
        document.documentElement.classList.remove("dark");
        localStorage.setItem("theme", "light");
    }
}

function toggleTheme() {
    isDark.value = !isDark.value;
    applyTheme();
}

export function useTheme() {
    return {
        isDark,
        toggleTheme,
        applyTheme,
    };
}