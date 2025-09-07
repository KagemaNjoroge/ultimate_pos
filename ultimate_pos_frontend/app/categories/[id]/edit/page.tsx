"use client";

import DashboardLayout from "@/components/layout/dashboard-layout";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { apiService } from "@/lib/api";
import { useApi } from "@/lib/hooks";
import { Category } from "@/lib/interfaces/category";
import { ArrowLeft } from "lucide-react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { toast } from "sonner";

export default function EditCategoryPage() {
  const params = useParams();
  const router = useRouter();
  const categoryId = params.id as string;

  const {
    data: category,
    loading: categoryLoading,
    error: categoryError,
  } = useApi<Category>(
    () => apiService.productCategories.getById(parseInt(categoryId)),
    [categoryId],
    `category_${categoryId}`
  );

  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: "",
    description: "",
  });

  // Update form data when category is loaded
  useEffect(() => {
    if (category) {
      setFormData({
        name: category.name,
        description: category.description || "",
      });
    }
  }, [category]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.name.trim()) {
      toast.error("Category name is required");
      return;
    }

    setLoading(true);
    try {
      await apiService.productCategories.update(parseInt(categoryId), formData);
      toast.success("Category updated successfully");
      router.push(`/categories/${categoryId}`);
    } catch (error: any) {
      toast.error(error.response?.data?.message || "Failed to update category");
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  if (categoryLoading) {
    return (
      <DashboardLayout>
        <div className="container mx-auto p-6">
          <div className="text-center py-10">Loading category...</div>
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
        <div className="flex items-center gap-4 mb-6">
          <Link href={`/categories/${categoryId}`}>
            <Button variant="ghost" size="sm">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Category
            </Button>
          </Link>
          <div>
            <h1 className="text-3xl font-bold">Edit Category</h1>
            <p className="text-muted-foreground">
              Update the category information
            </p>
          </div>
        </div>

        <Card className="max-w-2xl">
          <CardHeader>
            <CardTitle>Category Information</CardTitle>
            <CardDescription>
              Update the details for "{category.name}"
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="name">
                  Category Name <span className="text-red-500">*</span>
                </Label>
                <Input
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  placeholder="Enter category name"
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="description">Description</Label>
                <Textarea
                  id="description"
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  placeholder="Enter category description (optional)"
                  rows={4}
                />
              </div>

              <div className="flex items-center gap-4">
                <Button type="submit" disabled={loading}>
                  {loading ? "Updating..." : "Update Category"}
                </Button>
                <Link href={`/categories/${categoryId}`}>
                  <Button type="button" variant="outline">
                    Cancel
                  </Button>
                </Link>
              </div>
            </form>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}
