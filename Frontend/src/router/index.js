import { createRouter, createWebHistory } from "vue-router";

import { LandingPage } from "@/pages/landingPage";
import { LoginPage } from "@/pages/login";
import { SetupPage } from "@/pages/setup";
import { DashboardLayout, ClientDashboard } from "@/pages/dashboard";

const routes = [
  // ============================================
  //                    HOME
  // ============================================
  {
    path: "/",
    component: LandingPage,
  },

  // ============================================
  //                   AUTH
  // ============================================
  {
    path: "/login",
    component: LoginPage,
  },

  // ============================================
  //                   SETUP
  // ============================================
  {
    path: "/setup",
    component: SetupPage,
  },

  // ============================================
  //                 DASHBOARD
  // ============================================
  {
    path: "/dashboard",
    component: DashboardLayout,
  },

  {
    path: "/client-dashboard",
    component: ClientDashboard,
  },
];

export const router = createRouter({
  history: createWebHistory(),

  routes,
});
