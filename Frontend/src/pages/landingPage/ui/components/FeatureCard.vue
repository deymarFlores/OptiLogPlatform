<template>
  <div class="feature-card">
    <div class="feature-icon">
      <i :class="`fas ${icon}`"></i>
    </div>
    <h3>{{ title }}</h3>
    <p>{{ description }}</p>
  </div>
</template>

<script setup>
defineProps({
  icon: {
    type: String,
    required: true
  },
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  }
});
</script>

<style scoped>
.feature-card {
  background: rgba(18, 24, 34, 0.7);
  backdrop-filter: blur(10px);
  border-radius: 1.5rem;
  padding: 1.8rem;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.feature-card:hover {
  transform: translateY(-6px);
  background: rgba(28, 36, 48, 0.8);
  border-color: rgba(212, 163, 115, 0.3);
  box-shadow: 0 15px 30px -12px rgba(0, 0, 0, 0.5);
}

.feature-icon {
  width: 55px;
  height: 55px;
  background: rgba(212, 163, 115, 0.12);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.2rem;
  border: 1px solid rgba(212, 163, 115, 0.2);
}

.feature-icon i {
  font-size: 1.6rem;
  color: #d4a373;
}

.feature-card h3 {
  font-size: 1.2rem;
  margin-bottom: 0.6rem;
  font-weight: 600;
}

.feature-card p {
  color: #9aa5b5;
  font-size: 0.85rem;
  line-height: 1.5;
}
</style>
