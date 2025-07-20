"use client";

import DashboardLayout from "@/components/layout/dashboard-layout";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { ProductImage } from "@/components/ui/product-image";
import { apiService } from "@/lib/api";
import { useMutation, useProducts } from "@/lib/hooks";
import {
  Edit,
  Filter,
  Loader2,
  Package,
  Plus,
  Search,
  Trash2,
} from "lucide-react";

// Product type definition based on your API response
interface Product {
  id: number;
  name: string;
  description: string;
  track_inventory: boolean;
  display_image: string | null;
  status: string | null;
  price: number;
  supplier: number | null;
  category: number;
  photos: number[];
  tax_group: number | null;
}

/*
  {
      "id": 1,
      "created_at": "2025-07-19T12:26:28.753603+03:00",
      "updated_at": "2025-07-19T12:27:18.697066+03:00",
      "name": "Value Added Tax (VAT)",
      "description": "VAT is an indirect tax that is paid by the person who consumes taxable goods and taxable services supplied in Kenya and/or imported into Kenya.",
      "tax_rate": 16,
      "status": "ACTIVE"
    }
*/

// Tax group type definition
export interface TaxGroup {
  id: number;
  created_at: string;
  updated_at: string;
  name: string;
  description: string;
  tax_rate: number;
  status: string | null; // Can be "ACTIVE", "INACTIVE", or null
}


const getStatusBadgeVariant = (status: string | null) => {
  if (!status) return "secondary";

  switch (status.toUpperCase()) {
    case "ACTIVE":
      return "default";
    case "INACTIVE":
      return "destructive";
    default:
      return "secondary";
  }
};

const getStatusDisplay = (status: string | null) => {
  if (!status) return "No Status";
  return status.charAt(0).toUpperCase() + status.slice(1).toLowerCase();
};

const formatPrice = (price: number) => {
  return new Intl.NumberFormat("en-KE", {
    style: "currency",
    currency: "KES",
    minimumFractionDigits: 0,
  }).format(price);
};

export default function ProductsPage() {
  // Use the API hook to fetch products with pagination
  const {
    data: products,
    loading,
    error,
    paginationInfo,
    refetch,
    loadMore,
  } = useProducts();
  const { mutate: deleteProduct, loading: deleting } = useMutation();

  // Type the products array properly
  const productsList: Product[] = products || [];

  const handleDeleteProduct = async (productId: number) => {
    if (!confirm("Are you sure you want to delete this product?")) {
      return;
    }

    try {
      await deleteProduct(() => apiService.products.delete(productId), {
        onSuccess: () => {
          refetch(); // Refresh the products list
        },
        successMessage: "Product deleted successfully",
      });
    } catch (error) {
      // Error is handled by the mutation hook
    }
  };

  // Calculate stats
  const totalProducts = paginationInfo.count; // Use total count from pagination
  const activeProducts = productsList.filter(
    (p) => p.status === "ACTIVE"
  ).length;
  const inactiveProducts = productsList.filter(
    (p) => p.status === "INACTIVE" || !p.status
  ).length;
  const trackingInventory = productsList.filter(
    (p) => p.track_inventory
  ).length;

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-3xl font-bold tracking-tight">Products</h2>
            <p className="text-muted-foreground">
              Manage your product inventory and pricing
            </p>
          </div>
          <Button>
            <Plus className="mr-2 h-4 w-4" />
            Add Product
          </Button>
        </div>

        {/* Stats Cards */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Total Products
              </CardTitle>
              <Package className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{totalProducts}</div>
              <p className="text-xs text-muted-foreground">
                Products in catalog
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Active Products
              </CardTitle>
              <Package className="h-4 w-4 text-green-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{activeProducts}</div>
              <p className="text-xs text-muted-foreground">
                Products available for sale
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Inactive/No Status
              </CardTitle>
              <Package className="h-4 w-4 text-red-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{inactiveProducts}</div>
              <p className="text-xs text-muted-foreground">
                Products not available
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Tracking Inventory
              </CardTitle>
              <Package className="h-4 w-4 text-blue-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{trackingInventory}</div>
              <p className="text-xs text-muted-foreground">
                Products with inventory tracking
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Products Table */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Product Inventory</CardTitle>
                <CardDescription>
                  A list of all products in your inventory
                </CardDescription>
              </div>
              <div className="flex items-center space-x-2">
                <div className="relative">
                  <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                  <Input
                    placeholder="Search products..."
                    className="pl-8 w-64"
                  />
                </div>
                <Button variant="outline" size="icon">
                  <Filter className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="flex items-center justify-center py-8">
                <Loader2 className="h-8 w-8 animate-spin" />
                <span className="ml-2">Loading products...</span>
              </div>
            ) : error ? (
              <div className="flex flex-col items-center justify-center py-8 text-muted-foreground">
                <p className="mb-4">Failed to load products from API</p>
                <p className="text-sm text-red-500 mb-4">{error}</p>
                <Button variant="outline" size="sm" onClick={refetch}>
                  Retry
                </Button>
              </div>
            ) : products.length === 0 ? (
              <div className="flex items-center justify-center py-8 text-muted-foreground">
                <p>No products found. Add your first product to get started.</p>
              </div>
            ) : (
              <div className="space-y-4">
                {productsList.map((product: Product) => (
                  <div
                    key={product.id}
                    className="flex items-center justify-between p-4 border rounded-lg hover:bg-accent/50 transition-colors"
                  >
                    <div className="flex items-center space-x-4">
                      <div className="h-16 w-16 bg-muted rounded-lg flex items-center justify-center overflow-hidden">
                        <ProductImage
                          src={product.display_image}
                          alt={product.name}
                          width={64}
                          height={64}
                        />
                      </div>
                      <div>
                        <h4 className="text-sm font-medium">{product.name}</h4>
                        <p className="text-xs text-muted-foreground mb-1">
                          {product.description}
                        </p>
                        <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                          <span>ID: {product.id}</span>
                          <span>•</span>
                          <span>Category: {product.category}</span>
                          {product.track_inventory && (
                            <>
                              <span>•</span>
                              <span className="text-blue-600">
                                Tracking Inventory
                              </span>
                            </>
                          )}
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center space-x-4">
                      <div className="text-right">
                        <div className="text-sm font-medium">
                          {formatPrice(product.price)}
                        </div>
                        <div className="text-xs text-muted-foreground">
                          {product.photos.length} photo
                          {product.photos.length !== 1 ? "s" : ""}
                        </div>
                      </div>

                      <Badge variant={getStatusBadgeVariant(product.status)}>
                        {getStatusDisplay(product.status)}
                      </Badge>

                      <div className="flex items-center space-x-1">
                        <Button variant="ghost" size="icon">
                          <Edit className="h-4 w-4" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={() => handleDeleteProduct(product.id)}
                          disabled={deleting}
                        >
                          {deleting ? (
                            <Loader2 className="h-4 w-4 animate-spin" />
                          ) : (
                            <Trash2 className="h-4 w-4" />
                          )}
                        </Button>
                      </div>
                    </div>
                  </div>
                ))}

                {/* Load More Button */}
                {paginationInfo.hasNext && (
                  <div className="flex justify-center pt-4">
                    <Button
                      variant="outline"
                      onClick={loadMore}
                      disabled={loading}
                    >
                      {loading ? (
                        <>
                          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                          Loading...
                        </>
                      ) : (
                        `Load More (${
                          paginationInfo.count - productsList.length
                        } remaining)`
                      )}
                    </Button>
                  </div>
                )}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}
