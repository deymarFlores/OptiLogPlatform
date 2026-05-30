<template>
  <aside class="client-sidebar">
    <div class="sidebar-header">
      <h2><i class="fas fa-shopping-cart"></i> Mis Pedidos</h2>
      <button 
        v-if="selectedCompany"
        class="btn-new-order"
        @click="newOrder"
        title="Hacer nuevo pedido"
      >
        <i class="fas fa-plus-circle"></i> Nuevo
      </button>
    </div>

    <div v-if="userOrders && userOrders.length > 0" class="orders-history-section">
      <h3 class="section-title">
        <i class="fas fa-history"></i> Historial
      </h3>
      <div class="orders-history-list">
        <div 
          v-for="order in userOrders"
          :key="order.id"
          class="order-history-item"
          @click="$emit('focus-order', order)"
        >
          <div class="order-header">
            <span class="company-name">{{ order.company_name }}</span>
            <span class="order-date">{{ formatOrderDate(order.created_at) }}</span>
          </div>
          <div class="order-details">
            <span class="product">{{ order.product_name }}</span>
            <span class="quantity">×{{ order.quantity }}</span>
            <span class="total">{{ order.total_amount.toFixed(2) }} Bs</span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="userOrders && userOrders.length > 0" class="sidebar-divider"></div>

    <div class="search-section">
      <h3 class="section-title">
        <i class="fas fa-plus"></i> Nuevo Pedido
      </h3>
      
      <div class="search-box">
        <i class="fas fa-search"></i>
        <input 
          v-model="searchQuery"
          type="text"
          placeholder="Buscar producto..."
          class="search-input"
          @input="handleSearchInput"
          @keyup.enter="handleSearchImmediate"
        />
      </div>
      
      <div v-if="isSearching" class="searching-indicator">
        <i class="fas fa-spinner fa-spin"></i> Buscando...
      </div>
    </div>

    <div v-if="searchResults.length > 0 && !selectedProduct" class="search-results">
      <div class="products-list">
        <div 
          v-for="product in searchResults"
          :key="product.id"
          class="product-card"
          @click="selectProduct(product)"
        >
          <div class="product-header">
            <i class="fas fa-box"></i>
            <h4>{{ product.name }}</h4>
          </div>
          <div class="product-info">
            <span class="price">{{ product.price }} Bs</span>
            <span class="company">{{ product.company_name }}</span>
          </div>
          <div class="stock-badge">
            {{ product.available_stock }} disponibles
          </div>
        </div>
      </div>
    </div>

    <div v-if="selectedProduct" class="companies-section">
      <div class="selected-product-header">
        <button class="btn-clear-selection" @click="clearSelection">
          <i class="fas fa-arrow-left"></i>
        </button>
        <h3 class="section-title">
          <i class="fas fa-building"></i> {{ selectedProduct.name }}
        </h3>
      </div>
      <div class="companies-list">
        <div 
          v-for="company in availableCompanies"
          :key="company.company_id"
          class="company-card"
          :class="{ 'selected': selectedCompany?.company_id === company.company_id }"
          @click="selectCompany(company)"
        >
          <div class="company-header">
            <i class="fas fa-warehouse"></i>
            <h4>{{ company.company_name }}</h4>
          </div>
          <div class="company-info">
            <p class="price-detail">
              {{ selectedProduct.price }} Bs/{{ selectedProduct.units }}
            </p>
          </div>
          <div v-if="company.available_stock > 0" class="quantity-badge">
            {{ company.available_stock }} disponibles
          </div>
        </div>

        <div v-if="availableCompanies.length === 0" class="empty-state">
          <i class="fas fa-inbox"></i>
          <p>No hay empresas con este producto</p>
        </div>
      </div>
    </div>

    <div v-if="searchResults.length === 0 && searchQuery && !isSearching && !selectedProduct" class="no-results">
      <i class="fas fa-info-circle"></i>
      <p>No encontrado</p>
    </div>

    <div v-if="!searchQuery && !selectedProduct && (!userOrders || userOrders.length === 0)" class="no-orders-state">
      <i class="fas fa-inbox"></i>
      <p>Sin pedidos aún</p>
      <p class="hint">Busca un producto para hacer tu primer pedido</p>
    </div>
  </aside>
</template>

<script setup>
import { ref, computed } from 'vue';
import { typeMaterialsAPI } from '@/services/api';

defineProps({
  userOrders: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['product-selected', 'company-selected', 'new-order', 'focus-order']);

const searchQuery = ref('');
const searchResults = ref([]);
const selectedProduct = ref(null);
const selectedCompany = ref(null);
const isSearching = ref(false);
let debounceTimer = null;

const availableCompanies = computed(() => {
  if (!selectedProduct.value) return [];
  return searchResults.value.filter(r => r.id === selectedProduct.value.id);
});

const formatOrderDate = (dateString) => {
  try {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
  } catch {
    return dateString;
  }
};

const newOrder = () => {
  selectedProduct.value = null;
  selectedCompany.value = null;
  searchQuery.value = '';
  searchResults.value = [];
  emit('new-order');
};

const performSearch = async () => {
  const query = searchQuery.value.trim();
  
  if (!query || query.length < 2) {
    searchResults.value = [];
    return;
  }

  isSearching.value = true;
  try {
    const result = await typeMaterialsAPI.search(query);
    if (result.success) {
      searchResults.value = result.data;
    } else {
      console.error('Error en búsqueda:', result.error);
      searchResults.value = [];
    }
  } catch (error) {
    console.error('Error al buscar:', error);
    searchResults.value = [];
  } finally {
    isSearching.value = false;
  }
};

const handleSearchInput = () => {
  if (debounceTimer) {
    clearTimeout(debounceTimer);
  }
  
  debounceTimer = setTimeout(() => {
    performSearch();
  }, 500);
};

const handleSearchImmediate = () => {
  if (debounceTimer) {
    clearTimeout(debounceTimer);
  }
  performSearch();
};

const selectProduct = (product) => {
  selectedProduct.value = product;
  selectedCompany.value = null;
  emit('product-selected', product);
};

const selectCompany = (company) => {
  selectedCompany.value = company;
  emit('company-selected', {
    product: selectedProduct.value,
    company: company
  });
};

const clearSelection = () => {
  selectedProduct.value = null;
  selectedCompany.value = null;
  searchQuery.value = '';
  searchResults.value = [];
  emit('product-selected', null);
};
</script>

<style scoped>
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
  display: flex;
  align-items: center;
  justify-content: space-between;
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

.btn-new-order {
  background: rgba(212, 163, 115, 0.15);
  border: 1px solid rgba(212, 163, 115, 0.3);
  color: #d4a373;
  padding: 0.5rem 0.75rem;
  border-radius: 0.4rem;
  cursor: pointer;
  font-size: 0.7rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.35rem;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.btn-new-order:hover {
  background: rgba(212, 163, 115, 0.25);
  border-color: rgba(212, 163, 115, 0.5);
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

.searching-indicator {
  margin-top: 0.5rem;
  font-size: 0.75rem;
  color: #d4a373;
  text-align: center;
}

/* Sección de historial de órdenes */
.orders-history-section {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
}

.orders-history-list {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  max-height: 200px;
  overflow-y: auto;
}

.order-history-item {
  padding: 0.6rem;
  background: rgba(212, 163, 115, 0.08);
  border: 1px solid rgba(212, 163, 115, 0.2);
  border-radius: 0.4rem;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.order-history-item:hover {
  background: rgba(212, 163, 115, 0.15);
  border-color: rgba(212, 163, 115, 0.4);
  transform: translateX(2px);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
}

.company-name {
  font-size: 0.75rem;
  font-weight: 600;
  color: #d4a373;
}

.order-date {
  font-size: 0.65rem;
  color: #7a8ca2;
}

.order-details {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.7rem;
  color: #e8edf2;
}

.product {
  flex: 1;
  color: #c8cfd8;
}

.quantity {
  color: #7a8ca2;
  font-weight: 600;
}

.total {
  color: #d4a373;
  font-weight: 600;
}

.sidebar-divider {
  height: 1px;
  background: rgba(212, 163, 115, 0.15);
  margin: 1rem 0;
}

.no-orders-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem;
  text-align: center;
  color: #7a8ca2;
}

.no-orders-state i {
  font-size: 2rem;
  opacity: 0.3;
  color: #d4a373;
}

.no-orders-state p {
  margin: 0;
  font-size: 0.8rem;
}

.hint {
  font-size: 0.7rem !important;
  opacity: 0.7;
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

.selected-product-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.btn-clear-selection {
  background: rgba(212, 163, 115, 0.15);
  border: 1px solid rgba(212, 163, 115, 0.3);
  color: #d4a373;
  width: 28px;
  height: 28px;
  border-radius: 0.4rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.btn-clear-selection:hover {
  background: rgba(212, 163, 115, 0.3);
}

.search-results,
.companies-section {
  flex: 1;
  overflow-y: auto;
}

.products-list,
.companies-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.product-card,
.company-card {
  background: rgba(212, 163, 115, 0.08);
  border: 1px solid rgba(212, 163, 115, 0.15);
  border-radius: 0.75rem;
  padding: 0.75rem;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.product-card:hover,
.company-card:hover {
  background: rgba(212, 163, 115, 0.12);
  border-color: rgba(212, 163, 115, 0.3);
}

.company-card.selected {
  background: rgba(212, 163, 115, 0.25);
  border-color: #d4a373;
  box-shadow: 0 0 12px rgba(212, 163, 115, 0.2);
}

.product-header,
.company-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.product-header i,
.company-header i {
  color: #d4a373;
  font-size: 0.9rem;
}

.product-header h4,
.company-header h4 {
  margin: 0;
  font-size: 0.85rem;
  font-weight: 600;
  color: #ffffff;
}

.product-info {
  display: flex;
  justify-content: space-between;
  font-size: 0.7rem;
  color: #8fa3b3;
}

.price {
  color: #d4a373;
  font-weight: 600;
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

.stock-badge,
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
.no-selection,
.no-results {
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
.no-selection i,
.no-results i {
  font-size: 2rem;
  opacity: 0.5;
}

.empty-state p,
.no-selection p,
.no-results p {
  margin: 0;
  font-size: 0.85rem;
}

@media (max-width: 1024px) {
  .client-sidebar {
    width: 280px;
  }
}

@media (max-width: 768px) {
  .client-sidebar {
    width: 100%;
    max-height: 40%;
    border-right: none;
    border-bottom: 1px solid rgba(212, 163, 115, 0.15);
  }
}
</style>