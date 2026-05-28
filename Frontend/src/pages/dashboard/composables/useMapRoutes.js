import { ref, reactive, computed } from 'vue';

const routesState = reactive({
  routes: [],
  nextId: 1
});

export const useMapRoutes = () => {
  const allRoutes = computed(() => routesState.routes);

  const addRoute = (fromPointId, toPointId) => {
    // Evitar rutas duplicadas o rutas a sí mismo
    if (fromPointId === toPointId) return null;
    
    const alreadyExists = routesState.routes.some(
      r => (r.fromId === fromPointId && r.toId === toPointId) ||
            (r.fromId === toPointId && r.toId === fromPointId)
    );
    
    if (alreadyExists) return null;

    const newRoute = {
      id: routesState.nextId++,
      fromId: fromPointId,
      toId: toPointId,
      createdAt: new Date().toISOString(),
      distance: null, // Puede ser calculado después
      status: 'active'
    };
    
    routesState.routes.push(newRoute);
    return newRoute;
  };

  const removeRoute = (id) => {
    const index = routesState.routes.findIndex(r => r.id === id);
    if (index !== -1) {
      routesState.routes.splice(index, 1);
    }
  };

  const getRoute = (id) => {
    return routesState.routes.find(r => r.id === id);
  };

  const getRoutesBetween = (pointId) => {
    return routesState.routes.filter(r => r.fromId === pointId || r.toId === pointId);
  };

  const clearRoutes = () => {
    routesState.routes = [];
    routesState.nextId = 1;
  };

  const getRouteConnections = (pointId) => {
    const routes = getRoutesBetween(pointId);
    return routes.map(route => ({
      routeId: route.id,
      connectedPointId: route.fromId === pointId ? route.toId : route.fromId,
      direction: route.fromId === pointId ? 'outgoing' : 'incoming'
    }));
  };

  return {
    allRoutes,
    addRoute,
    removeRoute,
    getRoute,
    getRoutesBetween,
    getRouteConnections,
    clearRoutes
  };
};
