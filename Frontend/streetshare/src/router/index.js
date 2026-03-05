import { createRouter, createWebHistory } from "vue-router";

import LoginView from "@/views/Login/Login.vue";
import RegisterView from "@/views/Login/Register.vue";
import LandingPage from "@/views/LandingPage/LandingPage.vue";
import MainPage from "@/views/Main/Main.vue";
import UserMe from "@/views/User/UserMe.vue";
import {useAuthStore} from "@/store/authStore.js";

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
        path: "/user/me",
        name: "user_me",
        component: UserMe,
        meta: {requiresAuth: true, showNav: false }
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
        next("/main");
    } else {
        next();
    }

});

export default router;