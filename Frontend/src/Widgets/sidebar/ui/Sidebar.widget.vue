<template>
  <aside class="sidebar-widget">
    <div class="sidebar-header">
      <h3><i class="fas fa-map-marker-alt"></i> Mis Puntos</h3>
    </div>

    <div class="sidebar-section">
      <h4 class="section-title">
        <i class="fas fa-warehouse"></i> Almacenes
        <span v-if="pointsByType.almacenes.length > 0" class="count-badge">{{ pointsByType.almacenes.length }}</span>
      </h4>
      <div class="items-list">
        <p v-if="pointsByType.almacenes.length === 0" class="empty-message">No hay puntos registrados</p>
        <div v-for="point in pointsByType.almacenes" :key="point.id" class="point-item">
          <div class="point-info">
            <i :class="`fas ${point.icon}`"></i>
            <div class="point-details">
              <p class="point-name">{{ point.name }}</p>
              <p class="point-coords">{{ point.lat.toFixed(4) }}, {{ point.lng.toFixed(4) }}</p>
            </div>
          </div>
          <button class="btn-delete" @click="deletePoint(point.id)" title="Eliminar">
            <i class="fas fa-trash-alt"></i>
          </button>
        </div>
      </div>
    </div>

    <div class="sidebar-section">
      <h4 class="section-title">
        <i class="fas fa-store"></i> Tiendas
        <span v-if="pointsByType.tiendas.length > 0" class="count-badge">{{ pointsByType.tiendas.length }}</span>
      </h4>
      <div class="items-list">
        <p v-if="pointsByType.tiendas.length === 0" class="empty-message">No hay puntos registrados</p>
        <div v-for="point in pointsByType.tiendas" :key="point.id" class="point-item">
          <div class="point-info">
            <i :class="`fas ${point.icon}`"></i>
            <div class="point-details">
              <p class="point-name">{{ point.name }}</p>
              <p class="point-coords">{{ point.lat.toFixed(4) }}, {{ point.lng.toFixed(4) }}</p>
            </div>
          </div>
          <button class="btn-delete" @click="deletePoint(point.id)" title="Eliminar">
            <i class="fas fa-trash-alt"></i>
          </button>
        </div>
      </div>
    </div>

    <div class="sidebar-actions">
      <button 
        class="btn-action btn-routes" 
        @click="handleRoutesClick" 
        :disabled="allPoints.length < 2"
        title="Requiere al menos 2 puntos"
      >
        <i class="fas fa-route"></i> Gestión de Conexiones
      </button>
      <button 
        class="btn-action btn-materials" 
        @click="handleMaterialsClick" 
        :disabled="allPoints.length === 0"
      >
        <i class="fas fa-boxes"></i> Gestión de Materiales
      </button>
      <button class="btn-action btn-import">
        <i class="fas fa-upload"></i> Importar
      </button>
    </div>

    <Teleport to="body">
      <ConfirmationModal 
        :isOpen="showDeleteConfirm"
        title="Eliminar Punto"
        message="¿Estás seguro de que deseas eliminar este punto? Esta acción no se puede deshacer."
        icon="fa-trash-alt"
        confirmText="Eliminar"
        cancelText="Cancelar"
        :isDangerous="true"
        @confirm="confirmDelete"
        @cancel="cancelDelete"
      />
    </Teleport>
  </aside>
</template>

<script setup>
import { ref } from 'vue';
import { useMapPoints } from '@/pages/dashboard/composables/useMapPoints';
import { ConfirmationModal } from '@/Features/confirmation';

const mapPoints = useMapPoints();
const pointsByType = mapPoints.pointsByType;
const allPoints = mapPoints.allPoints;

const emit = defineEmits(['add-point', 'show-materials', 'show-routes']);

const showDeleteConfirm = ref(false);
const pendingDeleteId = ref(null);

const handleRoutesClick = () => {
  if (allPoints.value.length >= 2) {
    emit('show-routes');
  }
};

const handleMaterialsClick = () => {
  if (allPoints.value.length > 0) {
    emit('show-materials');
  }
};

const deletePoint = (id) => {
  pendingDeleteId.value = id;
  showDeleteConfirm.value = true;
};

const confirmDelete = () => {
  if (pendingDeleteId.value !== null) {
    mapPoints.removePoint(pendingDeleteId.value);
    pendingDeleteId.value = null;
  }
  showDeleteConfirm.value = false;
};

const cancelDelete = () => {
  pendingDeleteId.value = null;
  showDeleteConfirm.value = false;
};
</script>

<style scoped>
.sidebar-widget {
  width: 300px;
  background: linear-gradient(
    180deg,
    rgba(10, 15, 26, 0.95) 0%,
    rgba(20, 28, 40, 0.92) 100%
  );
  backdrop-filter: blur(10px);
  border-right: 1px solid rgba(212, 163, 115, 0.15);
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  padding: 1.5rem 1.2rem;
}

.sidebar-header {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(212, 163, 115, 0.15);
}

.sidebar-header h3 {
  font-size: 1.1rem;
  font-weight: 700;
  color: #ffffff;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0;
}

.sidebar-header i {
  color: #d4a373;
}

.sidebar-section {
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #d4a373;
  margin-bottom: 0.75rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
}

.section-title i {
  font-size: 0.9rem;
}

.count-badge {
  background: #d4a373;
  color: #0a0f1a;
  border-radius: 50%;
  width: 1.5rem;
  height: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  font-weight: 700;
  margin-left: auto;
}

.items-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.empty-message {
  font-size: 0.8rem;
  color: #8e9aab;
  font-style: italic;
  margin: 0;
  padding: 0.5rem;
  text-align: center;
}

.point-item {
  background: rgba(212, 163, 115, 0.08);
  border: 1px solid rgba(212, 163, 115, 0.15);
  border-radius: 0.75rem;
  padding: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.point-item:hover {
  background: rgba(212, 163, 115, 0.12);
  border-color: rgba(212, 163, 115, 0.3);
}

.point-info {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  flex: 1;
  min-width: 0;
}

.point-info i {
  color: #d4a373;
  font-size: 0.9rem;
  flex-shrink: 0;
  margin-top: 0.15rem;
}

.point-details {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
  min-width: 0;
}

.point-name {
  font-size: 0.8rem;
  color: #e8edf2;
  font-weight: 600;
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.point-coords {
  font-size: 0.7rem;
  color: #8e9aab;
  margin: 0;
  font-family: 'Courier New', monospace;
}

.btn-delete {
  background: transparent;
  border: none;
  color: #8e9aab;
  cursor: pointer;
  font-size: 0.8rem;
  transition: all 0.2s ease;
  flex-shrink: 0;
  padding: 0.25rem;
}

.btn-delete:hover {
  color: #e05a5a;
  transform: scale(1.15);
}

.sidebar-actions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-top: auto;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(212, 163, 115, 0.15);
}

.btn-action {
  background: rgba(212, 163, 115, 0.12);
  border: 1px solid rgba(212, 163, 115, 0.3);
  color: #d4a373;
  padding: 0.7rem 1rem;
  border-radius: 0.75rem;
  font-weight: 600;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.btn-action:hover {
  background: rgba(212, 163, 115, 0.2);
  border-color: rgba(212, 163, 115, 0.5);
  transform: translateY(-2px);
}

.btn-add {
  background: #d4a373;
  color: #0a0f1a;
  border-color: #d4a373;
  font-weight: 700;
}

.btn-add:hover {
  background: #e0b082;
  border-color: #e0b082;
}

.btn-materials {
  background: rgba(212, 163, 115, 0.15);
  border-color: rgba(212, 163, 115, 0.35);
}

.btn-materials:hover:not(:disabled) {
  background: rgba(212, 163, 115, 0.25);
  border-color: rgba(212, 163, 115, 0.5);
}

.btn-materials:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-routes {
  background: rgba(212, 163, 115, 0.12);
  border-color: rgba(212, 163, 115, 0.3);
}

.btn-routes:hover:not(:disabled) {
  background: rgba(212, 163, 115, 0.2);
  border-color: rgba(212, 163, 115, 0.5);
}

.btn-routes:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-import {
  background: transparent;
}

@media (max-width: 768px) {
  .sidebar-widget {
    width: 250px;
    padding: 1rem;
  }
}
</style>