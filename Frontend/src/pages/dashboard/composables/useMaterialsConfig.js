import { reactive, computed } from 'vue';

// Almacenamiento de materiales por punto
const materialsState = reactive({
  pointMaterials: {}, // { pointId: [{ id, type, quantity, price }, ...] }
  nextMaterialId: 1000
});

export function useMaterialsConfig() {
  // Obtener materiales de un punto específico
  const getMaterialsByPoint = (pointId) => {
    return materialsState.pointMaterials[pointId] || [];
  };

  // Obtener todos los materiales con info del punto
  const getAllMaterials = computed(() => {
    return materialsState.pointMaterials;
  });

  // Agregar material a un punto
  const addMaterial = (pointId, material) => {
    if (!materialsState.pointMaterials[pointId]) {
      materialsState.pointMaterials[pointId] = [];
    }

    const newMaterial = {
      id: materialsState.nextMaterialId++,
      type: material.type,
      quantity: material.quantity, // en toneladas
      price: material.price,
      timestamp: new Date().toISOString()
    };

    materialsState.pointMaterials[pointId].push(newMaterial);
    return newMaterial;
  };

  // Actualizar material
  const updateMaterial = (pointId, materialId, updates) => {
    const materials = materialsState.pointMaterials[pointId];
    if (materials) {
      const material = materials.find(m => m.id === materialId);
      if (material) {
        Object.assign(material, updates);
      }
    }
  };

  // Eliminar material
  const removeMaterial = (pointId, materialId) => {
    if (materialsState.pointMaterials[pointId]) {
      materialsState.pointMaterials[pointId] = materialsState.pointMaterials[pointId].filter(
        m => m.id !== materialId
      );
    }
  };

  // Obtener resumen de materiales por punto
  const getMaterialsSummary = (pointId) => {
    const materials = getMaterialsByPoint(pointId);
    if (materials.length === 0) return null;

    const totalQuantity = materials.reduce((sum, m) => sum + parseFloat(m.quantity || 0), 0);
    const totalValue = materials.reduce((sum, m) => sum + (parseFloat(m.quantity || 0) * parseFloat(m.price || 0)), 0);

    return {
      count: materials.length,
      totalQuantity,
      totalValue,
      materials
    };
  };

  // Limpiar materiales de todos los puntos
  const clearMaterials = () => {
    materialsState.pointMaterials = {};
    materialsState.nextMaterialId = 1000;
  };

  // Obtener config para exportar
  const getConfigData = () => {
    return {
      materials: { ...materialsState.pointMaterials },
      nextMaterialId: materialsState.nextMaterialId
    };
  };

  // Restaurar config
  const loadConfigData = (data) => {
    if (data && data.materials) {
      materialsState.pointMaterials = { ...data.materials };
      materialsState.nextMaterialId = data.nextMaterialId || 1000;
    }
  };

  return {
    getMaterialsByPoint,
    getAllMaterials,
    addMaterial,
    updateMaterial,
    removeMaterial,
    getMaterialsSummary,
    clearMaterials,
    getConfigData,
    loadConfigData
  };
}
