export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/';

export const API_ENDPOINTS = {
  api: API_BASE_URL,
  login: API_BASE_URL + 'auth/login',
  register: API_BASE_URL + 'auth/register',
  logout: API_BASE_URL + 'auth/logout',
  companies: API_BASE_URL + 'companies',
  typeLocations: API_BASE_URL + 'type-locations',
  typeMaterials: API_BASE_URL + 'type-materials',
  locations: API_BASE_URL + 'locations',
  orders: API_BASE_URL + 'orders'
};  

