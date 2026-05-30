<template>
  <div class="client-dashboard">
    <NavbarWidget />

    <div class="dashboard-content">
      <ClientSidebarWidget 
        :userOrders="userOrders"
        @product-selected="handleProductSelected"
        @company-selected="handleCompanySelected"
        @new-order="handleNewOrder"
        @focus-order="focusOnOrder"
      />

      <main class="map-section">
        <div class="map-wrapper">
          <MapContainer 
            ref="mapRef"
            class="client-map"
            :isConnectionModeActive="false"
            :locationTypes="[]"
            @map-click="handleMapClick"
          />

          <div v-if="showOrderHistory && userOrders.length > 0" class="order-history-overlay">
            <h4><i class="fas fa-history"></i> Historial de Pedidos</h4>
            <div class="orders-list">
              <div 
                v-for="order in userOrders"
                :key="order.id"
                class="order-item"
                @click="focusOnOrder(order)"
              >
                <span class="order-company">{{ order.company_name }}</span>
                <span class="order-product">{{ order.product_name }} ({{order.quantity}})</span>
                <span class="order-date">{{ formatDate(order.created_at) }}</span>
              </div>
            </div>
          </div>

          <div v-if="!selectedCompany" class="map-overlay-message">
            <div class="overlay-content">
              <i class="fas fa-map-marker-alt"></i>
              <p>Selecciona una empresa del sidebar para comenzar</p>
            </div>
          </div>
        </div>

        <div v-if="selectedCompany" class="order-panel">
          <div class="order-panel-header">
            <h3>{{ selectedCompany.company_name }}</h3>
            <button class="btn-close-panel" @click="cancelOrder">
              <i class="fas fa-times"></i>
            </button>
          </div>

          <div class="order-panel-body">
            <div class="product-info">
              <span class="product-name">{{ selectedProduct.name }}</span>
              <span class="product-price">{{ selectedProduct.price }} Bs/{{ selectedProduct.units }}</span>
            </div>

            <div v-if="!selectedDeliveryLocation" class="location-prompt">
              <button class="btn-location current" @click="useCurrentLocation">
                <i class="fas fa-location-dot"></i> Usar mi ubicación actual
              </button>
              <p class="map-hint">o haz clic en el mapa para seleccionar ubicación</p>
            </div>

            <div v-if="selectedDeliveryLocation" class="order-summary">
              <div class="quantity-section">
                <label>Cantidad disponible: {{ selectedCompany.available_stock }}</label>
                <div class="quantity-input">
                  <button @click="decrementQuantity" :disabled="orderQuantity <= 1" class="qty-btn">-</button>
                  <input 
                    v-model.number="orderQuantity" 
                    type="number"
                    min="1"
                    :max="selectedCompany.available_stock"
                    class="qty-input"
                  />
                  <button @click="incrementQuantity" :disabled="orderQuantity >= selectedCompany.available_stock" class="qty-btn">+</button>
                </div>
              </div>

              <div class="summary-item">
                <span>Subtotal:</span>
                <strong>{{ (selectedProduct.price * orderQuantity).toFixed(2) }} Bs</strong>
              </div>

              <div class="summary-item location">
                <span>Ubicación:</span>
                <span class="location-coords">{{ selectedDeliveryLocation.lat.toFixed(4) }}, {{ selectedDeliveryLocation.lng.toFixed(4) }}</span>
              </div>

              <div class="order-actions">
                <button class="btn-confirm" @click="confirmOrder" :disabled="isConfirming">
                  <i v-if="isConfirming" class="fas fa-spinner fa-spin"></i>
                  <i v-else class="fas fa-check"></i>
                  {{ isConfirming ? 'Enviando...' : 'Confirmar Pedido' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>

    <div v-if="message" :class="['message-toast', { error: message.isError }]">
      <i :class="['fas', message.isError ? 'fa-exclamation-triangle' : 'fa-check-circle']"></i>
      {{ message.text }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue';
import { NavbarWidget, ClientSidebarWidget } from '@/widgets';
import { MapContainer } from '@/Features/map';
import { ordersAPI } from '@/services/api';
import L from 'leaflet';

const mapRef = ref(null);
const selectedProduct = ref(null);
const selectedCompany = ref(null);
const selectedDeliveryLocation = ref(null);
const orderQuantity = ref(1);
const isConfirming = ref(false);
const message = ref(null);
const userOrders = ref([]);
const showOrderHistory = ref(true);
let deliveryMarker = null;
let orderMarkers = [];
let mapInstance = null;

const currentUserData = JSON.parse(sessionStorage.getItem("currentUserData") || "{}");
const userId = currentUserData.userId;

const showMessage = (text, isError = false) => {
  message.value = { text, isError };
  setTimeout(() => {
    message.value = null;
  }, 3500);
};

const formatDate = (dateString) => {
  try {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', { month: 'short', day: 'numeric' });
  } catch {
    return dateString;
  }
};

const loadUserOrders = async () => {
  if (!userId) return;
  
  try {
    const result = await ordersAPI.getByUser(userId);
    if (result.success) {
      userOrders.value = result.data;
      drawOrderMarkers();
    }
  } catch (error) {
    console.error('Error al cargar órdenes:', error);
  }
};


const drawOrderMarkers = () => {
  if (!mapInstance) return;
  
  orderMarkers.forEach(marker => mapInstance.removeLayer(marker));
  orderMarkers = [];
  
  userOrders.value.forEach(order => {
    const customIcon = L.divIcon({
      html: `
        <div style="position: relative; display: flex; flex-direction: column; align-items: center;">
          <!-- Etiqueta flotante sobre el icono - NARANJA con letras NEGRAS -->
          <div style="
            background: #f97316;
            color: #1a1a2e;
            font-size: 8px;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 12px;
            letter-spacing: 0.5px;
            white-space: nowrap;
            margin-bottom: 4px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
          ">
            <i class="fas fa-user" style="font-size: 7px; margin-right: 3px;"></i>
            CLIENTE
          </div>
          <!-- Icono principal con borde anaranjado -->
          <div style="
            background: linear-gradient(135deg, #fff 0%, #fff0db 100%);
            width: 38px;
            height: 38px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #1a1a2e;
            font-size: 16px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
            border: 3px solid #f97316;
            transition: transform 0.2s ease;
          ">
            <i class="fas fa-shopping-cart"></i>
          </div>
        </div>
      `,
      className: 'client-div-icon',
      iconSize: [38, 58],
      iconAnchor: [19, 50],
      popupAnchor: [0, -50]
    });

    const marker = L.marker([order.delivery_lat, order.delivery_lng], { icon: customIcon })
      .bindPopup(`
        <div style="font-family: 'Segoe UI', sans-serif; min-width: 180px;">
          <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px; padding-bottom: 6px; border-bottom: 1px solid #f97316;">
            <i class="fas fa-shopping-cart" style="color: #f97316; font-size: 18px;"></i>
            <strong style="color: #333; font-size: 14px;">Pedido de Cliente</strong>
          </div>
          <div style="margin-bottom: 4px;">
            <span style="color: #666; font-size: 11px;">🏢 Empresa:</span>
            <span style="color: #333; font-size: 11px; font-weight: 500;"> ${order.company_name}</span>
          </div>
          <div style="margin-bottom: 4px;">
            <span style="color: #666; font-size: 11px;">📦 Producto:</span>
            <span style="color: #333; font-size: 11px;"> ${order.product_name} (${order.quantity})</span>
          </div>
          <div>
            <span style="color: #666; font-size: 11px;">💰 Total:</span>
            <span style="color: #f97316; font-size: 11px; font-weight: 600;"> ${order.total_amount} Bs</span>
          </div>
        </div>
      `, {
        maxWidth: 260,
        minWidth: 200,
        className: 'client-popup'
      })
      .addTo(mapInstance);

    marker.on('mouseover', function() {
      const iconDiv = this._icon?.querySelector('div:last-child');
      if (iconDiv) {
        iconDiv.style.transform = 'scale(1.1)';
        iconDiv.style.transition = 'transform 0.2s ease';
      }
    });

    marker.on('mouseout', function() {
      const iconDiv = this._icon?.querySelector('div:last-child');
      if (iconDiv) {
        iconDiv.style.transform = 'scale(1)';
      }
    });

    orderMarkers.push(marker);
  });
};

const focusOnOrder = (order) => {
  if (mapInstance) {
    mapInstance.setView([order.delivery_lat, order.delivery_lng], 15);
    showMessage(`📍 ${order.company_name} - ${order.product_name}`);
  }
};

const handleProductSelected = (product) => {
  selectedProduct.value = product;
  selectedCompany.value = null;
  selectedDeliveryLocation.value = null;
  orderQuantity.value = 1;
  clearDeliveryMarker();
  showOrderHistory.value = true;
};

const handleCompanySelected = (data) => {
  selectedCompany.value = data.company;
  selectedProduct.value = data.product;
  selectedDeliveryLocation.value = null;
  orderQuantity.value = 1;
  clearDeliveryMarker();
  showOrderHistory.value = false;
};

const handleNewOrder = () => {
  selectedCompany.value = null;
  selectedProduct.value = null;
  selectedDeliveryLocation.value = null;
  orderQuantity.value = 1;
  clearDeliveryMarker();
  showOrderHistory.value = true;
  loadUserOrders();
};

const handleMapClick = (latlng) => {
  if (!selectedCompany.value) {
    showMessage('Primero selecciona una empresa del sidebar', true);
    return;
  }
  
  setDeliveryLocation(latlng.lat, latlng.lng);
};

const setDeliveryLocation = (lat, lng) => {
  selectedDeliveryLocation.value = { lat, lng };
  
  if (!mapRef.value) return;
  
  const map = mapRef.value.getMapInstance();
  if (!map) return;
  
  mapInstance = map;
  
  if (deliveryMarker) {
    map.removeLayer(deliveryMarker);
  }
  
  deliveryMarker = L.marker([lat, lng], {
    icon: L.icon({
      iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34]
    })
  }).addTo(map).bindPopup('📍 Ubicación de entrega');
  
  map.setView([lat, lng], 15);
};

const clearDeliveryMarker = () => {
  if (deliveryMarker && mapRef.value) {
    const map = mapRef.value.getMapInstance();
    if (map) {
      map.removeLayer(deliveryMarker);
    }
    deliveryMarker = null;
  }
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

const incrementQuantity = () => {
  if (orderQuantity.value < selectedCompany.value.available_stock) {
    orderQuantity.value++;
  }
};

const decrementQuantity = () => {
  if (orderQuantity.value > 1) {
    orderQuantity.value--;
  }
};

const cancelOrder = () => {
  selectedCompany.value = null;
  selectedProduct.value = null;
  selectedDeliveryLocation.value = null;
  orderQuantity.value = 1;
  clearDeliveryMarker();
  showOrderHistory.value = true;
  showMessage('✓ Pedido cancelado');
};

const confirmOrder = async () => {
  if (!userId) {
    showMessage('Error: Usuario no identificado', true);
    return;
  }

  if (!selectedDeliveryLocation.value) {
    showMessage('Primero selecciona una ubicación de entrega', true);
    return;
  }

  isConfirming.value = true;
  
  try {
    const orderData = {
      user_id: userId,
      company_id: selectedCompany.value.company_id,
      product_id: selectedProduct.value.id,
      product_name: selectedProduct.value.name,
      price: selectedProduct.value.price,
      quantity: orderQuantity.value,
      delivery_lat: selectedDeliveryLocation.value.lat,
      delivery_lng: selectedDeliveryLocation.value.lng
    };

    console.log('📤 Enviando pedido:', orderData);
    const result = await ordersAPI.create(orderData);
    
    if (result.success) {
      showMessage(`✅ Pedido confirmado: ${orderQuantity.value} x ${selectedProduct.value.name}`);
      
      setTimeout(() => {
        selectedCompany.value = null;
        selectedProduct.value = null;
        selectedDeliveryLocation.value = null;
        orderQuantity.value = 1;
        clearDeliveryMarker();
        showOrderHistory.value = true;
        isConfirming.value = false;
        loadUserOrders();
      }, 1500);
    } else {
      showMessage(`❌ Error: ${result.error}`, true);
      isConfirming.value = false;
    }
  } catch (error) {
    console.error('Error al crear pedido:', error);
    showMessage(`❌ Error al crear pedido: ${error.message}`, true);
    isConfirming.value = false;
  }
};

watch(selectedCompany, () => {
  nextTick(() => {
    if (mapRef.value) {
      const map = mapRef.value.getMapInstance();
      if (map) {
        map.invalidateSize();
      }
    }
  });
});

onMounted(() => {
  setTimeout(() => {
    if (mapRef.value) {
      mapInstance = mapRef.value.getMapInstance();
      if (mapInstance) {
        mapInstance.invalidateSize();
      }
      loadUserOrders();
    }
  }, 500);
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

.map-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

.map-wrapper {
  flex: 1;
  position: relative;
  min-height: 0;
}

.client-map {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.order-history-overlay {
  position: absolute;
  top: 1rem;
  right: 1rem;
  width: 220px;
  max-height: 300px;
  background: rgba(10, 15, 26, 0.95);
  border: 1px solid rgba(212, 163, 115, 0.2);
  border-radius: 0.6rem;
  padding: 0.75rem;
  z-index: 400;
  backdrop-filter: blur(8px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.order-history-overlay h4 {
  margin: 0 0 0.5rem;
  font-size: 0.75rem;
  color: #d4a373;
  text-transform: uppercase;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.orders-list {
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.order-item {
  padding: 0.5rem;
  background: rgba(212, 163, 115, 0.08);
  border: 1px solid rgba(212, 163, 115, 0.15);
  border-radius: 0.3rem;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.order-item:hover {
  background: rgba(212, 163, 115, 0.15);
  border-color: rgba(212, 163, 115, 0.3);
}

.order-company {
  font-size: 0.7rem;
  color: #d4a373;
  font-weight: 600;
}

.order-product {
  font-size: 0.65rem;
  color: #e8edf2;
}

.order-date {
  font-size: 0.6rem;
  color: #7a8ca2;
}

.map-overlay-message {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(10, 15, 26, 0.7);
  backdrop-filter: blur(4px);
  z-index: 300;
  pointer-events: none;
}

.overlay-content {
  text-align: center;
  color: #d4a373;
  padding: 1.5rem;
  background: rgba(10, 15, 26, 0.8);
  border-radius: 1rem;
  border: 1px solid rgba(212, 163, 115, 0.3);
}

.overlay-content i {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.overlay-content p {
  margin: 0;
  font-size: 0.85rem;
}

.order-panel {
  position: absolute;
  bottom: 1rem;
  left: 1rem;
  right: 1rem;
  background: rgba(10, 15, 26, 0.98);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(212, 163, 115, 0.2);
  border-radius: 0.75rem;
  z-index: 400;
  max-width: 380px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
}

.order-panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  background: rgba(212, 163, 115, 0.1);
  border-bottom: 1px solid rgba(212, 163, 115, 0.15);
  border-radius: 0.75rem 0.75rem 0 0;
}

.order-panel-header h3 {
  margin: 0;
  font-size: 0.85rem;
  font-weight: 600;
  color: #d4a373;
}

.btn-close-panel {
  background: none;
  border: none;
  color: #8fa3b3;
  cursor: pointer;
  font-size: 0.9rem;
  padding: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.btn-close-panel:hover {
  color: #e06c6c;
}

.order-panel-body {
  padding: 0.75rem 1rem;
}

.product-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(212, 163, 115, 0.15);
}

.product-name {
  font-size: 0.85rem;
  font-weight: 600;
  color: #ffffff;
}

.product-price {
  font-size: 0.8rem;
  color: #d4a373;
  font-weight: 600;
}

.location-prompt {
  text-align: center;
}

.btn-location {
  width: 100%;
  padding: 0.7rem;
  border: 1px solid rgba(212, 163, 115, 0.3);
  border-radius: 0.5rem;
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

.btn-location:hover {
  background: rgba(212, 163, 115, 0.2);
  border-color: rgba(212, 163, 115, 0.5);
}

.map-hint {
  font-size: 0.65rem;
  color: #7a8ca2;
  margin-top: 0.5rem;
}

.quantity-section {
  margin-bottom: 0.75rem;
}

.quantity-section label {
  font-size: 0.7rem;
  color: #8fa3b3;
  display: block;
  margin-bottom: 0.3rem;
}

.quantity-input {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.quantity-input .qty-btn {
  background: rgba(212, 163, 115, 0.15);
  border: 1px solid rgba(212, 163, 115, 0.3);
  color: #d4a373;
  width: 1.8rem;
  height: 1.8rem;
  border-radius: 0.3rem;
  cursor: pointer;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  font-weight: 600;
}

.quantity-input .qty-btn:hover:not(:disabled) {
  background: rgba(212, 163, 115, 0.25);
}

.quantity-input .qty-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.quantity-input .qty-input {
  width: 3.5rem;
  padding: 0.35rem;
  background: rgba(10, 15, 26, 0.6);
  border: 1px solid rgba(212, 163, 115, 0.3);
  border-radius: 0.3rem;
  color: #e8edf2;
  text-align: center;
  font-size: 0.85rem;
  font-weight: 600;
}

.quantity-input .qty-input:focus {
  outline: none;
  border-color: rgba(212, 163, 115, 0.6);
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

.summary-item.location {
  font-size: 0.7rem;
}

.location-coords {
  font-family: monospace;
  font-size: 0.7rem;
}

.order-actions {
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid rgba(212, 163, 115, 0.15);
}

.btn-confirm {
  width: 100%;
  padding: 0.7rem;
  background: rgba(212, 163, 115, 0.15);
  border: 1px solid rgba(212, 163, 115, 0.3);
  color: #d4a373;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
}

.btn-confirm:hover:not(:disabled) {
  background: rgba(212, 163, 115, 0.25);
  border-color: rgba(212, 163, 115, 0.5);
}

.btn-confirm:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.message-toast {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  background: #1e2a3a;
  border-left: 4px solid #d4a373;
  padding: 0.75rem 1.25rem;
  border-radius: 0.6rem;
  color: #e8edf2;
  font-size: 0.8rem;
  z-index: 2000;
  backdrop-filter: blur(8px);
  animation: slideInRight 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.message-toast.error {
  border-left-color: #e06c6c;
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
  .order-panel {
    left: 0.5rem;
    right: 0.5rem;
    max-width: none;
  }
  
  .order-history-overlay {
    width: 180px;
    max-height: 200px;
  }
}
</style>