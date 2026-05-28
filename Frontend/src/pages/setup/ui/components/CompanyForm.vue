<template>
  <div class="form-container">
    <h2>Información de tu Empresa</h2>
    <p class="form-subtitle">Completa los datos básicos de tu empresa</p>

    <form @submit.prevent="handleSubmit" class="company-form">
      <div class="form-group">
        <label for="companyName">Nombre de la Empresa</label>
        <input
          id="companyName"
          v-model="form.companyName"
          type="text"
          placeholder="Ej: OptiLog Bolivia"
          required
        />
      </div>

      <div class="form-group">
        <label for="description">Descripción</label>
        <textarea
          id="description"
          v-model="form.description"
          placeholder="Describe tu negocio..."
          rows="3"
        ></textarea>
      </div>

      <div class="form-group">
        <label for="city">Ciudad</label>
        <input
          id="city"
          v-model="form.city"
          type="text"
          placeholder="Ej: La Paz"
          required
        />
      </div>

      <div class="form-group">
        <label for="phone">Teléfono de Contacto</label>
        <input
          id="phone"
          v-model="form.phone"
          type="tel"
          placeholder="Ej: +591 2 1234567"
        />
      </div>

      <button type="submit" class="btn-next">
        <i class="fas fa-arrow-right"></i> Siguiente
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useSetupStore } from '@/pages/setup/composables/useSetupStore';

const emit = defineEmits(['next']);
const setupStore = useSetupStore();

const form = ref({
  companyName: setupStore.company.name || '',
  description: setupStore.company.description || '',
  city: setupStore.company.city || '',
  phone: setupStore.company.phone || ''
});

const handleSubmit = () => {
  setupStore.setCompany({
    name: form.value.companyName,
    description: form.value.description,
    city: form.value.city,
    phone: form.value.phone
  });

  console.log('📝 Empresa registrada:', {
    name: form.value.companyName,
    city: form.value.city
  });

  emit('next');
};
</script>

<style scoped>
.form-container {
  animation: slideIn 0.4s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

h2 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: #ffffff;
}

.form-subtitle {
  color: #a0abb9;
  font-size: 0.9rem;
  margin-bottom: 1.5rem;
}

.company-form {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #cbd5e6;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

input,
textarea {
  background: rgba(10, 15, 26, 0.6);
  border: 1px solid rgba(212, 163, 115, 0.3);
  border-radius: 0.75rem;
  padding: 0.8rem 1rem;
  color: #e8edf2;
  font-size: 0.9rem;
  font-family: inherit;
  transition: all 0.3s ease;
}

input:focus,
textarea:focus {
  outline: none;
  background: rgba(10, 15, 26, 0.8);
  border-color: #d4a373;
  box-shadow: 0 0 0 3px rgba(212, 163, 115, 0.1);
}

textarea {
  resize: vertical;
  min-height: 80px;
}

.btn-next {
  background: #d4a373;
  color: #0a0f1a;
  border: none;
  padding: 0.9rem 2rem;
  border-radius: 0.75rem;
  font-weight: 700;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 1rem;
}

.btn-next:hover {
  background: #e0b082;
  transform: translateX(4px);
  box-shadow: 0 8px 20px rgba(212, 163, 115, 0.3);
}

.btn-next:active {
  transform: translateX(2px);
}
</style>
