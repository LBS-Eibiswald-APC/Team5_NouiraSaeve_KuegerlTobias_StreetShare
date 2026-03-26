import { createRouter, createWebHistory } from "vue-router";

import LoginView from "@/views/Login/Login.vue";
import RegisterView from "@/views/Login/Register.vue";
import LandingPage from "@/views/LandingPage/LandingPage.vue";
import MainPage from "@/views/Main/Main.vue";
import {useAuthStore} from "@/store/authStore.js";
import Dashboard from "@/views/User/Dashboard.vue";

const routes = [
    {
        path: "/login",
        name: "login",
        component: LoginView,
        meta: { requiresAuth: false, showNav: true }
    },
    {
        path: "/register",
        name: "register",
        component: RegisterView,
        meta: { requiresAuth: false, showNav: true  }
    },
    {
        path: "/main",
        name: "main",
        component: MainPage,
        meta: { requiresAuth: true, showNav: false  }
    },
    {
        path: "/",
        name: "landing",
        component: LandingPage,
        meta: {requiresAuth: false, showNav: null }
    },
    {
        path: "/dashboard",
        name: "dashboard",
        component: Dashboard,
        meta: {requiresAuth: true, showNav: false }
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});


router.beforeEach(async (to, from, next) => {
    const auth = useAuthStore();

    await auth.ensureInitialized();

    if (to.meta.requiresAuth && !auth.isAuthenticated) {
        next("/login");
    } else if (to.path === "/login" && auth.isAuthenticated) {
        next("/main");
    } else {
        next();
    }

});

export default router;
