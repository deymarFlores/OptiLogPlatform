<template>
  <Teleport to="body">
    <Transition name="modal-fade">
      <div v-if="isOpen" class="modal-overlay" @click="handleOverlayClick">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h3>
              <i class="fas fa-store"></i> Agregar Nueva Sucursal
            </h3>
            <button class="btn-close" @click="cancel" aria-label="Cerrar">
              <i class="fas fa-times"></i>
            </button>
          </div>

          <div class="modal-body">
            <div class="location-info">
              <div class="coord-item">
                <label>Latitud</label>
                <p class="coord-value">{{ coordinates.lat.toFixed(4) }}</p>
              </div>
              <div class="coord-item">
                <label>Longitud</label>
                <p class="coord-value">{{ coordinates.lng.toFixed(4) }}</p>
              </div>
            </div>

            <div class="form-group">
              <label for="sucursal-type">Tipo de Sucursal *</label>
              <select
                id="sucursal-type"
                v-model="formData.typeLocationId"
                class="form-input"
              >
                <option value="">Selecciona un tipo...</option>
                <option v-for="type in locationTypes" :key="type.id" :value="type.id">
                  <i :class="`fas ${type.icon}`"></i> {{ type.name }}
                </option>
              </select>
              <small v-if="!formData.typeLocationId" class="error-text">
                El tipo de sucursal es requerido
              </small>
            </div>

            <div class="form-group">
              <label for="sucursal-name">Nombre de la Sucursal *</label>
              <input
                id="sucursal-name"
                v-model="formData.name"
                type="text"
                placeholder="Ej: Sucursal Centro, Sucursal Norte..."
                class="form-input"
                @keyup.enter="submit"
              />
              <small v-if="!formData.name" class="error-text">
                El nombre es requerido
              </small>
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn btn-secondary" @click="cancel">
              Cancelar
            </button>
            <button
              class="btn btn-primary"
              @click="submit"
              :disabled="!formData.name || !formData.typeLocationId || isSubmitting"
            >
              <span v-if="!isSubmitting">
                <i class="fas fa-plus"></i> Agregar Sucursal
              </span>
              <span v-else>
                <i class="fas fa-spinner fa-spin"></i> Agregando...
              </span>
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, reactive, watch } from 'vue';

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  coordinates: {
    type: Object,
    default: () => ({ lat: 0, lng: 0 })
  },
  locationTypes: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['submit', 'cancel']);

const isSubmitting = ref(false);
const formData = reactive({
  name: '',
  typeLocationId: ''
});

watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    formData.name = '';
    formData.typeLocationId = '';
  }
});

const submit = async () => {
  if (!formData.name.trim() || !formData.typeLocationId) {
    return;
  }

  isSubmitting.value = true;
  try {
    emit('submit', {
      name: formData.name.trim(),
      typeLocationId: formData.typeLocationId
    });
  } finally {
    isSubmitting.value = false;
  }
};

const cancel = () => {
  formData.name = '';
  formData.typeLocationId = '';
  emit('cancel');
};

const handleOverlayClick = (e) => {
  if (e.target === e.currentTarget) {
    cancel();
  }
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  backdrop-filter: blur(4px);
}

.modal-content {
  background: linear-gradient(135deg, rgba(20, 28, 40, 0.98) 0%, rgba(10, 15, 26, 0.98) 100%);
  border: 1px solid rgba(212, 163, 115, 0.2);
  border-radius: 1rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  width: 100%;
  max-width: 450px;
  max-height: 90vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem;
  border-bottom: 1px solid rgba(212, 163, 115, 0.15);
  flex-shrink: 0;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  color: #ffffff;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.modal-header i {
  color: #d4a373;
}

.btn-close {
  background: transparent;
  border: none;
  color: #8e9aab;
  cursor: pointer;
  font-size: 1.5rem;
  padding: 0;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.btn-close:hover {
  color: #d4a373;
  transform: rotate(90deg);
}

.modal-body {
  padding: 1.5rem;
  flex: 1;
}

.location-info {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
  background: rgba(212, 163, 115, 0.08);
  padding: 1rem;
  border-radius: 0.75rem;
  border: 1px solid rgba(212, 163, 115, 0.15);
}

.coord-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.coord-item label {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #8e9aab;
  font-weight: 600;
}

.coord-value {
  font-size: 0.95rem;
  color: #d4a373;
  margin: 0;
  font-weight: 700;
  font-family: 'Courier New', monospace;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 0.9rem;
  color: #e8edf2;
  font-weight: 600;
}

.form-input {
  background: rgba(212, 163, 115, 0.08);
  border: 1px solid rgba(212, 163, 115, 0.3);
  border-radius: 0.5rem;
  padding: 0.75rem 1rem;
  color: #e8edf2;
  font-size: 0.95rem;
  transition: all 0.3s ease;
}

.form-input:focus {
  outline: none;
  background: rgba(212, 163, 115, 0.12);
  border-color: rgba(212, 163, 115, 0.6);
  box-shadow: 0 0 0 3px rgba(212, 163, 115, 0.1);
}

.form-input::placeholder {
  color: #6e7a8a;
}

.error-text {
  font-size: 0.8rem;
  color: #e05a5a;
  font-style: italic;
}

.modal-footer {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid rgba(212, 163, 115, 0.15);
  flex-shrink: 0;
}

.btn {
  flex: 1;
  padding: 0.75rem 1.25rem;
  border-radius: 0.5rem;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.btn-primary {
  background: #d4a373;
  color: #0a0f1a;
}

.btn-primary:hover:not(:disabled) {
  background: #e0b082;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(212, 163, 115, 0.3);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background: transparent;
  border: 1px solid rgba(212, 163, 115, 0.3);
  color: #d4a373;
}

.btn-secondary:hover {
  background: rgba(212, 163, 115, 0.1);
  border-color: rgba(212, 163, 115, 0.6);
  transform: translateY(-2px);
}

select.form-input {
  appearance: none;
  padding-right: 2.5rem;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23d4a373' d='M6 9L1 4h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  background-color: rgba(212, 163, 115, 0.08);
  cursor: pointer;
}

select.form-input option {
  background: #141c28;
  color: #e8edf2;
}

select.form-input option:checked {
  background: #d4a373;
  color: #0a0f1a;
}

.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

@media (max-width: 640px) {
  .modal-content {
    width: 90%;
    border-radius: 0.75rem;
  }

  .modal-header {
    padding: 1.25rem;
  }

  .modal-body {
    padding: 1.25rem;
  }

  .modal-footer {
    padding: 1.25rem;
  }
}
</style>
