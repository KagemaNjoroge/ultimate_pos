# API Integration Guide

This guide shows how to use the API service and hooks to interact with your Django backend.

## Overview

The API integration consists of two main files:

- `/lib/api.ts` - Axios configuration with automatic token handling
- `/lib/hooks.ts` - React hooks for easy API usage

## Features

- ✅ Automatic Bearer token inclusion from localStorage
- ✅ Global error handling and user notifications
- ✅ Automatic redirect to login on 401 errors
- ✅ Pre-built API endpoints for all POS operations
- ✅ React hooks with loading states and error handling
- ✅ Mutation hooks for create/update/delete operations

## Basic Usage

### 1. API Service

```typescript
import { apiService } from "@/lib/api";

// Fetch all products
const response = await apiService.products.getAll();

// Create a new product
const newProduct = await apiService.products.create({
  name: "New Product",
  price: 99.99,
  stock: 10,
});

// Update a product
const updatedProduct = await apiService.products.update(1, {
  name: "Updated Product Name",
});

// Delete a product
await apiService.products.delete(1);
```

### 2. React Hooks

```typescript
import { useProducts, useMutation } from "@/lib/hooks";

function ProductsComponent() {
  // Fetch products with loading/error states
  const { data: products, loading, error, refetch } = useProducts();

  // Mutation hook for CRUD operations
  const { mutate, loading: mutating } = useMutation();

  const handleCreateProduct = async (productData) => {
    await mutate(() => apiService.products.create(productData), {
      onSuccess: () => {
        refetch(); // Refresh the list
      },
      successMessage: "Product created successfully",
    });
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      {products?.map((product) => (
        <div key={product.id}>{product.name}</div>
      ))}
    </div>
  );
}
```

## Available API Endpoints

### Products

- `apiService.products.getAll()` - Get all products
- `apiService.products.getById(id)` - Get product by ID
- `apiService.products.create(data)` - Create new product
- `apiService.products.update(id, data)` - Update product
- `apiService.products.delete(id)` - Delete product

### Sales

- `apiService.sales.getAll()` - Get all sales
- `apiService.sales.getById(id)` - Get sale by ID
- `apiService.sales.create(data)` - Create new sale
- `apiService.sales.update(id, data)` - Update sale
- `apiService.sales.delete(id)` - Delete sale

### Customers

- `apiService.customers.getAll()` - Get all customers
- `apiService.customers.getById(id)` - Get customer by ID
- `apiService.customers.create(data)` - Create new customer
- `apiService.customers.update(id, data)` - Update customer
- `apiService.customers.delete(id)` - Delete customer

### Stock

- `apiService.stock.getAll()` - Get all stock items
- `apiService.stock.getById(id)` - Get stock item by ID
- `apiService.stock.update(id, data)` - Update stock levels

### Reports

- `apiService.reports.getSalesReport(params)` - Get sales report
- `apiService.reports.getInventoryReport()` - Get inventory report
- `apiService.reports.getCustomerReport()` - Get customer report
- `apiService.reports.getFinancialReport(params)` - Get financial report

### Suppliers

- `apiService.suppliers.getAll()` - Get all suppliers
- `apiService.suppliers.getById(id)` - Get supplier by ID
- `apiService.suppliers.create(data)` - Create new supplier
- `apiService.suppliers.update(id, data)` - Update supplier
- `apiService.suppliers.delete(id)` - Delete supplier

### Settings

- `apiService.settings.getProfile()` - Get user profile
- `apiService.settings.updateProfile(data)` - Update user profile
- `apiService.settings.getBusinessSettings()` - Get business settings
- `apiService.settings.updateBusinessSettings(data)` - Update business settings
- `apiService.settings.getSystemSettings()` - Get system settings
- `apiService.settings.updateSystemSettings(data)` - Update system settings

## Available Hooks

### Data Fetching Hooks

- `useProducts()` - Fetch all products
- `useSales()` - Fetch all sales
- `useCustomers()` - Fetch all customers
- `useStock()` - Fetch all stock items
- `useSuppliers()` - Fetch all suppliers
- `useReports()` - Fetch all reports
- `useSettings()` - Fetch all settings

### Mutation Hook

- `useMutation()` - For create/update/delete operations

### Auth Hook

- `useAuth()` - Authentication utilities

## Token Management

The API service automatically:

- Adds `Authorization: Bearer <token>` header to all requests
- Handles token expiry (401 errors) by redirecting to login
- Stores and retrieves tokens from localStorage

### Manual Token Operations

```typescript
// Get current token
const token = localStorage.getItem("access_token");

// Set token (done automatically on login)
localStorage.setItem("access_token", "your-token");

// Clear tokens (done automatically on logout/401)
localStorage.removeItem("access_token");
localStorage.removeItem("refresh_token");
```

## Error Handling

The API service provides automatic error handling:

- **401 Unauthorized**: Redirects to login page
- **403 Forbidden**: Shows access denied message
- **500 Internal Server Error**: Shows server error message
- **Network errors**: Shows connection error message

## Example: Complete Component with API Integration

```typescript
"use client";

import { useProducts, useMutation } from "@/lib/hooks";
import { apiService } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Loader2 } from "lucide-react";

export default function ProductsPage() {
  const { data: products, loading, error, refetch } = useProducts();
  const { mutate: deleteProduct, loading: deleting } = useMutation();

  const handleDelete = async (productId: number) => {
    await deleteProduct(() => apiService.products.delete(productId), {
      onSuccess: () => refetch(),
      successMessage: "Product deleted successfully",
    });
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <Loader2 className="h-8 w-8 animate-spin" />
        <span className="ml-2">Loading products...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8 text-center">
        <p className="text-red-500 mb-4">Error: {error}</p>
        <Button onClick={refetch}>Retry</Button>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {products?.map((product) => (
        <div
          key={product.id}
          className="flex items-center justify-between p-4 border rounded"
        >
          <span>{product.name}</span>
          <Button
            variant="destructive"
            onClick={() => handleDelete(product.id)}
            disabled={deleting}
          >
            {deleting ? <Loader2 className="h-4 w-4 animate-spin" /> : "Delete"}
          </Button>
        </div>
      ))}
    </div>
  );
}
```

## Backend Requirements

Your Django backend should:

1. Accept `Authorization: Bearer <token>` headers
2. Return appropriate HTTP status codes (401 for unauthorized, etc.)
3. Have endpoints matching the API service URLs:
   - `/api/products/` (GET, POST)
   - `/api/products/{id}/` (GET, PUT, DELETE)
   - `/api/sales/` (GET, POST)
   - `/api/customers/` (GET, POST)
   - etc.

## Environment Variables

Make sure your `.env` file contains:

```
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

This URL is used as the base URL for all API calls.
