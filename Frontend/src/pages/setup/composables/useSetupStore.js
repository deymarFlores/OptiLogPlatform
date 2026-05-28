import { ref, reactive } from 'vue';

const setupState = reactive({
  company: {
    name: '',
    description: '',
    city: '',
    phone: ''
  },
  pointTypes: []
});

export function useSetupStore() {
  const setCompany = (data) => {
    setupState.company = {
      name: data.name,
      description: data.description,
      city: data.city,
      phone: data.phone
    };
  };

  const setPointTypes = (types) => {
    setupState.pointTypes = types;
  };

  const getSetupData = () => ({
    company: setupState.company,
    pointTypes: setupState.pointTypes
  });

  const resetSetup = () => {
    setupState.company = {
      name: '',
      description: '',
      city: '',
      phone: ''
    };
    setupState.pointTypes = [];
  };

  return {
    company: setupState.company,
    pointTypes: setupState.pointTypes,
    setCompany,
    setPointTypes,
    getSetupData,
    resetSetup
  };
}
