<template>
  <div class="hero">
    <div class="hero-content">
      <div class="badge-launch">
        <i class="fas fa-chart-line"></i> Investigación Operativa · Soluciones
        Avanzadas
      </div>
      <h1>
        Optimización de <span class="highlight">Transporte de Carga</span
        ><br />Región Metropolitana de La Paz
      </h1>
      <p>
        Integración de Vogel, MODI y ruteo geoespacial. Reducción certificada de
        costos logísticos y simulación de contingencias en tiempo real.
      </p>

      <div class="hero-stats">
        <div class="stat">
          <div class="stat-number">-28%</div>
          <div class="stat-label">Costos operativos</div>
        </div>
        <div class="stat">
          <div class="stat-number">+37%</div>
          <div class="stat-label">Eficiencia de rutas</div>
        </div>
        <div class="stat">
          <div class="stat-number">99.5%</div>
          <div class="stat-label">Disponibilidad</div>
        </div>
      </div>

      <button class="btn-cta" @click="$emit('explore')">
        <i class="fas fa-chalkboard-user"></i> Explorar Dashboard
      </button>
    </div>

    <div class="hero-image">
      <img
        src="@/assets/img/landingPage/imagen.jpg"
        alt="Dashboard OptiLog"
        class="hero-img"
      />
      <div class="glass-card">
        <i class="fas fa-chart-pie"></i> Costo total mínimo garantizado
      </div>
    </div>
  </div>
</template>

<script setup>
defineEmits(["explore"]);
</script>

<style scoped>
.hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  align-items: center;
  padding: 4rem 0 5rem;
}

.hero-content h1 {
  font-size: 3.2rem;
  font-weight: 800;
  line-height: 1.2;
  background: linear-gradient(135deg, #ffffff, #d4a373);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  margin-bottom: 1.2rem;
}

.hero-content .highlight {
  color: #d4a373;
  background: none;
  -webkit-background-clip: unset;
}

.hero-content p {
  font-size: 1rem;
  color: #a0abb9;
  margin-bottom: 2rem;
  line-height: 1.6;
  max-width: 90%;
}

.hero-stats {
  display: flex;
  gap: 2rem;
  margin-top: 2rem;
}

.stat {
  text-align: left;
  border-left: 2px solid #d4a373;
  padding-left: 1rem;
}

.stat-number {
  font-size: 2rem;
  font-weight: 800;
  color: #d4a373;
  line-height: 1;
}

.stat-label {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #8e9aab;
}

.badge-launch {
  display: inline-block;
  background: rgba(212, 163, 115, 0.2);
  padding: 0.3rem 1rem;
  border-radius: 40px;
  font-size: 0.7rem;
  margin-bottom: 1rem;
  color: #d4a373;
  letter-spacing: 0.5px;
}

.btn-cta {
  background: #d4a373;
  color: #0a0f1a;
  border: none;
  padding: 0.8rem 2rem;
  border-radius: 40px;
  font-weight: 700;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 2rem;
  letter-spacing: 0.5px;
}

.btn-cta:hover {
  background: #e0b082;
  transform: scale(1.02);
  box-shadow: 0 8px 20px rgba(212, 163, 115, 0.3);
}

.hero-image {
  position: relative;
  background: rgba(20, 28, 40, 0.6);
  backdrop-filter: blur(12px);
  border-radius: 28px;
  border: 1px solid rgba(212, 163, 115, 0.3);
  box-shadow: 0 25px 40px -12px rgba(0, 0, 0, 0.5);
  height: auto;
  overflow: hidden;
  max-width: 500px; 
  margin: 0 auto;
  border-radius: 28px;
}

.hero-image svg {
  width: 100%;
  border-radius: 20px;
}

.hero-img {
  width: 100%;
  height: 100%;
  border-radius: 20px;
  display: block;
  object-fit: cover;
}

.glass-card {
  background: rgba(10, 15, 26, 0.8);
  backdrop-filter: blur(12px);
  border-radius: 1rem;
  padding: 0.8rem 1.2rem;
  position: absolute;
  bottom: -15px;
  right: -10px;
  border: 1px solid rgba(212, 163, 115, 0.4);
  font-size: 0.8rem;
  font-weight: 600;
}

@media (max-width: 850px) {
  .hero {
    grid-template-columns: 1fr;
    text-align: center;
  }

  .hero-content p {
    max-width: 100%;
  }

  .hero-stats {
    justify-content: center;
  }

  .hero-content h1 {
    font-size: 2rem;
  }
}
</style>
