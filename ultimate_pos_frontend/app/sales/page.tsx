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
import { useSales } from "@/lib/hooks";
import {
  Calendar,
  DollarSign,
  Eye,
  Filter,
  Loader2,
  Plus,
  Search,
  ShoppingCart,
  TrendingUp,
} from "lucide-react";

// Sales type definition (adjust based on your API structure)
interface Sale {
  id: string | number;
  date: string;
  time?: string;
  customer?: string;
  items?: number;
  total: number;
  status: string;
  paymentMethod?: string;
}

// Mock data for fallback
const mockSalesData: Sale[] = [
  {
    id: "SALE-001",
    date: "2025-01-17",
    time: "14:30",
    customer: "John Doe",
    items: 3,
    total: 125.5,
    status: "Completed",
    paymentMethod: "Credit Card",
  },
  {
    id: "SALE-002",
    date: "2025-01-17",
    time: "13:45",
    customer: "Jane Smith",
    items: 2,
    total: 89.99,
    status: "Completed",
    paymentMethod: "Cash",
  },
  {
    id: "SALE-003",
    date: "2025-01-17",
    time: "12:20",
    customer: "Bob Johnson",
    items: 5,
    total: 234.75,
    status: "Pending",
    paymentMethod: "Debit Card",
  },
  {
    id: "SALE-004",
    date: "2025-01-16",
    time: "16:15",
    customer: "Alice Brown",
    items: 1,
    total: 67.25,
    status: "Completed",
    paymentMethod: "Cash",
  },
  {
    id: "SALE-005",
    date: "2025-01-16",
    time: "15:30",
    customer: "Mike Wilson",
    items: 4,
    total: 189.0,
    status: "Refunded",
    paymentMethod: "Credit Card",
  },
];

const getStatusBadgeVariant = (status: string) => {
  switch (status) {
    case "Completed":
      return "default";
    case "Pending":
      return "secondary";
    case "Refunded":
      return "destructive";
    default:
      return "default";
  }
};

const formatCurrency = (amount: number) => {
  return new Intl.NumberFormat("en-KE", {
    style: "currency",
    currency: "KES",
    minimumFractionDigits: 0,
  }).format(amount);
};

export default function SalesPage() {
  // Use the API hook to fetch sales
  const { data: apiSales, loading, error, refetch } = useSales();

  // Use API data if available, otherwise use mock data
  const salesData: Sale[] = apiSales || mockSalesData;

  const todaysSales = salesData.filter((sale) => sale.date === "2025-01-17");
  const totalRevenue = todaysSales.reduce((sum, sale) => sum + sale.total, 0);
  const averageOrderValue =
    todaysSales.length > 0 ? totalRevenue / todaysSales.length : 0;
  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-3xl font-bold tracking-tight">Sales</h2>
            <p className="text-muted-foreground">
              Track and manage all your sales transactions
            </p>
          </div>
          <Button>
            <Plus className="mr-2 h-4 w-4" />
            New Sale
          </Button>
        </div>

        {/* Stats Cards */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Today's Sales
              </CardTitle>
              <ShoppingCart className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{todaysSales.length}</div>
              <p className="text-xs text-muted-foreground">
                +12% from yesterday
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Today's Revenue
              </CardTitle>
              <DollarSign className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {formatCurrency(totalRevenue)}
              </div>
              <p className="text-xs text-muted-foreground">
                +8.2% from yesterday
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Avg. Order Value
              </CardTitle>
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {formatCurrency(averageOrderValue)}
              </div>
              <div className="text-2xl font-bold">
                ${averageOrderValue.toFixed(2)}
              </div>
              <p className="text-xs text-muted-foreground">
                +5.1% from yesterday
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Pending Orders
              </CardTitle>
              <Calendar className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {salesData.filter((s) => s.status === "Pending").length}
              </div>
              <p className="text-xs text-muted-foreground">
                Awaiting completion
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Sales Table */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Recent Sales</CardTitle>
                <CardDescription>
                  A list of recent sales transactions
                </CardDescription>
              </div>
              <div className="flex items-center space-x-2">
                <div className="relative">
                  <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                  <Input placeholder="Search sales..." className="pl-8 w-64" />
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
                <span className="ml-2">Loading sales...</span>
              </div>
            ) : error ? (
              <div className="flex flex-col items-center justify-center py-8 text-muted-foreground">
                <p className="mb-4">Failed to load sales from API</p>
                <p className="text-sm text-red-500 mb-4">{error}</p>
                <Button variant="outline" size="sm" onClick={refetch}>
                  Retry
                </Button>
              </div>
            ) : salesData.length === 0 ? (
              <div className="flex items-center justify-center py-8 text-muted-foreground">
                <p>No sales found. Make your first sale to get started.</p>
              </div>
            ) : (
              <div className="space-y-4">
                {salesData.map((sale: Sale) => (
                  <div
                    key={sale.id}
                    className="flex items-center justify-between p-4 border rounded-lg hover:bg-accent/50 transition-colors"
                  >
                    <div className="flex items-center space-x-4">
                      <div className="h-12 w-12 bg-muted rounded-lg flex items-center justify-center">
                        <ShoppingCart className="h-6 w-6 text-muted-foreground" />
                      </div>
                      <div>
                        <h4 className="text-sm font-medium">{sale.id}</h4>
                        <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                          <span>{sale.customer}</span>
                          <span>•</span>
                          <span>
                            {sale.date} at {sale.time}
                          </span>
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center space-x-4">
                      <div className="text-right">
                        <div className="text-sm font-medium">
                          {formatCurrency(sale.total)}
                        </div>
                        <div className="text-xs text-muted-foreground">
                          {sale.items} items • {sale.paymentMethod}
                        </div>
                      </div>

                      <Badge variant={getStatusBadgeVariant(sale.status)}>
                        {sale.status}
                      </Badge>

                      <Button variant="ghost" size="icon">
                        <Eye className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}
