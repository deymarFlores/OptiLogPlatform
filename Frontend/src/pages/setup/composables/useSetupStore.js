import { ref } from "vue";
import { typeMaterialsAPI } from "@/services/api";

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

  const loadProducts = async () => {
    try {
      console.log("📡 Cargando tipos de materiales...");
      const result = await typeMaterialsAPI.getAll();
      if (result.success && result.data) {
        products.value = result.data;
        saveToSessionStorage();
        console.log("✅ Tipos de materiales cargados:", products.value.length);
        return products.value;
      } else {
        console.error("Error al cargar tipos de materiales:", result.error);
        return [];
      }
    } catch (error) {
      console.error("Error en loadProducts:", error);
      return [];
    }
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
    loadProducts,
    getSetupData,
    resetSetup,
    resetSetupData,
  };
}
