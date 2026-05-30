<template>
  <div class="map-wrapper">
    <Transition name="slide-down">
      <div v-if="isEditSucursalesMode" class="edit-mode-indicator">
        <div class="indicator-content">
          <div class="indicator-left">
            <i class="fas fa-map-pin"></i>
            <div class="indicator-text">
              <p class="indicator-title">Modo Agregar Sucursal Activo</p>
              <p class="indicator-subtitle">
                Haz clic en el mapa para agregar una nueva sucursal
              </p>
            </div>
          </div>
          <button
            class="btn-close-mode"
            @click="exitEditMode"
            aria-label="Salir del modo edición"
          >
            <i class="fas fa-times"></i>
          </button>
        </div>
      </div>
    </Transition>

    <MapContainer
      ref="mapContainerRef"
      :isConnectionModeActive="isConnectionModeActive"
      :locationTypes="locationTypes"
      @map-click="handleMapClick"
      @route-created="handleRouteCreated"
      @route-started="handleRouteStarted"
    />

    <PointRegistrationForm
      v-if="!isEditSucursalesMode"
      :isOpen="showModal"
      :coordinates="modalCoordinates"
      :pointTypes="locationTypes"
      @submit="handlePointSubmit"
      @cancel="handleModalCancel"
    />

    <SucursalRegistrationForm
      v-if="isEditSucursalesMode"
      :isOpen="showSucursalModal"
      :coordinates="modalCoordinates"
      :locationTypes="locationTypes"
      @submit="handleSucursalSubmit"
      @cancel="handleSucursalCancel"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch, nextTick } from "vue";
import { useSetupStore } from "@/pages/setup/composables/useSetupStore";
import { useSucursalesManager } from "@/pages/dashboard/composables/useSucursalesManager";
import { useMapPoints } from "@/pages/dashboard/composables/useMapPoints";
import { useMapRoutes } from "@/pages/dashboard/composables/useMapRoutes";
import { typeLocationsAPI } from "@/services/api";
import { MapContainer, PointRegistrationForm } from "@/Features/map";
import SucursalRegistrationForm from "./SucursalRegistrationForm.vue";

const props = defineProps({
  isConnectionModeActive: Boolean,
  isEditSucursalesMode: {
    type: Boolean,
    default: false,
  },
  clientOrders: {
    type: Array,
    default: () => [],
  },
});

const emit = defineEmits([
  "sucursal-added",
  "sucursal-deleted",
  "exit-edit-mode",
]);

const mapContainerRef = ref(null);
const showModal = ref(false);
const showSucursalModal = ref(false);
const modalCoordinates = reactive({ lat: -16.5, lng: -68.15 });

const setupStore = useSetupStore();
const sucursalesManager = useSucursalesManager();
const mapPoints = useMapPoints();
const mapRoutes = useMapRoutes();

const locationTypes = computed(() => setupStore.pointTypes.value);

const drawSucursales = async () => {
  if (!mapContainerRef.value) {
    console.warn("mapContainerRef no disponible");
    return;
  }

  const sucursales = sucursalesManager.sucursales.value;
  console.log("📌 Dibujando sucursales:", sucursales.length);

  if (sucursales && sucursales.length > 0) {
    sucursales.forEach((sucursal) => {
      console.log(
        "  - Dibujando:",
        sucursal.name,
        "tipo:",
        sucursal.type_location_id,
      );
      mapContainerRef.value?.addSucursalMarker(sucursal);
    });
  }
};

const drawClientOrders = () => {
  if (!mapContainerRef.value || !props.clientOrders || props.clientOrders.length === 0) {
    return;
  }

  const map = mapContainerRef.value.getMapInstance();
  if (!map) return;

  console.log('📦 Dibujando pedidos de clientes:', props.clientOrders.length);

  props.clientOrders.forEach(order => {
    const customIcon = L.divIcon({
      html: `
        <div style="position: relative; display: flex; flex-direction: column; align-items: center;">
          <!-- Etiqueta flotante sobre el icono - COLOR PRINCIPAL DE LA PLATAFORMA -->
          <div style="
            background: #d4a373;
            color: #0a0f1a;
            font-size: 9px;
            font-weight: bold;
            padding: 3px 8px;
            border-radius: 12px;
            letter-spacing: 0.5px;
            white-space: nowrap;
            margin-bottom: 4px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.2);
          ">
            <i class="fas fa-user" style="font-size: 8px; margin-right: 3px;"></i>
            CLIENTE
          </div>
          <!-- Icono principal -->
          <div style="
            background: linear-gradient(135deg, #fff 0%, #f5e6d3 100%);
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #0a0f1a;
            font-size: 16px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
            border: 3px solid #d4a373;
            transition: transform 0.2s ease;
          ">
            <i class="fas fa-shopping-cart"></i>
          </div>
        </div>
      `,
      className: 'client-div-icon',
      iconSize: [36, 56],
      iconAnchor: [18, 48],
      popupAnchor: [0, -48]
    });

    const clientMarker = L.marker([order.delivery_lat, order.delivery_lng], {
      icon: customIcon
    }).addTo(map);

    const popupContent = `
      <div style="font-size: 13px; min-width: 200px; font-family: 'Segoe UI', sans-serif;">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px; padding-bottom: 6px; border-bottom: 1px solid #d4a373;">
          <i class="fas fa-shopping-cart" style="color: #d4a373; font-size: 18px;"></i>
          <strong style="color: #333;">Pedido de Cliente</strong>
        </div>
        <div style="margin-bottom: 5px;">
          <span style="color: #666;">📦 Producto:</span>
          <strong style="color: #333;"> ${order.product_name}</strong>
        </div>
        <div style="margin-bottom: 5px;">
          <span style="color: #666;">🔢 Cantidad:</span>
          <strong style="color: #333;"> ${order.quantity} ${order.product_name}</strong>
        </div>
        <div style="margin-bottom: 5px;">
          <span style="color: #666;">💰 Precio unitario:</span>
          <strong style="color: #d4a373;"> ${order.price} Bs</strong>
        </div>
        <div style="margin-bottom: 8px; padding-bottom: 6px; border-bottom: 1px solid #e0e0e0;">
          <span style="color: #666;">💵 Total:</span>
          <strong style="color: #d4a373; font-size: 14px;"> ${order.total_amount} Bs</strong>
        </div>
        <div style="font-size: 11px; color: #999; display: flex; align-items: center; gap: 4px;">
          <i class="fas fa-calendar-alt"></i>
          ${new Date(order.created_at).toLocaleDateString('es-ES', { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })}
        </div>
      </div>
    `;

    clientMarker.bindPopup(popupContent, {
      maxWidth: 280,
      minWidth: 220,
      className: 'client-popup'
    });

    // Efecto hover
    clientMarker.on('mouseover', function() {
      const icon = this._icon?.querySelector('div:last-child');
      if (icon) {
        icon.style.transform = 'scale(1.1)';
        icon.style.transition = 'transform 0.2s ease';
      }
    });

    clientMarker.on('mouseout', function() {
      const icon = this._icon?.querySelector('div:last-child');
      if (icon) {
        icon.style.transform = 'scale(1)';
      }
    });
  });
};

watch(
  locationTypes,
  (newTypes) => {
    if (
      newTypes &&
      newTypes.length > 0 &&
      sucursalesManager.sucursales.value.length > 0
    ) {
      console.log("📍 locationTypes disponibles, dibujando sucursales...");
      nextTick(() => {
        drawSucursales();
      });
    }
  },
  { deep: true },
);

watch(
  () => sucursalesManager.sucursales.value,
  (newSucursales) => {
    console.log("🔄 Sucursales cargadas:", newSucursales.length);
    if (
      newSucursales &&
      newSucursales.length > 0 &&
      locationTypes.value.length > 0
    ) {
      nextTick(() => {
        drawSucursales();
      });
    }
  },
  { deep: true, immediate: true },
);

watch(
  () => props.clientOrders,
  (newOrders) => {
    console.log("🔄 Pedidos de clientes cargados:", newOrders.length);
    if (newOrders && newOrders.length > 0) {
      nextTick(() => {
        drawClientOrders();
      });
    }
  },
  { deep: true, immediate: true },
);

onMounted(async () => {
  console.log("📍 MapComponent mounted");

  if (
    setupStore.pointTypes.value.length === 0 &&
    setupStore.company.value?.id
  ) {
    try {
      const result = await typeLocationsAPI.getByCompany(
        setupStore.company.value.id,
      );
      if (result.success && result.data.length > 0) {
        setupStore.setPointTypes(result.data);
      }
    } catch (error) {
      console.error("Error al cargar tipos de ubicación:", error);
    }
  }

  await sucursalesManager.loadSucursales();

  console.log(
    "📋 Sucursales cargadas:",
    sucursalesManager.sucursales.value.length,
  );

  setTimeout(() => {
    if (locationTypes.value.length > 0) {
      drawSucursales();
    }
    if (props.clientOrders && props.clientOrders.length > 0) {
      drawClientOrders();
    }
    drawAllRoutes();
  }, 500);
});

const handleMapClick = (latlng) => {
  if (!props.isEditSucursalesMode) {
    return;
  }

  modalCoordinates.lat = latlng.lat;
  modalCoordinates.lng = latlng.lng;
  showSucursalModal.value = true;
};

const handlePointSubmit = (pointData) => {
  const point = mapPoints.addPoint(pointData);
  mapContainerRef.value?.addMarker(point);
  showModal.value = false;
};

const handleModalCancel = () => {
  showModal.value = false;
};

const handleSucursalSubmit = async (sucursalData) => {
  const newSucursal = await sucursalesManager.addSucursal({
    name: sucursalData.name,
    lat: modalCoordinates.lat,
    lng: modalCoordinates.lng,
    type_location_id: sucursalData.typeLocationId,
  });

  if (newSucursal) {
    mapContainerRef.value?.addSucursalMarker(newSucursal);
    emit("sucursal-added", newSucursal);
  }

  showSucursalModal.value = false;
};

const handleSucursalCancel = () => {
  showSucursalModal.value = false;
};

const handleRouteCreated = (data) => {
  const fromPoint = mapPoints.getPoint(data.fromPointId);
  const toPoint = mapPoints.getPoint(data.toPointId);

  if (fromPoint && toPoint) {
    const route = mapRoutes.addRoute(data.fromPointId, data.toPointId);
    if (route && mapContainerRef.value) {
      mapContainerRef.value.drawRoute(fromPoint, toPoint, "#d4a373", 2);
    }
  }
};

const handleRouteStarted = (data) => {
  console.log("Conexión iniciada:", data);
};

const drawAllRoutes = () => {
  const routes = mapRoutes.allRoutes.value;
  if (routes.length === 0) return;

  routes.forEach((route) => {
    const fromPoint = mapPoints.getPoint(route.fromId);
    const toPoint = mapPoints.getPoint(route.toId);

    if (fromPoint && toPoint && mapContainerRef.value) {
      mapContainerRef.value.drawRoute(fromPoint, toPoint, "#d4a373", 2);
    }
  });
};

const openModal = (lat = -16.5, lng = -68.15) => {
  modalCoordinates.lat = lat;
  modalCoordinates.lng = lng;
  showModal.value = true;
};

const activateConnectionMode = () => {
  console.log("Modo de conexión activado");
};

const deactivateConnectionMode = () => {
  if (mapContainerRef.value) {
    mapContainerRef.value.cancelConnectionMode();
  }
};

const exitEditMode = () => {
  emit("exit-edit-mode");
};

defineExpose({
  openModal,
  activateConnectionMode,
  deactivateConnectionMode,
});
</script>

<style scoped>
.map-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
}

.edit-mode-indicator {
  position: absolute;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: linear-gradient(135deg, #d4a373 0%, #e0b082 100%);
  color: #0a0f1a;
  padding: 1rem 1.5rem;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  font-weight: 600;
  font-size: 0.9rem;
  z-index: 1000;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
  animation: slideDown 0.3s ease;
  border: 2px solid rgba(255, 255, 255, 0.2);
  max-width: 90%;
  width: auto;
}

.indicator-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  gap: 1rem;
}

.indicator-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.indicator-left i {
  font-size: 1.3rem;
  flex-shrink: 0;
}

.indicator-text {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.indicator-title {
  margin: 0;
  font-size: 1rem;
  font-weight: 700;
  color: #0a0f1a;
}

.indicator-subtitle {
  margin: 0;
  font-size: 0.85rem;
  color: rgba(10, 15, 26, 0.8);
}

.btn-close-mode {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: #0a0f1a;
  cursor: pointer;
  font-size: 1.25rem;
  padding: 0.5rem;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  flex-shrink: 0;
  font-weight: 700;
}

.btn-close-mode:hover {
  background: rgba(255, 255, 255, 0.4);
  transform: scale(1.1);
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}

.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
}

.slide-down-enter-from {
  opacity: 0;
  transform: translateX(-50%) translateY(-20px);
}

.slide-down-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(-20px);
}
</style>
