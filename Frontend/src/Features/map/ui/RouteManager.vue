<template>
  <div class="route-manager">
    <div class="manager-header">
      <h3>
        <i class="fas fa-route"></i> Gestor de Conexiones
      </h3>
      <button class="btn-close" @click="close">
        <i class="fas fa-times"></i>
      </button>
    </div>

    <div class="manager-content">
      <!-- Modo de conexión -->
      <div class="connection-mode">
        <h4>Modo Conexión</h4>
        <p class="hint-text">
          <i class="fas fa-info-circle"></i>
          {{ modeHint }}
        </p>
        <button 
          class="btn-mode" 
          :class="{ active: isConnectionModeActive }"
          @click="toggleConnectionMode"
        >
          <i :class="isConnectionModeActive ? 'fas fa-pause' : 'fas fa-play'"></i>
          {{ isConnectionModeActive ? 'Detener' : 'Iniciar' }} Conexiones
        </button>
      </div>

      <!-- Lista de rutas -->
      <div class="routes-list">
        <h4>Conexiones Activas</h4>
        <div v-if="allRoutes.length === 0" class="empty-state">
          <i class="fas fa-link"></i>
          <p>No hay conexiones registradas</p>
        </div>
        <div v-for="route in allRoutes" :key="route.id" class="route-item">
          <div class="route-info">
            <div class="route-points">
              <span class="point-from">{{ getPointName(route.fromId) }}</span>
              <span class="route-arrow">
                <i class="fas fa-arrow-right"></i>
              </span>
              <span class="point-to">{{ getPointName(route.toId) }}</span>
            </div>
            <p class="route-meta">ID: {{ route.id }}</p>
          </div>
          <button 
            class="btn-delete-route" 
            @click="deleteRoute(route.id)"
            title="Eliminar conexión"
          >
            <i class="fas fa-trash-alt"></i>
          </button>
        </div>
      </div>

      <!-- Estadísticas -->
      <div class="stats">
        <div class="stat-card">
          <i class="fas fa-sitemap"></i>
          <div>
            <p class="stat-label">Conexiones</p>
            <p class="stat-value">{{ allRoutes.length }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de confirmación -->
    <Teleport to="body">
      <ConfirmationModal 
        :isOpen="showDeleteConfirm"
        title="Eliminar Conexión"
        message="¿Estás seguro de que deseas eliminar esta conexión?"
        icon="fa-trash-alt"
        confirmText="Eliminar"
        cancelText="Cancelar"
        :isDangerous="true"
        @confirm="confirmDelete"
        @cancel="cancelDelete"
      />
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useMapPoints } from '@/pages/dashboard/composables/useMapPoints';
import { useMapRoutes } from '@/pages/dashboard/composables/useMapRoutes';
import { ConfirmationModal } from '@/Features/confirmation';

const mapPoints = useMapPoints();
const mapRoutes = useMapRoutes();

const emit = defineEmits(['close', 'toggle-connection-mode']);
const props = defineProps({
  isConnectionModeActive: Boolean
});

const allRoutes = mapRoutes.allRoutes;
const showDeleteConfirm = ref(false);
const pendingDeleteId = ref(null);

const modeHint = computed(() => {
  if (props.isConnectionModeActive) {
    return 'Modo activo: Clickea un punto para iniciar, luego clickea otro para conectar. Verás una línea siguiendo tu cursor.';
  }
  return 'Desactiva el modo para agregar conexiones entre tus puntos.';
});

const getPointName = (pointId) => {
  const point = mapPoints.getPoint(pointId);
  return point ? point.name : `Punto ${pointId}`;
};

const toggleConnectionMode = () => {
  emit('toggle-connection-mode');
};

const deleteRoute = (id) => {
  pendingDeleteId.value = id;
  showDeleteConfirm.value = true;
};

const confirmDelete = () => {
  if (pendingDeleteId.value !== null) {
    mapRoutes.removeRoute(pendingDeleteId.value);
    pendingDeleteId.value = null;
  }
  showDeleteConfirm.value = false;
};

const cancelDelete = () => {
  pendingDeleteId.value = null;
  showDeleteConfirm.value = false;
};

const close = () => {
  emit('close');
};
</script>

<style scoped>
.route-manager {
  background: rgba(18, 24, 34, 0.95);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(212, 163, 115, 0.2);
  border-radius: 0.75rem;
  padding: 1rem;
  max-height: 100%;
  overflow-y: auto;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.manager-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid rgba(212, 163, 115, 0.2);
}

.manager-header h3 {
  font-size: 0.95rem;
  font-weight: 700;
  color: #ffffff;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0;
}

.manager-header i {
  color: #d4a373;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1rem;
  color: #8e9aab;
  cursor: pointer;
  transition: color 0.3s ease;
}

.btn-close:hover {
  color: #d4a373;
}

.manager-content {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.connection-mode {
  background: rgba(212, 163, 115, 0.1);
  border: 1px solid rgba(212, 163, 115, 0.2);
  border-radius: 0.5rem;
  padding: 0.75rem;
}

.connection-mode h4 {
  font-size: 0.8rem;
  color: #d4a373;
  margin: 0 0 0.5rem 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.hint-text {
  font-size: 0.7rem;
  color: #8e9aab;
  margin: 0 0 0.5rem 0;
  display: flex;
  align-items: flex-start;
  gap: 0.4rem;
}

.hint-text i {
  color: #d4a373;
  flex-shrink: 0;
  margin-top: 0.15rem;
  font-size: 0.65rem;
}

.btn-mode {
  width: 100%;
  background: linear-gradient(135deg, #1e4a6e, #1f6e5c);
  color: white;
  border: none;
  border-radius: 0.4rem;
  padding: 0.6rem 0.8rem;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
}

.btn-mode:hover {
  transform: translateY(-1px);
  box-shadow: 0 3px 10px rgba(30, 74, 110, 0.3);
}

.btn-mode.active {
  background: linear-gradient(135deg, #d4a373, #c99252);
  color: #0a0f1a;
}

.routes-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.routes-list h4 {
  font-size: 0.8rem;
  color: #d4a373;
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.empty-state {
  text-align: center;
  padding: 1rem 0.75rem;
  background: rgba(212, 163, 115, 0.05);
  border-radius: 0.4rem;
  border: 1px dashed rgba(212, 163, 115, 0.2);
}

.empty-state i {
  font-size: 1.2rem;
  color: #8e9aab;
  margin-bottom: 0.3rem;
}

.empty-state p {
  font-size: 0.75rem;
  color: #8e9aab;
  margin: 0;
}

.route-item {
  background: rgba(212, 163, 115, 0.1);
  border: 1px solid rgba(212, 163, 115, 0.2);
  border-radius: 0.4rem;
  padding: 0.6rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.route-item:hover {
  background: rgba(212, 163, 115, 0.15);
  border-color: #d4a373;
}

.route-info {
  flex: 1;
  min-width: 0;
}

.route-points {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.75rem;
  color: #e8edf2;
  flex-wrap: wrap;
}

.point-from,
.point-to {
  background: rgba(212, 163, 115, 0.2);
  padding: 0.15rem 0.4rem;
  border-radius: 0.2rem;
  color: #d4a373;
  font-weight: 600;
  font-size: 0.7rem;
}

.route-arrow {
  color: #8e9aab;
  font-size: 0.6rem;
}

.route-meta {
  font-size: 0.6rem;
  color: #5e7a93;
  margin: 0.2rem 0 0 0;
}

.btn-delete-route {
  background: none;
  border: none;
  color: #8e9aab;
  font-size: 0.75rem;
  cursor: pointer;
  transition: color 0.3s ease;
  flex-shrink: 0;
}

.btn-delete-route:hover {
  color: #ff6b6b;
}

.stats {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 0.5rem;
}

.stat-card {
  background: rgba(212, 163, 115, 0.1);
  border: 1px solid rgba(212, 163, 115, 0.2);
  border-radius: 0.4rem;
  padding: 0.6rem 0.8rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.stat-card i {
  font-size: 1rem;
  color: #d4a373;
}

.stat-label {
  font-size: 0.65rem;
  color: #8e9aab;
  margin: 0;
  text-transform: uppercase;
}

.stat-value {
  font-size: 1.1rem;
  color: #e8edf2;
  font-weight: 700;
  margin: 0;
}
</style>
