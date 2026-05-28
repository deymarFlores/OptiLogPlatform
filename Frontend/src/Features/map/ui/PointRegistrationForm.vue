<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="handleCancel">
    <div class="modal-content">
      <div class="modal-header">
        <h4>Registrar Nuevo Punto</h4>
        <button class="btn-close" @click="handleCancel">
          <i class="fas fa-times"></i>
        </button>
      </div>

      <div class="modal-body">
        <div class="form-group">
          <label for="siteName">Nombre del Sitio</label>
          <input 
            v-model="formData.name" 
            id="siteName"
            type="text" 
            placeholder="Ej: Centro Logístico La Paz"
            @keyup.enter="handleSubmit"
          />
        </div>

        <div class="form-group">
          <label for="pointType">Tipo de Punto</label>
          <select v-model="formData.typeId" id="pointType">
            <option v-for="type in pointTypes" :key="type.id" :value="type.id">
              {{ type.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>Coordenadas</label>
          <div class="coords-display">
            <p>{{ formData.lat.toFixed(6) }}, {{ formData.lng.toFixed(6) }}</p>
          </div>
        </div>
      </div>

      <div class="modal-footer">
        <button class="btn-cancel" @click="handleCancel">Cancelar</button>
        <button class="btn-submit" @click="handleSubmit">Registrar Punto</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, reactive, watch } from 'vue';

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  coordinates: {
    type: Object,
    default: () => ({ lat: -16.5, lng: -68.15 })
  },
  pointTypes: {
    type: Array,
    default: () => [
      { id: 1, name: 'Almacén', icon: 'fa-warehouse', color: '#d4a373' },
      { id: 2, name: 'Tienda', icon: 'fa-shopping-bag', color: '#4a9eff' }
    ]
  }
});

const emit = defineEmits(['submit', 'cancel']);

const formData = reactive({
  name: '',
  typeId: 1,
  lat: props.coordinates.lat,
  lng: props.coordinates.lng
});

watch(() => props.coordinates, (newCoords) => {
  formData.lat = newCoords.lat;
  formData.lng = newCoords.lng;
}, { deep: true });

const handleSubmit = () => {
  if (!formData.name.trim()) {
    alert('Por favor ingresa el nombre del sitio');
    return;
  }

  const selectedType = props.pointTypes.find(t => t.id === formData.typeId);
  
  emit('submit', {
    name: formData.name,
    typeId: formData.typeId,
    typeName: selectedType.name,
    icon: selectedType.icon,
    color: selectedType.color,
    lat: formData.lat,
    lng: formData.lng
  });

  formData.name = '';
  formData.typeId = 1;
};

const handleCancel = () => {
  formData.name = '';
  formData.typeId = 1;
  emit('cancel');
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(6px);
}

.modal-content {
  background: rgba(18, 24, 34, 0.9);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(212, 163, 115, 0.2);
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
  width: 90%;
  max-width: 450px;
  overflow: hidden;
}

.modal-header {
  background: rgba(212, 163, 115, 0.15);
  border-bottom: 1px solid rgba(212, 163, 115, 0.2);
  color: #ffffff;
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h4 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 700;
  color: #d4a373;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.btn-close {
  background: rgba(212, 163, 115, 0.1);
  border: 1px solid rgba(212, 163, 115, 0.2);
  color: #d4a373;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  font-size: 1.2rem;
}

.btn-close:hover {
  background: rgba(212, 163, 115, 0.2);
  border-color: rgba(212, 163, 115, 0.4);
}

.modal-body {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.form-group label {
  font-weight: 600;
  color: #d4a373;
  font-size: 0.95rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-group input,
.form-group select {
  padding: 0.85rem;
  background: rgba(14, 18, 26, 0.5);
  border: 1px solid rgba(212, 163, 115, 0.3);
  border-radius: 8px;
  color: #ffffff;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  font-family: inherit;
}

.form-group input::placeholder {
  color: rgba(232, 237, 242, 0.4);
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #d4a373;
  background: rgba(14, 18, 26, 0.7);
  box-shadow: 0 0 0 3px rgba(212, 163, 115, 0.15);
}

.form-group select {
  cursor: pointer;
}

.coords-display {
  background: rgba(14, 18, 26, 0.5);
  padding: 0.85rem;
  border-radius: 8px;
  border: 1px solid rgba(212, 163, 115, 0.3);
  font-family: 'Courier New', monospace;
  font-size: 0.9rem;
  color: #d4a373;
  font-weight: 500;
}

.coords-display p {
  margin: 0;
}

.modal-footer {
  display: flex;
  gap: 0.75rem;
  padding: 1.5rem;
  background: rgba(0, 0, 0, 0.2);
  border-top: 1px solid rgba(212, 163, 115, 0.1);
  justify-content: flex-end;
}

.btn-cancel,
.btn-submit {
  padding: 0.8rem 1.5rem;
  border: 1px solid rgba(212, 163, 115, 0.3);
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.95rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.btn-cancel {
  background: rgba(95, 125, 149, 0.1);
  color: #8fa3b3;
  border-color: rgba(95, 125, 149, 0.3);
}

.btn-cancel:hover {
  background: rgba(95, 125, 149, 0.2);
  border-color: rgba(95, 125, 149, 0.5);
  color: #a8b9c5;
}

.btn-submit {
  background: rgba(212, 163, 115, 0.2);
  color: #d4a373;
  border-color: rgba(212, 163, 115, 0.4);
}

.btn-submit:hover {
  background: rgba(212, 163, 115, 0.35);
  border-color: rgba(212, 163, 115, 0.6);
  color: #e8c48e;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(212, 163, 115, 0.2);
}

@media (max-width: 768px) {
  .modal-content {
    width: 95%;
    max-width: 90vw;
  }

  .modal-header {
    padding: 1.2rem;
  }

  .modal-body {
    padding: 1.2rem;
  }

  .modal-footer {
    flex-direction: column;
    padding: 1.2rem;
  }

  .btn-cancel,
  .btn-submit {
    width: 100%;
  }
}

</style>
