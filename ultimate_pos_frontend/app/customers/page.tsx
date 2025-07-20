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
import { useCustomers } from "@/lib/hooks";
import {
  Edit,
  Eye,
  Filter,
  Loader2,
  Mail,
  Phone,
  Plus,
  Search,
  UserCheck,
  Users,
} from "lucide-react";
import { useRouter } from "next/navigation";
import { useState } from "react";

// Customer type definition based on API structure
interface Customer {
  id: number;
  created_at: string;
  updated_at: string;
  first_name: string;
  last_name: string;
  address: string;
  email: string;
  phone: string;
  tax_number: string;
  is_active: boolean;
  photo: string;
}

const getStatusBadgeVariant = (is_active: boolean) => {
  return is_active ? "default" : "outline";
};

const getStatusText = (is_active: boolean) => {
  return is_active ? "Active" : "Inactive";
};

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString("en-KE", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
};

export default function CustomersPage() {
  const router = useRouter();
  const [searchTerm, setSearchTerm] = useState("");

  // Use the API hook to fetch customers with pagination
  const {
    data: customers,
    loading,
    error,
    paginationInfo,
    refetch,
    loadMore,
  } = useCustomers();

  // Use API data if available, otherwise use empty array
  const customersData: Customer[] = customers || [];

  // Filter customers based on search term
  const filteredCustomers = customersData.filter((customer) => {
    const searchLower = searchTerm.toLowerCase();
    const fullName = `${customer.first_name || ""} ${
      customer.last_name || ""
    }`.toLowerCase();
    const email = (customer.email || "").toLowerCase();
    const phone = (customer.phone || "").toLowerCase();

    return (
      fullName.includes(searchLower) ||
      email.includes(searchLower) ||
      phone.includes(searchLower)
    );
  });

  const activeCustomers = customersData.filter((c) => c.is_active);
  const inactiveCustomers = customersData.filter((c) => !c.is_active);
  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-3xl font-bold tracking-tight">Customers</h2>
            <p className="text-muted-foreground">
              Manage your customer relationships and data
            </p>
          </div>
          <Button>
            <Plus className="mr-2 h-4 w-4" />
            Add Customer
          </Button>
        </div>

        {/* Stats Cards */}
        {loading ? (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            {Array.from({ length: 4 }).map((_, i) => (
              <Card key={i}>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <div className="h-4 w-20 bg-muted animate-pulse rounded"></div>
                  <div className="h-4 w-4 bg-muted animate-pulse rounded"></div>
                </CardHeader>
                <CardContent>
                  <div className="h-8 w-16 bg-muted animate-pulse rounded mb-2"></div>
                  <div className="h-3 w-24 bg-muted animate-pulse rounded"></div>
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Total Customers
                </CardTitle>
                <Users className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{paginationInfo.count}</div>
                <p className="text-xs text-muted-foreground">
                  All registered customers
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Active Customers
                </CardTitle>
                <UserCheck className="h-4 w-4 text-green-500" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {activeCustomers.length}
                </div>
                <p className="text-xs text-muted-foreground">
                  {customersData.length > 0
                    ? (
                        (activeCustomers.length / customersData.length) *
                        100
                      ).toFixed(1)
                    : 0}
                  % of total
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Inactive Customers
                </CardTitle>
                <Users className="h-4 w-4 text-red-500" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {inactiveCustomers.length}
                </div>
                <p className="text-xs text-muted-foreground">
                  Need re-engagement
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  New This Month
                </CardTitle>
                <Plus className="h-4 w-4 text-blue-500" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {
                    customersData.filter((c) => {
                      const created = new Date(c.created_at);
                      const thisMonth = new Date();
                      return (
                        created.getMonth() === thisMonth.getMonth() &&
                        created.getFullYear() === thisMonth.getFullYear()
                      );
                    }).length
                  }
                </div>
                <p className="text-xs text-muted-foreground">
                  New registrations
                </p>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Customers Table */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Customer Directory</CardTitle>
                <CardDescription>
                  Manage and view all customer information
                </CardDescription>
              </div>
              <div className="flex items-center space-x-2">
                <div className="relative">
                  <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                  <Input
                    placeholder="Search customers..."
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
                <span className="ml-2">Loading customers...</span>
              </div>
            ) : error ? (
              <div className="flex flex-col items-center justify-center py-8 text-muted-foreground">
                <p className="mb-4">Failed to load customers from API</p>
                <p className="text-sm text-red-500 mb-4">{error}</p>
                <Button variant="outline" size="sm" onClick={refetch}>
                  Retry
                </Button>
              </div>
            ) : filteredCustomers.length === 0 ? (
              <div className="flex items-center justify-center py-8 text-muted-foreground">
                <p>
                  {searchTerm
                    ? `No customers found matching "${searchTerm}"`
                    : "No customers found. Add your first customer to get started."}
                </p>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="text-sm text-muted-foreground">
                    Showing {filteredCustomers.length} of {paginationInfo.count}{" "}
                    customers
                    {searchTerm && (
                      <span className="ml-2 text-primary">
                        • Filtered by "{searchTerm}"
                      </span>
                    )}
                  </div>
                </div>
                <div className="space-y-4">
                  {filteredCustomers.map((customer: Customer) => (
                    <div
                      key={customer.id}
                      className="flex items-center justify-between p-4 border rounded-lg hover:bg-accent/50 transition-colors"
                    >
                      <div className="flex items-center space-x-4">
                        <div className="h-12 w-12 bg-muted rounded-full flex items-center justify-center overflow-hidden">
                          {customer.photo ? (
                            <ProductImage
                              src={customer.photo}
                              alt={`${customer.first_name} ${customer.last_name}`}
                              className="h-full w-full object-cover"
                            />
                          ) : (
                            <Users className="h-6 w-6 text-muted-foreground" />
                          )}
                        </div>
                        <div>
                          <h4
                            className="text-sm font-medium hover:text-primary cursor-pointer transition-colors"
                            onClick={() =>
                              router.push(`/customers/${customer.id}`)
                            }
                          >
                            {customer.first_name} {customer.last_name}
                          </h4>
                          <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                            <Mail className="h-3 w-3" />
                            <span>{customer.email}</span>
                          </div>
                          <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                            <Phone className="h-3 w-3" />
                            <span>{customer.phone}</span>
                          </div>
                          {customer.address && (
                            <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                              <span>📍</span>
                              <span className="truncate max-w-[200px]">
                                {customer.address}
                              </span>
                            </div>
                          )}
                        </div>
                      </div>

                      <div className="flex items-center space-x-4">
                        <div className="text-right">
                          <div className="text-sm font-medium">
                            ID: {customer.id}
                          </div>
                          <div className="text-xs text-muted-foreground">
                            Tax: {customer.tax_number}
                          </div>
                          <div className="text-xs text-muted-foreground">
                            Joined: {formatDate(customer.created_at)}
                          </div>
                        </div>

                        <Badge
                          variant={getStatusBadgeVariant(customer.is_active)}
                        >
                          {getStatusText(customer.is_active)}
                        </Badge>

                        <div className="flex items-center space-x-1">
                          <Button
                            variant="ghost"
                            size="icon"
                            onClick={() =>
                              router.push(`/customers/${customer.id}`)
                            }
                            title="View Details"
                          >
                            <Eye className="h-4 w-4" />
                          </Button>
                          <Button
                            variant="ghost"
                            size="icon"
                            title="Edit Customer"
                          >
                            <Edit className="h-4 w-4" />
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
                            paginationInfo.count - customersData.length
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
      </div>
    </DashboardLayout>
  );
}
