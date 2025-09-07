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
import { Sale } from "@/lib/interfaces";
import {
  ArrowUpDown,
  DollarSign,
  Eye,
  Filter,
  Loader2,
  Plus,
  Search,
  ShoppingCart,
  TrendingUp,
} from "lucide-react";
import { useState } from "react";

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

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return {
    date: date.toLocaleDateString("en-KE"),
    time: date.toLocaleTimeString("en-KE", {
      hour: "2-digit",
      minute: "2-digit",
    }),
    fullDate: date.toLocaleDateString("en-KE", {
      year: "numeric",
      month: "short",
      day: "numeric",
    }),
  };
};

const getStatusFromReceipt = (receipt_is_printed: boolean) => {
  return receipt_is_printed ? "Completed" : "Pending";
};

export default function SalesPage() {
  const [searchTerm, setSearchTerm] = useState("");
  const [sortBy, setSortBy] = useState<"date" | "amount" | "customer">("date");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("desc");

  // Use the API hook to fetch sales with pagination
  const {
    data: sales,
    loading,
    error,
    paginationInfo,
    refetch,
    loadMore,
  } = useSales();

  // Use API data if available, otherwise use empty array
  const salesData: Sale[] = sales || [];

  // Filter and sort sales data
  const filteredAndSortedSales = salesData
    .filter((sale) => {
      const searchLower = searchTerm.toLowerCase();
      const saleId = `SALE-${sale.id}`.toLowerCase();
      const customerId = `Customer #${sale.customer}`.toLowerCase();
      const amount = sale.grand_total.toString();

      return (
        saleId.includes(searchLower) ||
        customerId.includes(searchLower) ||
        amount.includes(searchLower)
      );
    })
    .sort((a, b) => {
      let comparison = 0;

      switch (sortBy) {
        case "date":
          comparison =
            new Date(a.created_at).getTime() - new Date(b.created_at).getTime();
          break;
        case "amount":
          comparison = a.grand_total - b.grand_total;
          break;
        case "customer":
          comparison = a.customer - b.customer;
          break;
        default:
          comparison = 0;
      }

      return sortOrder === "asc" ? comparison : -comparison;
    });

  // Calculate today's sales based on created_at date
  const today = new Date().toISOString().split("T")[0];
  const yesterday = new Date(Date.now() - 24 * 60 * 60 * 1000)
    .toISOString()
    .split("T")[0];

  const todaysSales = salesData.filter((sale) => {
    const saleDate = new Date(sale.created_at).toISOString().split("T")[0];
    return saleDate === today;
  });

  const yesterdaysSales = salesData.filter((sale) => {
    const saleDate = new Date(sale.created_at).toISOString().split("T")[0];
    return saleDate === yesterday;
  });

  const totalRevenue = todaysSales.reduce(
    (sum, sale) => sum + sale.grand_total,
    0
  );

  const yesterdayRevenue = yesterdaysSales.reduce(
    (sum, sale) => sum + sale.grand_total,
    0
  );

  const averageOrderValue =
    todaysSales.length > 0 ? totalRevenue / todaysSales.length : 0;

  const yesterdayAvgOrderValue =
    yesterdaysSales.length > 0 ? yesterdayRevenue / yesterdaysSales.length : 0;

  const pendingSales = salesData.filter(
    (sale) => !sale.receipt_is_printed
  ).length;

  const completedSales = salesData.filter(
    (sale) => sale.receipt_is_printed
  ).length;

  // Additional statistics
  const totalAllTimeRevenue = salesData.reduce(
    (sum, sale) => sum + sale.grand_total,
    0
  );
  const totalTaxCollected = salesData.reduce(
    (sum, sale) => sum + sale.tax_amount,
    0
  );
  const todaysTaxCollected = todaysSales.reduce(
    (sum, sale) => sum + sale.tax_amount,
    0
  );
  const avgTaxRate =
    salesData.length > 0
      ? salesData.reduce((sum, sale) => sum + sale.tax_percentage, 0) /
        salesData.length
      : 0;

  // Top performing days (by revenue)
  const salesByDate = salesData.reduce((acc: Record<string, number>, sale) => {
    const date = new Date(sale.created_at).toISOString().split("T")[0];
    acc[date] = (acc[date] || 0) + sale.grand_total;
    return acc;
  }, {});

  const highestRevenueDay = Object.entries(salesByDate).reduce(
    (max, [date, revenue]) => (revenue > max.revenue ? { date, revenue } : max),
    { date: "", revenue: 0 }
  );

  // Calculate percentage changes
  const salesChangePercent =
    yesterdaysSales.length > 0
      ? ((todaysSales.length - yesterdaysSales.length) /
          yesterdaysSales.length) *
        100
      : todaysSales.length > 0
      ? 100
      : 0;

  const revenueChangePercent =
    yesterdayRevenue > 0
      ? ((totalRevenue - yesterdayRevenue) / yesterdayRevenue) * 100
      : totalRevenue > 0
      ? 100
      : 0;

  const avgOrderChangePercent =
    yesterdayAvgOrderValue > 0
      ? ((averageOrderValue - yesterdayAvgOrderValue) /
          yesterdayAvgOrderValue) *
        100
      : averageOrderValue > 0
      ? 100
      : 0;

  // Helper function to format percentage change
  const formatPercentChange = (percent: number) => {
    const sign = percent >= 0 ? "+" : "";
    return `${sign}${percent.toFixed(1)}%`;
  };

  const getChangeColor = (percent: number) => {
    if (percent > 0) return "text-green-600";
    if (percent < 0) return "text-red-600";
    return "text-muted-foreground";
  };
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
        {loading ? (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4 xl:grid-cols-4">
            {Array.from({ length: 6 }).map((_, i) => (
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
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4 xl:grid-cols-4">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Today's Sales
                </CardTitle>
                <ShoppingCart className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{todaysSales.length}</div>
                <p className={`text-xs ${getChangeColor(salesChangePercent)}`}>
                  {formatPercentChange(salesChangePercent)} from yesterday
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
                <p
                  className={`text-xs ${getChangeColor(revenueChangePercent)}`}
                >
                  {formatPercentChange(revenueChangePercent)} from yesterday
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
                <p
                  className={`text-xs ${getChangeColor(avgOrderChangePercent)}`}
                >
                  {formatPercentChange(avgOrderChangePercent)} from yesterday
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Total Sales
                </CardTitle>
                <ShoppingCart className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{paginationInfo.count}</div>
                <p className="text-xs text-muted-foreground">
                  All time transactions
                </p>
              </CardContent>
            </Card>
          </div>
        )}

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
                  <Input
                    placeholder="Search sales..."
                    className="pl-8 w-64"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                  />
                </div>
                <Button
                  variant="outline"
                  size="icon"
                  onClick={() => {
                    const newOrder = sortOrder === "asc" ? "desc" : "asc";
                    setSortOrder(newOrder);
                  }}
                >
                  <ArrowUpDown className="h-4 w-4" />
                </Button>
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
            ) : filteredAndSortedSales.length === 0 ? (
              <div className="flex items-center justify-center py-8 text-muted-foreground">
                <p>
                  {searchTerm
                    ? `No sales found matching "${searchTerm}"`
                    : "No sales found. Make your first sale to get started."}
                </p>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="text-sm text-muted-foreground">
                    Showing {filteredAndSortedSales.length} of{" "}
                    {paginationInfo.count} sales
                    {searchTerm && (
                      <span className="ml-2 text-primary">
                        • Filtered by "{searchTerm}"
                      </span>
                    )}
                  </div>
                  <div className="text-sm text-muted-foreground">
                    Total:{" "}
                    {formatCurrency(
                      filteredAndSortedSales.reduce(
                        (sum, sale) => sum + sale.grand_total,
                        0
                      )
                    )}
                  </div>
                </div>
                <div className="space-y-4">
                  {filteredAndSortedSales.map((sale: Sale) => {
                    const { date, time, fullDate } = formatDate(
                      sale.created_at
                    );
                    const status = getStatusFromReceipt(
                      sale.receipt_is_printed
                    );

                    return (
                      <div
                        key={sale.id}
                        className="flex items-center justify-between p-4 border rounded-lg hover:bg-accent/50 transition-colors"
                      >
                        <div className="flex items-center space-x-4">
                          <div className="h-12 w-12 bg-muted rounded-lg flex items-center justify-center">
                            <ShoppingCart className="h-6 w-6 text-muted-foreground" />
                          </div>
                          <div>
                            <h4 className="text-sm font-medium">
                              SALE-{sale.id}
                            </h4>
                            <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                              <span>Customer #{sale.customer}</span>
                              <span>•</span>
                              <span>
                                {fullDate} at {time}
                              </span>
                            </div>
                          </div>
                        </div>

                        <div className="flex items-center space-x-4">
                          <div className="text-right">
                            <div className="text-sm font-medium">
                              {formatCurrency(sale.grand_total)}
                            </div>
                            <div className="text-xs text-muted-foreground">
                              Tax: {formatCurrency(sale.tax_amount)} (
                              {sale.tax_percentage}%)
                              {sale.discount > 0 &&
                                ` • Discount: ${formatCurrency(sale.discount)}`}
                            </div>
                          </div>

                          <Badge variant={getStatusBadgeVariant(status)}>
                            {status}
                          </Badge>

                          <Button variant="ghost" size="icon">
                            <Eye className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                    );
                  })}

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
                            paginationInfo.count - salesData.length
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
