import axios from "axios";
import { API_ENDPOINTS } from "@/conf/env";

const axiosInstance = axios.create({
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

export const loginAPI = async (email, password) => {
  try {
    const response = await axiosInstance.post(API_ENDPOINTS.login, {
      email,
      password,
    });
    return { success: true, data: response.data };
  } catch (error) {
    const errorMessage =
      error.response?.data?.message || error.message || "Error en login";
    return { success: false, error: errorMessage };
  }
};

export const registerAPI = async (name, role, email, password) => {
  try {
    const response = await axiosInstance.post(API_ENDPOINTS.register, {
      name,
      role,
      email,
      password,
    });
    return { success: true, data: response.data };
  } catch (error) {
    const errorMessage =
      error.response?.data?.message || error.message || "Error en registro";
    return { success: false, error: errorMessage };
  }
};

export const logoutAPI = async () => {
  try {
    const response = await axiosInstance.post(API_ENDPOINTS.logout);
    return { success: true, data: response.data };
  } catch (error) {
    const errorMessage =
      error.response?.data?.message || error.message || "Error en logout";
    return { success: false, error: errorMessage };
  }
};

export const companiesAPI = {
  create: async (userId, data) => {
    try {
      const response = await axiosInstance.post(
        `${API_ENDPOINTS.companies}/?user_id=${userId}`,
        data,
      );
      return { success: true, data: response.data };
    } catch (error) {
      const errorMessage =
        error.response?.data?.detail ||
        error.message ||
        "Error al crear empresa";
      return { success: false, error: errorMessage };
    }
  },

  getByUser: async (userId) => {
    try {
      const response = await axiosInstance.get(
        `${API_ENDPOINTS.companies}/user/${userId}`,
      );
      return { success: true, data: response.data };
    } catch (error) {
      const errorMessage =
        error.response?.data?.detail ||
        error.message ||
        "Error al obtener empresas";
      return { success: false, error: errorMessage };
    }
  },

  getById: async (companyId) => {
    try {
      const response = await axiosInstance.get(
        `${API_ENDPOINTS.companies}/${companyId}`,
      );
      return { success: true, data: response.data };
    } catch (error) {
      const errorMessage =
        error.response?.data?.detail ||
        error.message ||
        "Error al obtener empresa";
      return { success: false, error: errorMessage };
    }
  },

  update: async (companyId, data) => {
    try {
      const response = await axiosInstance.put(
        `${API_ENDPOINTS.companies}/${companyId}`,
        data,
      );
      return { success: true, data: response.data };
    } catch (error) {
      const errorMessage =
        error.response?.data?.detail ||
        error.message ||
        "Error al actualizar empresa";
      return { success: false, error: errorMessage };
    }
  },

  delete: async (companyId) => {
    try {
      const response = await axiosInstance.delete(
        `${API_ENDPOINTS.companies}/${companyId}`,
      );
      return { success: true, data: response.data };
    } catch (error) {
      const errorMessage =
        error.response?.data?.detail ||
        error.message ||
        "Error al eliminar empresa";
      return { success: false, error: errorMessage };
    }
  },
};

export const typeLocationsAPI = {
  create: async (companyId, data) => {
    try {
      const response = await axiosInstance.post(
        `${API_ENDPOINTS.typeLocations}/?company_id=${companyId}`,
        data,
      );
      return { success: true, data: response.data };
    } catch (error) {
      const errorMessage =
        error.response?.data?.detail ||
        error.message ||
        "Error al crear tipo de ubicación";
      return { success: false, error: errorMessage };
    }
  },

  getByCompany: async (companyId) => {
    try {
      const response = await axiosInstance.get(
        `${API_ENDPOINTS.typeLocations}/company/${companyId}`,
      );
      return { success: true, data: response.data };
    } catch (error) {
      const errorMessage =
        error.response?.data?.detail ||
        error.message ||
        "Error al obtener tipos de ubicación";
      return { success: false, error: errorMessage };
    }
  },

  getById: async (typeLocationId) => {
    try {
      const response = await axiosInstance.get(
        `${API_ENDPOINTS.typeLocations}/${typeLocationId}`,
      );
      return { success: true, data: response.data };
    } catch (error) {
      const errorMessage =
        error.response?.data?.detail ||
        error.message ||
        "Error al obtener tipo de ubicación";
      return { success: false, error: errorMessage };
    }
  },

  update: async (typeLocationId, data) => {
    try {
      const response = await axiosInstance.put(
        `${API_ENDPOINTS.typeLocations}/${typeLocationId}`,
        data,
      );
      return { success: true, data: response.data };
    } catch (error) {
      const errorMessage =
        error.response?.data?.detail ||
        error.message ||
        "Error al actualizar tipo de ubicación";
      return { success: false, error: errorMessage };
    }
  },

  delete: async (typeLocationId) => {
    try {
      const response = await axiosInstance.delete(
        `${API_ENDPOINTS.typeLocations}/${typeLocationId}`,
      );
      return { success: true, data: response.data };
    } catch (error) {
      const errorMessage =
        error.response?.data?.detail ||
        error.message ||
        "Error al eliminar tipo de ubicación";
      return { success: false, error: errorMessage };
    }
  },
};

export const locationsAPI = {
  create: async (companyId, data) => {
    try {
      const response = await axiosInstance.post(
        `${API_ENDPOINTS.locations}/?company_id=${companyId}`,
        data,
      );
      return { success: true, data: response.data };
    } catch (error) {
      const errorMessage =
        error.response?.data?.detail ||
        error.message ||
        "Error al crear sucursal";
      return { success: false, error: errorMessage };
    }
  },

  getByCompany: async (companyId) => {
    try {
      const response = await axiosInstance.get(
        `${API_ENDPOINTS.locations}/company/${companyId}`,
      );
      return { success: true, data: response.data };
    } catch (error) {
      const errorMessage =
        error.response?.data?.detail ||
        error.message ||
        "Error al obtener sucursales";
      return { success: false, error: errorMessage };
    }
  },

  getById: async (locationId) => {
    try {
      const response = await axiosInstance.get(
        `${API_ENDPOINTS.locations}/${locationId}`,
      );
      return { success: true, data: response.data };
    } catch (error) {
      const errorMessage =
        error.response?.data?.detail ||
        error.message ||
        "Error al obtener sucursal";
      return { success: false, error: errorMessage };
    }
  },

  update: async (locationId, data) => {
    try {
      const response = await axiosInstance.put(
        `${API_ENDPOINTS.locations}/${locationId}`,
        data,
      );
      return { success: true, data: response.data };
    } catch (error) {
      const errorMessage =
        error.response?.data?.detail ||
        error.message ||
        "Error al actualizar sucursal";
      return { success: false, error: errorMessage };
    }
  },

  delete: async (locationId) => {
    try {
      const response = await axiosInstance.delete(
        `${API_ENDPOINTS.locations}/${locationId}`,
      );
      return { success: true, data: response.data };
    } catch (error) {
      const errorMessage =
        error.response?.data?.detail ||
        error.message ||
        "Error al eliminar sucursal";
      return { success: false, error: errorMessage };
    }
  },
};

export const typeMaterialsAPI = {
  create: async (companyId, data) => {
    try {
      const response = await axiosInstance.post(
        `${API_ENDPOINTS.typeMaterials}/?company_id=${companyId}`,
        data,
      );
      return { success: true, data: response.data };
    } catch (error) {
      const errorMessage =
        error.response?.data?.detail ||
        error.message ||
        "Error al crear tipo de material";
      return { success: false, error: errorMessage };
    }
  },

  getByCompany: async (companyId) => {
    try {
      const response = await axiosInstance.get(
        `${API_ENDPOINTS.typeMaterials}/company/${companyId}`,
      );
      return { success: true, data: response.data };
    } catch (error) {
      const errorMessage =
        error.response?.data?.detail ||
        error.message ||
        "Error al obtener tipos de material";
      return { success: false, error: errorMessage };
    }
  },

  getById: async (typeMaterialId) => {
    try {
      const response = await axiosInstance.get(
        `${API_ENDPOINTS.typeMaterials}/${typeMaterialId}`,
      );
      return { success: true, data: response.data };
    } catch (error) {
      const errorMessage =
        error.response?.data?.detail ||
        error.message ||
        "Error al obtener tipo de material";
      return { success: false, error: errorMessage };
    }
  },

  update: async (typeMaterialId, data) => {
    try {
      const response = await axiosInstance.put(
        `${API_ENDPOINTS.typeMaterials}/${typeMaterialId}`,
        data,
      );
      return { success: true, data: response.data };
    } catch (error) {
      const errorMessage =
        error.response?.data?.detail ||
        error.message ||
        "Error al actualizar tipo de material";
      return { success: false, error: errorMessage };
    }
  },

  delete: async (typeMaterialId) => {
    try {
      const response = await axiosInstance.delete(
        `${API_ENDPOINTS.typeMaterials}/${typeMaterialId}`,
      );
      return { success: true, data: response.data };
    } catch (error) {
      const errorMessage =
        error.response?.data?.detail ||
        error.message ||
        "Error al eliminar tipo de material";
      return { success: false, error: errorMessage };
    }
  },

  search: async (query) => {
    try {
      const response = await axiosInstance.get(
        `${API_ENDPOINTS.typeMaterials}/search/?q=${encodeURIComponent(query)}`,
      );
      return { success: true, data: response.data };
    } catch (error) {
      const errorMessage =
        error.response?.data?.detail ||
        error.message ||
        "Error al buscar productos";
      return { success: false, error: errorMessage };
    }
  },
};

export const ordersAPI = {
  create: async (data) => {
    try {
      const response = await axiosInstance.post(
        `${API_ENDPOINTS.orders}`,
        data,
      );

      return response.data;
    } catch (error) {
      const errorMessage =
        error.response?.data?.detail ||
        error.message ||
        "Error al crear pedido";
      return { success: false, error: errorMessage };
    }
  },

  getByUser: async (userId) => {
    try {
      const response = await axiosInstance.get(
        `${API_ENDPOINTS.orders}/user/${userId}`,
      );

      return response.data;
    } catch (error) {
      const errorMessage =
        error.response?.data?.detail ||
        error.message ||
        "Error al obtener pedidos";
      return { success: false, error: errorMessage };
    }
  },

  getByCompany: async (companyId) => {
    try {
      const response = await axiosInstance.get(
        `${API_ENDPOINTS.orders}/company/${companyId}`,
      );

      return response.data;
    } catch (error) {
      const errorMessage =
        error.response?.data?.detail ||
        error.message ||
        "Error al obtener pedidos de empresa";
      return { success: false, error: errorMessage };
    }
  },

  getById: async (orderId) => {
    try {
      const response = await axiosInstance.get(
        `${API_ENDPOINTS.orders}/${orderId}`,
      );

      return response.data;
    } catch (error) {
      const errorMessage =
        error.response?.data?.detail ||
        error.message ||
        "Error al obtener pedido";
      return { success: false, error: errorMessage };
    }
  },
};

export default axiosInstance;
