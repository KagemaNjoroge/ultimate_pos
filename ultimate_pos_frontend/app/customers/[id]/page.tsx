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
import { ProductImage } from "@/components/ui/product-image";
import { Separator } from "@/components/ui/separator";
import { apiService } from "@/lib/api";
import { useApi } from "@/lib/hooks";
import {
  ArrowLeft,
  Calendar,
  CheckCircle,
  Clock,
  CreditCard,
  Edit,
  Loader2,
  Mail,
  MapPin,
  Phone,
  Receipt,
  User,
  XCircle,
} from "lucide-react";
import { useParams, useRouter } from "next/navigation";
import { useState } from "react";

// Customer interface
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

// Sale interface for customer's purchase history
interface Sale {
  id: number;
  created_at: string;
  updated_at: string;
  grand_total: number;
  tax_amount: number;
  tax_percentage: number;
  sub_total: number;
  receipt_is_printed: boolean;
  customer: number;
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString("en-KE", {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};

const formatPrice = (price: number) => {
  return new Intl.NumberFormat("en-KE", {
    style: "currency",
    currency: "KES",
    minimumFractionDigits: 0,
  }).format(price);
};

const getStatusBadgeVariant = (status: string) => {
  switch (status.toLowerCase()) {
    case "completed":
      return "default";
    case "pending":
      return "secondary";
    case "cancelled":
      return "destructive";
    default:
      return "outline";
  }
};

const getPaymentMethodIcon = (method: string) => {
  switch (method.toLowerCase()) {
    case "mpesa":
    case "m-pesa":
      return <CreditCard className="h-4 w-4" />;
    case "cash":
      return <Receipt className="h-4 w-4" />;
    default:
      return <CreditCard className="h-4 w-4" />;
  }
};

export default function CustomerDetailPage() {
  const params = useParams();
  const router = useRouter();
  const customerId = params.id as string;

  // State for managing tabs or sections
  const [activeTab, setActiveTab] = useState<
    "overview" | "purchases" | "activity"
  >("overview");

  // Fetch customer details
  const {
    data: customer,
    loading: customerLoading,
    error: customerError,
    refetch: refetchCustomer,
  } = useApi<Customer>(
    () => apiService.customers.getById(Number(customerId)),
    [customerId]
  );

  // Fetch customer's sales history
  const {
    data: customerSales,
    loading: salesLoading,
    error: salesError,
  } = useApi<Sale[]>(
    () =>
      apiService.sales
        .getAll({
          customer: Number(customerId),
        })
        .then((response) => ({
          ...response,
          data: response.data.results.filter(
            (sale: Sale) => sale.customer === Number(customerId)
          ),
        })),
    [customerId]
  );

  const sales: Sale[] = customerSales || [];

  // Calculate customer statistics
  const totalPurchases = sales.length;
  const totalSpent = sales.reduce((sum, sale) => sum + sale.grand_total, 0);
  const completedPurchases = sales.filter(
    (sale) => sale.receipt_is_printed === true
  ).length;
  const lastPurchase =
    sales.length > 0
      ? sales.sort(
          (a, b) =>
            new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
        )[0]
      : null;

  if (customerLoading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4" />
            <p>Loading customer details...</p>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  if (customerError || !customer) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <XCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
            <h2 className="text-xl font-semibold mb-2">Customer Not Found</h2>
            <p className="text-muted-foreground mb-4">
              {customerError ||
                "The customer you're looking for doesn't exist."}
            </p>
            <Button onClick={() => router.push("/customers")}>
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back to Customers
            </Button>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Button
              variant="outline"
              size="icon"
              onClick={() => router.push("/customers")}
            >
              <ArrowLeft className="h-4 w-4" />
            </Button>
            <div>
              <h1 className="text-3xl font-bold tracking-tight">
                {customer.first_name || ""} {customer.last_name || ""}
              </h1>
              <p className="text-muted-foreground">
                Customer ID: {customer.id} • Joined{" "}
                {formatDate(customer.created_at)}
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <Badge variant={customer.is_active ? "default" : "destructive"}>
              {customer.is_active ? "Active" : "Inactive"}
            </Badge>
            <Button size="sm">
              <Edit className="mr-2 h-4 w-4" />
              Edit Customer
            </Button>
          </div>
        </div>

        {/* Customer Overview Cards */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Total Purchases
              </CardTitle>
              <Receipt className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{totalPurchases}</div>
              <p className="text-xs text-muted-foreground">
                {completedPurchases} completed
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Spent</CardTitle>
              <CreditCard className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {formatPrice(totalSpent)}
              </div>
              <p className="text-xs text-muted-foreground">
                {totalPurchases > 0
                  ? formatPrice(totalSpent / totalPurchases)
                  : formatPrice(0)}{" "}
                avg per order
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Last Purchase
              </CardTitle>
              <Clock className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {lastPurchase ? formatPrice(lastPurchase.grand_total) : "—"}
              </div>
              <p className="text-xs text-muted-foreground">
                {lastPurchase
                  ? formatDate(lastPurchase.created_at)
                  : "No purchases yet"}
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Customer Status
              </CardTitle>
              {customer.is_active ? (
                <CheckCircle className="h-4 w-4 text-green-500" />
              ) : (
                <XCircle className="h-4 w-4 text-red-500" />
              )}
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {customer.is_active ? "Active" : "Inactive"}
              </div>
              <p className="text-xs text-muted-foreground">
                Last updated {formatDate(customer.updated_at)}
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Main Content */}
        <div className="grid gap-6 md:grid-cols-3">
          {/* Customer Information */}
          <Card className="md:col-span-1">
            <CardHeader>
              <CardTitle>Customer Information</CardTitle>
              <CardDescription>
                Personal details and contact information
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Profile Photo */}
              <div className="flex items-center space-x-4">
                <div className="h-16 w-16 bg-muted rounded-full flex items-center justify-center overflow-hidden">
                  {customer.photo ? (
                    <ProductImage
                      src={customer.photo}
                      alt={`${customer.first_name || ""} ${
                        customer.last_name || ""
                      }`}
                      className="h-full w-full object-cover"
                    />
                  ) : (
                    <User className="h-8 w-8 text-muted-foreground" />
                  )}
                </div>
                <div>
                  <h3 className="font-medium">
                    {customer.first_name || ""} {customer.last_name || ""}
                  </h3>
                  <p className="text-sm text-muted-foreground">
                    Customer #{customer.id}
                  </p>
                </div>
              </div>

              <Separator />

              {/* Contact Details */}
              <div className="space-y-4">
                <div className="flex items-center space-x-3">
                  <Mail className="h-4 w-4 text-muted-foreground" />
                  <div>
                    <p className="font-medium">Email</p>
                    <p className="text-sm text-muted-foreground">
                      {customer.email || "No email provided"}
                    </p>
                  </div>
                </div>

                <div className="flex items-center space-x-3">
                  <Phone className="h-4 w-4 text-muted-foreground" />
                  <div>
                    <p className="font-medium">Phone</p>
                    <p className="text-sm text-muted-foreground">
                      {customer.phone || "No phone provided"}
                    </p>
                  </div>
                </div>

                <div className="flex items-start space-x-3">
                  <MapPin className="h-4 w-4 text-muted-foreground mt-1" />
                  <div>
                    <p className="font-medium">Address</p>
                    <p className="text-sm text-muted-foreground">
                      {customer.address || "No address provided"}
                    </p>
                  </div>
                </div>

                <div className="flex items-center space-x-3">
                  <Receipt className="h-4 w-4 text-muted-foreground" />
                  <div>
                    <p className="font-medium">Tax Number</p>
                    <p className="text-sm text-muted-foreground">
                      {customer.tax_number || "No tax number provided"}
                    </p>
                  </div>
                </div>

                <div className="flex items-center space-x-3">
                  <Calendar className="h-4 w-4 text-muted-foreground" />
                  <div>
                    <p className="font-medium">Member Since</p>
                    <p className="text-sm text-muted-foreground">
                      {formatDate(customer.created_at)}
                    </p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Purchase History */}
          <Card className="md:col-span-2">
            <CardHeader>
              <CardTitle>Purchase History</CardTitle>
              <CardDescription>
                Complete history of customer's transactions
              </CardDescription>
            </CardHeader>
            <CardContent>
              {salesLoading ? (
                <div className="flex items-center justify-center py-8">
                  <Loader2 className="h-6 w-6 animate-spin" />
                  <span className="ml-2">Loading purchase history...</span>
                </div>
              ) : salesError ? (
                <div className="text-center py-8 text-muted-foreground">
                  <p>Failed to load purchase history</p>
                  <p className="text-sm text-red-500">{salesError}</p>
                </div>
              ) : sales.length === 0 ? (
                <div className="text-center py-8 text-muted-foreground">
                  <Receipt className="h-12 w-12 mx-auto mb-4 opacity-50" />
                  <p>No purchases found</p>
                  <p className="text-sm">
                    This customer hasn't made any purchases yet.
                  </p>
                </div>
              ) : (
                <div className="space-y-4">
                  {sales
                    .sort(
                      (a, b) =>
                        new Date(b.created_at).getTime() -
                        new Date(a.created_at).getTime()
                    )
                    .map((sale) => (
                      <div
                        key={sale.id}
                        className="flex items-center justify-between p-4 border rounded-lg hover:bg-accent/50 transition-colors"
                      >
                        <div className="flex items-center space-x-4">
                          <div className="h-10 w-10 bg-muted rounded-lg flex items-center justify-center">
                            {getPaymentMethodIcon("mpesa")}
                          </div>
                          <div>
                            <h4 className="font-medium">Sale #{sale.id}</h4>
                            <p className="text-sm text-muted-foreground">
                              {formatDate(sale.created_at)}
                            </p>
                          </div>
                        </div>

                        <div className="flex items-center space-x-4">
                          <div className="text-right">
                            <div className="font-medium">
                              {formatPrice(sale.grand_total)}
                            </div>
                            <div className="text-sm text-muted-foreground">
                              {"mpesa"}
                            </div>
                          </div>
                          <Badge
                            variant={getStatusBadgeVariant(
                              sale.receipt_is_printed ? "Completed" : "Pending"
                            )}
                          >
                            {sale.receipt_is_printed ? "Completed" : "Pending"}
                          </Badge>
                          <Button variant="ghost" size="icon">
                            <ArrowLeft className="h-4 w-4 rotate-180" />
                          </Button>
                        </div>
                      </div>
                    ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  );
}
