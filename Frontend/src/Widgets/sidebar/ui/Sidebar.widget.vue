<template>
  <aside class="sidebar-widget">
    <div class="sidebar-header">
      <h3><i class="fas fa-map-marker-alt"></i> Mis Puntos</h3>
    </div>

    <div class="sidebar-section sucursales-section">
      <button
        v-if="!isEditSucursalesMode"
        class="btn-action btn-add-sucursal"
        @click="handleAddSucursal"
      >
        <i class="fas fa-plus"></i> Agregar Sucursal
      </button>

      <button v-else class="btn-action btn-stop-edit" @click="handleStopEdit">
        <i class="fas fa-check"></i> Guardar y Cerrar
      </button>
    </div>

    <div v-for="type in locationTypes" :key="type.id" class="sidebar-section">
      <h4 class="section-title">
        <i :class="`fas ${type.icon}`"></i> {{ type.name }}
        <span
          v-if="
            (sucursalesByType[type.id] &&
              sucursalesByType[type.id].length > 0) ||
            (pointsByType[type.name] && pointsByType[type.name].length > 0)
          "
          class="count-badge"
        >
          {{
            (sucursalesByType[type.id] ? sucursalesByType[type.id].length : 0) +
            (pointsByType[type.name] ? pointsByType[type.name].length : 0)
          }}
        </span>
      </h4>

      <div class="items-list">
        <div
          v-for="sucursal in sucursalesByType[type.id] || []"
          :key="sucursal.id"
          class="point-item"
        >
          <div class="point-info">
            <i :class="`fas ${type.icon}`"></i>
            <div class="point-details">
              <p class="point-name">{{ sucursal.name }}</p>
              <p class="point-coords">
                {{ sucursal.lat.toFixed(4) }}, {{ sucursal.lng.toFixed(4) }}
              </p>
            </div>
          </div>
          <button
            class="btn-delete"
            @click="deleteSucursal(sucursal.id)"
            title="Eliminar"
          >
            <i class="fas fa-trash-alt"></i>
          </button>
        </div>

        <div
          v-for="point in pointsByType[type.name] || []"
          :key="point.id"
          class="point-item"
        >
          <div class="point-info">
            <i :class="`fas ${point.icon}`"></i>
            <div class="point-details">
              <p class="point-name">{{ point.name }}</p>
              <p class="point-coords">
                {{ point.lat.toFixed(4) }}, {{ point.lng.toFixed(4) }}
              </p>
            </div>
          </div>
          <button
            class="btn-delete"
            @click="deletePoint(point.id)"
            title="Eliminar"
          >
            <i class="fas fa-trash-alt"></i>
          </button>
        </div>

        <p
          v-if="
            (!sucursalesByType[type.id] ||
              sucursalesByType[type.id].length === 0) &&
            (!pointsByType[type.name] || pointsByType[type.name].length === 0)
          "
          class="empty-message"
        >
          Sin registros
        </p>
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
import { ref, onMounted, computed } from "vue";
import { useMapPoints } from "@/pages/dashboard/composables/useMapPoints";
import { useSucursalesManager } from "@/pages/dashboard/composables/useSucursalesManager";
import { useSetupStore } from "@/pages/setup/composables/useSetupStore";
import { ConfirmationModal } from "@/Features/confirmation";

const props = defineProps({
  isEditSucursalesMode: {
    type: Boolean,
    default: false,
  },
});

const mapPoints = useMapPoints();
const pointsByType = mapPoints.pointsByType;
const allPoints = mapPoints.allPoints;

const setupStore = useSetupStore();

const locationTypes = computed(() => setupStore.pointTypes.value);
const pointTypeNames = computed(() => mapPoints.getPointTypeNames());

const sucursalesManager = useSucursalesManager();
const sucursales = computed(() => sucursalesManager.sucursales.value);

const sucursalesByType = computed(() => {
  const grouped = {};

  locationTypes.value.forEach((type) => {
    grouped[type.id] = sucursales.value.filter(
      (s) => s.type_location_id === type.id,
    );
  });

  return grouped;
});

const emit = defineEmits([
  "add-point",
  "show-materials",
  "show-routes",
  "toggle-edit-mode",
]);

const showDeleteConfirm = ref(false);
const pendingDeleteId = ref(null);
const pendingSucursalDeleteId = ref(null);

const getTypeById = (typeId) => {
  return locationTypes.value.find((t) => t.id === typeId);
};

const getTypeIcon = (typeName) => {
  const type = locationTypes.value.find((t) => t.name === typeName);
  return type ? `fas ${type.icon}` : "fas fa-map-pin";
};

onMounted(() => {
  sucursalesManager.loadSucursales();
});

const handleRoutesClick = () => {
  if (allPoints.value.length >= 2) {
    emit("show-routes");
  }
};

const handleMaterialsClick = () => {
  if (allPoints.value.length > 0) {
    emit("show-materials");
  }
};

const handleAddSucursal = () => {
  emit("toggle-edit-mode", true);
};

const handleStopEdit = () => {
  emit("toggle-edit-mode", false);
};

const deletePoint = (id) => {
  pendingDeleteId.value = id;
  pendingSucursalDeleteId.value = null;
  showDeleteConfirm.value = true;
};

const deleteSucursal = (id) => {
  pendingSucursalDeleteId.value = id;
  pendingDeleteId.value = null;
  showDeleteConfirm.value = true;
};

const confirmDelete = () => {
  if (pendingDeleteId.value !== null) {
    mapPoints.removePoint(pendingDeleteId.value);
    pendingDeleteId.value = null;
  } else if (pendingSucursalDeleteId.value !== null) {
    sucursalesManager.deleteSucursal(pendingSucursalDeleteId.value);
    pendingSucursalDeleteId.value = null;
  }
  showDeleteConfirm.value = false;
};

const cancelDelete = () => {
  pendingDeleteId.value = null;
  pendingSucursalDeleteId.value = null;
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
  font-family: "Courier New", monospace;
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

.sucursales-section {
  border-bottom: 2px solid rgba(212, 163, 115, 0.25);
  padding-bottom: 1.5rem;
  margin-bottom: 1.5rem;
}

.btn-add-sucursal {
  width: 100%;
  background: #d4a373;
  color: #0a0f1a;
  border-color: #d4a373;
  font-weight: 700;
  margin-top: 0.75rem;
}

.btn-add-sucursal:hover {
  background: #e0b082;
  border-color: #e0b082;
  transform: translateY(-2px);
}

.btn-stop-edit {
  width: 100%;
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
  color: #ffffff;
  border-color: #ff6b6b;
  font-weight: 700;
  margin-top: 0.75rem;
  animation: pulse-button 0.6s ease-in-out infinite;
}

.btn-stop-edit:hover {
  background: linear-gradient(135deg, #ff5555 0%, #dd4a42 100%);
  border-color: #ff5555;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3);
  animation: none;
}

@keyframes pulse-button {
  0%,
  100% {
    box-shadow: 0 0 0 0 rgba(255, 107, 107, 0.4);
  }
  50% {
    box-shadow: 0 0 0 6px rgba(255, 107, 107, 0.1);
  }
}

.btn-edit-sucursal {
  width: 100%;
  margin-top: 0.75rem;
  background: rgba(212, 163, 115, 0.15);
  border-color: rgba(212, 163, 115, 0.35);
  transition: all 0.3s ease;
}

.btn-edit-sucursal:hover {
  background: rgba(212, 163, 115, 0.25);
  border-color: rgba(212, 163, 115, 0.5);
  transform: translateY(-2px);
}

.btn-edit-sucursal.active {
  background: #d4a373;
  color: #0a0f1a;
  border-color: #d4a373;
  font-weight: 700;
}

@media (max-width: 768px) {
  .sidebar-widget {
    width: 250px;
    padding: 1rem;
  }
}
</style>
