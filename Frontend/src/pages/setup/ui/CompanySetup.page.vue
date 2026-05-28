<template>
  <div class="setup-wrapper">
    <div class="bg-overlay"></div>
    <div class="bg-gradient"></div>

    <div class="setup-container">
      <div class="setup-header">
        <i class="fas fa-cog"></i>
        <h1>Configuración Inicial</h1>
        <p>Registra tu empresa y tipos de puntos de acopio</p>
      </div>

      <div class="setup-content">
        <div v-show="currentStep === 1" class="step-content">
          <CompanyForm @next="goToStep2" />
        </div>

        <div v-show="currentStep === 2" class="step-content">
          <PointTypesForm @back="goToStep1" @complete="handleSetupComplete" />
        </div>
      </div>

      <div class="progress-indicator">
        <div :class="['step', { active: currentStep === 1 }]">
          <span>1</span>
          <p>Empresa</p>
        </div>
        <div class="line"></div>
        <div :class="['step', { active: currentStep === 2 }]">
          <span>2</span>
          <p>Tipos de Puntos</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import CompanyForm from './components/CompanyForm.vue';
import PointTypesForm from './components/PointTypesForm.vue';

const router = useRouter();
const currentStep = ref(1);

const goToStep2 = () => {
  currentStep.value = 2;
};

const goToStep1 = () => {
  currentStep.value = 1;
};

const handleSetupComplete = () => {
  console.log('✅ Configuración completada');
  router.push('/dashboard');
};
</script>

<style scoped>
.setup-wrapper {
  position: relative;
  width: 100%;
  min-height: 100vh;
  background: #0a0f1a;
  color: #e8edf2;
  overflow-x: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.bg-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -2;
  background-image: url('https://images.unsplash.com/photo-1494412574643-ff11b0a5c1c3?q=80&w=2070&auto=format');
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
  background: linear-gradient(135deg, rgba(10, 15, 26, 0.92) 0%, rgba(20, 28, 40, 0.88) 100%);
  backdrop-filter: blur(2px);
}

.setup-container {
  max-width: 600px;
  width: 100%;
  background: rgba(18, 24, 34, 0.8);
  backdrop-filter: blur(12px);
  border-radius: 2rem;
  padding: 3rem;
  border: 1px solid rgba(212, 163, 115, 0.2);
  box-shadow: 0 25px 40px -12px rgba(0, 0, 0, 0.5);
  position: relative;
  z-index: 10;
}

.setup-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.setup-header i {
  font-size: 3rem;
  color: #d4a373;
  margin-bottom: 1rem;
  display: block;
}

.setup-header h1 {
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
  background: linear-gradient(135deg, #ffffff, #d4a373);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.setup-header p {
  color: #a0abb9;
  font-size: 0.95rem;
}

.setup-content {
  min-height: 300px;
  margin-bottom: 2rem;
}

.step-content {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.progress-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(212, 163, 115, 0.2);
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  opacity: 0.5;
  transition: all 0.3s ease;
}

.step.active {
  opacity: 1;
}

.step span {
  width: 40px;
  height: 40px;
  background: rgba(212, 163, 115, 0.1);
  border: 2px solid rgba(212, 163, 115, 0.3);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: #d4a373;
}

.step.active span {
  background: #d4a373;
  color: #0a0f1a;
  border-color: #d4a373;
}

.step p {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #8e9aab;
}

.line {
  width: 30px;
  height: 2px;
  background: rgba(212, 163, 115, 0.2);
}

@media (max-width: 640px) {
  .setup-container {
    padding: 2rem;
  }

  .setup-header h1 {
    font-size: 1.5rem;
  }
}
</style>
