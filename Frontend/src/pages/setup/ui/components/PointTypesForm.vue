<template>
  <div class="form-container">
    <h2>Tipos de Puntos de Distribución</h2>
    <p class="form-subtitle">
      Define los tipos de ubicaciones de sucursales que tu empresa maneja
    </p>

    <div v-if="isLoading" class="loading-spinner">
      <i class="fas fa-spinner fa-spin"></i> Cargando...
    </div>

    <div v-else class="points-list">
      <div
        v-for="pointType in form.pointTypes"
        :key="pointType.id"
        class="point-item"
      >
        <div class="point-header">
          <input
            v-model="pointType.name"
            type="text"
            class="point-name"
            placeholder="Ej: Almacén, Tienda, Centro de Distribución"
          />
          <button
            type="button"
            class="btn-remove"
            @click="removePointType(pointType.id)"
            :disabled="isDeleting"
          >
            <i class="fas fa-trash"></i>
          </button>
        </div>
        <div class="point-details">
          <div class="detail-group">
            <label>Icono</label>
            <select v-model="pointType.icon" class="icon-select">
              <option value="fa-warehouse">📦 Almacén</option>
              <option value="fa-store">🏪 Tienda</option>
              <option value="fa-truck">🚚 Centro de Distribución</option>
              <option value="fa-boxes">📫 Punto de Recepción</option>
              <option value="fa-location-dot">📍 Sucursal</option>
            </select>
          </div>
          <div class="detail-group">
            <label>Color</label>
            <input v-model="pointType.color" type="color" class="color-input" />
          </div>
        </div>
      </div>
    </div>

    <button
      type="button"
      class="btn-add"
      @click="addPointType"
      :disabled="isLoading"
    >
      <i class="fas fa-plus"></i> Agregar Tipo de Ubicación
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
      <button type="button" class="btn-complete" @click="handleNext">
        <i class="fas fa-arrow-right"></i>
        Siguiente
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useSetupStore } from "@/pages/setup/composables/useSetupStore";
import { typeLocationsAPI } from "@/services/api";

const emit = defineEmits(["back", "next"]);
const setupStore = useSetupStore();

const form = ref({
  pointTypes: [],
});

const isLoading = ref(false);
const isDeleting = ref(false);

let nextId = 1;

const loadPointTypes = async () => {
  const companyId = setupStore.company.value?.id;

  if (!companyId) {
    console.warn("No hay company_id disponible");
    const savedCompany = sessionStorage.getItem("setupCompany");
    if (savedCompany) {
      const company = JSON.parse(savedCompany);
      if (company.id) {
        setupStore.setCompany(company);
        return loadPointTypes();
      }
    }
    return;
  }

  isLoading.value = true;

  form.value.pointTypes = [];

  const result = await typeLocationsAPI.getByCompany(companyId);

  if (result.success && result.data.length > 0) {
    form.value.pointTypes = result.data;
    if (result.data.length > 0) {
      nextId =
        Math.max(...result.data.map((pt) => parseInt(pt.id.slice(-1)))) + 1 ||
        1;
    } else {
      nextId = 1;
    }
  } else {
    form.value.pointTypes = [];
    nextId = 1;
  }

  isLoading.value = false;
};

const addPointType = () => {
  form.value.pointTypes.push({
    id: `new-${Date.now()}`,
    name: "",
    icon: "fa-warehouse",
    color: "#" + Math.floor(Math.random() * 16777215).toString(16),
  });
};

const removePointType = async (id) => {
  form.value.pointTypes = form.value.pointTypes.filter((pt) => pt.id !== id);
};

const handleNext = () => {
  const validTypes = form.value.pointTypes.filter((pt) => pt.name.trim());

  if (validTypes.length === 0) {
    console.warn("No hay tipos de ubicación válidos");
    return;
  }

  setupStore.setPointTypes(validTypes);
  console.log(
    "📝 Tipos de ubicación guardados en memoria (paso 2):",
    validTypes,
  );
  emit("next");
};

onMounted(() => {
  form.value.pointTypes = [];

  if (setupStore.pointTypes.value && setupStore.pointTypes.value.length > 0) {
    console.log("📌 Empresa con tipos existentes, cargando...");
    setTimeout(() => {
      loadPointTypes();
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

.points-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
  max-height: 300px;
  overflow-y: auto;
}

.point-item {
  background: rgba(10, 15, 26, 0.4);
  border: 1px solid rgba(212, 163, 115, 0.2);
  border-radius: 1rem;
  padding: 1rem;
}

.point-header {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.point-name {
  flex: 1;
  background: rgba(10, 15, 26, 0.6);
  border: 1px solid rgba(212, 163, 115, 0.3);
  border-radius: 0.5rem;
  padding: 0.6rem 0.8rem;
  color: #e8edf2;
  font-size: 0.9rem;
  font-weight: 600;
}

.point-name:focus {
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

.point-details {
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

.icon-select,
.color-input {
  background: rgba(10, 15, 26, 0.6);
  border: 1px solid rgba(212, 163, 115, 0.3);
  border-radius: 0.5rem;
  padding: 0.5rem;
  color: #e8edf2;
  font-size: 0.85rem;
  cursor: pointer;
}

.icon-select:focus,
.color-input:focus {
  outline: none;
  border-color: #d4a373;
}

.color-input {
  height: 40px;
}

.btn-add {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  background: rgba(212, 163, 115, 0.1);
  border: 1px dashed rgba(212, 163, 115, 0.5);
  color: #d4a373;
  padding: 0.8rem;
  border-radius: 0.5rem;
  cursor: pointer;
  margin-bottom: 1.5rem;
  transition: all 0.3s ease;
  font-weight: 600;
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
  justify-content: space-between;
}

.btn-back,
.btn-complete {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.8rem 1.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  border: none;
}

.btn-back {
  flex: 1;
  background: rgba(160, 171, 185, 0.1);
  color: #a0abb9;
}

.btn-back:hover:not(:disabled) {
  background: rgba(160, 171, 185, 0.2);
}

.btn-complete {
  flex: 1;
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

.detail-group label {
  font-size: 0.65rem;
  color: #8e9aab;
  text-transform: uppercase;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.icon-select,
.color-input {
  padding: 0.5rem;
  background: rgba(10, 15, 26, 0.6);
  border: 1px solid rgba(212, 163, 115, 0.3);
  border-radius: 0.4rem;
  color: #e8edf2;
  font-size: 0.8rem;
  cursor: pointer;
}

.icon-select:focus,
.color-input:focus {
  outline: none;
  border-color: #d4a373;
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

  .points-list {
    max-height: 250px;
  }

  .point-details {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column;
  }
}
</style>
