<template>
  <div class="landing-page">
    <div class="bg-overlay"></div>
    <div class="bg-gradient"></div>

    <div class="landing">
      <HeaderNav @openModal="openAccessModal" />

      <HeroSection @explore="handleDashboard" />

      <FeaturesGrid />

      <MethodsSection />

      <CTASection @startAnalysis="openAccessModal" />

      <FooterSection />
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";

// Componentes
import HeaderNav from "./components/HeaderNav.vue";
import HeroSection from "./components/HeroSection.vue";
import FeaturesGrid from "./components/FeaturesGrid.vue";
import MethodsSection from "./components/MethodsSection.vue";
import CTASection from "./components/CTASection.vue";
import FooterSection from "./components/FooterSection.vue";

const router = useRouter();

const openAccessModal = () => {
  router.push("/login");
};

const handleDashboard = () => {
  router.push("/dashboard");
};
</script>

<style scoped>
.landing-page {
  position: relative;
  width: 100%;
  min-height: 100vh;
  background: #0a0f1a;
  color: #e8edf2;
  overflow-x: hidden;
}

/* Fondos dinámicos */
.bg-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -2;
  background-image: url("https://images.unsplash.com/photo-1494412574643-ff11b0a5c1c3?q=80&w=2070&auto=format");
  background-size: cover;
  background-position: center;
  filter: brightness(0.25) contrast(1.1);
}

.bg-gradient {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  background: linear-gradient(
    135deg,
    rgba(10, 15, 26, 0.92) 0%,
    rgba(20, 28, 40, 0.88) 100%
  );
  backdrop-filter: blur(2px);
}

/* Layout principal */
.landing {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
  position: relative;
  z-index: 2;
}

@media (max-width: 850px) {
  .landing {
    padding: 0 1.2rem;
  }
}
</style>

<style>
/* Estilos globales para la página */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: "Inter", sans-serif;
  background: #0a0f1a;
  color: #e8edf2;
  overflow-x: hidden;
}
</style>
