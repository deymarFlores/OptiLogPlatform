import { ref } from "vue";

const initializeFromSessionStorage = () => {
  try {
    const stored = sessionStorage.getItem("setupStore");
    if (stored) {
      return JSON.parse(stored);
    }
  } catch (error) {
    console.error("Error al parsear setupStore del sessionStorage:", error);
  }
  return null;
};

const storedData = initializeFromSessionStorage();

const userId = ref(storedData?.userId || "");
const company = ref(
  storedData?.company || {
    id: "",
    name: "",
    description: "",
    city: "",
    phone: "",
  },
);
const pointTypes = ref(storedData?.pointTypes || []);
const products = ref(storedData?.products || []);

const saveToSessionStorage = () => {
  try {
    const data = {
      userId: userId.value,
      company: company.value,
      pointTypes: pointTypes.value,
      products: products.value,
    };
    sessionStorage.setItem("setupStore", JSON.stringify(data));
  } catch (error) {
    console.error("Error al guardar setupStore en sessionStorage:", error);
  }
};

export function useSetupStore() {
  const setUserId = (id) => {
    console.log("🔧 setUserId:", id);
    userId.value = id;
    saveToSessionStorage();
  };

  const setCompany = (data) => {
    console.log("🔧 setCompany:", data);
    company.value = {
      id: data.id || "",
      name: data.name || "",
      description: data.description || "",
      city: data.city || "",
      phone: data.phone || "",
    };
    console.log("🔧 company.value después:", company.value);
    saveToSessionStorage();
  };

  const setPointTypes = (types) => {
    pointTypes.value = types;
    saveToSessionStorage();
  };

  const setProducts = (productsData) => {
    products.value = productsData;
    saveToSessionStorage();
  };

  const getSetupData = () => ({
    userId: userId.value,
    company: company.value,
    pointTypes: pointTypes.value,
    products: products.value,
  });

  const resetSetup = () => {
    userId.value = "";
    company.value = {
      id: "",
      name: "",
      description: "",
      city: "",
      phone: "",
    };
    pointTypes.value = [];
    products.value = [];
    sessionStorage.removeItem("setupStore");
  };

  const resetSetupData = () => {
    company.value = {
      id: "",
      name: "",
      description: "",
      city: "",
      phone: "",
    };
    pointTypes.value = [];
    products.value = [];
    sessionStorage.removeItem("setupStore");
  };

  return {
    userId: userId,
    company: company,
    pointTypes: pointTypes,
    products: products,
    setUserId,
    setCompany,
    setPointTypes,
    setProducts,
    getSetupData,
    resetSetup,
    resetSetupData,
  };
}
