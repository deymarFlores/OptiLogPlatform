<template>
  <div class="materials-management">
    <!-- Toast Notifications -->
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

    <!-- Header -->
    <div class="management-header">
      <div class="header-left">
        <button class="btn-back" @click="handleBackToMap">
          <i class="fas fa-arrow-left"></i>
          <span>Volver al Mapa</span>
        </button>
        <div class="header-title">
          <h1><i class="fas fa-boxes"></i> Gestión de Materiales</h1>
          <p>Configura los productos y precios por punto logístico</p>
        </div>
      </div>
      <div class="header-stats">
        <div class="stat-card">
          <span class="stat-label">Puntos Configurados</span>
          <strong class="stat-value">{{ sucursales.length }}</strong>
        </div>
        <div class="stat-card">
          <span class="stat-label">Total de Productos</span>
          <strong class="stat-value">{{ totalMaterials }}</strong>
        </div>
        <div class="stat-card">
          <span class="stat-label">Valor Total</span>
          <strong class="stat-value">Bs {{ totalValue.toFixed(2) }}</strong>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div class="management-content">
      <!-- Panel de Puntos -->
      <div class="materials-list">
        <div class="list-header">
          <h2>Puntos Logísticos</h2>
          <div class="list-controls">
            <input
              v-model="searchPoint"
              type="text"
              placeholder="Buscar punto..."
              class="search-input"
            />
            <select v-model="filterType" class="filter-select">
              <option value="">Todos los tipos</option>
              <option value="Almacén">Almacenes</option>
              <option value="Tienda">Tiendas</option>
            </select>
          </div>
        </div>

        <div class="points-grid">
          <div
            v-for="point in filteredPoints"
            :key="point.id"
            class="point-card"
            :class="{ active: activePointId === point.id }"
            @click="selectPoint(point.id)"
          >
            <div class="card-icon">
              <i :class="`fas ${getTypeIcon(point.type_location_id)}`"></i>
            </div>
            <div class="card-content">
              <h3>{{ point.name }}</h3>
              <p class="card-type">{{ getTypeName(point.type_location_id) }}</p>
              <p class="card-coords">
                {{ point.lat.toFixed(4) }}, {{ point.lng.toFixed(4) }}
              </p>
            </div>
            <div class="card-badge">
              <span v-if="getMaterialsSummary(point.id)" class="badge-count">
                {{ getMaterialsSummary(point.id).count }}
              </span>
              <i class="fas fa-chevron-right"></i>
            </div>
          </div>

          <div v-if="filteredPoints.length === 0" class="empty-state">
            <i class="fas fa-inbox"></i>
            <p>No hay sucursales registradas</p>
          </div>
        </div>
      </div>

      <!-- Panel de Materiales -->
      <div class="materials-editor">
        <div v-if="selectedPoint" class="editor-wrapper">
          <!-- Editor Header -->
          <div class="editor-header">
            <div class="selected-point-info">
              <i
                :class="`fas ${getTypeIcon(selectedPoint.type_location_id)}`"
              ></i>
              <div>
                <h3>{{ selectedPoint.name }}</h3>
                <p>{{ getTypeName(selectedPoint.type_location_id) }}</p>
              </div>
            </div>
          </div>

          <!-- Contenido scrolleable -->
          <div class="editor-content-scroll">
            <!-- Formulario de Producto -->
            <form @submit.prevent="addMaterial" class="add-material-form">
              <h4>Agregar Producto</h4>
              <div class="form-grid">
                <div class="form-group">
                  <label for="productSelect">Producto</label>
                  <select
                    v-model="formData.productId"
                    id="productSelect"
                    required
                    class="product-select"
                  >
                    <option value="">Seleccionar producto...</option>
                    <option
                      v-for="product in products"
                      :key="product.id"
                      :value="product.id"
                    >
                      {{ product.name }} ({{ product.price }} Bs/{{
                        product.unit
                      }})
                    </option>
                  </select>
                </div>
                <div class="form-group">
                  <label for="quantity">Cantidad Disponible</label>
                  <div class="quantity-input-group">
                    <input
                      v-model.number="formData.quantity"
                      id="quantity"
                      type="number"
                      step="0.1"
                      placeholder="0.0"
                      required
                    />
                    <span v-if="selectedProduct" class="unit-badge">{{
                      selectedProduct.unit
                    }}</span>
                  </div>
                </div>
              </div>
              <button type="submit" class="btn-submit" :disabled="isSubmitting">
                <i class="fas fa-plus"></i>
                {{ isSubmitting ? "Agregando..." : "Agregar Producto" }}
              </button>
            </form>

            <!-- Tabla de Materiales -->
            <div
              v-if="getActiveMaterialsSummary()"
              class="materials-table-section"
            >
              <h4>Productos Registrados</h4>
              <div class="table-responsive">
                <table class="materials-table">
                  <thead>
                    <tr>
                      <th>Producto</th>
                      <th class="text-right">Cantidad</th>
                      <th class="text-right">Unidad</th>
                      <th class="text-right">Precio (Bs/unidad)</th>
                      <th class="text-right">Subtotal (Bs)</th>
                      <th class="text-center">Acción</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="material in getActiveMaterialsSummary().materials"
                      :key="material.id"
                    >
                      <td class="product-name">
                        <i class="fas fa-package"></i>
                        {{ material.material_name }}
                      </td>
                      <td class="text-right">
                        {{ parseFloat(material.stock).toFixed(2) }}
                      </td>
                      <td class="text-right">{{ material.units }}</td>
                      <td class="text-right">
                        {{ parseFloat(material.price).toFixed(2) }}
                      </td>
                      <td class="text-right subtotal">
                        {{
                          (
                            parseFloat(material.stock) *
                            parseFloat(material.price)
                          ).toFixed(2)
                        }}
                      </td>
                      <td class="text-center">
                        <button
                          @click="deleteMaterial(material.id)"
                          class="btn-action-delete"
                          title="Eliminar"
                          :disabled="isDeleting"
                        >
                          <i class="fas fa-trash-alt"></i>
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <div v-else class="empty-materials">
              <i class="fas fa-inbox"></i>
              <p>No hay productos registrados para este punto</p>
              <p class="hint">
                Agrega tu primer producto usando el formulario de arriba
              </p>
            </div>
          </div>
        </div>

        <div v-else class="no-selection">
          <i class="fas fa-hand-point-left"></i>
          <p>Selecciona un punto para gestionar sus productos</p>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <div class="management-footer">
      <button class="btn-cancel" @click="handleBackToMap">
        <i class="fas fa-arrow-left"></i> Cancelar
      </button>
      <button class="btn-complete" @click="handleContinue">
        <i class="fas fa-check"></i> Completar Configuración
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useSucursalesManager } from "@/pages/dashboard/composables/useSucursalesManager";
import { useSetupStore } from "@/pages/setup/composables/useSetupStore";
import { locationStockAPI, typeMaterialsAPI } from "@/services/api";

const sucursalesManager = useSucursalesManager();
const setupStore = useSetupStore();

const toasts = ref([]);
let nextToastId = 0;

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

const activePointId = ref(null);
const searchPoint = ref("");
const filterType = ref("");
const formData = ref({
  productId: "",
  quantity: "",
});
const locationStocks = ref({});
const isLoading = ref(false);
const isSubmitting = ref(false);
const isDeleting = ref(false);

const products = computed(() => setupStore.products.value || []);

const sucursales = computed(() => sucursalesManager.sucursales.value || []);

const filteredPoints = computed(() => {
  return sucursales.value.filter((point) => {
    const matchesSearch = point.name
      .toLowerCase()
      .includes(searchPoint.value.toLowerCase());
    const matchesType =
      !filterType.value || point.type_location_id === filterType.value;
    return matchesSearch && matchesType;
  });
});

const selectedPoint = computed(() => {
  if (!activePointId.value) return null;
  return sucursales.value.find((p) => p.id === activePointId.value);
});

const selectedProduct = computed(() => {
  if (!formData.value.productId) return null;
  return products.value.find((p) => p.id === formData.value.productId);
});

const totalMaterials = computed(() => {
  let count = 0;
  for (let locationId in locationStocks.value) {
    count += (locationStocks.value[locationId] || []).length;
  }
  return count;
});

const totalValue = computed(() => {
  let total = 0;
  for (let locationId in locationStocks.value) {
    const stocks = locationStocks.value[locationId] || [];
    stocks.forEach((stock) => {
      total += (parseFloat(stock.price) || 0) * (parseFloat(stock.stock) || 0);
    });
  }
  return total;
});

const getMaterialsSummary = (locationId) => {
  const stocks = locationStocks.value[locationId] || [];
  if (stocks.length === 0) return null;

  const totalValue = stocks.reduce(
    (sum, stock) =>
      sum + (parseFloat(stock.price) || 0) * (parseFloat(stock.stock) || 0),
    0,
  );
  return {
    count: stocks.length,
    totalValue: totalValue,
    materials: stocks,
  };
};

const getTypeIcon = (typeId) => {
  const type = setupStore.pointTypes.value?.find((t) => t.id === typeId);
  return type?.icon ? `${type.icon}` : "fa-warehouse";
};

const getTypeName = (typeId) => {
  const type = setupStore.pointTypes.value?.find((t) => t.id === typeId);
  return type?.name || "Sucursal";
};

const getActiveMaterialsSummary = () => {
  if (!activePointId.value) return null;
  return getMaterialsSummary(activePointId.value);
};

const selectPoint = async (pointId) => {
  activePointId.value = pointId;
  resetForm();
  await loadLocationStocks(pointId);
};

const resetForm = () => {
  formData.value = {
    productId: "",
    quantity: "",
  };
};

const loadLocationStocks = async (locationId) => {
  try {
    const result = await locationStockAPI.getByLocation(locationId);
    if (result.success) {
      locationStocks.value[locationId] = result.data || [];
    } else {
      locationStocks.value[locationId] = [];
      showToast(
        "Error al cargar los productos: " +
          (result.error || "Error desconocido"),
        "error",
      );
    }
  } catch (error) {
    console.error("Error en loadLocationStocks:", error);
    locationStocks.value[locationId] = [];
    showToast("Error de conexión al cargar productos", "error");
  }
};

const loadTypeMaterials = async () => {
  try {
    isLoading.value = true;

    if (setupStore.products.value && setupStore.products.value.length > 0) {
      return setupStore.products.value;
    }

    const result = await typeMaterialsAPI.getAll();
    if (result.success && result.data) {
      setupStore.setProducts(result.data);
      showToast(
        ` ${result.data.length} productos cargados correctamente`,
        "success",
      );
      return result.data;
    } else {
      showToast("Error al cargar tipos de materiales", "error");
      return [];
    }
  } catch (error) {
    console.error("Error en loadTypeMaterials:", error);
    showToast("Error de conexión al cargar productos", "error");
    return [];
  } finally {
    isLoading.value = false;
  }
};

const addMaterial = async () => {
  if (!formData.value.productId || !formData.value.quantity) {
    showToast(
      "Por favor selecciona un producto y completa la cantidad",
      "warning",
    );
    return;
  }

  if (!activePointId.value || !selectedProduct.value) {
    showToast("Selecciona una sucursal primero", "warning");
    return;
  }

  const quantity = parseFloat(formData.value.quantity);
  if (isNaN(quantity) || quantity <= 0) {
    showToast("Por favor ingresa una cantidad válida mayor a 0", "warning");
    return;
  }

  isSubmitting.value = true;
  try {
    const result = await locationStockAPI.create({
      location_id: activePointId.value,
      type_material_id: formData.value.productId,
      stock: quantity,
    });

    if (result.success) {
      await loadLocationStocks(activePointId.value);
      resetForm();
      showToast("✅ Producto agregado correctamente", "success");
    } else {
      showToast(
        "Error: " + (result.error || "No se pudo agregar el producto"),
        "error",
      );
    }
  } catch (error) {
    console.error("Error al agregar material:", error);
    showToast("Error de conexión al agregar producto", "error");
  } finally {
    isSubmitting.value = false;
  }
};

const deleteMaterial = async (stockId) => {
  isDeleting.value = true;
  try {
    const result = await locationStockAPI.delete(stockId);
    if (result.success) {
      if (activePointId.value) {
        await loadLocationStocks(activePointId.value);
      }
      showToast("✅ Producto eliminado correctamente", "success");
    } else {
      showToast(
        "Error: " + (result.error || "No se pudo eliminar el producto"),
        "error",
      );
    }
  } catch (error) {
    console.error("Error al eliminar material:", error);
    showToast("Error de conexión al eliminar producto", "error");
  } finally {
    isDeleting.value = false;
  }
};

const handleBackToMap = () => {
  emit("back-to-map");
};

const handleContinue = () => {
  emit("continue");
};

const emit = defineEmits(["back-to-map", "continue"]);

onMounted(async () => {
  await loadTypeMaterials();
  await sucursalesManager.loadSucursales();

  if (sucursales.value.length > 0) {
    await selectPoint(sucursales.value[0].id);
  } else {
    showToast("No hay sucursales disponibles", "warning");
  }
});
</script>

<style scoped>
.materials-management {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #0a0f1a;
  color: #e8edf2;
}

/* Toast Notifications */
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

.toast.info {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  border-left: 4px solid #60a5fa;
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

/* Header */
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
  min-width: 130px;
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

/* Content */
.management-content {
  display: flex;
  flex: 1;
  gap: 0;
  overflow: hidden;
}

.materials-list {
  width: 30%;
  background: rgba(14, 18, 26, 0.5);
  border-right: 1px solid rgba(212, 163, 115, 0.2);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.list-header {
  padding: 0.9rem;
  border-bottom: 1px solid rgba(212, 163, 115, 0.2);
  background: rgba(212, 163, 115, 0.08);
  flex-shrink: 0;
}

.list-header h2 {
  margin: 0 0 0.6rem;
  font-size: 0.95rem;
  color: #d4a373;
  font-weight: 600;
}

.list-controls {
  display: flex;
  gap: 0.5rem;
  flex-direction: column;
}

.search-input,
.filter-select {
  width: 100%;
  padding: 0.5rem;
  background: rgba(14, 18, 26, 0.5);
  border: 1px solid rgba(212, 163, 115, 0.3);
  border-radius: 6px;
  color: #ffffff;
  font-size: 0.8rem;
  transition: all 0.3s ease;
}

.search-input:focus,
.filter-select:focus {
  outline: none;
  border-color: #d4a373;
  box-shadow: 0 0 0 3px rgba(212, 163, 115, 0.1);
}

.search-input::placeholder {
  color: rgba(232, 237, 242, 0.3);
}

.points-grid {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.point-card {
  background: rgba(212, 163, 115, 0.08);
  border: 1.5px solid rgba(212, 163, 115, 0.15);
  border-radius: 8px;
  padding: 0.7rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.point-card:hover {
  background: rgba(212, 163, 115, 0.15);
  border-color: rgba(212, 163, 115, 0.3);
}

.point-card.active {
  background: rgba(212, 163, 115, 0.25);
  border-color: #d4a373;
  box-shadow: 0 0 12px rgba(212, 163, 115, 0.2);
}

.card-icon {
  font-size: 1.5rem;
  color: #d4a373;
  flex-shrink: 0;
}

.card-content {
  flex: 1;
  min-width: 0;
}

.card-content h3 {
  margin: 0;
  font-size: 0.85rem;
  font-weight: 600;
  color: #ffffff;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-type {
  margin: 0.1rem 0 0;
  font-size: 0.65rem;
  color: #8fa3b3;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.card-coords {
  margin: 0.1rem 0 0;
  font-size: 0.65rem;
  color: #8fa3b3;
  font-family: monospace;
}

.card-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-shrink: 0;
}

.badge-count {
  background: #d4a373;
  color: #0a0f1a;
  border-radius: 20px;
  padding: 0.3rem 0.7rem;
  font-size: 0.75rem;
  font-weight: 700;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  color: #8fa3b3;
  text-align: center;
}

.empty-state i {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  opacity: 0.5;
}

/* Editor */
.materials-editor {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: #0a0f1a;
}

.editor-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.editor-header {
  padding: 0.9rem 1.2rem;
  border-bottom: 1px solid rgba(212, 163, 115, 0.2);
  background: rgba(212, 163, 115, 0.08);
  flex-shrink: 0;
}

.selected-point-info {
  display: flex;
  align-items: center;
  gap: 0.7rem;
}

.selected-point-info i {
  font-size: 1.8rem;
  color: #d4a373;
}

.selected-point-info h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #ffffff;
}

.selected-point-info p {
  margin: 0.1rem 0 0;
  font-size: 0.75rem;
  color: #8fa3b3;
}

/* Content scrollable */
.editor-content-scroll {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.no-selection,
.empty-materials {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #8fa3b3;
  text-align: center;
  gap: 0.75rem;
  padding: 2rem;
}

.no-selection i,
.empty-materials i {
  font-size: 3rem;
  opacity: 0.3;
  margin-bottom: 0.5rem;
}

.hint {
  font-size: 0.8rem;
  color: #5f7d95;
}

.add-material-form {
  background: rgba(212, 163, 115, 0.1);
  border: 1px solid rgba(212, 163, 115, 0.2);
  border-radius: 8px;
  padding: 1rem;
  flex-shrink: 0;
}

.add-material-form h4 {
  margin: 0 0 0.75rem;
  color: #d4a373;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.7rem;
  margin-bottom: 0.7rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.form-group label {
  font-size: 0.7rem;
  color: #8fa3b3;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.form-group input,
.product-select {
  padding: 0.5rem;
  background: rgba(14, 18, 26, 0.5);
  border: 1px solid rgba(212, 163, 115, 0.3);
  border-radius: 6px;
  color: #ffffff;
  font-size: 0.8rem;
  transition: all 0.3s ease;
}

.product-select {
  cursor: pointer;
}

.product-select option {
  background: #0a0f1a;
  color: #ffffff;
}

.form-group input:focus,
.product-select:focus {
  outline: none;
  border-color: #d4a373;
  box-shadow: 0 0 0 3px rgba(212, 163, 115, 0.1);
}

.quantity-input-group {
  position: relative;
  display: flex;
  align-items: center;
}

.quantity-input-group input {
  width: 100%;
  padding-right: 2.5rem;
}

.unit-badge {
  position: absolute;
  right: 0.5rem;
  background: rgba(212, 163, 115, 0.2);
  color: #d4a373;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.65rem;
  font-weight: 600;
  text-transform: uppercase;
  pointer-events: none;
}

.btn-submit {
  width: 100%;
  background: rgba(212, 163, 115, 0.25);
  color: #d4a373;
  border: 1px solid rgba(212, 163, 115, 0.5);
  padding: 0.6rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  font-size: 0.8rem;
}

.btn-submit:hover:not(:disabled) {
  background: rgba(212, 163, 115, 0.4);
  border-color: #d4a373;
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.materials-table-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.materials-table-section h4 {
  margin: 0 0 0.7rem;
  color: #d4a373;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  flex-shrink: 0;
}

.table-responsive {
  overflow: auto;
  border-radius: 8px;
  border: 1px solid rgba(212, 163, 115, 0.2);
  flex: 1;
}

.materials-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

.materials-table thead {
  background: rgba(212, 163, 115, 0.15);
  border-bottom: 2px solid rgba(212, 163, 115, 0.3);
}

.materials-table th {
  padding: 0.6rem;
  text-align: left;
  color: #d4a373;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.materials-table td {
  padding: 0.6rem;
  border-bottom: 1px solid rgba(212, 163, 115, 0.15);
  color: #e8edf2;
}

.materials-table tbody tr:hover {
  background: rgba(212, 163, 115, 0.08);
}

.product-name {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.product-name i {
  color: #d4a373;
}

.text-right {
  text-align: right;
}

.text-center {
  text-align: center;
}

.subtotal {
  color: #d4a373;
  font-weight: 600;
}

.btn-action-delete {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.3);
  width: 32px;
  height: 32px;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.btn-action-delete:hover:not(:disabled) {
  background: rgba(239, 68, 68, 0.3);
  border-color: rgba(239, 68, 68, 0.6);
  color: #f87171;
}

.btn-action-delete:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Footer */
.management-footer {
  background: rgba(212, 163, 115, 0.1);
  border-top: 1px solid rgba(212, 163, 115, 0.2);
  padding: 1rem 1.5rem;
  display: flex;
  gap: 0.8rem;
  justify-content: flex-end;
  flex-shrink: 0;
}

.btn-cancel,
.btn-complete {
  padding: 0.6rem 1.4rem;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  font-size: 0.8rem;
}

.btn-cancel {
  background: rgba(95, 125, 149, 0.15);
  color: #8fa3b3;
  border: 1px solid rgba(95, 125, 149, 0.3);
}

.btn-cancel:hover {
  background: rgba(95, 125, 149, 0.25);
  border-color: rgba(95, 125, 149, 0.5);
}

.btn-complete {
  background: rgba(212, 163, 115, 0.3);
  color: #d4a373;
  border: 1px solid rgba(212, 163, 115, 0.5);
}

.btn-complete:hover {
  background: rgba(212, 163, 115, 0.45);
  border-color: #d4a373;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(212, 163, 115, 0.2);
}

/* Scrollbar */
.points-grid::-webkit-scrollbar,
.table-responsive::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

.points-grid::-webkit-scrollbar-track,
.table-responsive::-webkit-scrollbar-track {
  background: rgba(212, 163, 115, 0.1);
}

.points-grid::-webkit-scrollbar-thumb,
.table-responsive::-webkit-scrollbar-thumb {
  background: rgba(212, 163, 115, 0.3);
  border-radius: 10px;
}

.points-grid::-webkit-scrollbar-thumb:hover,
.table-responsive::-webkit-scrollbar-thumb:hover {
  background: rgba(212, 163, 115, 0.5);
}

/* Responsive */
@media (max-width: 1024px) {
  .management-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .header-stats {
    width: 100%;
    justify-content: space-between;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .management-content {
    flex-direction: column;
  }

  .materials-list {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid rgba(212, 163, 115, 0.2);
    max-height: 35%;
  }

  .materials-editor {
    flex: 1;
  }

  .management-footer {
    flex-direction: column-reverse;
  }

  .btn-cancel,
  .btn-complete {
    width: 100%;
  }

  .add-material-form {
    margin: 1rem;
  }

  .materials-table-section {
    margin: 1rem;
  }
}
</style>
