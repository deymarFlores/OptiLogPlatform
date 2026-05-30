<template>
  <div class="form-container">
    <h2>Tipos de Productos de tu Empresa</h2>
    <p class="form-subtitle">
      Define los tipos de productos que tu empresa ofrece
    </p>

    <div v-if="isLoading" class="loading-spinner">
      <i class="fas fa-spinner fa-spin"></i> Cargando...
    </div>

    <div v-else class="products-list">
      <div
        v-for="product in form.products"
        :key="product.id"
        class="product-item"
      >
        <div class="product-header">
          <input
            v-model="product.name"
            type="text"
            class="product-name"
            placeholder="Ej: Producto A, Servicio B"
          />
          <button
            type="button"
            class="btn-remove"
            @click="removeProduct(product.id)"
            :disabled="isDeleting"
          >
            <i class="fas fa-trash"></i>
          </button>
        </div>
        <div class="product-details">
          <div class="detail-group">
            <label>Unidad de Medida</label>
            <select v-model="product.units" class="unit-select">
              <option value="">Seleccionar...</option>
              <option value="unidad">Unidad</option>
              <option value="kg">Kilogramo (kg)</option>
              <option value="g">Gramo (g)</option>
              <option value="L">Litro (L)</option>
              <option value="mL">Mililitro (mL)</option>
              <option value="m">Metro (m)</option>
              <option value="cm">Centímetro (cm)</option>
              <option value="h">Hora (h)</option>
              <option value="otro">Otro</option>
            </select>
          </div>
          <div class="detail-group">
            <label>Precio por {{ product.units || "unidad" }} (Bs.)</label>
            <input
              v-model.number="product.price"
              type="number"
              class="price-input"
              placeholder="0.00"
              step="0.01"
              min="0"
            />
          </div>
        </div>
      </div>
    </div>

    <button
      type="button"
      class="btn-add"
      @click="addProduct"
      :disabled="isLoading"
    >
      <i class="fas fa-plus"></i> Agregar Tipo de Producto
    </button>

    <div class="form-actions">
      <button
        type="button"
        class="btn-back"
        @click="$emit('back')"
        :disabled="isLoading"
      >
        <i class="fas fa-arrow-left"></i> Atrás
      </button>
      <button
        type="button"
        class="btn-complete"
        @click="handleComplete"
        :disabled="isLoading || isSaving"
      >
        <i v-if="isSaving" class="fas fa-spinner fa-spin"></i>
        <i v-else class="fas fa-check"></i>
        {{ isSaving ? "Guardando..." : "Completar Configuración" }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useSetupStore } from "@/pages/setup/composables/useSetupStore";
import {
  companiesAPI,
  typeLocationsAPI,
  typeMaterialsAPI,
} from "@/services/api";

const emit = defineEmits(["back", "complete"]);
const setupStore = useSetupStore();

const form = ref({
  products: [],
});

const isLoading = ref(false);
const isSaving = ref(false);
const isDeleting = ref(false);

let nextId = 1;

const loadProducts = async () => {
  const companyId = setupStore.company.value?.id;

  if (!companyId) {
    console.warn("No hay company_id disponible");
    const savedCompany = sessionStorage.getItem("setupCompany");
    if (savedCompany) {
      const company = JSON.parse(savedCompany);
      if (company.id) {
        setupStore.setCompany(company);
        return loadProducts();
      }
    }
    return;
  }

  isLoading.value = true;

  form.value.products = [];

  const result = await typeMaterialsAPI.getByCompany(companyId);

  if (result.success && result.data.length > 0) {
    form.value.products = result.data;
    if (result.data.length > 0) {
      nextId =
        Math.max(...result.data.map((p) => parseInt(p.id.slice(-1)))) + 1 || 1;
    } else {
      nextId = 1;
    }
  } else {
    form.value.products = [];
    nextId = 1;
  }

  isLoading.value = false;
};

const addProduct = () => {
  form.value.products.push({
    id: `new-${Date.now()}`,
    name: "",
    units: "",
    price: 0,
  });
};

const removeProduct = async (id) => {
  form.value.products = form.value.products.filter((p) => p.id !== id);
};

const handleComplete = async () => {
  const validProducts = form.value.products.filter(
    (p) => p.name.trim() && p.units && p.price > 0,
  );

  if (validProducts.length === 0) {
    console.warn("No hay productos válidos");
    return;
  }

  isSaving.value = true;

  try {
    setupStore.setProducts(validProducts);
    console.log("📝 Productos guardados en memoria (paso 3):", validProducts);

    const userId = setupStore.userId.value;
    const company = setupStore.company.value;
    const pointTypes = setupStore.pointTypes.value;
    const products = validProducts;

    console.log("🚀 Iniciando envío de datos al backend...");
    console.log("  - userId:", userId);
    console.log("  - empresa:", company);
    console.log("  - tipos:", pointTypes);
    console.log("  - productos:", products);

    console.log("📤 Paso 1: Crear empresa...");
    const companyResult = await companiesAPI.create(userId, {
      name: company.name,
      address: company.city,
      phone: company.phone,
      description: company.description,
    });

    if (!companyResult.success) {
      console.error("Error al crear empresa:", companyResult.error);
      alert("Error al crear la empresa: " + companyResult.error);
      isSaving.value = false;
      return;
    }

    const companyId = companyResult.data.id;
    console.log("✅ Empresa creada con ID:", companyId);

    setupStore.setCompany({
      ...company,
      id: companyId,
    });

    console.log("📤 Paso 2: Crear tipos de ubicación...");
    const createdTypes = [];
    for (const type of pointTypes) {
      const typeResult = await typeLocationsAPI.create(companyId, {
        name: type.name,
        icon: type.icon,
        color: type.color,
      });

      if (!typeResult.success) {
        console.error("Error al crear tipo de ubicación:", typeResult.error);
        alert("Error al crear tipos de ubicación: " + typeResult.error);
        isSaving.value = false;
        return;
      }

      createdTypes.push(typeResult.data);
      console.log("✅ Tipo creado:", typeResult.data.name);
    }

    console.log("📤 Paso 3: Crear productos/materiales...");
    const createdProducts = [];
    for (const product of products) {
      const productResult = await typeMaterialsAPI.create(companyId, {
        name: product.name,
        units: product.units,
        price: product.price,
      });

      if (!productResult.success) {
        console.error("Error al crear producto:", productResult.error);
        alert("Error al crear productos: " + productResult.error);
        isSaving.value = false;
        return;
      }

      createdProducts.push(productResult.data);
      console.log("✅ Producto creado:", productResult.data.name);
    }

    console.log("✅ ¡SETUP COMPLETADO! Todos los datos enviados al backend");
    console.log("  - Empresa: " + companyId);
    console.log("  - Tipos creados: " + createdTypes.length);
    console.log("  - Productos creados: " + createdProducts.length);

    emit("complete");
  } catch (error) {
    console.error("Error inesperado:", error);
    alert("Error durante la configuración: " + error.message);
  } finally {
    isSaving.value = false;
  }
};

onMounted(() => {
  form.value.products = [];

  if (setupStore.products.value && setupStore.products.value.length > 0) {
    console.log("📌 Empresa con productos existentes, cargando...");
    setTimeout(() => {
      loadProducts();
    }, 100);
  } else {
    console.log("📌 Empresa nueva, formulario vacío");
    isLoading.value = false;
  }
});
</script>

<style scoped>
.form-container {
  animation: slideIn 0.4s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.loading-spinner {
  text-align: center;
  padding: 2rem;
  color: #d4a373;
  font-size: 1.1rem;
}

h2 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: #ffffff;
}

.form-subtitle {
  color: #a0abb9;
  font-size: 0.9rem;
  margin-bottom: 1.5rem;
}

.products-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
  max-height: 300px;
  overflow-y: auto;
}

.product-item {
  background: rgba(10, 15, 26, 0.4);
  border: 1px solid rgba(212, 163, 115, 0.2);
  border-radius: 1rem;
  padding: 1rem;
}

.product-header {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.product-name {
  flex: 1;
  background: rgba(10, 15, 26, 0.6);
  border: 1px solid rgba(212, 163, 115, 0.3);
  border-radius: 0.5rem;
  padding: 0.6rem 0.8rem;
  color: #e8edf2;
  font-size: 0.9rem;
  font-weight: 600;
}

.product-name:focus {
  outline: none;
  border-color: #d4a373;
}

.btn-remove {
  background: rgba(224, 61, 61, 0.2);
  border: 1px solid rgba(224, 61, 61, 0.4);
  color: #e05a5a;
  width: 40px;
  height: 40px;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-remove:hover:not(:disabled) {
  background: rgba(224, 61, 61, 0.3);
}

.btn-remove:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.product-details {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}

.detail-group {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

label {
  font-size: 0.75rem;
  color: #a0abb9;
  font-weight: 600;
  text-transform: uppercase;
}

.price-input {
  padding: 0.5rem;
  background: rgba(10, 15, 26, 0.6);
  border: 1px solid rgba(212, 163, 115, 0.3);
  border-radius: 0.4rem;
  color: #e8edf2;
  font-size: 0.8rem;
}

.price-input:focus {
  outline: none;
  border-color: #d4a373;
}

.unit-select {
  padding: 0.5rem;
  background: rgba(10, 15, 26, 0.6);
  border: 1px solid rgba(212, 163, 115, 0.3);
  border-radius: 0.4rem;
  color: #e8edf2;
  font-size: 0.8rem;
  cursor: pointer;
}

.unit-select:focus {
  outline: none;
  border-color: #d4a373;
}

.unit-select option {
  background: #0a0f1a;
  color: #e8edf2;
}

.btn-add {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  padding: 0.8rem;
  background: rgba(212, 163, 115, 0.1);
  border: 1px dashed rgba(212, 163, 115, 0.5);
  color: #d4a373;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 600;
  margin-bottom: 1.5rem;
  transition: all 0.3s ease;
}

.btn-add:hover:not(:disabled) {
  background: rgba(212, 163, 115, 0.2);
  border-color: #d4a373;
}

.btn-add:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn-back,
.btn-complete {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.8rem;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.btn-back {
  background: rgba(160, 171, 185, 0.1);
  color: #a0abb9;
}

.btn-back:hover:not(:disabled) {
  background: rgba(160, 171, 185, 0.2);
}

.btn-complete {
  background: rgba(212, 163, 115, 0.3);
  color: #d4a373;
}

.btn-complete:hover:not(:disabled) {
  background: rgba(212, 163, 115, 0.4);
}

.btn-back:disabled,
.btn-complete:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 600px) {
  h2 {
    font-size: 1.25rem;
  }

  .products-list {
    max-height: 250px;
  }

  .product-details {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column;
  }
}
</style>
