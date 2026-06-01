<template>
  <div class="routing-optimization-container">
    <div class="optimization-header">
      <h3>Optimizacion de Rutas</h3>
      <button 
        class="btn-optimize"
        @click="optimizeRoutes"
        :disabled="isLoading || !hasData"
      >
        <i v-if="isLoading" class="fas fa-spinner fa-spin"></i>
        <i v-else class="fas fa-rocket"></i>
        {{ isLoading ? 'Optimizando...' : 'Optimizar Rutas' }}
      </button>
    </div>

    <div v-if="hasData" class="data-summary">
      <div class="summary-item">
        <span class="label">Sucursales:</span>
        <span class="value">{{ suppliersCount }}</span>
      </div>
      <div class="summary-item">
        <span class="label">Pedidos:</span>
        <span class="value">{{ customersCount }}</span>
      </div>
      <div class="summary-item">
        <span class="label">Costo/km:</span>
        <div class="cost-input">
          <input 
            v-model.number="costPerKm" 
            type="number" 
            step="0.1"
            min="0"
            class="input-cost"
          />
          <span>Bs</span>
        </div>
      </div>
    </div>

    <div v-if="!hasData && !isLoading" class="no-data-state">
      <i class="fas fa-info-circle"></i>
      <p>No hay sucursales o pedidos para optimizar</p>
      <small>Primero crea sucursales y registra pedidos de clientes</small>
    </div>

    <transition name="fade">
      <div v-if="optimizationResult && !isLoading" class="optimization-results">
        <div class="results-header">
          <h4>Optimizacion Completada</h4>
          <button class="btn-close-results" @click="clearResults">
            <i class="fas fa-times"></i>
          </button>
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
            <h6>Stock por Sucursal</h6>
            <div v-for="supplier in optimizationResult.suppliers_data" :key="supplier.id" class="supply-item">
              <span>{{ supplier.name }}</span>
              <strong>{{ supplier.total_stock }} und</strong>
            </div>
            <div class="total-supply">
              <span>Total Stock:</span>
              <strong>{{ totalStock }} und</strong>
            </div>
          </div>
          
          <div class="summary-box">
            <h6>Demanda por Pedido</h6>
            <div v-for="customer in optimizationResult.customers_data" :key="customer.id" class="demand-item">
              <span>{{ getShortName(customer.name) }}</span>
              <strong>{{ customer.total_demand }} und</strong>
            </div>
            <div class="total-demand">
              <span>Total Demanda:</span>
              <strong>{{ totalDemand }} und</strong>
            </div>
          </div>
        </div>

        <div class="analysis-section">
          <h5>Analisis Vogel + MODI</h5>
          
          <div class="analysis-tabs">
            <button 
              v-for="tab in ['rutas', 'matriz', 'asignaciones']"
              :key="tab"
              :class="['tab-btn', { active: activeTab === tab }]"
              @click="activeTab = tab"
            >
              {{ tabLabels[tab] }}
            </button>
          </div>

          <div v-show="activeTab === 'rutas'" class="tab-content routes-list">
            <div 
              v-for="(route, idx) in optimizationResult.routes"
              :key="idx"
              class="route-item"
              @click="focusRoute(route)"
            >
              <div class="route-header">
                <span class="route-number">{{ idx + 1 }}</span>
                <span class="supplier-name">{{ route.supplier_name }}</span>
                <span class="arrow">→</span>
                <span class="customer-name">{{ route.customer_name }}</span>
              </div>
              <div class="route-details">
                <span class="distance">
                  <i class="fas fa-road"></i> {{ route.distance_km.toFixed(2) }} km
                </span>
                <span class="cost">
                  <i class="fas fa-money-bill"></i> {{ route.cost.toFixed(2) }} Bs
                </span>
              </div>
            </div>
            <div v-if="optimizationResult.routes.length === 0" class="empty-routes">
              <p>No hay rutas asignadas</p>
            </div>
          </div>

          <div v-show="activeTab === 'matriz'" class="tab-content matrix-table">
            <div class="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>Sucursal / Pedido</th>
                    <th v-for="(customer, idx) in optimizationResult.customers_data" :key="customer.id">
                      <div class="customer-name-cell">
                        <strong>{{ getShortName(customer.name, 20) }}</strong>
                        <span class="demand-badge">({{ customer.total_demand }} und)</span>
                      </div>
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(supplier, i) in optimizationResult.suppliers_data" :key="supplier.id">
                    <td class="supplier-cell">
                      <strong>{{ supplier.name }}</strong>
                      <span class="stock-badge">({{ supplier.total_stock }} und)</span>
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
                <span>Menor costo por pedido</span>
              </div>
              <div class="legend-item">
                <span class="legend-color zero-cost"></span>
                <span>Costo cero (cliente ficticio)</span>
              </div>
            </div>
          </div>

          <div v-show="activeTab === 'asignaciones'" class="tab-content assignments-list">
            <div class="assignments-info">
              <p><strong>Solucion Vogel (VAM):</strong> {{ vogelAllocationsCount }} asignaciones</p>
              <p><strong>Solucion MODI:</strong> {{ modiAllocationsCount }} asignaciones</p>
              <p><strong>Optimo:</strong> {{ isOptimal ? 'Si' : 'No verificado' }}</p>
            </div>
            
            <div class="assignments-details">
              <div 
                v-for="(alloc, idx) in optimizationResult.routes"
                :key="idx"
                class="assignment-item"
              >
                <span class="supplier">{{ alloc.supplier_name }}</span>
                <span class="arrow">→</span>
                <span class="customer">{{ alloc.customer_name }}</span>
                <span class="quantity-badge">{{ getQuantity(alloc) }} und</span>
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
    </transition>

    <transition name="fade">
      <div v-if="error" class="error-message">
        <i class="fas fa-exclamation-circle"></i>
        <span>{{ error }}</span>
        <button class="btn-close-error" @click="error = null">
          <i class="fas fa-times"></i>
        </button>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { routingAPI, ordersAPI } from '@/services/api';
import { useSetupStore } from '@/pages/setup/composables/useSetupStore';

const setupStore = useSetupStore();
const isLoading = ref(false);
const error = ref(null);
const costPerKm = ref(5.5);
const optimizationResult = ref(null);
const activeTab = ref('rutas');

const tabLabels = {
  rutas: 'Rutas',
  matriz: 'Matriz Costos',
  asignaciones: 'Asignaciones'
};

const suppliersCount = ref(0);
const customersCount = ref(0);

const hasData = computed(() => suppliersCount.value > 0 && customersCount.value > 0);

const totalCost = computed(() => optimizationResult.value?.total_cost || 0);
const totalDistance = computed(() => optimizationResult.value?.total_distance_km || 0);
const allocationsCount = computed(() => optimizationResult.value?.total_allocations || 0);
const averageCost = computed(() => {
  if (allocationsCount.value === 0) return 0;
  return totalCost.value / allocationsCount.value;
});

const totalStock = computed(() => {
  if (!optimizationResult.value) return 0;
  return optimizationResult.value.suppliers_data.reduce((sum, s) => sum + (s.total_stock || 0), 0);
});

const totalDemand = computed(() => {
  if (!optimizationResult.value) return 0;
  return optimizationResult.value.customers_data.reduce((sum, c) => sum + (c.total_demand || 0), 0);
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

const getShortName = (name, maxLength = 15) => {
  if (!name) return 'Sin nombre';
  if (name.length <= maxLength) return name;
  return name.substring(0, maxLength) + '...';
};

const getQuantity = (alloc) => {
  if (alloc.quantity) return alloc.quantity;
  const route = optimizationResult.value?.routes?.find(r => 
    r.supplier_id === alloc.supplier_id && r.customer_id === alloc.customer_id
  );
  return route?.quantity || 0;
};

const isBestCost = (supplierIdx, customerIdx) => {
  const matrix = optimizationResult.value?.cost_matrix;
  if (!matrix || matrix.length === 0) return false;
  
  const column = matrix.map(row => row[customerIdx]);
  const minCost = Math.min(...column);
  const currentCost = matrix[supplierIdx][customerIdx];
  
  return currentCost === minCost && currentCost > 0;
};

const optimizeRoutes = async () => {
  const companyId = setupStore.company.value?.id;
  
  if (!companyId) {
    error.value = 'No se encontró empresa activa';
    return;
  }

  isLoading.value = true;
  error.value = null;

  try {
    const ordersResponse = await ordersAPI.getByCompany(companyId);
    let productIdToUse = null;
    
    if (ordersResponse && ordersResponse.success && ordersResponse.data && ordersResponse.data.length > 0) {
      productIdToUse = ordersResponse.data[0].product_id || null;
      console.log('Product ID extraído de órdenes:', productIdToUse);
    } else {
      console.warn('No se encontraron órdenes para extraer product_id');
    }
    
    const result = await routingAPI.optimizeFromCompany(companyId, costPerKm.value, productIdToUse);
    
    if (result.success && result.data) {
      optimizationResult.value = result.data;
    } else {
      error.value = result.error || 'Error desconocido en optimizacion';
    }
  } catch (err) {
    console.error('Error:', err);
    error.value = err.message || 'Error al optimizar rutas';
  } finally {
    isLoading.value = false;
  }
};

const clearResults = () => {
  optimizationResult.value = null;
  activeTab.value = 'rutas';
};

const focusRoute = (route) => {
  console.log('Enfocando ruta:', route);
};

const visualizeRoutesOnMap = () => {
  console.log('Visualizando rutas en mapa');
};

const downloadAnalysis = () => {
  if (!optimizationResult.value) return;

  const data = {
    timestamp: new Date().toISOString(),
    company: setupStore.company.value?.name,
    totalCost: totalCost.value,
    totalDistance: totalDistance.value,
    routes: optimizationResult.value.routes,
    costMatrix: optimizationResult.value.cost_matrix,
    suppliers: optimizationResult.value.suppliers_data,
    customers: optimizationResult.value.customers_data
  };

  const json = JSON.stringify(data, null, 2);
  const blob = new Blob([json], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `optimizacion_${Date.now()}.json`;
  a.click();
  URL.revokeObjectURL(url);
};

onMounted(async () => {
  suppliersCount.value = 3;
  customersCount.value = 5;
});
</script>

<style scoped>
.routing-optimization-container {
  background: white;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.optimization-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #f0f0f0;
}

.optimization-header h3 {
  font-size: 18px;
  color: #1a1a1a;
  margin: 0;
}

.btn-optimize {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-optimize:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-optimize:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.data-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: #f9f9f9;
  border-radius: 8px;
  border-left: 3px solid #667eea;
}

.summary-item .label {
  font-weight: 600;
  color: #555;
  font-size: 14px;
}

.summary-item .value {
  font-size: 20px;
  font-weight: bold;
  color: #667eea;
}

.cost-input {
  display: flex;
  align-items: center;
  gap: 8px;
}

.input-cost {
  width: 80px;
  padding: 6px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-weight: 600;
}

.no-data-state {
  text-align: center;
  padding: 40px 20px;
  color: #999;
}

.no-data-state i {
  font-size: 48px;
  margin-bottom: 10px;
  opacity: 0.5;
}

.no-data-state p {
  margin: 10px 0;
  font-weight: 600;
}

.no-data-state small {
  color: #bbb;
}

.optimization-results {
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  padding: 20px;
  background: #fafafa;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.results-header h4 {
  margin: 0;
  color: #27ae60;
  font-size: 16px;
}

.btn-close-results {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: #999;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
  margin-bottom: 30px;
}

.metric-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  border: 1px solid #e0e0e0;
  transition: all 0.3s ease;
}

.metric-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.metric-value {
  font-size: 28px;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 8px;
}

.metric-label {
  font-size: 12px;
  color: #666;
  font-weight: 500;
}

.supply-demand-summary {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 30px;
}

.summary-box {
  background: white;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
}

.summary-box h6 {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: #333;
  border-left: 3px solid #667eea;
  padding-left: 10px;
}

.supply-item, .demand-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
  font-size: 13px;
}

.total-supply, .total-demand {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  margin-top: 8px;
  border-top: 2px solid #e0e0e0;
  font-weight: 600;
  color: #667eea;
}

.analysis-section {
  margin-top: 25px;
}

.analysis-section h5 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 14px;
}

.analysis-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
  border-bottom: 2px solid #e0e0e0;
}

.tab-btn {
  padding: 10px 15px;
  border: none;
  background: none;
  cursor: pointer;
  color: #999;
  font-weight: 500;
  font-size: 14px;
  border-bottom: 2px solid transparent;
  transition: all 0.3s ease;
}

.tab-btn.active {
  color: #667eea;
  border-bottom-color: #667eea;
}

.tab-content {
  background: white;
  padding: 15px;
  border-radius: 6px;
}

.routes-list {
  max-height: 400px;
  overflow-y: auto;
}

.route-item {
  padding: 12px;
  margin-bottom: 10px;
  background: #f9f9f9;
  border-radius: 6px;
  border-left: 3px solid #667eea;
  cursor: pointer;
  transition: all 0.3s ease;
}

.route-item:hover {
  background: #f0f0f0;
  transform: translateX(4px);
}

.route-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  font-weight: 500;
  font-size: 13px;
}

.route-number {
  background: #667eea;
  color: white;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: bold;
}

.supplier-name {
  flex: 0 0 auto;
}

.arrow {
  color: #999;
}

.customer-name {
  flex: 1;
  text-align: right;
}

.route-details {
  display: flex;
  gap: 15px;
  font-size: 12px;
  color: #666;
}

.distance, .cost {
  display: flex;
  align-items: center;
  gap: 4px;
}

.empty-routes {
  text-align: center;
  padding: 40px;
  color: #999;
}

.matrix-table {
  max-height: 500px;
  overflow: auto;
}

.table-wrapper {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
  min-width: 600px;
}

table th {
  background: #f0f0f0;
  padding: 12px;
  text-align: left;
  font-weight: 600;
  border-bottom: 2px solid #ddd;
}

table td {
  padding: 10px;
  border-bottom: 1px solid #eee;
}

.supplier-cell {
  font-weight: 600;
  background: #f9f9f9;
  white-space: nowrap;
}

.stock-badge {
  font-size: 10px;
  color: #666;
  margin-left: 5px;
  font-weight: normal;
}

.cost-cell {
  text-align: right;
  color: #667eea;
  font-weight: 500;
}

.cost-cell.best-cost {
  background: #e8f5e9;
  color: #2e7d32;
  font-weight: bold;
}

.customer-name-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 100px;
}

.demand-badge {
  font-size: 10px;
  background: #e8f5e9;
  color: #2e7d32;
  padding: 2px 6px;
  border-radius: 10px;
  display: inline-block;
  text-align: center;
}

.matrix-legend {
  display: flex;
  gap: 20px;
  margin-top: 15px;
  padding: 10px;
  background: #f9f9f9;
  border-radius: 6px;
  font-size: 11px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: 3px;
}

.legend-color.best-cost {
  background: #e8f5e9;
  border: 1px solid #2e7d32;
}

.legend-color.zero-cost {
  background: #fff3e0;
  border: 1px solid #f57c00;
}

.assignments-list {
  max-height: 400px;
  overflow-y: auto;
}

.assignments-info {
  background: #f0f7ff;
  padding: 12px;
  border-radius: 6px;
  margin-bottom: 15px;
  font-size: 13px;
  color: #333;
}

.assignments-info p {
  margin: 6px 0;
}

.assignments-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.assignment-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background: white;
  border-radius: 4px;
  font-size: 12px;
}

.supplier, .customer {
  flex: 1;
}

.quantity-badge {
  background: #667eea;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: 600;
  font-size: 11px;
}

.cost-badge {
  background: #27ae60;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: 600;
  font-size: 11px;
}

.action-buttons {
  display: flex;
  gap: 10px;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #e0e0e0;
}

.btn-visualize, .btn-download {
  flex: 1;
  padding: 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.btn-visualize {
  background: #3498db;
  color: white;
}

.btn-visualize:hover {
  background: #2980b9;
}

.btn-download {
  background: #27ae60;
  color: white;
}

.btn-download:hover {
  background: #229954;
}

.error-message {
  background: #fee;
  color: #c33;
  padding: 15px;
  border-radius: 6px;
  margin-top: 15px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.error-message i {
  font-size: 18px;
}

.btn-close-error {
  margin-left: auto;
  background: none;
  border: none;
  color: #c33;
  cursor: pointer;
  font-size: 18px;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>