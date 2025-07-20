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
import { useProductCategories } from "@/lib/hooks";
import { Edit, Eye, FolderOpen, Plus, Trash2 } from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";
import { toast } from "sonner";

interface Category {
  id: number;
  name: string;
  description: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export default function CategoriesPage() {
  const {
    data: categories,
    loading,
    error,
    paginationInfo,
    loadMore,
    refetch,
  } = useProductCategories();
  const [deletingId, setDeletingId] = useState<number | null>(null);
  const [productCounts, setProductCounts] = useState<Record<number, number>>(
    {}
  );
  const [loadingCounts, setLoadingCounts] = useState(false);

  // Fetch product counts for all categories
  const fetchProductCounts = async (categoriesList: Category[]) => {
    if (categoriesList.length === 0) return;

    setLoadingCounts(true);
    try {
      const counts: Record<number, number> = {};

      // Fetch product count for each category
      await Promise.all(
        categoriesList.map(async (category) => {
          try {
            const response = await apiService.products.getAll({
              category: category.id,
            });
            counts[category.id] = response.data.count || 0;
          } catch (error) {
            console.error(
              `Failed to fetch product count for category ${category.id}:`,
              error
            );
            counts[category.id] = 0;
          }
        })
      );

      setProductCounts(counts);
    } catch (error) {
      console.error("Failed to fetch product counts:", error);
    } finally {
      setLoadingCounts(false);
    }
  };

  // Fetch product counts when categories change
  useEffect(() => {
    if (categories.length > 0) {
      fetchProductCounts(categories);
    }
  }, [categories]);

  const handleDelete = async (id: number) => {
    if (!confirm("Are you sure you want to delete this category?")) return;

    setDeletingId(id);
    try {
      await apiService.productCategories.delete(id);
      toast.success("Category deleted successfully");
      refetch();
      // Remove the deleted category from product counts
      setProductCounts((prev) => {
        const updated = { ...prev };
        delete updated[id];
        return updated;
      });
    } catch (error: any) {
      toast.error(error.response?.data?.message || "Failed to delete category");
    } finally {
      setDeletingId(null);
    }
  };

  if (loading && categories.length === 0) {
    return (
      <DashboardLayout>
        <div className="container mx-auto p-6">
          <div className="flex items-center justify-between mb-6">
            <h1 className="text-3xl font-bold">Categories</h1>
          </div>
          <div className="text-center py-10">Loading categories...</div>
        </div>
      </DashboardLayout>
    );
  }

  if (error && categories.length === 0) {
    return (
      <DashboardLayout>
        <div className="container mx-auto p-6">
          <div className="flex items-center justify-between mb-6">
            <h1 className="text-3xl font-bold">Categories</h1>
          </div>
          <div className="text-center py-10 text-red-500">Error: {error}</div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="container mx-auto p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold">Categories</h1>
            <p className="text-muted-foreground">
              Manage your product categories and organize your inventory
            </p>
          </div>
          <Link href="/categories/create">
            <Button>
              <Plus className="w-4 h-4 mr-2" />
              Add Category
            </Button>
          </Link>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>All Categories</CardTitle>
            <CardDescription>
              {paginationInfo.count > 0
                ? `Showing ${categories.length} of ${paginationInfo.count} categories`
                : "No categories found"}
            </CardDescription>
          </CardHeader>
          <CardContent>
            {categories.length === 0 ? (
              <div className="text-center py-10">
                <p className="text-muted-foreground mb-4">
                  No categories found
                </p>
                <Link href="/categories/create">
                  <Button>
                    <Plus className="w-4 h-4 mr-2" />
                    Create your first category
                  </Button>
                </Link>
              </div>
            ) : (
              <>
                <div className="space-y-4">
                  {categories.map((category: Category) => (
                    <div
                      key={category.id}
                      className="flex items-center justify-between p-4 border rounded-lg hover:bg-accent/50 transition-colors"
                    >
                      <div className="flex items-center space-x-4">
                        <div className="h-12 w-12 bg-muted rounded-lg flex items-center justify-center">
                          <FolderOpen className="h-6 w-6 text-muted-foreground" />
                        </div>
                        <div>
                          <h4 className="text-sm font-medium">
                            {category.name}
                          </h4>
                          <p className="text-xs text-muted-foreground mb-1">
                            {category.description || "No description"}
                          </p>
                          <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                            <span>ID: {category.id}</span>
                            <span>•</span>
                            <span>
                              Created:{" "}
                              {new Date(
                                category.created_at
                              ).toLocaleDateString()}
                            </span>
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Badge variant="secondary">
                          {productCounts[category.id] !== undefined
                            ? `${productCounts[category.id]} products`
                            : loadingCounts
                            ? "Loading..."
                            : "0 products"}
                        </Badge>
                        <Badge
                          variant={
                            category.status === "ACTIVE"
                              ? "default"
                              : "secondary"
                          }
                        >
                          {category.status}
                        </Badge>
                        <div className="flex items-center gap-2">
                          <Link href={`/categories/${category.id}`}>
                            <Button variant="ghost" size="sm">
                              <Eye className="w-4 h-4" />
                            </Button>
                          </Link>
                          <Link href={`/categories/${category.id}/edit`}>
                            <Button variant="ghost" size="sm">
                              <Edit className="w-4 h-4" />
                            </Button>
                          </Link>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleDelete(category.id)}
                            disabled={deletingId === category.id}
                          >
                            <Trash2 className="w-4 h-4" />
                          </Button>
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
                      disabled={loading}
                    >
                      {loading ? "Loading..." : "Load More"}
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
