import { ref, reactive, computed } from 'vue';

const pointsState = reactive({
  points: [],
  nextId: 1
});

export const useMapPoints = () => {
  const allPoints = computed(() => pointsState.points);
  
  const pointsByType = computed(() => {
    return {
      almacenes: pointsState.points.filter(p => p.typeId === 1),
      tiendas: pointsState.points.filter(p => p.typeId === 2)
    };
  });

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
    const index = pointsState.points.findIndex(p => p.id === id);
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
    addPoint,
    removePoint,
    getPoint,
    clearPoints
  };
};
