<template>
  <nav class="navbar-widget">
    <div class="navbar-content">
      <div class="navbar-brand">
        <i class="fas fa-chart-network"></i>
        <span>OptiLog<span class="brand-highlight">Executive</span></span>
      </div>
      <div class="navbar-actions">
        <button class="nav-btn" title="Documentación">
          <i class="fas fa-book"></i>
        </button>
        <button class="nav-btn" title="Configuración">
          <i class="fas fa-cog"></i>
        </button>
        <button class="nav-btn logout-btn" title="Cerrar Sesión">
          <i class="fas fa-sign-out-alt"></i>
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup>
</script>

<style scoped>
.navbar-widget {
  background: rgba(18, 24, 34, 0.9);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(212, 163, 115, 0.2);
  padding: 1.2rem 2rem;
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar-content {
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

.navbar-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.nav-btn {
  background: rgba(212, 163, 115, 0.1);
  border: 1px solid rgba(212, 163, 115, 0.3);
  color: #d4a373;
  width: 40px;
  height: 40px;
  border-radius: 0.75rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
}

.nav-btn:hover {
  background: rgba(212, 163, 115, 0.2);
  border-color: #d4a373;
  transform: translateY(-2px);
}

.nav-btn.logout-btn {
  color: #e05a5a;
  border-color: rgba(224, 61, 61, 0.3);
  background: rgba(224, 61, 61, 0.1);
}

.nav-btn.logout-btn:hover {
  background: rgba(224, 61, 61, 0.2);
  border-color: #e05a5a;
}
</style>