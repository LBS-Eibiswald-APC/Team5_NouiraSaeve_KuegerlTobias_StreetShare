import { createRouter, createWebHistory } from "vue-router";

import LoginView from "@/components/Login/Login.vue";
import LandingPage from "@/components/Landing/LandingPage.vue";
import {useAuthStore} from "@/store/authStore.js";

const routes = [
    {
        path: "/login",
        name: "login",
        component: LoginView,
        meta: { requiresAuth: false }
    },
    {
        path: "/",
        name: "landing",
        component: LandingPage,
        meta: { requiresAuth: true }
    }

];

const router = createRouter({
    history: createWebHistory(),
    routes
});


router.beforeEach((to, from, next) => {
    const auth = useAuthStore();
    if (to.meta.requiresAuth && !auth.isAuthenticated) {
        next("/login");
    } else if (to.path === "/login" && auth.isAuthenticated) {
        next("/");
    } else {
        next();
    }

});

export default router;