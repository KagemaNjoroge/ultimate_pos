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
import {
  AlertTriangle,
  Edit,
  Filter,
  Package,
  Plus,
  Search,
  TrendingDown,
  Warehouse,
} from "lucide-react";

// Mock data for stock
const stockItems = [
  {
    id: "STK-001",
    name: "Wireless Headphones",
    sku: "WH-001",
    category: "Electronics",
    currentStock: 45,
    minStock: 10,
    maxStock: 100,
    costPrice: 50.0,
    sellingPrice: 99.99,
    supplier: "TechCorp",
    lastRestock: "2025-01-10",
    status: "In Stock",
  },
  {
    id: "STK-002",
    name: "Coffee Mug",
    sku: "CM-002",
    category: "Kitchenware",
    currentStock: 3,
    minStock: 5,
    maxStock: 50,
    costPrice: 6.0,
    sellingPrice: 12.99,
    supplier: "KitchenPlus",
    lastRestock: "2025-01-05",
    status: "Low Stock",
  },
  {
    id: "STK-003",
    name: "Laptop Stand",
    sku: "LS-003",
    category: "Office",
    currentStock: 0,
    minStock: 5,
    maxStock: 30,
    costPrice: 25.0,
    sellingPrice: 49.99,
    supplier: "OfficeMax",
    lastRestock: "2024-12-20",
    status: "Out of Stock",
  },
  {
    id: "STK-004",
    name: "Water Bottle",
    sku: "WB-004",
    category: "Sports",
    currentStock: 120,
    minStock: 20,
    maxStock: 150,
    costPrice: 8.0,
    sellingPrice: 19.99,
    supplier: "SportGear",
    lastRestock: "2025-01-15",
    status: "Overstocked",
  },
  {
    id: "STK-005",
    name: "Desk Lamp",
    sku: "DL-005",
    category: "Lighting",
    currentStock: 25,
    minStock: 10,
    maxStock: 40,
    costPrice: 18.0,
    sellingPrice: 34.99,
    supplier: "LightHouse",
    lastRestock: "2025-01-12",
    status: "In Stock",
  },
];

const totalValue = stockItems.reduce(
  (sum, item) => sum + item.currentStock * item.costPrice,
  0
);
const lowStockItems = stockItems.filter(
  (item) => item.currentStock <= item.minStock
);
const outOfStockItems = stockItems.filter((item) => item.currentStock === 0);

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

const getStockStatus = (item: (typeof stockItems)[0]) => {
  if (item.currentStock === 0) return "Out of Stock";
  if (item.currentStock <= item.minStock) return "Low Stock";
  if (item.currentStock >= item.maxStock * 0.9) return "Overstocked";
  return "In Stock";
};

export default function StockPage() {
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

        {/* Stats Cards */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Items</CardTitle>
              <Package className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stockItems.length}</div>
              <p className="text-xs text-muted-foreground">
                Different SKUs in inventory
              </p>
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
              <div className="text-2xl font-bold">${totalValue.toFixed(2)}</div>
              <p className="text-xs text-muted-foreground">
                Total stock value at cost
              </p>
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
              <div className="text-2xl font-bold">{lowStockItems.length}</div>
              <p className="text-xs text-muted-foreground">
                Items need restocking
              </p>
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
              <div className="text-2xl font-bold">{outOfStockItems.length}</div>
              <p className="text-xs text-muted-foreground">
                Items completely depleted
              </p>
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
                  />
                </div>
                <Button variant="outline" size="icon">
                  <Filter className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {stockItems.map((item) => {
                const status = getStockStatus(item);
                const stockPercentage =
                  (item.currentStock / item.maxStock) * 100;

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
                        <h4 className="text-sm font-medium">{item.name}</h4>
                        <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                          <span>SKU: {item.sku}</span>
                          <span>•</span>
                          <span>{item.category}</span>
                          <span>•</span>
                          <span>Supplier: {item.supplier}</span>
                        </div>
                        <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                          <span>Cost: ${item.costPrice}</span>
                          <span>•</span>
                          <span>Price: ${item.sellingPrice}</span>
                          <span>•</span>
                          <span>Last Restock: {item.lastRestock}</span>
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center space-x-4">
                      <div className="text-right">
                        <div className="text-sm font-medium">
                          {item.currentStock} / {item.maxStock}
                        </div>
                        <div className="text-xs text-muted-foreground">
                          Min: {item.minStock}
                        </div>
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

                      <Badge variant={getStatusBadgeVariant(status)}>
                        {status}
                      </Badge>

                      <Button variant="ghost" size="icon">
                        <Edit className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}
