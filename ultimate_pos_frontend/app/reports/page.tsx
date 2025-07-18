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
import {
  BarChart,
  Calendar,
  DollarSign,
  Download,
  FileText,
  PieChart,
  ShoppingCart,
  TrendingUp,
  Users,
} from "lucide-react";

// Mock data for reports
const salesReports = [
  {
    id: "RPT-001",
    title: "Daily Sales Report",
    description: "Sales performance for today",
    type: "Sales",
    date: "2025-01-17",
    value: "$1,245.50",
    change: "+12.5%",
    trend: "up",
  },
  {
    id: "RPT-002",
    title: "Weekly Revenue Summary",
    description: "Revenue breakdown for this week",
    type: "Revenue",
    date: "Jan 11-17, 2025",
    value: "$8,456.75",
    change: "+8.2%",
    trend: "up",
  },
  {
    id: "RPT-003",
    title: "Monthly Customer Report",
    description: "Customer acquisition and retention",
    type: "Customers",
    date: "January 2025",
    value: "156 customers",
    change: "+15.3%",
    trend: "up",
  },
  {
    id: "RPT-004",
    title: "Inventory Turnover",
    description: "Stock movement and turnover rates",
    type: "Inventory",
    date: "Last 30 days",
    value: "2.4x turnover",
    change: "-2.1%",
    trend: "down",
  },
];

const topProducts = [
  { name: "Wireless Headphones", sales: 145, revenue: "$14,498.55" },
  { name: "Coffee Mug", sales: 98, revenue: "$1,273.02" },
  { name: "Water Bottle", sales: 76, revenue: "$1,519.24" },
  { name: "Desk Lamp", sales: 54, revenue: "$1,889.46" },
  { name: "Phone Case", sales: 43, revenue: "$1,074.57" },
];

const recentReports = [
  {
    id: "LOG-001",
    name: "Sales Report - January 2025",
    type: "PDF",
    size: "2.4 MB",
    generated: "2025-01-17 14:30",
    status: "Ready",
  },
  {
    id: "LOG-002",
    name: "Customer Analytics - Q4 2024",
    type: "Excel",
    size: "1.8 MB",
    generated: "2025-01-15 09:15",
    status: "Ready",
  },
  {
    id: "LOG-003",
    name: "Inventory Report - Weekly",
    type: "PDF",
    size: "3.1 MB",
    generated: "2025-01-14 16:45",
    status: "Ready",
  },
];

export default function ReportsPage() {
  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-3xl font-bold tracking-tight">
              Reports & Analytics
            </h2>
            <p className="text-muted-foreground">
              Business insights and performance analytics
            </p>
          </div>
          <Button>
            <FileText className="mr-2 h-4 w-4" />
            Generate Report
          </Button>
        </div>

        {/* Key Metrics */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {salesReports.map((report) => {
            const Icon =
              report.type === "Sales"
                ? ShoppingCart
                : report.type === "Revenue"
                ? DollarSign
                : report.type === "Customers"
                ? Users
                : BarChart;

            return (
              <Card key={report.id}>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">
                    {report.title}
                  </CardTitle>
                  <Icon className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{report.value}</div>
                  <div className="flex items-center space-x-1 text-xs text-muted-foreground">
                    {report.trend === "up" ? (
                      <TrendingUp className="h-3 w-3 text-green-500" />
                    ) : (
                      <TrendingUp className="h-3 w-3 text-red-500 rotate-180" />
                    )}
                    <span
                      className={
                        report.trend === "up"
                          ? "text-green-500"
                          : "text-red-500"
                      }
                    >
                      {report.change}
                    </span>
                    <span>from last period</span>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>

        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {/* Top Products */}
          <Card className="col-span-2">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <BarChart className="h-5 w-5" />
                <span>Top Selling Products</span>
              </CardTitle>
              <CardDescription>
                Best performing products this month
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {topProducts.map((product, index) => (
                  <div
                    key={product.name}
                    className="flex items-center justify-between"
                  >
                    <div className="flex items-center space-x-3">
                      <div className="flex items-center justify-center w-8 h-8 rounded-full bg-muted text-sm font-medium">
                        {index + 1}
                      </div>
                      <div>
                        <p className="text-sm font-medium">{product.name}</p>
                        <p className="text-xs text-muted-foreground">
                          {product.sales} units sold
                        </p>
                      </div>
                    </div>
                    <div className="text-sm font-medium">{product.revenue}</div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Quick Actions */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <PieChart className="h-5 w-5" />
                <span>Quick Reports</span>
              </CardTitle>
              <CardDescription>Generate common reports</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <Button variant="outline" className="w-full justify-start">
                  <ShoppingCart className="mr-2 h-4 w-4" />
                  Sales Summary
                </Button>
                <Button variant="outline" className="w-full justify-start">
                  <Users className="mr-2 h-4 w-4" />
                  Customer Report
                </Button>
                <Button variant="outline" className="w-full justify-start">
                  <BarChart className="mr-2 h-4 w-4" />
                  Inventory Analysis
                </Button>
                <Button variant="outline" className="w-full justify-start">
                  <DollarSign className="mr-2 h-4 w-4" />
                  Financial Report
                </Button>
                <Button variant="outline" className="w-full justify-start">
                  <Calendar className="mr-2 h-4 w-4" />
                  Monthly Overview
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Recent Reports */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <FileText className="h-5 w-5" />
              <span>Recent Reports</span>
            </CardTitle>
            <CardDescription>
              Previously generated reports available for download
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentReports.map((report) => (
                <div
                  key={report.id}
                  className="flex items-center justify-between p-4 border rounded-lg hover:bg-accent/50 transition-colors"
                >
                  <div className="flex items-center space-x-4">
                    <div className="h-12 w-12 bg-muted rounded-lg flex items-center justify-center">
                      <FileText className="h-6 w-6 text-muted-foreground" />
                    </div>
                    <div>
                      <h4 className="text-sm font-medium">{report.name}</h4>
                      <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                        <span>{report.type}</span>
                        <span>•</span>
                        <span>{report.size}</span>
                        <span>•</span>
                        <span>Generated: {report.generated}</span>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center space-x-2">
                    <Badge variant="default">{report.status}</Badge>
                    <Button variant="ghost" size="icon">
                      <Download className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}
