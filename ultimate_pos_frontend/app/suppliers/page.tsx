"use client";

import { CreateSupplierForm } from "@/components/forms/create-supplier-form";
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
import { useSuppliers } from "@/lib/hooks";
import { Supplier } from "@/lib/interfaces";
import {
  Edit,
  Filter,
  Globe,
  Loader2,
  Mail,
  Phone,
  Plus,
  Search,
  Truck,
} from "lucide-react";
import { useState } from "react";

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString("en-KE", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
};

export default function SuppliersPage() {
  const [searchTerm, setSearchTerm] = useState("");
  const [showCreateForm, setShowCreateForm] = useState(false);

  // Use the API hook to fetch suppliers with pagination
  const {
    data: suppliers,
    loading,
    error,
    paginationInfo,
    refetch,
    loadMore,
  } = useSuppliers();

  // Use API data if available, otherwise use empty array
  const suppliersData: Supplier[] = suppliers || [];

  // Filter suppliers based on search term
  const filteredSuppliers = suppliersData.filter((supplier) => {
    const searchLower = searchTerm.toLowerCase();
    const name = (supplier.name || "").toLowerCase();
    const email = (supplier.email || "").toLowerCase();
    const phone = (supplier.phone || "").toLowerCase();
    const address = (supplier.address || "").toLowerCase();

    return (
      name.includes(searchLower) ||
      email.includes(searchLower) ||
      phone.includes(searchLower) ||
      address.includes(searchLower)
    );
  });
  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-3xl font-bold tracking-tight">Suppliers</h2>
            <p className="text-muted-foreground">
              Manage your supplier relationships and procurement
            </p>
          </div>
          <Button onClick={() => setShowCreateForm(true)}>
            <Plus className="mr-2 h-4 w-4" />
            Add Supplier
          </Button>
        </div>

        {/* Suppliers Table */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Supplier Directory</CardTitle>
                <CardDescription>
                  Manage and view all supplier information
                </CardDescription>
              </div>
              <div className="flex items-center space-x-2">
                <div className="relative">
                  <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                  <Input
                    placeholder="Search suppliers..."
                    className="pl-8 w-64"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
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
                <span className="ml-2">Loading suppliers...</span>
              </div>
            ) : error ? (
              <div className="flex flex-col items-center justify-center py-8 text-muted-foreground">
                <p className="mb-4">Failed to load suppliers from API</p>
                <p className="text-sm text-red-500 mb-4">{error}</p>
                <Button variant="outline" size="sm" onClick={refetch}>
                  Retry
                </Button>
              </div>
            ) : filteredSuppliers.length === 0 ? (
              <div className="flex items-center justify-center py-8 text-muted-foreground">
                <p>
                  {searchTerm
                    ? `No suppliers found matching "${searchTerm}"`
                    : "No suppliers found. Add your first supplier to get started."}
                </p>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="text-sm text-muted-foreground">
                    Showing {filteredSuppliers.length} of {paginationInfo.count}{" "}
                    suppliers
                    {searchTerm && (
                      <span className="ml-2 text-primary">
                        • Filtered by "{searchTerm}"
                      </span>
                    )}
                  </div>
                </div>
                <div className="space-y-4">
                  {filteredSuppliers.map((supplier: Supplier) => (
                    <div
                      key={supplier.id}
                      className="flex items-center justify-between p-4 border rounded-lg hover:bg-accent/50 transition-colors"
                    >
                      <div className="flex items-center space-x-4">
                        <div className="h-12 w-12 bg-muted rounded-lg flex items-center justify-center">
                          {supplier.logo ? (
                            <img
                              src={supplier.logo}
                              alt={supplier.name}
                              className="h-full w-full object-cover rounded-lg"
                            />
                          ) : (
                            <Truck className="h-6 w-6 text-muted-foreground" />
                          )}
                        </div>
                        <div>
                          <h4 className="text-sm font-medium">
                            {supplier.name}
                          </h4>
                          <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                            <span>Tax ID: {supplier.tax_id}</span>
                            {supplier.website && (
                              <>
                                <span>•</span>
                                <Globe className="h-3 w-3" />
                                <a
                                  href={supplier.website}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="text-blue-600 hover:underline"
                                >
                                  Website
                                </a>
                              </>
                            )}
                          </div>
                          <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                            <Mail className="h-3 w-3" />
                            <span>{supplier.email}</span>
                            <span>•</span>
                            <Phone className="h-3 w-3" />
                            <span>{supplier.phone}</span>
                          </div>
                          {supplier.address && (
                            <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                              <span>📍</span>
                              <span className="truncate max-w-[300px]">
                                {supplier.address}
                              </span>
                            </div>
                          )}
                        </div>
                      </div>

                      <div className="flex items-center space-x-4">
                        <div className="text-right">
                          <div className="text-sm font-medium">
                            ID: {supplier.id}
                          </div>
                          {supplier.additional_notes && (
                            <div className="text-xs text-muted-foreground max-w-[200px] truncate">
                              Notes: {supplier.additional_notes}
                            </div>
                          )}
                          <div className="text-xs text-muted-foreground">
                            {supplier.logo ? "Has Logo" : "No Logo"}
                          </div>
                        </div>

                        <Button variant="ghost" size="icon">
                          <Edit className="h-4 w-4" />
                        </Button>
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
                            paginationInfo.count - suppliersData.length
                          } remaining)`
                        )}
                      </Button>
                    </div>
                  )}
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Create Supplier Modal */}
        <CreateSupplierForm
          open={showCreateForm}
          onOpenChange={setShowCreateForm}
          onSuccess={refetch}
        />
      </div>
    </DashboardLayout>
  );
}
