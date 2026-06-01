<template>
  <div class="layout-container">
    <NavbarWidget />

    <div class="content-container">
      <SidebarWidget
        :isEditSucursalesMode="isEditSucursalesMode"
        @add-point="handleAddPoint"
        @show-materials="handleShowMaterials"
        @show-routes="handleShowRoutes"
        @show-optimization="handleShowOptimization"
        @toggle-edit-mode="handleToggleEditMode"
      />

      <main class="body-container">
        <div v-show="currentView === 'map' || currentView === 'routes'" class="map-and-routing">
          <MapComponent
            ref="mapComponentRef"
            :isConnectionModeActive="isConnectionModeActive"
            :isEditSucursalesMode="isEditSucursalesMode"
            :clientOrders="clientOrders"
            :optimizationRoutes="optimizationRoutes"
            @toggle-connection-mode="handleToggleConnectionMode"
            @sucursal-added="handleSucursalAdded"
            @exit-edit-mode="handleExitEditMode"
            @clear-routes="clearOptimizationRoutes"
          />
        </div>

        <MaterialsManagement
          v-show="currentView === 'materials'"
          @back-to-map="handleBackToMap"
          @continue="handleContinueMaterials"
        />

        <OptimizationView
          v-show="currentView === 'optimization'"
          :suppliers-count="suppliersCount"
          :customers-count="customersCount"
          @back-to-map="handleBackToMap"
          @visualize-routes="handleVisualizeRoutes"
        />

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

    <button 
      v-show="currentView === 'map'" 
      class="btn-optimize-float" 
      @click="handleShowOptimization"
    >
      <i class="fas fa-chart-line"></i>
      <span>Optimizar</span>
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { MapComponent } from "./components";
import { MaterialsManagement } from "@/pages/materials";
import { NavbarWidget, SidebarWidget } from "@/widgets";
import { useSetupStore } from "@/pages/setup/composables/useSetupStore";
import {
  companiesAPI,
  typeLocationsAPI,
  typeMaterialsAPI,
  locationsAPI,
  ordersAPI,
} from "@/services/api";
import RouteManagementView from "./RouteManagementView.vue";
import OptimizationView from "./components/OptimizationView.vue";

const mapComponentRef = ref(null);
const currentView = ref("map");
const isConnectionModeActive = ref(false);
const isEditSucursalesMode = ref(false);
const clientOrders = ref([]);
const setupStore = useSetupStore();
const suppliersCount = ref(0);
const customersCount = ref(0);
const optimizationRoutes = ref([]);

const updateCounts = async () => {
  const companyId = setupStore.company.value?.id;
  if (companyId) {
    try {
      const locations = await locationsAPI.getByCompany(companyId);
      suppliersCount.value = locations.success ? locations.data.length : 0;
      
      const orders = await ordersAPI.getByCompany(companyId);
      customersCount.value = orders.success ? orders.data.length : 0;
    } catch (error) {
      console.error('Error al cargar conteos:', error);
    }
  }
};

const handleShowOptimization = () => {
  currentView.value = "optimization";
};

const handleVisualizeRoutes = (routes) => {
  optimizationRoutes.value = routes;
  currentView.value = "map";
  
  setTimeout(() => {
    if (mapComponentRef.value) {
      mapComponentRef.value.drawOptimizationRoutes(routes);
    }
  }, 100);
};

const clearOptimizationRoutes = () => {
  optimizationRoutes.value = [];
};

onMounted(async () => {
  console.log("DashboardLayout mounted");

  const setupData = setupStore.getSetupData();
  console.log("Setup data:", setupData);

  if (!setupData.company || !setupData.company.id) {
    console.log("No hay empresa en setupStore, obteniendo del backend...");

    const currentUserData = JSON.parse(
      sessionStorage.getItem("currentUserData") || "{}",
    );
    const userId = currentUserData.userId || setupData.userId;

    if (userId) {
      console.log("Obteniendo empresa para userId:", userId);
      const companyResponse = await companiesAPI.getByUser(userId);

      if (
        companyResponse.success &&
        companyResponse.data &&
        companyResponse.data.length > 0
      ) {
        const company = companyResponse.data[0];
        console.log("Empresa cargada:", company);
        setupStore.setCompany({
          id: company.id,
          name: company.name,
          description: company.description || "",
          city: company.address || "",
          phone: company.phone || "",
        });
      }
    }
  } else {
    console.log("Empresa ya existe:", setupData.company.name);
  }

  const currentSetupData = setupStore.getSetupData();
  const companyId = currentSetupData.company?.id;

  if (companyId) {
    await updateCounts();

    if (currentSetupData.pointTypes.length === 0) {
      console.log("Cargando tipos de sucursales...");
      try {
        const typesResponse = await typeLocationsAPI.getByCompany(companyId);
        if (typesResponse.success && typesResponse.data.length > 0) {
          console.log("Tipos de sucursales cargados:", typesResponse.data);
          setupStore.setPointTypes(typesResponse.data);
        }
      } catch (error) {
        console.error("Error al cargar tipos de sucursales:", error);
      }
    }

    console.log("Cargando tipos de materiales...");
    try {
      const materialsResponse = await typeMaterialsAPI.getByCompany(companyId);
      if (materialsResponse.success && materialsResponse.data.length > 0) {
        console.log("Tipos de materiales cargados:", materialsResponse.data);
        setupStore.setProducts(materialsResponse.data);
      }
    } catch (error) {
      console.error("Error al cargar tipos de materiales:", error);
    }

    console.log("Cargando sucursales existentes...");
    try {
      const sucursalesResponse = await locationsAPI.getByCompany(companyId);
      if (sucursalesResponse.success && sucursalesResponse.data.length > 0) {
        console.log("Sucursales cargadas:", sucursalesResponse.data);
      }
    } catch (error) {
      console.error("Error al cargar sucursales:", error);
    }

    console.log("Cargando pedidos de clientes...");
    try {
      const ordersResponse = await ordersAPI.getByCompany(companyId);
      if (ordersResponse.success && ordersResponse.data.length > 0) {
        console.log("Pedidos cargados:", ordersResponse.data);
        clientOrders.value = ordersResponse.data;
      } else {
        clientOrders.value = [];
      }
    } catch (error) {
      console.error("Error al cargar pedidos:", error);
    }
  }
});

const handleAddPoint = () => {
  if (mapComponentRef.value) {
    mapComponentRef.value.openModal();
  }
};

const handleShowMaterials = () => {
  currentView.value = "materials";
};

const handleShowRoutes = () => {
  currentView.value = "routes";
};

const handleBackToMap = () => {
  currentView.value = "map";
  isConnectionModeActive.value = false;
  isEditSucursalesMode.value = false;
  clearOptimizationRoutes();
};

const handleContinueMaterials = () => {
  currentView.value = "map";
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

const handleToggleEditMode = (isEditMode) => {
  isEditSucursalesMode.value = isEditMode;
};

const handleExitEditMode = () => {
  isEditSucursalesMode.value = false;
};

const handleSucursalAdded = (sucursal) => {
  console.log("Sucursal agregada:", sucursal);
  updateCounts();
};
</script>

<style scoped>
.layout-container {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #eef2f9;
  overflow: hidden;
}

.content-container {
  display: flex;
  width: 100%;
  flex: 1;
  overflow: hidden;
}

.body-container {
  flex: 1;
  overflow: auto;
  background: #eef2f9;
  display: flex;
  flex-direction: column;
  position: relative;
  width: 100%;
}

.map-and-routing {
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding: 15px;
  height: 100%;
  overflow-y: auto;
}

.map-and-routing > div:first-child {
  flex: 1;
  min-height: 400px;
}

.btn-optimize-float {
  position: fixed;
  bottom: 24px;
  right: 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 14px 24px;
  border-radius: 40px;
  cursor: pointer;
  font-weight: 600;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 10px;
  z-index: 1000;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.btn-optimize-float:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.btn-optimize-float i {
  font-size: 16px;
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

.body-container > * {
  width: 100%;
  height: 100%;
  flex: 1;
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

  .btn-optimize-float {
    padding: 10px 18px;
    font-size: 12px;
    bottom: 16px;
    right: 16px;
  }
}
</style>