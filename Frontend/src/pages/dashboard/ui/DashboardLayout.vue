<template>
  <div class="layout-container">
    <NavbarWidget />

    <div class="content-container">
      <SidebarWidget 
        @add-point="handleAddPoint" 
        @show-materials="handleShowMaterials"
        @show-routes="handleShowRoutes"
      />

      <main class="body-container">
        <MapComponent 
          v-show="currentView === 'map' || currentView === 'routes'" 
          ref="mapComponentRef"
          :isConnectionModeActive="isConnectionModeActive"
          @toggle-connection-mode="handleToggleConnectionMode"
        />
        <MaterialsManagement 
          v-show="currentView === 'materials'" 
          @back-to-map="handleBackToMap"
          @continue="handleContinueMaterials"
        />
        
        <!-- RouteManager como overlay flotante -->
        <Teleport to="body" v-if="currentView === 'routes'">
          <div class="route-manager-overlay">
            <div class="route-manager-container">
              <RouteManagementView
                :isConnectionModeActive="isConnectionModeActive"
                @close="handleBackToMap"
                @toggle-connection-mode="handleToggleConnectionMode"
              />
            </div>
          </div>
        </Teleport>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { MapComponent } from './components';
import { MaterialsManagement } from '@/pages/materials';
import { NavbarWidget, SidebarWidget } from "@/widgets";
import RouteManagementView from './RouteManagementView.vue';

const mapComponentRef = ref(null);
const currentView = ref('map');
const isConnectionModeActive = ref(false);

const handleAddPoint = () => {
  if (mapComponentRef.value) {
    mapComponentRef.value.openModal();
  }
};

const handleShowMaterials = () => {
  currentView.value = 'materials';
};

const handleShowRoutes = () => {
  currentView.value = 'routes';
};

const handleBackToMap = () => {
  currentView.value = 'map';
  isConnectionModeActive.value = false;
};

const handleContinueMaterials = () => {
  // Aquí se puede agregar lógica para continuar al siguiente paso
  currentView.value = 'map';
};

const handleToggleConnectionMode = () => {
  isConnectionModeActive.value = !isConnectionModeActive.value;
  if (mapComponentRef.value) {
    if (isConnectionModeActive.value) {
      mapComponentRef.value.activateConnectionMode();
    } else {
      mapComponentRef.value.deactivateConnectionMode();
    }
  }
};
</script>

<style scoped>
.layout-container {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #eef2f9;
}

.content-container {
  display: flex;
  width: 100%;
  height: calc(100vh - 62px);
}

.body-container {
  flex: 1;
  overflow: hidden;
  background: #eef2f9;
  height: calc(100vh - 62px);
  display: flex;
  flex-direction: column;
  position: relative;
}

.dashboard-content {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

.dashboard-content h2 {
  color: #ffffff;
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 1rem;
  background: linear-gradient(135deg, #ffffff, #d4a373);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.dashboard-content p {
  color: #a0abb9;
  font-size: 1rem;
}

::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(212, 163, 115, 0.1);
}

::-webkit-scrollbar-thumb {
  background: rgba(212, 163, 115, 0.3);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(212, 163, 115, 0.5);
}
</style>

<style>
.route-manager-overlay {
  position: fixed;
  inset: 0;
  background: none;
  pointer-events: none;
  display: flex;
  align-items: flex-start;
  justify-content: flex-end;
  z-index: 2000;
  padding: 1rem;
  padding-top: 4.5rem;
}

.route-manager-container {
  width: 100%;
  max-width: 380px;
  max-height: calc(100vh - 100px);
  overflow-y: auto;
  pointer-events: auto;
  animation: slideInRight 0.3s ease-out;
}

@keyframes slideInRight {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@media (max-width: 768px) {
  .route-manager-overlay {
    align-items: flex-start;
    justify-content: flex-end;
    padding: 0.5rem;
    padding-top: 4rem;
  }

  .route-manager-container {
    max-width: calc(100vw - 1rem);
    max-height: calc(100vh - 80px);
  }
}
</style>
