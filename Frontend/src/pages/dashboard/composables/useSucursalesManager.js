import { ref, reactive, computed } from 'vue';
import { locationsAPI } from '@/services/api';
import { useSetupStore } from '@/pages/setup/composables/useSetupStore';

const sucursalesState = reactive({
  sucursales: [],
  isEditMode: false,
  isLoading: false
});

export const useSucursalesManager = () => {
  const setupStore = useSetupStore();
  
  const getCompanyId = () => {
    const companyId = setupStore.company.value?.id;
    console.log('🔍 getCompanyId:', companyId);
    return companyId;
  };

  const sucursales = computed(() => sucursalesState.sucursales);
  const isEditMode = computed(() => sucursalesState.isEditMode);
  const isLoading = computed(() => sucursalesState.isLoading);
  const hasSucursales = computed(() => sucursalesState.sucursales.length > 0);

  const loadSucursales = async () => {
    const currentCompanyId = getCompanyId();
    console.log('📡 loadSucursales - companyId:', currentCompanyId);
    
    if (!currentCompanyId) {
      console.warn('No hay company_id disponible');
      return;
    }
    
    sucursalesState.isLoading = true;
    try {
      const result = await locationsAPI.getByCompany(currentCompanyId);
      console.log('📦 Respuesta locationsAPI:', result);
      
      if (result.success) {
        sucursalesState.sucursales = result.data;
        console.log('✅ Sucursales cargadas:', sucursalesState.sucursales.length);
      } else {
        console.error('Error al cargar sucursales:', result.error);
        sucursalesState.sucursales = [];
      }
    } catch (error) {
      console.error('Error al cargar sucursales:', error);
      sucursalesState.sucursales = [];
    } finally {
      sucursalesState.isLoading = false;
    }
  };

  const addSucursal = async (data) => {
    const currentCompanyId = getCompanyId();
    if (!currentCompanyId) {
      console.error('No hay company_id disponible');
      return null;
    }

    try {
      const result = await locationsAPI.create(currentCompanyId, {
        name: data.name,
        lat: data.lat,
        lng: data.lng,
        type_location_id: data.type_location_id
      });

      if (result.success) {
        sucursalesState.sucursales.push(result.data);
        return result.data;
      } else {
        console.error('Error al crear sucursal:', result.error);
        return null;
      }
    } catch (error) {
      console.error('Error al crear sucursal:', error);
      return null;
    }
  };

  const updateSucursal = async (locationId, data) => {
    try {
      const result = await locationsAPI.update(locationId, {
        name: data.name,
        lat: data.lat,
        lng: data.lng
      });

      if (result.success) {
        const index = sucursalesState.sucursales.findIndex(s => s.id === locationId);
        if (index !== -1) {
          sucursalesState.sucursales[index] = result.data;
        }
        return result.data;
      } else {
        console.error('Error al actualizar sucursal:', result.error);
        return null;
      }
    } catch (error) {
      console.error('Error al actualizar sucursal:', error);
      return null;
    }
  };

  const deleteSucursal = async (locationId) => {
    try {
      const result = await locationsAPI.delete(locationId);

      if (result.success) {
        const index = sucursalesState.sucursales.findIndex(s => s.id === locationId);
        if (index !== -1) {
          sucursalesState.sucursales.splice(index, 1);
        }
        return true;
      } else {
        console.error('Error al eliminar sucursal:', result.error);
        return false;
      }
    } catch (error) {
      console.error('Error al eliminar sucursal:', error);
      return false;
    }
  };

  const toggleEditMode = () => {
    sucursalesState.isEditMode = !sucursalesState.isEditMode;
  };

  const enterEditMode = () => {
    sucursalesState.isEditMode = true;
  };

  const exitEditMode = () => {
    sucursalesState.isEditMode = false;
  };

  const getSucursal = (id) => {
    return sucursalesState.sucursales.find(s => s.id === id);
  };

  return {
    sucursales,
    isEditMode,
    isLoading,
    hasSucursales,
    loadSucursales,
    addSucursal,
    updateSucursal,
    deleteSucursal,
    toggleEditMode,
    enterEditMode,
    exitEditMode,
    getSucursal
  };
};