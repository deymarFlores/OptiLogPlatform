<template>
  <section id="metodos" class="methods-section">
    <h2 class="section-title">Modelos de Optimización</h2>
    <div class="methods-grid">
      <div v-for="method in methods" :key="method.id" class="method-item">
        <i :class="`fas ${method.icon}`"></i>
        <h4>{{ method.title }}</h4>
        <p>{{ method.description }}</p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted } from 'vue';

const methods = [
  {
    id: 1,
    icon: 'fa-chart-simple',
    title: 'Problema de Transporte',
    description: 'Minimización de costos de envío desde múltiples fuentes a destinos.'
  },
  {
    id: 2,
    icon: 'fa-calculator',
    title: 'Método de Vogel',
    description: 'Solución inicial de alta calidad basada en penalizaciones.'
  },
  {
    id: 3,
    icon: 'fa-arrow-trend-down',
    title: 'MODI (UV)',
    description: 'Optimización iterativa hasta alcanzar solución óptima.'
  },
  {
    id: 4,
    icon: 'fa-route',
    title: 'Ruta Óptima',
    description: 'Búsqueda exhaustiva (DFS) con función de costo multicriterio.'
  },
  {
    id: 5,
    icon: 'fa-weight-hanging',
    title: 'Pesos Dinámicos',
    description: 'Ajusta α, β, γ: distancia, costo monetario y tiempo.'
  },
  {
    id: 6,
    icon: 'fa-code-branch',
    title: 'Backtracking',
    description: 'Exploración de rutas sin usar Dijkstra, 100% manual.'
  }
];

onMounted(() => {
  // Animación de carga
  const items = document.querySelectorAll('.method-item');
  items.forEach((el, idx) => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    setTimeout(() => {
      el.style.transition = 'all 0.5s ease';
      el.style.opacity = '1';
      el.style.transform = 'translateY(0)';
    }, idx * 80);
  });
});
</script>

<style scoped>
.methods-section {
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(12px);
  border-radius: 2rem;
  padding: 3rem 2rem;
  margin: 2rem 0;
  border: 1px solid rgba(212, 163, 115, 0.2);
}

.section-title {
  text-align: center;
  font-size: 2rem;
  font-weight: 700;
  margin: 0 0 2rem;
  letter-spacing: -0.3px;
  position: relative;
  color: #ffffff;
}

.section-title:after {
  content: '';
  display: block;
  width: 60px;
  height: 3px;
  background: #d4a373;
  margin: 0.8rem auto 0;
  border-radius: 3px;
}

.methods-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  text-align: center;
}

.method-item {
  padding: 1.5rem;
}

.method-item i {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: #d4a373;
}

.method-item h4 {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.method-item p {
  font-size: 0.8rem;
  color: #9aa5b5;
}

@media (max-width: 850px) {
  .methods-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
}
</style>
