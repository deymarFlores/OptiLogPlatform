<template>
  <footer class="footer">
    <span><i class="fas fa-copyright"></i> 2025 OptiLog · Soluciones en Logística</span>
    <span><i class="fas fa-map-pin"></i> Basado en Vogel, MODI y ruteo DFS</span>
  </footer>
</template>

<style scoped>
.footer {
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  padding: 2rem 0;
  margin-top: 3rem;
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
  color: #6c7a8e;
  font-size: 0.8rem;
}

@media (max-width: 850px) {
  .footer {
    flex-direction: column;
    text-align: center;
  }
}
</style>
