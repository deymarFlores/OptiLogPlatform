<template>
  <nav class="navbar">
    <div class="logo">
      <i class="fas fa-chart-network"></i>
      <span>OptiLog<span class="logo-highlight">Platform</span></span>
    </div>
    <div class="nav-links">
      <a href="#features" @click.prevent="scrollToSection('#features')">Capacidades</a>
      <a href="#metodos" @click.prevent="scrollToSection('#metodos')">Métodos IO</a>
      <a href="#demo" @click.prevent="scrollToSection('#demo')">Estrategia</a>
      <button class="btn-demo" @click="$emit('openModal')">
        <i class="fas fa-lock-open"></i> Acceso Corporativo
      </button>
    </div>
  </nav>
</template>

<script setup>
const scrollToSection = (selector) => {
  const element = document.querySelector(selector);
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' });
  }
};
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.8rem 0;
  flex-wrap: wrap;
  gap: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1.5rem;
  font-weight: 700;
  letter-spacing: -0.5px;
  color: #ffffff;
}

.logo i {
  color: #d4a373;
  font-size: 2rem;
}

.logo span {
  background: linear-gradient(135deg, #ffffff, #d4a373);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.logo-highlight {
  color: #d4a373;
  background: none;
  -webkit-background-clip: unset;
}

.nav-links {
  display: flex;
  gap: 2.2rem;
  align-items: center;
}

.nav-links a {
  text-decoration: none;
  color: #cbd5e6;
  font-weight: 500;
  font-size: 0.9rem;
  transition: 0.2s;
  letter-spacing: 0.3px;
}

.nav-links a:hover {
  color: #d4a373;
}

.btn-demo {
  background: rgba(212, 163, 115, 0.15);
  border: 1px solid rgba(212, 163, 115, 0.5);
  color: #d4a373;
  padding: 0.6rem 1.5rem;
  border-radius: 40px;
  font-weight: 600;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(4px);
}

.btn-demo:hover {
  background: #d4a373;
  color: #0a0f1a;
  border-color: #d4a373;
}

@media (max-width: 850px) {
  .navbar {
    flex-direction: column;
  }
  
  .nav-links {
    flex-direction: column;
    width: 100%;
  }
}
</style>
