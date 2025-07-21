import axios, { AxiosError, AxiosResponse } from "axios";
import { toast } from "sonner";

// Create axios instance with base configuration
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_BACKEND_URL,
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
});

// Request interceptor to add authorization token
api.interceptors.request.use(
  (config) => {
    // Get token from localStorage
    const token = localStorage.getItem("access_token");

    // Add authorization header if token exists
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle common errors
api.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  (error: AxiosError) => {
    // Handle 401 Unauthorized errors
    if (error.response?.status === 401) {
      // Clear tokens from localStorage
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");

      // Show error message
      toast.error("Session expired. Please login again.");

      // Redirect to login page
      window.location.href = "/auth/login";
    }

    // Handle 403 Forbidden errors
    if (error.response?.status === 403) {
      toast.error(
        "Access denied. You don't have permission to perform this action."
      );
    }

    // Handle 500 Internal Server Error
    if (error.response?.status === 500) {
      toast.error("Internal server error. Please try again later.");
    }

    // Handle network errors
    if (!error.response) {
      toast.error("Network error. Please check your connection.");
    }

    return Promise.reject(error);
  }
);

// API service functions for common operations
export const apiService = {
  // Generic GET request with query parameters support
  get: <T = any>(url: string, params = {}, config = {}) =>
    api.get<T>(url, { ...config, params }),

  // Generic POST request
  post: <T = any>(url: string, data = {}, config = {}) =>
    api.post<T>(url, data, config),

  // Generic PUT request
  put: <T = any>(url: string, data = {}, config = {}) =>
    api.put<T>(url, data, config),

  // Generic PATCH request
  patch: <T = any>(url: string, data = {}, config = {}) =>
    api.patch<T>(url, data, config),

  // Generic DELETE request with query parameters support
  delete: <T = any>(url: string, params = {}, config = {}) =>
    api.delete<T>(url, { ...config, params }),

  // Photos API
  photos: {
    getAll: (params = {}) => api.get("/utils/photos/", { params }),
    getById: (id: number, params = {}) =>
      api.get(`/utils/photos/${id}/`, { params }),
    create: (formData: FormData) =>
      api.post("/utils/photos/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }),
    update: (id: number, formData: FormData) =>
      api.put(`/utils/photos/${id}/`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }),
    delete: (id: number) => api.delete(`/utils/photos/${id}/`),
  },

  // Products API
  products: {
    getAll: (params = {}) => api.get("/products/products/api/", { params }),
    getById: (id: number, params = {}) =>
      api.get(`/products/products/api/${id}/`, { params }),
    create: (data: any) => api.post("/products/products/api/", data),
    update: (id: number, data: any) =>
      api.put(`/products/products/api/${id}/`, data),
    delete: (id: number) => api.delete(`/products/products/api/${id}/`),
  },
  // Tax Groups API
  taxGroups: {
    getAll: (params = {}) => api.get("/products/tax-groups/api/", { params }),
    getById: (id: number, params = {}) =>
      api.get(`/products/tax-groups/api/${id}/`, { params }),
    create: (data: any) => api.post("/products/tax-groups/api/", data),
    update: (id: number, data: any) =>
      api.put(`/products/tax-groups/api/${id}/`, data),
    delete: (id: number) => api.delete(`/products/tax-groups/api/${id}/`),
  },

  // Product Categories API
  productCategories: {
    getAll: (params = {}) => api.get("/products/categories/api/", { params }),
    getById: (id: number, params = {}) =>
      api.get(`/products/categories/api/${id}/`, { params }),
    create: (data: any) => api.post("/products/categories/api/", data),
    update: (id: number, data: any) =>
      api.put(`/products/categories/api/${id}/`, data),
    delete: (id: number) => api.delete(`/products/categories/api/${id}/`),
  },

  // Sales API
  sales: {
    getAll: (params = {}) => api.get("sales/api/", { params }),
    getById: (id: number, params = {}) =>
      api.get(`sales/api/${id}/`, { params }),
    create: (data: any) => api.post("sales/api/", data),
    update: (id: number, data: any) => api.put(`sales/api/${id}/`, data),
    delete: (id: number) => api.delete(`sales/api/${id}/`),
  },

  // Customers API
  customers: {
    getAll: (params = {}) => api.get("/customers/api/", { params }),
    getById: (id: number, params = {}) =>
      api.get(`/customers/api/${id}/`, { params }),
    create: (data: any) => api.post("/customers/api/", data),
    update: (id: number, data: any) => api.put(`/customers/api/${id}/`, data),
    delete: (id: number) => api.delete(`/customers/api/${id}/`),
  },

  // Stock API
  stock: {
    getAll: (params = {}) => api.get("inventory/api/", { params }),
    getById: (id: number, params = {}) =>
      api.get(`inventory/api/${id}/`, { params }),
    update: (id: number, data: any) => api.put(`inventory/api/${id}/`, data),
  },

  // Reports API
  reports: {
    getSalesReport: (params = {}) => api.get("/api/reports/sales/", { params }),
    getInventoryReport: (params = {}) =>
      api.get("/api/reports/inventory/", { params }),
    getCustomerReport: (params = {}) =>
      api.get("/api/reports/customers/", { params }),
    getFinancialReport: (params = {}) =>
      api.get("/api/reports/financial/", { params }),
  },

  // Suppliers API
  suppliers: {
    getAll: (params = {}) => api.get("/suppliers/api/", { params }),
    getById: (id: number, params = {}) =>
      api.get(`/suppliers/api/${id}/`, { params }),
    create: (data: any) => api.post("/suppliers/api/", data),
    update: (id: number, data: any) => api.put(`/suppliers/api/${id}/`, data),
    delete: (id: number) => api.delete(`/suppliers/api/${id}/`),
  },

  // Settings/Profile API
  settings: {
    getProfile: (params = {}) => api.get("/api/profile/", { params }),
    updateProfile: (data: any) => api.put("/api/profile/", data),
    getBusinessSettings: (params = {}) =>
      api.get("/api/settings/business/", { params }),
    updateBusinessSettings: (data: any) =>
      api.put("/api/settings/business/", data),
    getSystemSettings: (params = {}) =>
      api.get("/api/settings/system/", { params }),
    updateSystemSettings: (data: any) => api.put("/api/settings/system/", data),
  },
  // Dashboard
  dashboard: {
    getAll: (params = {}) => api.get("dashboard/", { params }),
  },
  // Profile API
  profile: {
    get: (params = {}) => api.get("/accounts/profile/", { params }),
    update: (data: any) => api.put("/accounts/profile/", data),
  },

  // Authentication API (doesn't need token)
  auth: {
    login: (credentials: { username: string; password: string }) =>
      axios.post(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/token/`,
        credentials,
        {
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
        }
      ),
    refresh: (refreshToken: string) =>
      axios.post(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/token/refresh/`, {
        refresh: refreshToken,
      }),
    logout: () => api.get("/accounts/logout-api/"),
  },
};

// Export the configured axios instance and service
export default api;
export { api };

