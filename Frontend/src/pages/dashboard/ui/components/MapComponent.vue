<template>
  <div class="map-wrapper">
    <MapContainer 
      ref="mapContainerRef" 
      :isConnectionModeActive="isConnectionModeActive"
      @map-click="handleMapClick"
      @route-created="handleRouteCreated"
      @route-started="handleRouteStarted"
    />
    <PointRegistrationForm 
      :isOpen="showModal" 
      :coordinates="modalCoordinates"
      :pointTypes="pointTypes"
      @submit="handlePointSubmit"
      @cancel="handleModalCancel"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { useSetupStore } from '@/pages/setup/composables/useSetupStore';
import { useMapPoints } from '@/pages/dashboard/composables/useMapPoints';
import { useMapRoutes } from '@/pages/dashboard/composables/useMapRoutes';
import { MapContainer, PointRegistrationForm } from '@/Features/map';

defineProps({
  isConnectionModeActive: Boolean
});

const mapContainerRef = ref(null);
const showModal = ref(false);
const modalCoordinates = reactive({ lat: -16.5, lng: -68.15 });

const setupStore = useSetupStore();
const setupData = setupStore.getSetupData();
const mapPoints = useMapPoints();
const mapRoutes = useMapRoutes();

const pointTypes = ref([
  ...(setupData.pointTypes.length > 0 ? setupData.pointTypes : [
    { id: 1, name: 'Almacén', icon: 'fa-warehouse', color: '#d4a373' },
    { id: 2, name: 'Tienda', icon: 'fa-shopping-bag', color: '#4a9eff' }
  ])
]);

onMounted(() => {
  // Dibujar rutas existentes cuando se monta el componente
  setTimeout(() => {
    drawAllRoutes();
  }, 500);
});

const handleMapClick = (latlng) => {
  modalCoordinates.lat = latlng.lat;
  modalCoordinates.lng = latlng.lng;
  showModal.value = true;
};

const handlePointSubmit = (pointData) => {
  const point = mapPoints.addPoint(pointData);
  mapContainerRef.value?.addMarker(point);
  showModal.value = false;
};

const handleModalCancel = () => {
  showModal.value = false;
};

const handleRouteCreated = (data) => {
  const fromPoint = mapPoints.getPoint(data.fromPointId);
  const toPoint = mapPoints.getPoint(data.toPointId);
  
  if (fromPoint && toPoint) {
    const route = mapRoutes.addRoute(data.fromPointId, data.toPointId);
    if (route && mapContainerRef.value) {
      mapContainerRef.value.drawRoute(fromPoint, toPoint, '#d4a373', 2);
    }
  }
};

const handleRouteStarted = (data) => {
  // Aquí podemos agregar efectos visuales cuando inicia la conexión
};

const drawAllRoutes = () => {
  const routes = mapRoutes.allRoutes.value;
  if (routes.length === 0) return;

  routes.forEach(route => {
    const fromPoint = mapPoints.getPoint(route.fromId);
    const toPoint = mapPoints.getPoint(route.toId);
    
    if (fromPoint && toPoint && mapContainerRef.value) {
      mapContainerRef.value.drawRoute(fromPoint, toPoint, '#d4a373', 2);
    }
  });
};

const openModal = (lat = -16.5, lng = -68.15) => {
  modalCoordinates.lat = lat;
  modalCoordinates.lng = lng;
  showModal.value = true;
};

const activateConnectionMode = () => {
  // Instrucción al usuario en modo conexión
  console.log('Modo de conexión activado');
};

const deactivateConnectionMode = () => {
  if (mapContainerRef.value) {
    mapContainerRef.value.cancelConnectionMode();
  }
};

defineExpose({ 
  openModal,
  activateConnectionMode,
  deactivateConnectionMode
});
</script>
<style scoped>
.map-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
}
</style>

