import { ref, reactive } from 'vue';

const setupState = reactive({
  company: {
    name: '',
    description: '',
    city: '',
    phone: ''
  },
  pointTypes: [],
  products: []
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

  const setProducts = (products) => {
    setupState.products = products;
  };

  const getSetupData = () => ({
    company: setupState.company,
    pointTypes: setupState.pointTypes,
    products: setupState.products
  });

  const resetSetup = () => {
    setupState.company = {
      name: '',
      description: '',
      city: '',
      phone: ''
    };
    setupState.pointTypes = [];
    setupState.products = [];
  };

  return {
    company: setupState.company,
    pointTypes: setupState.pointTypes,
    products: setupState.products,
    setCompany,
    setPointTypes,
    setProducts,
    getSetupData,
    resetSetup
  };
}
