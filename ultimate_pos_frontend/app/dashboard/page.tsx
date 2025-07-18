import DashboardLayout from "@/components/layout/dashboard-layout";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  DollarSign,
  Package,
  ShoppingCart,
  TrendingDown,
  TrendingUp,
  Users,
} from "lucide-react";

// Mock data for dashboard cards
const dashboardStats = [
  {
    title: "Total Revenue",
    value: "$12,345",
    change: "+12.5%",
    trend: "up" as const,
    icon: DollarSign,
  },
  {
    title: "Total Sales",
    value: "1,234",
    change: "+8.2%",
    trend: "up" as const,
    icon: ShoppingCart,
  },
  {
    title: "Total Customers",
    value: "856",
    change: "+3.1%",
    trend: "up" as const,
    icon: Users,
  },
  {
    title: "Products in Stock",
    value: "2,456",
    change: "-2.3%",
    trend: "down" as const,
    icon: Package,
  },
];

// Mock data for recent sales
const recentSales = [
  {
    id: "1",
    customer: "John Doe",
    amount: "$125.00",
    status: "Completed",
    time: "2 minutes ago",
  },
  {
    id: "2",
    customer: "Jane Smith",
    amount: "$89.50",
    status: "Pending",
    time: "5 minutes ago",
  },
  {
    id: "3",
    customer: "Bob Johnson",
    amount: "$234.75",
    status: "Completed",
    time: "10 minutes ago",
  },
  {
    id: "4",
    customer: "Alice Brown",
    amount: "$67.25",
    status: "Completed",
    time: "15 minutes ago",
  },
];

export default function DashboardPage() {
  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
          <p className="text-muted-foreground">
            Welcome back! Here's what's happening with your business today.
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {dashboardStats.map((stat) => {
            const Icon = stat.icon;
            return (
              <Card key={stat.title}>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">
                    {stat.title}
                  </CardTitle>
                  <Icon className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{stat.value}</div>
                  <div className="flex items-center space-x-1 text-xs text-muted-foreground">
                    {stat.trend === "up" ? (
                      <TrendingUp className="h-3 w-3 text-green-500" />
                    ) : (
                      <TrendingDown className="h-3 w-3 text-red-500" />
                    )}
                    <span
                      className={
                        stat.trend === "up" ? "text-green-500" : "text-red-500"
                      }
                    >
                      {stat.change}
                    </span>
                    <span>from last month</span>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>

        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
          {/* Recent Sales */}
          <Card className="col-span-4">
            <CardHeader>
              <CardTitle>Recent Sales</CardTitle>
              <CardDescription>
                Latest transactions from your store
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {recentSales.map((sale) => (
                  <div
                    key={sale.id}
                    className="flex items-center justify-between"
                  >
                    <div className="space-y-1">
                      <p className="text-sm font-medium leading-none">
                        {sale.customer}
                      </p>
                      <p className="text-xs text-muted-foreground">
                        {sale.time}
                      </p>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Badge
                        variant={
                          sale.status === "Completed" ? "default" : "secondary"
                        }
                      >
                        {sale.status}
                      </Badge>
                      <div className="text-sm font-medium">{sale.amount}</div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Quick Actions */}
          <Card className="col-span-3">
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
              <CardDescription>Common tasks you can perform</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center justify-between p-3 border rounded-lg hover:bg-accent cursor-pointer transition-colors">
                  <div>
                    <p className="text-sm font-medium">New Sale</p>
                    <p className="text-xs text-muted-foreground">
                      Process a new transaction
                    </p>
                  </div>
                  <ShoppingCart className="h-4 w-4 text-muted-foreground" />
                </div>
                <div className="flex items-center justify-between p-3 border rounded-lg hover:bg-accent cursor-pointer transition-colors">
                  <div>
                    <p className="text-sm font-medium">Add Product</p>
                    <p className="text-xs text-muted-foreground">
                      Add new product to inventory
                    </p>
                  </div>
                  <Package className="h-4 w-4 text-muted-foreground" />
                </div>
                <div className="flex items-center justify-between p-3 border rounded-lg hover:bg-accent cursor-pointer transition-colors">
                  <div>
                    <p className="text-sm font-medium">Add Customer</p>
                    <p className="text-xs text-muted-foreground">
                      Register a new customer
                    </p>
                  </div>
                  <Users className="h-4 w-4 text-muted-foreground" />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Low Stock Alert */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Package className="h-5 w-5" />
              <span>Low Stock Alert</span>
            </CardTitle>
            <CardDescription>Products that need restocking</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {["Widget A", "Gadget B", "Tool C"].map((product, index) => (
                <div
                  key={product}
                  className="flex items-center justify-between"
                >
                  <div>
                    <p className="text-sm font-medium">{product}</p>
                    <p className="text-xs text-muted-foreground">
                      Only {3 - index} items left in stock
                    </p>
                  </div>
                  <Badge variant="destructive">Low Stock</Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}
