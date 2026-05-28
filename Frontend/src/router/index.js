import { createRouter, createWebHistory } from "vue-router";

import { LandingPage } from "@/pages/landingPage";
import { SetupPage } from "@/pages/setup";
import { DashboardLayout } from "@/pages/dashboard";

const routes = [
  // ============================================
  //                    HOME
  // ============================================
  {
    path: "/",
    component: LandingPage,
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
];

export const router = createRouter({
  history: createWebHistory(),

  routes,
});
