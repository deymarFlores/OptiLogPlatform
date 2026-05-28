<template>
  <div class="form-container">
    <h2>Productos de tu Empresa</h2>
    <p class="form-subtitle">Define los productos que tu empresa ofrece</p>

    <div class="products-list">
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
          <button type="button" class="btn-remove" @click="removeProduct(product.id)">
            <i class="fas fa-trash"></i>
          </button>
        </div>
        <div class="product-details">
          <div class="detail-group">
            <label>Unidad de Medida</label>
            <select v-model="product.unit" class="unit-select">
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
            <label>Precio por {{ product.unit || 'unidad' }} (Bs.)</label>
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

    <button type="button" class="btn-add" @click="addProduct">
      <i class="fas fa-plus"></i> Agregar Producto
    </button>

    <div class="form-actions">
      <button type="button" class="btn-back" @click="$emit('back')">
        <i class="fas fa-arrow-left"></i> Atrás
      </button>
      <button type="button" class="btn-complete" @click="handleComplete">
        <i class="fas fa-check"></i> Completar Configuración
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useSetupStore } from '@/pages/setup/composables/useSetupStore';

const emit = defineEmits(['back', 'complete']);
const setupStore = useSetupStore();

const form = ref({
  products: setupStore.products.length
    ? setupStore.products
    : []
});

let nextId = 1;

const addProduct = () => {
  form.value.products.push({
    id: nextId++,
    name: '',
    unit: '',
    price: 0
  });
};

const removeProduct = (id) => {
  form.value.products = form.value.products.filter(p => p.id !== id);
};

const handleComplete = () => {
  const validProducts = form.value.products.filter(
    p => p.name.trim() && p.unit && p.price > 0
  );

  if (validProducts.length === 0) {
    console.error('❌ Debes agregar al menos un producto con nombre, unidad y precio');
    return;
  }

  setupStore.setProducts(validProducts);

  console.log('✅ Productos registrados:', validProducts);
  console.log('📋 Configuración completa:', setupStore.getSetupData());

  emit('complete');
};
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

.btn-remove:hover {
  background: rgba(224, 61, 61, 0.3);
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

.detail-group label {
  font-size: 0.65rem;
  color: #8e9aab;
  text-transform: uppercase;
  font-weight: 600;
  letter-spacing: 0.5px;
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
  width: 100%;
  padding: 0.8rem;
  background: rgba(212, 163, 115, 0.15);
  border: 1px dashed rgba(212, 163, 115, 0.4);
  color: #d4a373;
  border-radius: 0.8rem;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  margin-bottom: 1.5rem;
}

.btn-add:hover {
  background: rgba(212, 163, 115, 0.25);
  border-color: #d4a373;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn-back,
.btn-complete {
  flex: 1;
  padding: 0.8rem;
  border: none;
  border-radius: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.btn-back {
  background: rgba(212, 163, 115, 0.1);
  color: #d4a373;
  border: 1px solid rgba(212, 163, 115, 0.3);
}

.btn-back:hover {
  background: rgba(212, 163, 115, 0.2);
}

.btn-complete {
  background: #d4a373;
  color: #0a0f1a;
}

.btn-complete:hover {
  background: #e0b082;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(212, 163, 115, 0.3);
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
