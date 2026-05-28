<template>
  <div class="client-dashboard">
    <NavbarWidget />

    <div class="dashboard-content">
      <!-- Sidebar con búsqueda -->
      <aside class="client-sidebar">
        <div class="sidebar-header">
          <h2><i class="fas fa-shopping-cart"></i> Buscar Producto</h2>
        </div>

        <div class="search-section">
          <div class="search-box">
            <i class="fas fa-search"></i>
            <input 
              v-model="searchQuery"
              type="text"
              placeholder="Buscar producto..."
              class="search-input"
            />
          </div>
        </div>

        <!-- Empresas disponibles -->
        <div v-if="selectedProduct" class="companies-section">
          <h3 class="section-title">
            <i class="fas fa-building"></i> Empresas disponibles
          </h3>
          <div class="companies-list">
            <div 
              v-for="company in availableCompanies"
              :key="company.id"
              class="company-card"
              :class="{ 'selected': selectedCompany?.id === company.id }"
              @click="selectCompany(company)"
            >
              <div class="company-header">
                <i class="fas fa-warehouse"></i>
                <h4>{{ company.name }}</h4>
              </div>
              <div class="company-info">
                <p class="product-detail">
                  <i class="fas fa-box"></i>
                  {{ selectedProduct.name }}
                </p>
                <p class="price-detail">
                  <i class="fas fa-tag"></i>
                  {{ selectedProduct.price }} Bs/{{ selectedProduct.unit }}
                </p>
              </div>
              <div v-if="getMaterialQuantity(company.id)" class="quantity-badge">
                {{ getMaterialQuantity(company.id) }} disponibles
              </div>
            </div>

            <div v-if="availableCompanies.length === 0" class="empty-state">
              <i class="fas fa-inbox"></i>
              <p>No hay empresas con este producto</p>
            </div>
          </div>
        </div>

        <div v-else class="no-selection">
          <i class="fas fa-info-circle"></i>
          <p>Busca un producto para ver empresas disponibles</p>
        </div>
      </aside>

      <!-- Mapa para seleccionar ubicación -->
      <main class="map-section">
        <div v-if="!selectedCompany" class="map-placeholder">
          <i class="fas fa-map"></i>
          <p>Selecciona una empresa para indicar tu ubicación de entrega</p>
        </div>

        <div v-else class="location-selector">
          <div class="location-header">
            <h3>{{ selectedCompany.name }}</h3>
            <p>Selecciona tu ubicación de entrega</p>
          </div>

          <div class="map-container" id="clientMap"></div>

          <div class="location-options">
            <button class="btn-location current" @click="useCurrentLocation">
              <i class="fas fa-location-dot"></i> Usar ubicación actual
            </button>
            <button class="btn-location map" disabled>
              <i class="fas fa-map-pin"></i> Haz click en el mapa
            </button>
          </div>

          <div v-if="selectedDeliveryLocation" class="order-summary">
            <h4>Resumen del pedido</h4>
            <div class="summary-item">
              <span>Empresa:</span>
              <strong>{{ selectedCompany.name }}</strong>
            </div>
            <div class="summary-item">
              <span>Producto:</span>
              <strong>{{ selectedProduct.name }}</strong>
            </div>
            <div class="summary-item">
              <span>Ubicación:</span>
              <strong>{{ selectedDeliveryLocation.lat.toFixed(4) }}, {{ selectedDeliveryLocation.lng.toFixed(4) }}</strong>
            </div>
            <button class="btn-confirm" @click="confirmOrder">
              <i class="fas fa-check"></i> Confirmar Pedido
            </button>
          </div>
        </div>
      </main>
    </div>

    <!-- Toast message -->
    <div v-if="message" :class="['message-toast', { error: message.isError }]">
      <i :class="['fas', message.isError ? 'fa-exclamation-triangle' : 'fa-check-circle']"></i>
      {{ message.text }}
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useSetupStore } from '@/pages/setup/composables/useSetupStore';
import { NavbarWidget } from '@/widgets';
import L from 'leaflet';

const setupStore = useSetupStore();
const searchQuery = ref('');
const selectedProduct = ref(null);
const selectedCompany = ref(null);
const selectedDeliveryLocation = ref(null);
const message = ref(null);
let clientMap = null;
let deliveryMarker = null;

// Obtener productos configurados por las empresas (simulado)
const allProducts = computed(() => {
  return setupStore.products || [];
});

// Buscar productos que coincidan con la búsqueda
const filteredProducts = computed(() => {
  if (!searchQuery.value) return [];
  return allProducts.value.filter(p =>
    p.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

// Obtener empresas disponibles (simulado - en producción sería desde API)
const availableCompanies = computed(() => {
  if (!selectedProduct.value) return [];
  
  // Simular empresas que tienen el producto
  return [
    {
      id: 1,
      name: 'Logística Integral',
      materials: [
        { productId: selectedProduct.value.id, quantity: 100 }
      ]
    },
    {
      id: 2,
      name: 'Distribuidora Central',
      materials: [
        { productId: selectedProduct.value.id, quantity: 75 }
      ]
    },
    {
      id: 3,
      name: 'TransLogístico S.A.',
      materials: [
        { productId: selectedProduct.value.id, quantity: 150 }
      ]
    }
  ];
});

const getMaterialQuantity = (companyId) => {
  const company = availableCompanies.value.find(c => c.id === companyId);
  if (!company || !selectedProduct.value) return 0;
  
  const material = company.materials.find(m => m.productId === selectedProduct.value.id);
  return material ? material.quantity : 0;
};

const showMessage = (text, isError = false) => {
  message.value = { text, isError };
  setTimeout(() => {
    message.value = null;
  }, 3500);
};

const selectProduct = (product) => {
  selectedProduct.value = product;
  selectedCompany.value = null;
  selectedDeliveryLocation.value = null;
  if (deliveryMarker) {
    clientMap.removeLayer(deliveryMarker);
    deliveryMarker = null;
  }
};

const selectCompany = (company) => {
  selectedCompany.value = company;
  selectedDeliveryLocation.value = null;
  
  // Inicializar mapa
  setTimeout(() => {
    initializeMap();
  }, 100);
};

const initializeMap = () => {
  if (clientMap) {
    clientMap.remove();
  }

  const defaultLat = -16.5;
  const defaultLng = -68.15;

  clientMap = L.map('clientMap').setView([defaultLat, defaultLng], 13);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19
  }).addTo(clientMap);

  // Click en mapa para seleccionar ubicación
  clientMap.on('click', (e) => {
    const lat = e.latlng.lat;
    const lng = e.latlng.lng;
    setDeliveryLocation(lat, lng);
  });
};

const setDeliveryLocation = (lat, lng) => {
  selectedDeliveryLocation.value = { lat, lng };

  if (deliveryMarker) {
    clientMap.removeLayer(deliveryMarker);
  }

  deliveryMarker = L.marker([lat, lng], {
    icon: L.icon({
      iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34]
    })
  }).addTo(clientMap).bindPopup('Ubicación de entrega');

  clientMap.setView([lat, lng], 15);
};

const useCurrentLocation = () => {
  if (!navigator.geolocation) {
    showMessage('Geolocalización no soportada en este navegador', true);
    return;
  }

  navigator.geolocation.getCurrentPosition(
    (position) => {
      const { latitude, longitude } = position.coords;
      setDeliveryLocation(latitude, longitude);
      showMessage('✅ Ubicación actual establecida');
    },
    (error) => {
      showMessage(`❌ Error al obtener ubicación: ${error.message}`, true);
    }
  );
};

const confirmOrder = () => {
  showMessage(`✅ Pedido confirmado. Se procesará tu solicitud de ${selectedProduct.value.name}`);
  
  setTimeout(() => {
    // Aquí se podría guardar el pedido y redirigir
    selectedCompany.value = null;
    selectedProduct.value = null;
    selectedDeliveryLocation.value = null;
    if (deliveryMarker && clientMap) {
      clientMap.removeLayer(deliveryMarker);
      deliveryMarker = null;
    }
    searchQuery.value = '';
  }, 1500);
};

onMounted(() => {
  // Aplicar búsqueda rápida si hay
  const queryParams = new URLSearchParams(window.location.search);
  const productSearch = queryParams.get('product');
  if (productSearch) {
    searchQuery.value = productSearch;
  }
});

// Watcher para búsqueda de producto
const handleProductSearch = () => {
  const results = filteredProducts.value;
  if (results.length === 1) {
    selectProduct(results[0]);
  }
};

// Exponemos para template
const getSearchResults = computed(() => {
  return filteredProducts.value;
});
</script>

<style scoped>
.client-dashboard {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #0a0f1a;
  overflow: hidden;
}

.dashboard-content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* Sidebar */
.client-sidebar {
  width: 320px;
  background: linear-gradient(180deg, rgba(10, 15, 26, 0.95) 0%, rgba(20, 28, 40, 0.92) 100%);
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

.sidebar-header h2 {
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

.search-section {
  margin-bottom: 1.5rem;
}

.search-box {
  position: relative;
  display: flex;
  align-items: center;
}

.search-box i {
  position: absolute;
  left: 0.8rem;
  color: #d4a373;
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 0.7rem 0.8rem 0.7rem 2.3rem;
  background: rgba(10, 15, 26, 0.6);
  border: 1px solid rgba(212, 163, 115, 0.3);
  border-radius: 0.75rem;
  color: #e8edf2;
  font-size: 0.85rem;
}

.search-input:focus {
  outline: none;
  border-color: #d4a373;
  box-shadow: 0 0 0 3px rgba(212, 163, 115, 0.1);
}

.search-input::placeholder {
  color: #5a6678;
}

.section-title {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #d4a373;
  margin: 1rem 0 0.75rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
}

.companies-section {
  flex: 1;
  overflow-y: auto;
}

.companies-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.company-card {
  background: rgba(212, 163, 115, 0.08);
  border: 1px solid rgba(212, 163, 115, 0.15);
  border-radius: 0.75rem;
  padding: 0.75rem;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.company-card:hover {
  background: rgba(212, 163, 115, 0.12);
  border-color: rgba(212, 163, 115, 0.3);
}

.company-card.selected {
  background: rgba(212, 163, 115, 0.25);
  border-color: #d4a373;
  box-shadow: 0 0 12px rgba(212, 163, 115, 0.2);
}

.company-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.company-header i {
  color: #d4a373;
  font-size: 0.9rem;
}

.company-header h4 {
  margin: 0;
  font-size: 0.8rem;
  font-weight: 600;
  color: #ffffff;
}

.company-info {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.company-info p {
  margin: 0;
  font-size: 0.7rem;
  color: #8fa3b3;
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.company-info i {
  color: #d4a373;
}

.quantity-badge {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: #d4a373;
  color: #0a0f1a;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.65rem;
  font-weight: 700;
}

.empty-state,
.no-selection {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  color: #8fa3b3;
  text-align: center;
  gap: 0.5rem;
}

.empty-state i,
.no-selection i {
  font-size: 2rem;
  opacity: 0.5;
}

.empty-state p,
.no-selection p {
  margin: 0;
  font-size: 0.85rem;
}

/* Main Map Section */
.map-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: #0a0f1a;
}

.map-placeholder {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #8fa3b3;
  gap: 1rem;
}

.map-placeholder i {
  font-size: 3rem;
  opacity: 0.3;
}

.location-selector {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.location-header {
  padding: 1rem 1.5rem;
  background: rgba(212, 163, 115, 0.1);
  border-bottom: 1px solid rgba(212, 163, 115, 0.15);
  flex-shrink: 0;
}

.location-header h3 {
  margin: 0;
  font-size: 1rem;
  color: #ffffff;
}

.location-header p {
  margin: 0.25rem 0 0;
  font-size: 0.8rem;
  color: #8fa3b3;
}

#clientMap {
  flex: 1;
  background: #1a2332;
}

.location-options {
  display: flex;
  gap: 0.75rem;
  padding: 1rem;
  background: rgba(212, 163, 115, 0.08);
  border-top: 1px solid rgba(212, 163, 115, 0.15);
  flex-shrink: 0;
}

.btn-location {
  flex: 1;
  padding: 0.7rem;
  border: 1px solid rgba(212, 163, 115, 0.3);
  border-radius: 0.6rem;
  background: rgba(212, 163, 115, 0.12);
  color: #d4a373;
  font-weight: 600;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
}

.btn-location:hover:not(:disabled) {
  background: rgba(212, 163, 115, 0.2);
  border-color: rgba(212, 163, 115, 0.5);
}

.btn-location:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.order-summary {
  padding: 1rem;
  background: rgba(212, 163, 115, 0.15);
  border-top: 1px solid rgba(212, 163, 115, 0.3);
  flex-shrink: 0;
}

.order-summary h4 {
  margin: 0 0 0.75rem;
  font-size: 0.8rem;
  color: #d4a373;
  text-transform: uppercase;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  margin-bottom: 0.5rem;
  color: #e8edf2;
}

.summary-item span {
  color: #8fa3b3;
}

.btn-confirm {
  width: 100%;
  margin-top: 0.75rem;
  padding: 0.7rem;
  background: #d4a373;
  border: none;
  border-radius: 0.6rem;
  color: #0a0f1a;
  font-weight: 700;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
}

.btn-confirm:hover {
  background: #e0b082;
  transform: translateY(-2px);
}

/* Messages */
.message-toast {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  background: #1e2a3a;
  border-left: 4px solid #d4a373;
  padding: 1rem 1.5rem;
  border-radius: 0.8rem;
  color: #e8edf2;
  font-size: 0.85rem;
  z-index: 2000;
  backdrop-filter: blur(8px);
  animation: slideInRight 0.3s ease;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.message-toast.error {
  border-left-color: #e06c6c;
}

.message-toast i {
  flex-shrink: 0;
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

@media (max-width: 1024px) {
  .client-sidebar {
    width: 280px;
  }
}

@media (max-width: 768px) {
  .dashboard-content {
    flex-direction: column;
  }

  .client-sidebar {
    width: 100%;
    max-height: 40%;
    border-right: none;
    border-bottom: 1px solid rgba(212, 163, 115, 0.15);
  }

  .map-section {
    flex: 1;
  }
}
</style>
