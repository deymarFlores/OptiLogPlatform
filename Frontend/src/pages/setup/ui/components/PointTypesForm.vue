<template>
  <div class="form-container">
    <h2>Tipos de Puntos de Acopio</h2>
    <p class="form-subtitle">Define los tipos de puntos que tu empresa maneja</p>

    <div class="points-list">
      <div
        v-for="pointType in form.pointTypes"
        :key="pointType.id"
        class="point-item"
      >
        <div class="point-header">
          <input
            v-model="pointType.name"
            type="text"
            class="point-name"
            placeholder="Ej: Almacén, Tienda, Centro de Distribución"
          />
          <button type="button" class="btn-remove" @click="removePointType(pointType.id)">
            <i class="fas fa-trash"></i>
          </button>
        </div>
        <div class="point-details">
          <div class="detail-group">
            <label>Icono</label>
            <select v-model="pointType.icon" class="icon-select">
              <option value="fa-warehouse">📦 Almacén</option>
              <option value="fa-store">🏪 Tienda</option>
              <option value="fa-truck">🚚 Centro de Distribución</option>
              <option value="fa-boxes">📫 Punto de Recepción</option>
              <option value="fa-location-dot">📍 Sucursal</option>
            </select>
          </div>
          <div class="detail-group">
            <label>Color</label>
            <input
              v-model="pointType.color"
              type="color"
              class="color-input"
            />
          </div>
        </div>
      </div>
    </div>

    <button type="button" class="btn-add" @click="addPointType">
      <i class="fas fa-plus"></i> Agregar Tipo de Punto
    </button>

    <div class="form-actions">
      <button type="button" class="btn-back" @click="$emit('back')">
        <i class="fas fa-arrow-left"></i> Atrás
      </button>
      <button type="button" class="btn-complete" @click="handleComplete">
        <i class="fas fa-check"></i> Completar Configuración
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useSetupStore } from '@/pages/setup/composables/useSetupStore';

const emit = defineEmits(['back', 'complete']);
const setupStore = useSetupStore();

const form = ref({
  pointTypes: setupStore.pointTypes.length
    ? setupStore.pointTypes
    : [
        { id: 1, name: 'Almacén', icon: 'fa-warehouse', color: '#1e4a6e' },
        { id: 2, name: 'Tienda', icon: 'fa-store', color: '#e67e22' }
      ]
});

let nextId = 3;

const addPointType = () => {
  form.value.pointTypes.push({
    id: nextId++,
    name: '',
    icon: 'fa-warehouse',
    color: '#' + Math.floor(Math.random() * 16777215).toString(16)
  });
};

const removePointType = (id) => {
  form.value.pointTypes = form.value.pointTypes.filter(pt => pt.id !== id);
};

const handleComplete = () => {
  const validTypes = form.value.pointTypes.filter(pt => pt.name.trim());

  if (validTypes.length === 0) {
    console.error('❌ Debes agregar al menos un tipo de punto');
    return;
  }

  setupStore.setPointTypes(validTypes);

  console.log('✅ Tipos de puntos registrados:', validTypes);

  emit('complete');
};
</script>

<style scoped>
.form-container {
  animation: slideIn 0.4s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(20px);
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

.points-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
  max-height: 300px;
  overflow-y: auto;
}

.point-item {
  background: rgba(10, 15, 26, 0.4);
  border: 1px solid rgba(212, 163, 115, 0.2);
  border-radius: 1rem;
  padding: 1rem;
}

.point-header {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.point-name {
  flex: 1;
  background: rgba(10, 15, 26, 0.6);
  border: 1px solid rgba(212, 163, 115, 0.3);
  border-radius: 0.5rem;
  padding: 0.6rem 0.8rem;
  color: #e8edf2;
  font-size: 0.9rem;
  font-weight: 600;
}

.point-name:focus {
  outline: none;
  border-color: #d4a373;
}

.btn-remove {
  background: rgba(224, 61, 61, 0.2);
  border: 1px solid rgba(224, 61, 61, 0.4);
  color: #e05a5a;
  width: 40px;
  height: 40px;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-remove:hover {
  background: rgba(224, 61, 61, 0.3);
}

.point-details {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}

.detail-group {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.detail-group label {
  font-size: 0.7rem;
  font-weight: 600;
  color: #8e9aab;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.icon-select,
.color-input {
  background: rgba(10, 15, 26, 0.6);
  border: 1px solid rgba(212, 163, 115, 0.3);
  border-radius: 0.5rem;
  padding: 0.5rem;
  color: #e8edf2;
  cursor: pointer;
}

.icon-select:focus,
.color-input:focus {
  outline: none;
  border-color: #d4a373;
}

.color-input {
  height: 38px;
  cursor: color-picker;
}

.btn-add {
  background: rgba(212, 163, 115, 0.2);
  border: 1px solid rgba(212, 163, 115, 0.5);
  color: #d4a373;
  padding: 0.7rem 1.2rem;
  border-radius: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.btn-add:hover {
  background: rgba(212, 163, 115, 0.3);
  border-color: #d4a373;
}

.form-actions {
  display: flex;
  gap: 1rem;
}

.btn-back,
.btn-complete {
  flex: 1;
  padding: 0.9rem 1.5rem;
  border-radius: 0.75rem;
  font-weight: 700;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  border: none;
}

.btn-back {
  background: rgba(255, 255, 255, 0.1);
  color: #cbd5e6;
}

.btn-back:hover {
  background: rgba(255, 255, 255, 0.15);
}

.btn-complete {
  background: #d4a373;
  color: #0a0f1a;
}

.btn-complete:hover {
  background: #e0b082;
  box-shadow: 0 8px 20px rgba(212, 163, 115, 0.3);
}
</style>
