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
import { useProducts, useStock } from "@/lib/hooks";
import {
  AlertTriangle,
  Edit,
  Filter,
  Loader2,
  Package,
  Plus,
  Search,
  TrendingDown,
  Warehouse,
} from "lucide-react";
import { useEffect, useMemo, useState } from "react";

// Stock interface based on API response
interface Stock {
  id: number;
  created_at: string;
  updated_at: string;
  quantity: number;
  alert_quantity: number;
  cost_price: string;
  selling_price: string;
  reserved_quantity: number;
  available_quantity: number;
  minimum_stock_level: number;
  maximum_stock_level: number | null;
  location: string | null;
  warehouse: string | null;
  batch_number: string | null;
  serial_number: string | null;
  expiry_date: string | null;
  manufacturing_date: string | null;
  is_active: boolean;
  is_damaged: boolean;
  is_expired: boolean;
  supplier_sku: string | null;
  notes: string | null;
  last_restocked_date: string | null;
  last_sold_date: string | null;
  product: number;
  branch: number | null;
}

// Product interface
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
}

const getStatusBadgeVariant = (status: string) => {
  switch (status) {
    case "In Stock":
      return "default";
    case "Low Stock":
      return "secondary";
    case "Out of Stock":
      return "destructive";
    case "Overstocked":
      return "outline";
    default:
      return "default";
  }
};

const getStockStatus = (stock: Stock) => {
  if (!stock.is_active) return "Inactive";
  if (stock.is_damaged) return "Damaged";
  if (stock.is_expired) return "Expired";
  if (stock.quantity === 0) return "Out of Stock";
  if (
    stock.quantity <= stock.alert_quantity ||
    stock.quantity <= stock.minimum_stock_level
  )
    return "Low Stock";
  if (
    stock.maximum_stock_level &&
    stock.quantity >= stock.maximum_stock_level * 0.9
  )
    return "Overstocked";
  return "In Stock";
};

const formatDate = (dateString: string | null) => {
  if (!dateString) return "N/A";
  return new Date(dateString).toLocaleDateString("en-KE", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
};

const formatPrice = (price: string | number) => {
  const numPrice = typeof price === "string" ? parseFloat(price) : price;
  return new Intl.NumberFormat("en-KE", {
    style: "currency",
    currency: "KES",
    minimumFractionDigits: 0,
  }).format(numPrice);
};

export default function StockPage() {
  const [searchTerm, setSearchTerm] = useState("");

  // Fetch stock data
  const {
    data: stockData,
    loading: stockLoading,
    error: stockError,
    paginationInfo: stockPaginationInfo,
    refetch: refetchStock,
    loadMore: loadMoreStock,
  } = useStock();

  // Fetch products data to get product names - use large limit to get all products
  const {
    data: productsData,
    loading: productsLoading,
    error: productsError,
    loadMore: loadMoreProducts,
    paginationInfo: productsPagination,
  } = useProducts({ limit: 1000 }); // Large limit to ensure we get all products

  const stockItems: Stock[] = stockData || [];
  const products: Product[] = productsData || [];

  // Create a product lookup map for efficient searching
  const productMap = useMemo(() => {
    const map = new Map<number, Product>();
    products.forEach((product) => {
      map.set(product.id, product);
    });

    // Debug logging
    const missingProductIds = stockItems
      .filter((stock) => !map.has(stock.product))
      .map((stock) => stock.product);
    if (missingProductIds.length > 0) {
      console.log("Missing product IDs:", missingProductIds);
      console.log(
        "Available product IDs:",
        products.map((p) => p.id)
      );
    } else if (stockItems.length > 0) {
      console.log("All products found successfully!");
    }

    return map;
  }, [products, stockItems]);

  // Auto-load more products if we have more pages and missing products
  const [hasTriedLoadingMore, setHasTriedLoadingMore] = useState(false);

  useEffect(() => {
    if (
      !productsLoading &&
      !hasTriedLoadingMore &&
      productsPagination.hasNext
    ) {
      // Check if we have missing products
      const hasMissingProducts = stockItems.some(
        (stock) => !productMap.has(stock.product)
      );

      if (hasMissingProducts) {
        console.log("Loading more products to find missing items...");
        loadMoreProducts();
        setHasTriedLoadingMore(true);
      }
    }
  }, [
    stockItems,
    productMap,
    productsLoading,
    hasTriedLoadingMore,
    productsPagination.hasNext,
    loadMoreProducts,
  ]);

  // Filter stock items based on search term
  const filteredStockItems = useMemo(() => {
    if (!searchTerm.trim()) return stockItems;

    const searchLower = searchTerm.toLowerCase();
    return stockItems.filter((stock) => {
      const product = productMap.get(stock.product);
      const productName = (product?.name || "").toLowerCase();
      const location = (stock.location || "").toLowerCase();
      const warehouse = (stock.warehouse || "").toLowerCase();
      const batchNumber = (stock.batch_number || "").toLowerCase();
      const serialNumber = (stock.serial_number || "").toLowerCase();
      const supplierSku = (stock.supplier_sku || "").toLowerCase();

      return (
        productName.includes(searchLower) ||
        location.includes(searchLower) ||
        warehouse.includes(searchLower) ||
        batchNumber.includes(searchLower) ||
        serialNumber.includes(searchLower) ||
        supplierSku.includes(searchLower)
      );
    });
  }, [stockItems, searchTerm, productMap]);

  // Calculate statistics
  const totalValue = useMemo(() => {
    return stockItems.reduce((sum, item) => {
      const costPrice = parseFloat(item.cost_price) || 0;
      return sum + item.quantity * costPrice;
    }, 0);
  }, [stockItems]);

  const lowStockItems = useMemo(() => {
    return stockItems.filter((item) => {
      const status = getStockStatus(item);
      return status === "Low Stock";
    });
  }, [stockItems]);

  const outOfStockItems = useMemo(() => {
    return stockItems.filter((item) => item.quantity === 0);
  }, [stockItems]);

  const loading = stockLoading || productsLoading;
  const error = stockError || productsError;
  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-3xl font-bold tracking-tight">
              Stock Management
            </h2>
            <p className="text-muted-foreground">
              Monitor and manage your inventory levels
            </p>
          </div>
          <Button>
            <Plus className="mr-2 h-4 w-4" />
            Add Stock
          </Button>
        </div>

        {/* Error State */}
        {error && (
          <Card className="border-destructive">
            <CardContent className="pt-6">
              <div className="flex items-center space-x-2 text-destructive">
                <AlertTriangle className="h-4 w-4" />
                <p>Error loading stock data: {error}</p>
              </div>
              <Button
                variant="outline"
                onClick={() => {
                  refetchStock();
                }}
                className="mt-2"
              >
                Retry
              </Button>
            </CardContent>
          </Card>
        )}

        {/* Stats Cards */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Items</CardTitle>
              <Package className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="flex items-center space-x-2">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span className="text-sm">Loading...</span>
                </div>
              ) : (
                <>
                  <div className="text-2xl font-bold">
                    {stockPaginationInfo.count}
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Different SKUs in inventory
                  </p>
                </>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Inventory Value
              </CardTitle>
              <Warehouse className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="flex items-center space-x-2">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span className="text-sm">Loading...</span>
                </div>
              ) : (
                <>
                  <div className="text-2xl font-bold">
                    {formatPrice(totalValue)}
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Total stock value at cost
                  </p>
                </>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Low Stock Items
              </CardTitle>
              <TrendingDown className="h-4 w-4 text-yellow-500" />
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="flex items-center space-x-2">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span className="text-sm">Loading...</span>
                </div>
              ) : (
                <>
                  <div className="text-2xl font-bold">
                    {lowStockItems.length}
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Items need restocking
                  </p>
                </>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Out of Stock
              </CardTitle>
              <AlertTriangle className="h-4 w-4 text-red-500" />
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="flex items-center space-x-2">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span className="text-sm">Loading...</span>
                </div>
              ) : (
                <>
                  <div className="text-2xl font-bold">
                    {outOfStockItems.length}
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Items completely depleted
                  </p>
                </>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Stock Table */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Inventory Overview</CardTitle>
                <CardDescription>
                  Current stock levels and inventory details
                </CardDescription>
              </div>
              <div className="flex items-center space-x-2">
                <div className="relative">
                  <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                  <Input
                    placeholder="Search inventory..."
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
                <span className="ml-2">Loading inventory...</span>
              </div>
            ) : filteredStockItems.length === 0 ? (
              <div className="text-center py-8">
                <Package className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <h3 className="text-lg font-medium">
                  No inventory items found
                </h3>
                <p className="text-muted-foreground">
                  {searchTerm
                    ? "Try adjusting your search terms"
                    : "Start by adding some stock items"}
                </p>
              </div>
            ) : (
              <div className="space-y-4">
                {filteredStockItems.map((item) => {
                  const product = productMap.get(item.product);
                  const status = getStockStatus(item);
                  const maxStock = item.maximum_stock_level || 100;
                  const stockPercentage = (item.quantity / maxStock) * 100;
                  const costPrice = parseFloat(item.cost_price) || 0;
                  const sellingPrice = parseFloat(item.selling_price) || 0;

                  return (
                    <div
                      key={item.id}
                      className="flex items-center justify-between p-4 border rounded-lg hover:bg-accent/50 transition-colors"
                    >
                      <div className="flex items-center space-x-4">
                        <div className="h-12 w-12 bg-muted rounded-lg flex items-center justify-center">
                          <Package className="h-6 w-6 text-muted-foreground" />
                        </div>
                        <div>
                          <h4 className="text-sm font-medium">
                            {productsLoading
                              ? `Product ${item.product} (Loading...)`
                              : product?.name
                              ? product.name
                              : `Product ${item.product} (Not Found)`}
                          </h4>
                          <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                            <span>ID: {item.id}</span>
                            {item.supplier_sku && (
                              <>
                                <span>•</span>
                                <span>SKU: {item.supplier_sku}</span>
                              </>
                            )}
                            {item.location && (
                              <>
                                <span>•</span>
                                <span>Location: {item.location}</span>
                              </>
                            )}
                          </div>
                          <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                            {costPrice > 0 && (
                              <>
                                <span>Cost: {formatPrice(costPrice)}</span>
                                <span>•</span>
                              </>
                            )}
                            {sellingPrice > 0 && (
                              <>
                                <span>Price: {formatPrice(sellingPrice)}</span>
                                <span>•</span>
                              </>
                            )}
                            <span>
                              Last Updated: {formatDate(item.updated_at)}
                            </span>
                          </div>
                          {item.warehouse && (
                            <div className="text-xs text-muted-foreground">
                              Warehouse: {item.warehouse}
                            </div>
                          )}
                          {item.batch_number && (
                            <div className="text-xs text-muted-foreground">
                              Batch: {item.batch_number}
                            </div>
                          )}
                          {item.expiry_date && (
                            <div className="text-xs text-muted-foreground">
                              Expires: {formatDate(item.expiry_date)}
                            </div>
                          )}
                        </div>
                      </div>

                      <div className="flex items-center space-x-4">
                        <div className="text-right">
                          <div className="text-sm font-medium">
                            {item.quantity}
                            {item.maximum_stock_level &&
                              ` / ${item.maximum_stock_level}`}
                          </div>
                          <div className="text-xs text-muted-foreground">
                            Alert: {item.alert_quantity}
                            {item.minimum_stock_level > 0 &&
                              ` | Min: ${item.minimum_stock_level}`}
                          </div>
                          {item.reserved_quantity > 0 && (
                            <div className="text-xs text-muted-foreground">
                              Reserved: {item.reserved_quantity}
                            </div>
                          )}
                          <div className="w-16 bg-muted rounded-full h-1.5 mt-1">
                            <div
                              className={`h-1.5 rounded-full ${
                                stockPercentage > 90
                                  ? "bg-orange-500"
                                  : stockPercentage > 20
                                  ? "bg-green-500"
                                  : stockPercentage > 0
                                  ? "bg-yellow-500"
                                  : "bg-red-500"
                              }`}
                              style={{
                                width: `${Math.min(stockPercentage, 100)}%`,
                              }}
                            />
                          </div>
                        </div>

                        <div className="flex flex-col space-y-1">
                          <Badge variant={getStatusBadgeVariant(status)}>
                            {status}
                          </Badge>
                          {item.is_damaged && (
                            <Badge variant="destructive" className="text-xs">
                              Damaged
                            </Badge>
                          )}
                          {item.is_expired && (
                            <Badge variant="destructive" className="text-xs">
                              Expired
                            </Badge>
                          )}
                          {!item.is_active && (
                            <Badge variant="secondary" className="text-xs">
                              Inactive
                            </Badge>
                          )}
                        </div>

                        <Button variant="ghost" size="icon">
                          <Edit className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  );
                })}

                {/* Load More Button */}
                {stockPaginationInfo.hasNext && (
                  <div className="flex justify-center pt-4">
                    <Button
                      variant="outline"
                      onClick={loadMoreStock}
                      disabled={stockLoading}
                    >
                      {stockLoading ? (
                        <>
                          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                          Loading...
                        </>
                      ) : (
                        `Load More (${
                          stockPaginationInfo.count - stockItems.length
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
