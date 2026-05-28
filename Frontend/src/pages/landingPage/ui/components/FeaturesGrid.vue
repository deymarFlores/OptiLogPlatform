<template>
  <section id="features" class="features-section">
    <h2 class="section-title">Inteligencia Logística</h2>
    <div class="features-grid">
      <FeatureCard
        v-for="feature in features"
        :key="feature.id"
        :icon="feature.icon"
        :title="feature.title"
        :description="feature.description"
      />
    </div>
  </section>
</template>

<script setup>
import { onMounted } from 'vue';
import FeatureCard from './FeatureCard.vue';

const features = [
  {
    id: 1,
    icon: 'fa-warehouse',
    title: 'Gestión de Almacenes',
    description: 'Registro geoespacial de centros de acopio y clientes con capacidades y demandas configurables.'
  },
  {
    id: 2,
    icon: 'fa-chart-line',
    title: 'Vogel + MODI',
    description: 'Algoritmos clásicos de transporte para minimizar costos de distribución. Asignación óptima almacén→cliente.'
  },
  {
    id: 3,
    icon: 'fa-road',
    title: 'Ruta Óptima Multicriterio',
    description: 'Búsqueda exhaustiva (DFS) con pesos α, β, γ: distancia, costo monetario y tiempo.'
  },
  {
    id: 4,
    icon: 'fa-map-marked-alt',
    title: 'Visualización Geoespacial',
    description: 'Conexiones interactivas, grosores proporcionales a tonelaje, rutas óptimas en tiempo real.'
  },
  {
    id: 5,
    icon: 'fa-ban',
    title: 'Simulación de Contingencias',
    description: 'Bloqueos, accidentes o cierre de rutas. Reoptimización inmediata de alternativas.'
  },
  {
    id: 6,
    icon: 'fa-chart-simple',
    title: 'Executive Dashboard',
    description: 'KPIs: costo total de transporte, métricas de ruta óptima, exportación de datos JSON.'
  }
];

onMounted(() => {
  // Animación de carga
  const cards = document.querySelectorAll('.feature-card');
  cards.forEach((el, idx) => {
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
.features-section {
  padding: 2rem 0;
}

.section-title {
  text-align: center;
  font-size: 2rem;
  font-weight: 700;
  margin: 4rem 0 2rem;
  letter-spacing: -0.3px;
  position: relative;
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

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.8rem;
  margin-bottom: 3rem;
}
</style>
