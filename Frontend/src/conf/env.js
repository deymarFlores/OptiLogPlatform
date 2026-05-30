export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/';

export const API_ENDPOINTS = {
  login: API_BASE_URL + 'auth/login',
  register: API_BASE_URL + 'auth/register',
  logout: API_BASE_URL + 'auth/logout',
  companies: API_BASE_URL + 'api/companies',
  typeLocations: API_BASE_URL + 'api/type-locations',
  typeMaterials: API_BASE_URL + 'api/type-materials',
  locations: API_BASE_URL + 'api/locations',
  orders: API_BASE_URL + 'api/orders'
};  

