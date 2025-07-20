import { api, apiService } from "@/lib/api";
import { useEffect, useRef, useState } from "react";
import { toast } from "sonner";

// Cache interface
interface CacheEntry<T> {
  data: T;
  timestamp: number;
  loading: boolean;
  error: string | null;
}

// Global cache for API data
const apiCache = new Map<string, CacheEntry<any>>();

// Cache duration in milliseconds (5 minutes)
const CACHE_DURATION = 5 * 60 * 1000;

// Function to generate cache key
function getCacheKey(endpoint: string, params: any = {}): string {
  return `${endpoint}_${JSON.stringify(params)}`;
}

// Function to check if cache is valid
function isCacheValid(cacheEntry: CacheEntry<any>): boolean {
  return Date.now() - cacheEntry.timestamp < CACHE_DURATION;
}

// Pagination interface for API responses
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// Generic hook for API calls with caching
export function useApi<T = any>(
  apiCall: () => Promise<any>,
  dependencies: any[] = [],
  cacheKey?: string
) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const hasInitialized = useRef(false);

  const fetchData = async (forceRefresh = false) => {
    try {
      // Generate cache key if provided
      const key = cacheKey || `api_${JSON.stringify(dependencies)}`;

      // Check cache first if not forcing refresh
      if (!forceRefresh && cacheKey) {
        const cached = apiCache.get(key);
        if (cached && isCacheValid(cached)) {
          setData(cached.data);
          setLoading(false);
          setError(cached.error);
          return;
        }
      }

      setLoading(true);
      setError(null);
      const response = await apiCall();
      const responseData = response.data;

      setData(responseData);

      // Cache the response if cache key is provided
      if (cacheKey) {
        apiCache.set(key, {
          data: responseData,
          timestamp: Date.now(),
          loading: false,
          error: null,
        });
      }
    } catch (err: any) {
      const errorMessage =
        err.response?.data?.message || err.message || "An error occurred";
      setError(errorMessage);
      toast.error(errorMessage);

      // Cache the error if cache key is provided
      if (cacheKey) {
        const key = cacheKey || `api_${JSON.stringify(dependencies)}`;
        apiCache.set(key, {
          data: null,
          timestamp: Date.now(),
          loading: false,
          error: errorMessage,
        });
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!hasInitialized.current) {
      hasInitialized.current = true;
      fetchData();
    }
  }, dependencies);

  return { data, loading, error, refetch: () => fetchData(true) };
}

// Generic hook for paginated API calls with caching
export function usePaginatedApi<T = any>(
  apiCall: (params?: any) => Promise<any>,
  dependencies: any[] = [],
  initialParams: any = {},
  baseCacheKey?: string
) {
  const [data, setData] = useState<T[]>([]);
  const [paginationInfo, setPaginationInfo] = useState({
    count: 0,
    next: null as string | null,
    previous: null as string | null,
    hasNext: false,
    hasPrevious: false,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [params, setParams] = useState(initialParams);
  const hasInitialized = useRef(false);

  const fetchData = async (newParams = params, forceRefresh = false) => {
    try {
      // Generate cache key based on parameters
      const cacheKey = baseCacheKey
        ? `${baseCacheKey}_${getCacheKey(newParams)}`
        : undefined;

      // Check cache first if not forcing refresh
      if (!forceRefresh && cacheKey) {
        const cached = apiCache.get(cacheKey);
        if (cached && isCacheValid(cached)) {
          const cachedData = cached.data as PaginatedResponse<T>;
          setData(cachedData.results);
          setPaginationInfo({
            count: cachedData.count,
            next: cachedData.next,
            previous: cachedData.previous,
            hasNext: cachedData.next !== null,
            hasPrevious: cachedData.previous !== null,
          });
          setLoading(false);
          setError(cached.error);
          return;
        }
      }

      setLoading(true);
      setError(null);
      const response = await apiCall(newParams);
      const responseData = response.data as PaginatedResponse<T>;

      setData(responseData.results);
      setPaginationInfo({
        count: responseData.count,
        next: responseData.next,
        previous: responseData.previous,
        hasNext: responseData.next !== null,
        hasPrevious: responseData.previous !== null,
      });

      // Cache the response if cache key is provided
      if (cacheKey) {
        apiCache.set(cacheKey, {
          data: responseData,
          timestamp: Date.now(),
          loading: false,
          error: null,
        });
      }
    } catch (err: any) {
      const errorMessage =
        err.response?.data?.message || err.message || "An error occurred";
      setError(errorMessage);
      toast.error(errorMessage);

      // Cache the error if cache key is provided
      if (baseCacheKey) {
        const cacheKey = `${baseCacheKey}_${getCacheKey(newParams)}`;
        apiCache.set(cacheKey, {
          data: null,
          timestamp: Date.now(),
          loading: false,
          error: errorMessage,
        });
      }
    } finally {
      setLoading(false);
    }
  };

  const loadMore = async () => {
    if (!paginationInfo.hasNext) return;

    try {
      const nextParams = { ...params, offset: data.length };
      const response = await apiCall(nextParams);
      const responseData = response.data as PaginatedResponse<T>;

      setData((prev) => [...prev, ...responseData.results]);
      setPaginationInfo({
        count: responseData.count,
        next: responseData.next,
        previous: responseData.previous,
        hasNext: responseData.next !== null,
        hasPrevious: responseData.previous !== null,
      });
    } catch (err: any) {
      const errorMessage =
        err.response?.data?.message || err.message || "An error occurred";
      setError(errorMessage);
      toast.error(errorMessage);
    }
  };

  const updateParams = (newParams: any) => {
    setParams(newParams);
    fetchData(newParams, true); // Force refresh with new params
  };

  useEffect(() => {
    if (!hasInitialized.current) {
      hasInitialized.current = true;
      fetchData();
    }
  }, dependencies);

  return {
    data,
    loading,
    error,
    paginationInfo,
    refetch: () => fetchData(params, true),
    loadMore,
    updateParams,
    setParams: updateParams,
  };
}

// Hook for products with pagination and caching
export function useProducts(params = {}) {
  return usePaginatedApi(
    (p) => apiService.products.getAll(p),
    [],
    params,
    "products"
  );
}

// Hook for sales with pagination and caching
export function useSales(params = {}) {
  return usePaginatedApi(
    (p) => apiService.sales.getAll(p),
    [],
    params,
    "sales"
  );
}

// Hook for customers with pagination and caching
export function useCustomers(params = {}) {
  return usePaginatedApi(
    (p) => apiService.customers.getAll(p),
    [],
    params,
    "customers"
  );
}

// Hook for stock with pagination and caching
export function useStock(params = {}) {
  return usePaginatedApi(
    (p) => apiService.stock.getAll(p),
    [],
    params,
    "stock"
  );
}

// Hook for suppliers with pagination and caching
export function useSuppliers(params = {}) {
  return usePaginatedApi(
    (p) => apiService.suppliers.getAll(p),
    [],
    params,
    "suppliers"
  );
}

// Hook for product categories with pagination and caching
export function useProductCategories(params = {}) {
  return usePaginatedApi(
    (p) => apiService.productCategories.getAll(p),
    [],
    params,
    "product_categories"
  );
}

// Legacy hooks for backward compatibility (returns results array)
export function useProductsLegacy() {
  const { data } = useApi(() => apiService.products.getAll());
  return { data: data?.results || [], loading: false, error: null };
}

export function useSalesLegacy() {
  const { data } = useApi(() => apiService.sales.getAll());
  return { data: data?.results || [], loading: false, error: null };
}

export function useCustomersLegacy() {
  const { data } = useApi(() => apiService.customers.getAll());
  return { data: data?.results || [], loading: false, error: null };
}

export function useStockLegacy() {
  const { data } = useApi(() => apiService.stock.getAll());
  return { data: data?.results || [], loading: false, error: null };
}

export function useSuppliersLegacy() {
  const { data } = useApi(() => apiService.suppliers.getAll());
  return { data: data?.results || [], loading: false, error: null };
}

// Utility function to extract results from paginated response
export function extractResults<T>(
  paginatedData: PaginatedResponse<T> | null
): T[] {
  return paginatedData?.results || [];
}

// Utility function to check if response is paginated
export function isPaginatedResponse<T>(
  data: any
): data is PaginatedResponse<T> {
  return (
    data && typeof data === "object" && "results" in data && "count" in data
  );
}

// Hook for reports
export function useReports() {
  const [salesReport, setSalesReport] = useState(null);
  const [inventoryReport, setInventoryReport] = useState(null);
  const [customerReport, setCustomerReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchReports = async () => {
    try {
      setLoading(true);
      setError(null);

      const [salesRes, inventoryRes, customerRes] = await Promise.all([
        apiService.reports.getSalesReport({}),
        apiService.reports.getInventoryReport(),
        apiService.reports.getCustomerReport(),
      ]);

      setSalesReport(salesRes.data);
      setInventoryReport(inventoryRes.data);
      setCustomerReport(customerRes.data);
    } catch (err: any) {
      const errorMessage =
        err.response?.data?.message || err.message || "Failed to fetch reports";
      setError(errorMessage);
      toast.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReports();
  }, []);

  return {
    salesReport,
    inventoryReport,
    customerReport,
    loading,
    error,
    refetch: fetchReports,
  };
}

// Hook for settings
export function useSettings() {
  const [profile, setProfile] = useState(null);
  const [businessSettings, setBusinessSettings] = useState(null);
  const [systemSettings, setSystemSettings] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchSettings = async () => {
    try {
      setLoading(true);
      setError(null);

      const [profileRes, businessRes, systemRes] = await Promise.all([
        apiService.settings.getProfile(),
        apiService.settings.getBusinessSettings(),
        apiService.settings.getSystemSettings(),
      ]);

      setProfile(profileRes.data);
      setBusinessSettings(businessRes.data);
      setSystemSettings(systemRes.data);
    } catch (err: any) {
      const errorMessage =
        err.response?.data?.message ||
        err.message ||
        "Failed to fetch settings";
      setError(errorMessage);
      toast.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSettings();
  }, []);

  return {
    profile,
    businessSettings,
    systemSettings,
    loading,
    error,
    refetch: fetchSettings,
  };
}

// Hook for mutations (create, update, delete operations)
export function useMutation<T = any>() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const mutate = async (
    apiCall: () => Promise<any>,
    {
      onSuccess,
      onError,
      successMessage = "Operation completed successfully",
    }: {
      onSuccess?: (data: T) => void;
      onError?: (error: string) => void;
      successMessage?: string;
    } = {}
  ) => {
    try {
      setLoading(true);
      setError(null);

      const response = await apiCall();

      toast.success(successMessage);
      onSuccess?.(response.data);

      return response.data;
    } catch (err: any) {
      const errorMessage =
        err.response?.data?.message || err.message || "Operation failed";
      setError(errorMessage);
      toast.error(errorMessage);
      onError?.(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { mutate, loading, error };
}

// Auth utility functions
export function useAuth() {
  const isAuthenticated = () => {
    return !!localStorage.getItem("access_token");
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    window.location.href = "/auth/login";
  };

  return {
    isAuthenticated,
    logout,
  };
}

// Hook for multipart file uploads
export function useFileUpload() {
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState<{
    [key: string]: number;
  }>({});
  const [error, setError] = useState<string | null>(null);

  const uploadFile = async (
    file: File,
    endpoint: string,
    metadata?: Record<string, any>
  ): Promise<any> => {
    try {
      setUploading(true);
      setError(null);

      // Create FormData for multipart upload
      const formData = new FormData();
      formData.append("file", file, file.name);

      // Add metadata if provided
      if (metadata) {
        Object.entries(metadata).forEach(([key, value]) => {
          if (value !== undefined && value !== null) {
            formData.append(
              key,
              typeof value === "string" ? value : JSON.stringify(value)
            );
          }
        });
      }

      // Add file metadata
      formData.append("file_name", file.name);
      formData.append("file_size", file.size.toString());
      formData.append("file_type", file.type);

      // Initialize progress tracking
      const fileKey = `${file.name}-${Date.now()}`;
      setUploadProgress((prev) => ({ ...prev, [fileKey]: 0 }));

      // Create axios config with progress tracking
      const config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        onUploadProgress: (progressEvent: any) => {
          if (progressEvent.lengthComputable) {
            const percentCompleted = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            setUploadProgress((prev) => ({
              ...prev,
              [fileKey]: percentCompleted,
            }));
          }
        },
      };

      // Upload using axios directly with progress tracking
      const response = await api.post(endpoint, formData, config);

      // Clean up progress tracking
      setUploadProgress((prev) => {
        const newProgress = { ...prev };
        delete newProgress[fileKey];
        return newProgress;
      });

      toast.success(`${file.name} uploaded successfully`);
      return response.data;
    } catch (err: any) {
      const errorMessage =
        err.response?.data?.message ||
        err.response?.data?.error ||
        err.message ||
        "Failed to upload file";
      setError(errorMessage);
      toast.error(errorMessage);
      throw err;
    } finally {
      setUploading(false);
    }
  };

  const uploadMultipleFiles = async (
    files: File[],
    endpoint: string,
    metadata?: Record<string, any>
  ): Promise<any[]> => {
    const results: any[] = [];

    for (const file of files) {
      try {
        const result = await uploadFile(file, endpoint, metadata);
        results.push(result);
      } catch (error) {
        // Continue with other files even if one fails
        console.error(`Failed to upload ${file.name}:`, error);
      }
    }

    return results;
  };

  return {
    uploadFile,
    uploadMultipleFiles,
    uploading,
    uploadProgress,
    error,
  };
}
