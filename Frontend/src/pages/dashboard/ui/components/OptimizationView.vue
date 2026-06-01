<template>
  <div class="optimization-management">
    <div class="toast-container">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="toast"
        :class="toast.type"
      >
        <i :class="toast.icon"></i>
        <span>{{ toast.message }}</span>
      </div>
    </div>

    <div class="management-header">
      <div class="header-left">
        <button class="btn-back" @click="handleBackToMap">
          <i class="fas fa-arrow-left"></i>
          <span>Volver al Mapa</span>
        </button>
        <div class="header-title">
          <h1><i class="fas fa-chart-line"></i> Optimizacion de Rutas</h1>
          <p>
            Optimiza la distribucion de productos usando algoritmos Vogel y MODI
          </p>
        </div>
      </div>
      <div class="header-stats">
        <div class="stat-card">
          <span class="stat-label">Sucursales</span>
          <strong class="stat-value">{{ suppliersCount }}</strong>
        </div>
        <div class="stat-card">
          <span class="stat-label">Pedidos</span>
          <strong class="stat-value">{{ customersCount }}</strong>
        </div>
        <div class="stat-card">
          <span class="stat-label">Costo/km</span>
          <div class="cost-input-header">
            <input
              v-model.number="costPerKm"
              type="number"
              step="0.1"
              min="0"
            />
            <span>Bs</span>
          </div>
        </div>

        <div class="stat-card product-stat-card">
          <span class="stat-label">Producto</span>
          <select
            v-model="selectedProductId"
            class="product-select-header"
            :disabled="products.length === 0"
          >
            <option
              v-for="product in products"
              :key="product.id"
              :value="product.id"
            >
              {{ product.name }}
            </option>
          </select>
        </div>

        <div class="stat-card optimize-card">
          <button
            class="btn-optimize-header"
            @click="optimizeRoutes"
            :disabled="isLoading || !hasData || !selectedProductId"
          >
            <i v-if="isLoading" class="fas fa-spinner fa-spin"></i>
            <i v-else class="fas fa-rocket"></i>
            {{ isLoading ? "Optimizando..." : "Optimizar" }}
          </button>
        </div>
      </div>
    </div>

    <div class="management-content">
      <div v-if="optimizationResult && !isLoading" class="results-panel">
        <div class="panel-header">
          <h2><i class="fas fa-chart-bar"></i> Resultados de Optimizacion</h2>
        </div>

        <div class="optimized-product-info">
          <i class="fas fa-box"></i>
          <span
            >Producto optimizado:
            <strong>{{ optimizedProductName }}</strong></span
          >
        </div>

        <div class="metrics-grid">
          <div class="metric-card">
            <div class="metric-value">{{ totalCost.toFixed(2) }}</div>
            <div class="metric-label">Costo Total (Bs)</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">{{ totalDistance.toFixed(1) }}</div>
            <div class="metric-label">Distancia Total (km)</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">{{ allocationsCount }}</div>
            <div class="metric-label">Asignaciones</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">{{ averageCost.toFixed(2) }}</div>
            <div class="metric-label">Costo Promedio</div>
          </div>
        </div>

        <div class="supply-demand-summary">
          <div class="summary-box">
            <h4><i class="fas fa-boxes"></i> Stock por Sucursal</h4>
            <div
              v-for="supplier in optimizationResult.suppliers_data"
              :key="supplier.id"
              class="supply-item"
            >
              <span>{{ supplier.name }}</span>
              <strong>{{ supplier.total_stock }} und</strong>
            </div>
            <div class="total-supply">
              <span>Total Stock:</span>
              <strong>{{ totalStock }} und</strong>
            </div>
          </div>

          <div class="summary-box">
            <h4><i class="fas fa-shopping-cart"></i> Demanda por Cliente</h4>
            <div
              v-for="customer in optimizationResult.customers_data"
              :key="customer.id"
              class="demand-item"
            >
              <span>{{ getCustomerDisplayName(customer) }}</span>
              <strong>{{ customer.total_demand }} und</strong>
            </div>
            <div class="total-demand">
              <span>Total Demanda:</span>
              <strong>{{ totalDemand }} und</strong>
            </div>
          </div>
        </div>

        <div class="analysis-section">
          <div class="analysis-tabs">
            <button
              v-for="tab in tabs"
              :key="tab.key"
              :class="['tab-btn', { active: activeTab === tab.key }]"
              @click="activeTab = tab.key"
            >
              <i :class="tab.icon"></i> {{ tab.label }}
            </button>
          </div>

          <div v-if="activeTab === 'rutas'" class="routes-container">
            <div
              v-for="(route, idx) in optimizationResult.routes"
              :key="idx"
              class="route-item"
            >
              <div class="route-header">
                <span class="route-number">{{ idx + 1 }}</span>
                <span class="supplier-name">
                  <i class="fas fa-warehouse"></i> {{ route.supplier_name }}
                </span>
                <i class="fas fa-arrow-right arrow"></i>
                <span class="customer-name">
                  <i class="fas fa-user"></i>
                  {{ getCustomerDisplayNameFromRoute(route) }}
                </span>
              </div>
              <div class="route-details">
                <span class="quantity">
                  <i class="fas fa-box"></i> {{ route.quantity }} und
                </span>
                <span class="distance">
                  <i class="fas fa-road"></i>
                  {{ route.distance_km.toFixed(2) }} km
                </span>
                <span class="unit-cost">
                  <i class="fas fa-tag"></i>
                  {{
                    route.unit_cost?.toFixed(2) ||
                    (route.cost / route.quantity).toFixed(2)
                  }}
                  Bs/und
                </span>
                <span class="cost">
                  <i class="fas fa-money-bill-wave"></i>
                  {{ route.cost.toFixed(2) }} Bs
                </span>
              </div>
            </div>
            <div
              v-if="optimizationResult.routes.length === 0"
              class="empty-state"
            >
              <i class="fas fa-inbox"></i>
              <p>No hay rutas asignadas</p>
            </div>
          </div>

          <div v-if="activeTab === 'matriz'" class="matrix-container">
            <div class="table-wrapper">
              <table class="cost-matrix-table">
                <thead>
                  <tr>
                    <th>Sucursal / Cliente</th>
                    <th
                      v-for="(
                        customer, idx
                      ) in optimizationResult.customers_data"
                      :key="customer.id"
                    >
                      <div class="customer-name-cell">
                        <i class="fas fa-user"></i>
                        <strong>{{ getCustomerDisplayName(customer) }}</strong>
                        <span class="demand-badge"
                          >({{ customer.total_demand }} und)</span
                        >
                      </div>
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(supplier, i) in optimizationResult.suppliers_data"
                    :key="supplier.id"
                  >
                    <td class="supplier-cell">
                      <i class="fas fa-warehouse"></i>
                      <strong>{{ supplier.name }}</strong>
                      <span class="stock-badge"
                        >({{ supplier.total_stock }} und)</span
                      >
                    </td>
                    <td
                      v-for="(cost, j) in optimizationResult.cost_matrix[i]"
                      :key="j"
                      :class="['cost-cell', { 'best-cost': isBestCost(i, j) }]"
                    >
                      {{ cost.toFixed(2) }} Bs
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div class="matrix-legend">
              <div class="legend-item">
                <span class="legend-color best-cost"></span>
                <span>Menor costo por cliente</span>
              </div>
              <div class="legend-item">
                <span class="legend-color zero-cost"></span>
                <span>Costo cero (excedente de stock)</span>
              </div>
              <div class="legend-item">
                <i class="fas fa-warehouse"></i>
                <span>Sucursal</span>
              </div>
              <div class="legend-item">
                <i class="fas fa-user"></i>
                <span>Cliente</span>
              </div>
            </div>
          </div>

          <div
            v-if="activeTab === 'asignaciones'"
            class="assignments-container"
          >
            <div class="assignments-info">
              <div class="info-item">
                <i class="fas fa-chart-line"></i>
                <span
                  ><strong>Vogel (VAM):</strong>
                  {{ vogelAllocationsCount }} asignaciones</span
                >
              </div>
              <div class="info-item">
                <i class="fas fa-chart-line"></i>
                <span
                  ><strong>MODI:</strong>
                  {{ modiAllocationsCount }} asignaciones</span
                >
              </div>
              <div class="info-item">
                <i class="fas fa-check-circle"></i>
                <span
                  ><strong>Optimo:</strong>
                  {{ isOptimal ? "Si" : "No verificado" }}</span
                >
              </div>
            </div>

            <div class="assignments-details">
              <div
                v-for="(alloc, idx) in optimizationResult.routes"
                :key="idx"
                class="assignment-item"
              >
                <span class="assignment-number">{{ idx + 1 }}</span>
                <span class="supplier">{{ alloc.supplier_name }}</span>
                <i class="fas fa-arrow-right arrow-icon"></i>
                <span class="customer">{{
                  getCustomerDisplayNameFromRoute(alloc)
                }}</span>
                <span class="quantity-badge">{{ alloc.quantity }} und</span>
                <span class="cost-badge">{{ alloc.cost.toFixed(2) }} Bs</span>
              </div>
            </div>
          </div>
        </div>

        <div class="action-buttons">
          <button class="btn-visualize" @click="visualizeRoutesOnMap">
            <i class="fas fa-map"></i> Visualizar en Mapa
          </button>
          <button class="btn-download" @click="downloadAnalysis">
            <i class="fas fa-download"></i> Descargar Analisis
          </button>
        </div>
      </div>

      <div v-if="isLoading" class="loading-state">
        <i class="fas fa-spinner fa-spin"></i>
        <p>Optimizando rutas...</p>
        <small>Calculando distancias y asignaciones optimas</small>
      </div>

      <div
        v-if="!hasData && !isLoading && !optimizationResult"
        class="no-data-state"
      >
        <i class="fas fa-info-circle"></i>
        <p>No hay sucursales o pedidos para optimizar</p>
        <small>Primero crea sucursales y registra pedidos de clientes</small>
      </div>

      <div
        v-if="hasData && !optimizationResult && !isLoading"
        class="no-data-state"
      >
        <i class="fas fa-chart-line"></i>
        <p>Selecciona un producto y presiona el boton Optimizar</p>
        <small
          >El sistema calculara la mejor distribucion usando Vogel y MODI</small
        >
      </div>

      <div v-if="error" class="error-state">
        <i class="fas fa-exclamation-triangle"></i>
        <p>{{ error }}</p>
        <button class="btn-close-error" @click="error = null">
          <i class="fas fa-times"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { routingAPI, productsAPI } from "@/services/api";
import { useSetupStore } from "@/pages/setup/composables/useSetupStore";

const props = defineProps({
  suppliersCount: {
    type: Number,
    default: 0,
  },
  customersCount: {
    type: Number,
    default: 0,
  },
});

const emit = defineEmits(["back-to-map", "visualize-routes"]);

const setupStore = useSetupStore();
const isLoading = ref(false);
const error = ref(null);
const costPerKm = ref(5.5);
const optimizationResult = ref(null);
const activeTab = ref("rutas");
const toasts = ref([]);
const products = ref([]);
const selectedProductId = ref(null);
let nextToastId = 0;

const tabs = [
  { key: "rutas", label: "Rutas", icon: "fas fa-route" },
  { key: "matriz", label: "Matriz Costos", icon: "fas fa-table" },
  { key: "asignaciones", label: "Asignaciones", icon: "fas fa-tasks" },
];

const optimizedProductName = computed(() => {
  if (!selectedProductId.value) return "No seleccionado";
  const product = products.value.find((p) => p.id === selectedProductId.value);
  return product ? product.name : "Desconocido";
});

const showToast = (message, type = "success") => {
  const id = nextToastId++;
  const iconMap = {
    success: "fas fa-check-circle",
    error: "fas fa-exclamation-circle",
    warning: "fas fa-exclamation-triangle",
    info: "fas fa-info-circle",
  };

  toasts.value.push({
    id,
    message,
    type,
    icon: iconMap[type] || iconMap.success,
  });

  setTimeout(() => {
    toasts.value = toasts.value.filter((t) => t.id !== id);
  }, 3000);
};

const hasData = computed(
  () => props.suppliersCount > 0 && props.customersCount > 0,
);

const totalCost = computed(() => optimizationResult.value?.total_cost || 0);
const totalDistance = computed(
  () => optimizationResult.value?.total_distance_km || 0,
);
const allocationsCount = computed(
  () => optimizationResult.value?.total_allocations || 0,
);
const averageCost = computed(() => {
  if (allocationsCount.value === 0) return 0;
  return totalCost.value / allocationsCount.value;
});

const totalStock = computed(() => {
  if (!optimizationResult.value) return 0;
  return optimizationResult.value.suppliers_data.reduce(
    (sum, s) => sum + (s.total_stock || 0),
    0,
  );
});

const totalDemand = computed(() => {
  if (!optimizationResult.value) return 0;
  return optimizationResult.value.customers_data.reduce(
    (sum, c) => sum + (c.total_demand || 0),
    0,
  );
});

const vogelAllocationsCount = computed(() => {
  return optimizationResult.value?.vogel_solution?.allocations?.length || 0;
});

const modiAllocationsCount = computed(() => {
  return optimizationResult.value?.modi_solution?.allocations?.length || 0;
});

const isOptimal = computed(() => {
  return optimizationResult.value?.modi_solution?.is_optimal || false;
});

const getCustomerDisplayName = (customer) => {
  if (!customer) return 'Cliente';
  
  let fullName = '';
  
  if (customer.user_name) {
    fullName = customer.user_name;
  } else if (customer.name && customer.name.includes(' - ')) {
    fullName = customer.name.split(' - ')[0];
  } else if (customer.name) {
    fullName = customer.name;
  } else {
    return 'Cliente';
  }
  
  let firstName = fullName.trim().split(' ')[0];
  
  if (firstName.length > 15) {
    firstName = firstName.substring(0, 12) + '...';
  }
  
  return firstName;
};

const getCustomerDisplayNameFromRoute = (route) => {
  if (!route) return "Cliente";
  if (!route.customer_name) return "Cliente";

  let displayName = route.customer_name;

  if (displayName.toLowerCase().includes("pedido")) {
    displayName = displayName.replace(/pedido/gi, "Cliente");
  }

  if (displayName.length > 25) {
    displayName = displayName.substring(0, 22) + "...";
  }

  return displayName;
};

const isBestCost = (supplierIdx, customerIdx) => {
  const matrix = optimizationResult.value?.cost_matrix;
  if (!matrix || matrix.length === 0) return false;

  const column = matrix.map((row) => row[customerIdx]);
  const minCost = Math.min(...column);
  const currentCost = matrix[supplierIdx][customerIdx];

  return currentCost === minCost && currentCost > 0;
};

const loadProducts = async () => {
  const companyId = setupStore.company.value?.id;

  if (!companyId) {
    console.warn("No hay empresa activa para cargar productos");
    return;
  }

  try {
    const response = await productsAPI.getByCompany(companyId);

    console.log("Respuesta de productsAPI:", response);

    if (Array.isArray(response)) {
      products.value = response;
    } else if (response && response.success && Array.isArray(response.data)) {
      products.value = response.data;
    } else if (response && response.data && Array.isArray(response.data)) {
      products.value = response.data;
    } else {
      products.value = [];
      console.warn("Formato de respuesta no reconocido:", response);
    }

    if (products.value.length > 0) {
      selectedProductId.value = products.value[0].id;
      console.log("Productos cargados:", products.value);
      console.log("Producto seleccionado ID:", selectedProductId.value);
    } else {
      console.warn("No hay productos disponibles para esta empresa");
      showToast("No hay productos registrados", "warning");
    }
  } catch (err) {
    console.error("Error cargando productos:", err);
    showToast("Error al cargar los productos", "error");
    products.value = [];
  }
};

const optimizeRoutes = async () => {
  const companyId = setupStore.company.value?.id;

  if (!companyId) {
    error.value = "No se encontro empresa activa";
    showToast("No se encontro empresa activa", "error");
    return;
  }

  if (!selectedProductId.value) {
    error.value = "Por favor selecciona un producto para optimizar";
    showToast("Por favor selecciona un producto para optimizar", "warning");
    return;
  }

  isLoading.value = true;
  error.value = null;

  try {
    const result = await routingAPI.optimizeFromCompany(
      companyId,
      costPerKm.value,
      selectedProductId.value,
    );

    if (result.success && result.data) {
      optimizationResult.value = result.data;
      showToast(
        `Optimizacion completada para el producto: ${optimizedProductName.value}`,
        "success",
      );
    } else {
      error.value = result.error || "Error en optimizacion";
      showToast(error.value, "error");
    }
  } catch (err) {
    console.error("Error:", err);
    error.value = err.message || "Error al optimizar rutas";
    showToast(error.value, "error");
  } finally {
    isLoading.value = false;
  }
};

const visualizeRoutesOnMap = () => {
  if (!optimizationResult.value || !optimizationResult.value.routes) {
    showToast("No hay rutas para visualizar", "warning");
    return;
  }

  const routes = optimizationResult.value.routes.map((route) => {
    const supplier = optimizationResult.value.suppliers_data.find(
      (s) => s.id === route.supplier_id,
    );
    const customer = optimizationResult.value.customers_data.find(
      (c) => c.id === route.customer_id,
    );

    return {
      supplier: {
        id: route.supplier_id,
        name: route.supplier_name,
        lat: supplier?.lat || 0,
        lng: supplier?.lng || 0,
      },
      customer: {
        id: route.customer_id,
        name: route.customer_name,
        lat: customer?.lat || 0,
        lng: customer?.lng || 0,
      },
      geometry: route.geometry,
      quantity: route.quantity,
      cost: route.cost,
      distance_km: route.distance_km,
    };
  });

  emit("visualize-routes", routes);
  handleBackToMap();
};

const downloadAnalysis = () => {
  if (!optimizationResult.value) return;

  const data = {
    timestamp: new Date().toISOString(),
    company: setupStore.company.value?.name,
    productId: selectedProductId.value,
    productName: optimizedProductName.value,
    totalCost: totalCost.value,
    totalDistance: totalDistance.value,
    allocations: allocationsCount.value,
    routes: optimizationResult.value.routes,
    costMatrix: optimizationResult.value.cost_matrix,
    suppliers: optimizationResult.value.suppliers_data,
    customers: optimizationResult.value.customers_data,
  };

  const json = JSON.stringify(data, null, 2);
  const blob = new Blob([json], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `optimizacion_${optimizedProductName.value}_${Date.now()}.json`;
  a.click();
  URL.revokeObjectURL(url);
};

const handleBackToMap = () => {
  emit("back-to-map");
};

onMounted(() => {
  loadProducts();
});
</script>

<style scoped>
.optimization-management {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #0a0f1a;
  color: #e8edf2;
}

.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.toast {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  border-radius: 8px;
  color: white;
  font-size: 14px;
  font-weight: 500;
  animation: slideIn 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  min-width: 280px;
}

.toast i {
  font-size: 18px;
}

.toast.success {
  background: linear-gradient(135deg, #10b981, #059669);
  border-left: 4px solid #34d399;
}

.toast.error {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  border-left: 4px solid #f87171;
}

.toast.warning {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  border-left: 4px solid #fbbf24;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.management-header {
  background: rgba(212, 163, 115, 0.1);
  border-bottom: 1px solid rgba(212, 163, 115, 0.2);
  padding: 1rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  flex-shrink: 0;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
}

.btn-back {
  background: rgba(212, 163, 115, 0.15);
  border: 1px solid rgba(212, 163, 115, 0.3);
  color: #d4a373;
  padding: 0.5rem 0.9rem;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-weight: 600;
  transition: all 0.3s ease;
  white-space: nowrap;
  flex-shrink: 0;
  font-size: 0.85rem;
}

.btn-back:hover {
  background: rgba(212, 163, 115, 0.25);
  border-color: rgba(212, 163, 115, 0.5);
}

.header-title h1 {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 700;
  color: #ffffff;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.header-title h1 i {
  color: #d4a373;
}

.header-title p {
  margin: 0.1rem 0 0;
  font-size: 0.8rem;
  color: #8fa3b3;
}

.header-stats {
  display: flex;
  gap: 1rem;
}

.stat-card {
  background: rgba(14, 18, 26, 0.5);
  border: 1px solid rgba(212, 163, 115, 0.2);
  border-radius: 8px;
  padding: 0.5rem 0.9rem;
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  min-width: 100px;
  text-align: center;
}

.stat-label {
  font-size: 0.7rem;
  color: #8fa3b3;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  font-weight: 600;
}

.stat-value {
  font-size: 1.2rem;
  color: #d4a373;
  font-weight: 700;
}

.cost-input-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.3rem;
}

.cost-input-header input {
  width: 60px;
  padding: 0.2rem 0.3rem;
  background: rgba(14, 18, 26, 0.5);
  border: 1px solid rgba(212, 163, 115, 0.3);
  border-radius: 4px;
  color: #d4a373;
  text-align: center;
  font-weight: 600;
}

.product-stat-card {
  min-width: 120px;
}

.product-select-header {
  background: rgba(14, 18, 26, 0.5);
  border: 1px solid rgba(212, 163, 115, 0.3);
  border-radius: 4px;
  color: #d4a373;
  padding: 0.2rem 0.3rem;
  font-weight: 600;
  cursor: pointer;
  text-align: center;
}

.product-select-header:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.optimize-card {
  background: linear-gradient(
    135deg,
    rgba(102, 126, 234, 0.2),
    rgba(118, 75, 162, 0.2)
  );
  border-color: rgba(102, 126, 234, 0.4);
}

.btn-optimize-header {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  gap: 0.4rem;
  justify-content: center;
}

.btn-optimize-header:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-optimize-header:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.management-content {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
}

.results-panel {
  background: rgba(14, 18, 26, 0.5);
  border-radius: 12px;
  border: 1px solid rgba(212, 163, 115, 0.2);
  overflow: hidden;
}

.panel-header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid rgba(212, 163, 115, 0.2);
  background: rgba(212, 163, 115, 0.08);
}

.panel-header h2 {
  margin: 0;
  font-size: 1rem;
  color: #d4a373;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.optimized-product-info {
  margin: 1rem 1.5rem 0 1.5rem;
  padding: 0.8rem 1rem;
  background: rgba(102, 126, 234, 0.15);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 0.8rem;
  font-size: 0.9rem;
}

.optimized-product-info i {
  color: #667eea;
  font-size: 1.1rem;
}

.optimized-product-info strong {
  color: #667eea;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  padding: 1.5rem;
  border-bottom: 1px solid rgba(212, 163, 115, 0.1);
}

.metric-card {
  background: rgba(212, 163, 115, 0.08);
  border: 1px solid rgba(212, 163, 115, 0.15);
  border-radius: 8px;
  padding: 1rem;
  text-align: center;
}

.metric-value {
  font-size: 1.8rem;
  font-weight: bold;
  color: #d4a373;
  margin-bottom: 0.3rem;
}

.metric-label {
  font-size: 0.7rem;
  color: #8fa3b3;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.supply-demand-summary {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  padding: 1.5rem;
  border-bottom: 1px solid rgba(212, 163, 115, 0.1);
}

.summary-box {
  background: rgba(212, 163, 115, 0.08);
  border: 1px solid rgba(212, 163, 115, 0.15);
  border-radius: 8px;
  padding: 1rem;
}

.summary-box h4 {
  margin: 0 0 1rem 0;
  font-size: 0.85rem;
  color: #d4a373;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.supply-item,
.demand-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(212, 163, 115, 0.1);
  font-size: 0.8rem;
}

.total-supply,
.total-demand {
  display: flex;
  justify-content: space-between;
  padding: 0.8rem 0;
  margin-top: 0.5rem;
  border-top: 2px solid rgba(212, 163, 115, 0.2);
  font-weight: 600;
  color: #d4a373;
}

.analysis-section {
  padding: 1.5rem;
}

.analysis-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid rgba(212, 163, 115, 0.2);
}

.tab-btn {
  padding: 0.6rem 1.2rem;
  border: none;
  background: none;
  cursor: pointer;
  color: #8fa3b3;
  font-weight: 600;
  font-size: 0.85rem;
  border-bottom: 2px solid transparent;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.tab-btn.active {
  color: #d4a373;
  border-bottom-color: #d4a373;
}

.routes-container {
  max-height: 400px;
  overflow-y: auto;
}

.route-item {
  background: rgba(212, 163, 115, 0.08);
  border: 1px solid rgba(212, 163, 115, 0.15);
  border-radius: 8px;
  padding: 0.8rem;
  margin-bottom: 0.8rem;
}

.route-header {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  margin-bottom: 0.5rem;
  font-size: 0.85rem;
}

.route-number {
  background: #d4a373;
  color: #0a0f1a;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  font-weight: bold;
}

.supplier-name,
.customer-name {
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.arrow {
  color: #d4a373;
  font-size: 0.7rem;
}

.route-details {
  display: flex;
  gap: 1rem;
  font-size: 0.7rem;
  color: #8fa3b3;
  padding-left: 2rem;
  flex-wrap: wrap;
}

.quantity,
.distance,
.unit-cost,
.cost {
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.matrix-container {
  max-height: 500px;
  overflow: auto;
}

.table-wrapper {
  overflow-x: auto;
}

.cost-matrix-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.75rem;
}

.cost-matrix-table th {
  background: rgba(212, 163, 115, 0.15);
  padding: 0.6rem;
  text-align: left;
  font-weight: 600;
  color: #d4a373;
  border-bottom: 1px solid rgba(212, 163, 115, 0.2);
}

.cost-matrix-table td {
  padding: 0.6rem;
  border-bottom: 1px solid rgba(212, 163, 115, 0.1);
}

.supplier-cell {
  font-weight: 600;
  background: rgba(212, 163, 115, 0.08);
  white-space: nowrap;
}

.stock-badge,
.demand-badge {
  font-size: 0.65rem;
  padding: 0.1rem 0.3rem;
  border-radius: 10px;
  margin-left: 0.4rem;
}

.stock-badge {
  background: rgba(212, 163, 115, 0.2);
  color: #d4a373;
}

.demand-badge {
  background: rgba(102, 126, 234, 0.2);
  color: #667eea;
}

.customer-name-cell {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  min-width: 80px;
}

.cost-cell {
  text-align: right;
  color: #8fa3b3;
}

.cost-cell.best-cost {
  background: rgba(212, 163, 115, 0.2);
  color: #d4a373;
  font-weight: bold;
}

.matrix-legend {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
  padding: 0.8rem;
  background: rgba(212, 163, 115, 0.08);
  border-radius: 8px;
  font-size: 0.7rem;
  flex-wrap: wrap;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: 3px;
}

.legend-color.best-cost {
  background: rgba(212, 163, 115, 0.2);
  border: 1px solid #d4a373;
}

.legend-color.zero-cost {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid #ef4444;
}

.assignments-container {
  max-height: 400px;
  overflow-y: auto;
}

.assignments-info {
  display: flex;
  gap: 1rem;
  padding: 0.8rem;
  background: rgba(212, 163, 115, 0.08);
  border-radius: 8px;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.75rem;
  color: #8fa3b3;
}

.assignments-details {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.assignment-item {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.6rem;
  background: rgba(212, 163, 115, 0.08);
  border: 1px solid rgba(212, 163, 115, 0.15);
  border-radius: 6px;
  font-size: 0.75rem;
  flex-wrap: wrap;
}

.assignment-number {
  background: #d4a373;
  color: #0a0f1a;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.65rem;
  font-weight: bold;
}

.supplier,
.customer {
  flex: 1;
}

.arrow-icon {
  color: #d4a373;
  font-size: 0.7rem;
}

.quantity-badge {
  background: #667eea;
  color: white;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-weight: 600;
  font-size: 0.7rem;
}

.cost-badge {
  background: rgba(212, 163, 115, 0.2);
  color: #d4a373;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-weight: 600;
  font-size: 0.7rem;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
  padding: 1rem 1.5rem 1.5rem 1.5rem;
  border-top: 1px solid rgba(212, 163, 115, 0.1);
}

.btn-visualize,
.btn-download {
  flex: 1;
  padding: 0.8rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  font-size: 0.85rem;
}

.btn-visualize {
  background: rgba(52, 152, 219, 0.2);
  color: #3498db;
  border: 1px solid rgba(52, 152, 219, 0.3);
}

.btn-visualize:hover {
  background: rgba(52, 152, 219, 0.3);
  border-color: rgba(52, 152, 219, 0.5);
}

.btn-download {
  background: rgba(46, 204, 113, 0.2);
  color: #2ecc71;
  border: 1px solid rgba(46, 204, 113, 0.3);
}

.btn-download:hover {
  background: rgba(46, 204, 113, 0.3);
  border-color: rgba(46, 204, 113, 0.5);
}

.loading-state,
.no-data-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  color: #8fa3b3;
  text-align: center;
  gap: 0.8rem;
}

.loading-state i,
.no-data-state i,
.error-state i {
  font-size: 3rem;
  opacity: 0.5;
}

.error-state {
  background: rgba(239, 68, 68, 0.1);
  border-radius: 12px;
  border: 1px solid rgba(239, 68, 68, 0.3);
  position: relative;
}

.btn-close-error {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  color: #ef4444;
  cursor: pointer;
  font-size: 1rem;
}

@media (max-width: 1024px) {
  .management-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .header-stats {
    width: 100%;
    justify-content: space-between;
    flex-wrap: wrap;
  }

  .metrics-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .supply-demand-summary {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .management-content {
    padding: 1rem;
  }

  .metrics-grid {
    grid-template-columns: 1fr;
  }

  .header-stats {
    flex-wrap: wrap;
  }

  .stat-card {
    min-width: calc(50% - 0.5rem);
  }

  .analysis-tabs {
    flex-wrap: wrap;
  }

  .action-buttons {
    flex-direction: column;
  }
}
</style>
