<template>
  <div class="materials-container">
    <div class="materials-header">
      <button class="btn-back" @click="$emit('back')">
        <i class="fas fa-arrow-left"></i> Volver
      </button>
      <h3>Requerimiento de Material</h3>
      <div></div>
    </div>

    <div class="materials-content">
      <!-- Lista de puntos con formulario de materiales -->
      <div class="points-materials-list">
        <div 
          v-for="point in points" 
          :key="point.id" 
          class="point-material-card"
          :class="{ 'active': activePointId === point.id }"
        >
          <div class="card-header" @click="activePointId = point.id">
            <div class="point-info">
              <i :class="`fas ${point.icon}`"></i>
              <div>
                <p class="point-name">{{ point.name }}</p>
                <p class="point-location">{{ point.lat.toFixed(4) }}, {{ point.lng.toFixed(4) }}</p>
              </div>
            </div>
            <div class="materials-count">
              <span v-if="getMaterialsSummary(point.id)" class="count-badge">
                {{ getMaterialsSummary(point.id).count }} material(es)
              </span>
              <i :class="activePointId === point.id ? 'fas fa-chevron-up' : 'fas fa-chevron-down'"></i>
            </div>
          </div>

          <div v-if="activePointId === point.id" class="card-content">
            <!-- Resumen si hay materiales -->
            <div v-if="getMaterialsSummary(point.id)" class="materials-summary">
              <div class="summary-item">
                <span>Total Cantidad:</span>
                <strong>{{ getMaterialsSummary(point.id).totalQuantity.toFixed(2) }} ton</strong>
              </div>
              <div class="summary-item">
                <span>Valor Total:</span>
                <strong>Bs {{ getMaterialsSummary(point.id).totalValue.toFixed(2) }}</strong>
              </div>
            </div>

            <!-- Formulario para agregar material -->
            <form @submit.prevent="addMaterialToPoint(point.id)" class="add-material-form">
              <div class="form-row">
                <div class="form-group">
                  <label for="materialType">Tipo de Producto</label>
                  <input 
                    v-model="newMaterials[point.id].type"
                    id="materialType"
                    type="text" 
                    placeholder="Ej: Pasta"
                    required
                  />
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label for="materialQuantity">Cantidad (Toneladas)</label>
                  <input 
                    v-model.number="newMaterials[point.id].quantity"
                    id="materialQuantity"
                    type="number" 
                    step="0.1"
                    placeholder="Ej: 50.5"
                    required
                  />
                </div>
                <div class="form-group">
                  <label for="materialPrice">Precio (Bs/ton)</label>
                  <input 
                    v-model.number="newMaterials[point.id].price"
                    id="materialPrice"
                    type="number" 
                    step="0.01"
                    placeholder="Ej: 150.50"
                    required
                  />
                </div>
              </div>

              <button type="submit" class="btn-add-material">
                <i class="fas fa-plus"></i> Agregar Material
              </button>
            </form>

            <!-- Tabla de materiales -->
            <div v-if="getMaterialsSummary(point.id)" class="materials-table-wrapper">
              <table class="materials-table">
                <thead>
                  <tr>
                    <th>Producto</th>
                    <th>Cantidad (ton)</th>
                    <th>Precio (Bs/ton)</th>
                    <th>Subtotal (Bs)</th>
                    <th>Acción</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="material in getMaterialsSummary(point.id).materials" :key="material.id">
                    <td>{{ material.type }}</td>
                    <td>{{ parseFloat(material.quantity).toFixed(2) }}</td>
                    <td>{{ parseFloat(material.price).toFixed(2) }}</td>
                    <td>{{ (parseFloat(material.quantity) * parseFloat(material.price)).toFixed(2) }}</td>
                    <td>
                      <button 
                        @click="deleteMaterial(point.id, material.id)"
                        class="btn-delete"
                        title="Eliminar"
                      >
                        <i class="fas fa-trash-alt"></i>
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="materials-footer">
      <button class="btn-continue" @click="$emit('continue')">
        <i class="fas fa-chevron-right"></i> Continuar Configuración
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { useMapPoints } from '@/pages/dashboard/composables/useMapPoints';
import { useMaterialsConfig } from '@/pages/dashboard/composables/useMaterialsConfig';

const mapPoints = useMapPoints();
const materialsConfig = useMaterialsConfig();

const activePointId = ref(null);
const newMaterials = ref({});

const points = computed(() => mapPoints.allPoints.value);

// Inicializar formarios para cada punto
watch(
  () => points.value,
  (newPoints) => {
    newPoints.forEach(point => {
      if (!newMaterials.value[point.id]) {
        newMaterials.value[point.id] = {
          type: '',
          quantity: '',
          price: ''
        };
      }
    });
    if (newPoints.length > 0 && !activePointId.value) {
      activePointId.value = newPoints[0].id;
    }
  },
  { immediate: true }
);

const getMaterialsSummary = (pointId) => {
  return materialsConfig.getMaterialsSummary(pointId);
};

const addMaterialToPoint = (pointId) => {
  const material = newMaterials.value[pointId];
  
  if (!material.type.trim() || !material.quantity || !material.price) {
    alert('Por favor completa todos los campos');
    return;
  }

  materialsConfig.addMaterial(pointId, {
    type: material.type,
    quantity: material.quantity,
    price: material.price
  });

  // Limpiar formulario
  newMaterials.value[pointId] = {
    type: '',
    quantity: '',
    price: ''
  };
};

const deleteMaterial = (pointId, materialId) => {
  if (confirm('¿Estás seguro de eliminar este material?')) {
    materialsConfig.removeMaterial(pointId, materialId);
  }
};

defineEmits(['back', 'continue']);
</script>

<style scoped>
.materials-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: rgba(18, 24, 34, 0.8);
  backdrop-filter: blur(12px);
}

.materials-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.2rem;
  border-bottom: 1px solid rgba(212, 163, 115, 0.2);
  background: rgba(212, 163, 115, 0.1);
}

.materials-header h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 700;
  color: #d4a373;
}

.btn-back {
  background: rgba(212, 163, 115, 0.1);
  border: 1px solid rgba(212, 163, 115, 0.2);
  color: #d4a373;
  padding: 0.6rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  font-weight: 600;
}

.btn-back:hover {
  background: rgba(212, 163, 115, 0.2);
  border-color: rgba(212, 163, 115, 0.4);
}

.materials-content {
  flex: 1;
  overflow-y: auto;
  padding: 1.2rem;
}

.points-materials-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.point-material-card {
  background: rgba(14, 18, 26, 0.5);
  border: 1px solid rgba(212, 163, 115, 0.2);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.point-material-card.active {
  border-color: rgba(212, 163, 115, 0.4);
  box-shadow: 0 0 12px rgba(212, 163, 115, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  background: rgba(212, 163, 115, 0.08);
  border-bottom: 1px solid rgba(212, 163, 115, 0.15);
  cursor: pointer;
  transition: all 0.3s ease;
}

.card-header:hover {
  background: rgba(212, 163, 115, 0.12);
}

.point-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
}

.point-info i {
  font-size: 1.5rem;
  color: #d4a373;
  min-width: 1.5rem;
}

.point-name {
  margin: 0;
  font-weight: 700;
  color: #ffffff;
  font-size: 0.95rem;
}

.point-location {
  margin: 0.25rem 0 0;
  font-size: 0.8rem;
  color: #8fa3b3;
}

.materials-count {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.count-badge {
  background: rgba(212, 163, 115, 0.2);
  color: #d4a373;
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
}

.card-content {
  padding: 1.2rem;
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.materials-summary {
  display: flex;
  gap: 1rem;
  background: rgba(212, 163, 115, 0.1);
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid rgba(212, 163, 115, 0.2);
}

.summary-item {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.summary-item span {
  color: #8fa3b3;
  font-size: 0.85rem;
  font-weight: 600;
}

.summary-item strong {
  color: #d4a373;
  font-size: 0.95rem;
  text-align: right;
}

.add-material-form {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.form-row {
  display: flex;
  gap: 0.8rem;
}

.form-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.form-group label {
  font-weight: 600;
  color: #d4a373;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-group input {
  padding: 0.7rem;
  background: rgba(14, 18, 26, 0.5);
  border: 1px solid rgba(212, 163, 115, 0.3);
  border-radius: 8px;
  color: #ffffff;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  font-family: inherit;
}

.form-group input:focus {
  outline: none;
  border-color: #d4a373;
  background: rgba(14, 18, 26, 0.7);
  box-shadow: 0 0 0 3px rgba(212, 163, 115, 0.15);
}

.form-group input::placeholder {
  color: rgba(232, 237, 242, 0.3);
}

.btn-add-material {
  background: rgba(212, 163, 115, 0.2);
  color: #d4a373;
  border: 1px solid rgba(212, 163, 115, 0.4);
  padding: 0.8rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-size: 0.85rem;
}

.btn-add-material:hover {
  background: rgba(212, 163, 115, 0.35);
  border-color: rgba(212, 163, 115, 0.6);
  color: #e8c48e;
}

.materials-table-wrapper {
  overflow-x: auto;
}

.materials-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.85rem;
}

.materials-table thead {
  background: rgba(212, 163, 115, 0.1);
  border-bottom: 2px solid rgba(212, 163, 115, 0.3);
}

.materials-table th {
  padding: 0.8rem;
  text-align: left;
  color: #d4a373;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.materials-table td {
  padding: 0.8rem;
  border-bottom: 1px solid rgba(212, 163, 115, 0.15);
  color: #e8edf2;
}

.materials-table tbody tr:hover {
  background: rgba(212, 163, 115, 0.05);
}

.btn-delete {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.3);
  width: 32px;
  height: 32px;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.btn-delete:hover {
  background: rgba(239, 68, 68, 0.2);
  border-color: rgba(239, 68, 68, 0.5);
  color: #f87171;
}

.materials-footer {
  padding: 1.2rem;
  border-top: 1px solid rgba(212, 163, 115, 0.2);
  background: rgba(212, 163, 115, 0.08);
  display: flex;
  justify-content: flex-end;
}

.btn-continue {
  background: rgba(212, 163, 115, 0.2);
  color: #d4a373;
  border: 1px solid rgba(212, 163, 115, 0.4);
  padding: 0.8rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
}

.btn-continue:hover {
  background: rgba(212, 163, 115, 0.35);
  border-color: rgba(212, 163, 115, 0.6);
  color: #e8c48e;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(212, 163, 115, 0.2);
}

/* Scrollbar styling */
.materials-content::-webkit-scrollbar {
  width: 6px;
}

.materials-content::-webkit-scrollbar-track {
  background: rgba(212, 163, 115, 0.1);
  border-radius: 10px;
}

.materials-content::-webkit-scrollbar-thumb {
  background: rgba(212, 163, 115, 0.3);
  border-radius: 10px;
}

.materials-content::-webkit-scrollbar-thumb:hover {
  background: rgba(212, 163, 115, 0.5);
}

/* Responsive */
@media (max-width: 768px) {
  .form-row {
    flex-direction: column;
  }

  .materials-summary {
    flex-direction: column;
  }
}
</style>
