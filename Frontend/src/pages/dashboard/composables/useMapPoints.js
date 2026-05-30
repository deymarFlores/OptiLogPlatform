import { ref, reactive, computed } from 'vue';
import { useSetupStore } from '@/pages/setup/composables/useSetupStore';

const pointsState = reactive({
  points: [],
  nextId: 1
});

export const useMapPoints = () => {
  const setupStore = useSetupStore();
  const setupData = setupStore.getSetupData();
  
  const allPoints = computed(() => pointsState.points);
  
  const pointsByType = computed(() => {
    const grouped = {};
    
    // Crear un grupo para cada tipo disponible
    if (setupData.pointTypes.length > 0) {
      setupData.pointTypes.forEach(type => {
        grouped[type.name] = pointsState.points.filter(p => 
          p.typeId === type.id || p.typeName === type.name
        );
      });
    } else {
      // Fallback si no hay tipos (solo para compatibilidad)
      grouped['Almacenes'] = pointsState.points.filter(p => p.typeId === 1);
      grouped['Tiendas'] = pointsState.points.filter(p => p.typeId === 2);
    }
    
    return grouped;
  });
  
  const getPointTypeNames = () => {
    return setupData.pointTypes.map(t => t.name);
  };

  const addPoint = (data) => {
    const newPoint = {
      id: pointsState.nextId++,
      name: data.name,
      typeId: data.typeId,
      typeName: data.typeName,
      icon: data.icon,
      color: data.color,
      lat: data.lat,
      lng: data.lng,
      timestamp: new Date().toISOString()
    };
    pointsState.points.push(newPoint);
    return newPoint;
  };

  const removePoint = (id) => {
    const index = pointsState.findIndex(p => p.id === id);
    if (index !== -1) {
      pointsState.points.splice(index, 1);
    }
  };

  const getPoint = (id) => {
    return pointsState.points.find(p => p.id === id);
  };

  const clearPoints = () => {
    pointsState.points = [];
    pointsState.nextId = 1;
  };

  return {
    allPoints,
    pointsByType,
    getPointTypeNames,
    addPoint,
    removePoint,
    getPoint,
    clearPoints
  };
};
