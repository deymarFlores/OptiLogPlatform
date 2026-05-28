<template>
  <nav class="setup-navbar">
    <div class="navbar-container">
      <div class="navbar-brand">
        <i class="fas fa-chart-network"></i>
        <span>OptiLog<span class="brand-highlight">Executive</span></span>
      </div>
      <div class="navbar-info">
        <p><i class="fas fa-cog"></i> Configuración Inicial</p>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.setup-navbar {
  background: rgba(18, 24, 34, 0.9);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(212, 163, 115, 0.2);
  padding: 1.2rem 2rem;
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar-container {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #ffffff;
  font-weight: 700;
  font-size: 1.3rem;
  letter-spacing: -0.5px;
}

.navbar-brand i {
  color: #d4a373;
  font-size: 2rem;
}

.navbar-brand span {
  background: linear-gradient(135deg, #ffffff, #d4a373);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.brand-highlight {
  color: #d4a373;
  background: none;
  -webkit-background-clip: unset;
}

.navbar-info {
  color: #a0abb9;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.navbar-info p {
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.navbar-info i {
  color: #d4a373;
}
</style>
