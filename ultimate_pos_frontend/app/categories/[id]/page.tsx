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
import { apiService } from "@/lib/api";
import { useApi, useProducts } from "@/lib/hooks";
import { ArrowLeft, Edit, Package } from "lucide-react";
import Link from "next/link";
import { useParams } from "next/navigation";

interface Product {
  id: number;
  name: string;
  description: string;
  price: string;

  category: number;

  sku: string;
}

interface Category {
  id: number;
  name: string;
  description: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export default function CategoryDetailsPage() {
  const params = useParams();
  const categoryId = params.id as string;

  // Fetch category details
  const {
    data: category,
    loading: categoryLoading,
    error: categoryError,
  } = useApi<Category>(
    () => apiService.productCategories.getById(parseInt(categoryId)),
    [categoryId],
    `category_${categoryId}`
  );

  // Fetch products in this category
  const {
    data: products,
    loading: productsLoading,
    error: productsError,
    paginationInfo,
    loadMore,
  } = useProducts({ category: categoryId });

  if (categoryLoading) {
    return (
      <DashboardLayout>
        <div className="container mx-auto p-6">
          <div className="text-center py-10">Loading category details...</div>
        </div>
      </DashboardLayout>
    );
  }

  if (categoryError) {
    return (
      <DashboardLayout>
        <div className="container mx-auto p-6">
          <div className="flex items-center gap-4 mb-6">
            <Link href="/categories">
              <Button variant="ghost" size="sm">
                <ArrowLeft className="w-4 h-4 mr-2" />
                Back to Categories
              </Button>
            </Link>
          </div>
          <div className="text-center py-10 text-red-500">
            Error: {categoryError}
          </div>
        </div>
      </DashboardLayout>
    );
  }

  if (!category) {
    return (
      <DashboardLayout>
        <div className="container mx-auto p-6">
          <div className="flex items-center gap-4 mb-6">
            <Link href="/categories">
              <Button variant="ghost" size="sm">
                <ArrowLeft className="w-4 h-4 mr-2" />
                Back to Categories
              </Button>
            </Link>
          </div>
          <div className="text-center py-10">Category not found</div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="container mx-auto p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-4">
            <Link href="/categories">
              <Button variant="ghost" size="sm">
                <ArrowLeft className="w-4 h-4 mr-2" />
                Back to Categories
              </Button>
            </Link>
            <div>
              <h1 className="text-3xl font-bold">{category.name}</h1>
              <p className="text-muted-foreground">
                {category.description || "No description provided"}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Link href={`/categories/${category.id}/edit`}>
              <Button variant="outline">
                <Edit className="w-4 h-4 mr-2" />
                Edit Category
              </Button>
            </Link>
          </div>
        </div>

        {/* Category Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Total Products
              </CardTitle>
              <Package className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{paginationInfo.count}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Status</CardTitle>
            </CardHeader>
            <CardContent>
              <Badge
                variant={category.status === "ACTIVE" ? "default" : "secondary"}
                className="text-lg"
              >
                {category.status}
              </Badge>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Category Created
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {new Date(category.created_at).toLocaleDateString()}
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Last Updated
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {new Date(category.updated_at).toLocaleDateString()}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Products in Category */}
        <Card>
          <CardHeader>
            <CardTitle>Products in {category.name}</CardTitle>
            <CardDescription>
              {paginationInfo.count > 0
                ? `Showing ${products.length} of ${paginationInfo.count} products`
                : "No products in this category"}
            </CardDescription>
          </CardHeader>
          <CardContent>
            {productsLoading && products.length === 0 ? (
              <div className="text-center py-10">Loading products...</div>
            ) : productsError && products.length === 0 ? (
              <div className="text-center py-10 text-red-500">
                Error loading products: {productsError}
              </div>
            ) : products.length === 0 ? (
              <div className="text-center py-10">
                <p className="text-muted-foreground mb-4">
                  No products found in this category
                </p>
                <Link href="/products/create">
                  <Button>
                    <Package className="w-4 h-4 mr-2" />
                    Add Product to Category
                  </Button>
                </Link>
              </div>
            ) : (
              <>
                <div className="space-y-4">
                  {products.map((product: Product) => (
                    <div
                      key={product.id}
                      className="flex items-center justify-between p-4 border rounded-lg hover:bg-accent/50 transition-colors"
                    >
                      <div className="flex items-center space-x-4">
                        <div className="h-12 w-12 bg-muted rounded-lg flex items-center justify-center">
                          <Package className="h-6 w-6 text-muted-foreground" />
                        </div>
                        <div>
                          <h4 className="text-sm font-medium">
                            {product.name}
                          </h4>
                          {product.description && (
                            <p className="text-xs text-muted-foreground mb-1 truncate max-w-xs">
                              {product.description}
                            </p>
                          )}
                          <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                            <span>SKU: {product.sku}</span>
                            <span>•</span>
                            <span>${parseFloat(product.price).toFixed(2)}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                {paginationInfo.hasNext && (
                  <div className="mt-4 text-center">
                    <Button
                      variant="outline"
                      onClick={loadMore}
                      disabled={productsLoading}
                    >
                      {productsLoading ? "Loading..." : "Load More Products"}
                    </Button>
                  </div>
                )}
              </>
            )}
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}
