<template>
  <section id="demo" class="cta-section">
    <h2>Optimice su cadena de suministro</h2>
    <p class="cta-subtitle">Acceda a la plataforma de optimización con mapa Leaflet, transporte y ruteo inteligente.</p>
    <button class="btn-large" @click="$emit('startAnalysis')">
      <i class="fas fa-chart-line"></i> Iniciar Análisis
    </button>
    <p class="cta-footer">Demo estratégica · Investigación Operativa · Sin infraestructura externa</p>
  </section>
</template>

<script setup>
defineEmits(['startAnalysis']);
</script>

<style scoped>
.cta-section {
  text-align: center;
  background: rgba(15, 21, 30, 0.7);
  backdrop-filter: blur(12px);
  border-radius: 2rem;
  padding: 3rem;
  margin: 3rem 0;
  border: 1px solid rgba(212, 163, 115, 0.2);
}

.cta-section h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.cta-subtitle {
  color: #a0abb9;
  margin-bottom: 1.5rem;
}

.btn-large {
  background: #d4a373;
  color: #0a0f1a;
  border: none;
  padding: 1rem 2.8rem;
  font-size: 1rem;
  font-weight: 700;
  border-radius: 50px;
  cursor: pointer;
  margin-top: 1.5rem;
  transition: 0.2s;
  letter-spacing: 0.5px;
}

.btn-large:hover {
  background: #e0b082;
  transform: scale(1.02);
  box-shadow: 0 8px 20px rgba(212, 163, 115, 0.3);
}

.cta-footer {
  font-size: 0.7rem;
  margin-top: 1.2rem;
  opacity: 0.7;
}
</style>
