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
    DollarSign,
    Edit,
    Filter,
    Mail,
    Package,
    Phone,
    Plus,
    Search,
    Truck,
} from "lucide-react";

// Mock data for suppliers
const suppliers = [
  {
    id: "SUP-001",
    name: "TechCorp Solutions",
    email: "orders@techcorp.com",
    phone: "+1 (555) 100-2000",
    address: "123 Technology Blvd, Tech City, TC 12345",
    contactPerson: "John Smith",
    productsSupplied: 15,
    totalOrders: 24,
    totalValue: 12450.0,
    lastOrder: "2025-01-15",
    status: "Active",
    rating: 4.8,
    paymentTerms: "30 days",
  },
  {
    id: "SUP-002",
    name: "KitchenPlus Wholesale",
    email: "supply@kitchenplus.com",
    phone: "+1 (555) 200-3000",
    address: "456 Kitchen Ave, Food City, FC 23456",
    contactPerson: "Sarah Johnson",
    productsSupplied: 8,
    totalOrders: 18,
    totalValue: 5680.5,
    lastOrder: "2025-01-12",
    status: "Active",
    rating: 4.5,
    paymentTerms: "15 days",
  },
  {
    id: "SUP-003",
    name: "OfficeMax Distributors",
    email: "wholesale@officemax.com",
    phone: "+1 (555) 300-4000",
    address: "789 Office Park, Business City, BC 34567",
    contactPerson: "Mike Wilson",
    productsSupplied: 12,
    totalOrders: 6,
    totalValue: 3240.25,
    lastOrder: "2025-01-08",
    status: "Active",
    rating: 4.2,
    paymentTerms: "45 days",
  },
  {
    id: "SUP-004",
    name: "SportGear International",
    email: "orders@sportgear.com",
    phone: "+1 (555) 400-5000",
    address: "321 Sports Complex, Athletic City, AC 45678",
    contactPerson: "Lisa Brown",
    productsSupplied: 20,
    totalOrders: 32,
    totalValue: 18950.75,
    lastOrder: "2025-01-17",
    status: "Active",
    rating: 4.9,
    paymentTerms: "30 days",
  },
  {
    id: "SUP-005",
    name: "LightHouse Fixtures",
    email: "sales@lighthouse.com",
    phone: "+1 (555) 500-6000",
    address: "654 Lamp Street, Bright City, BR 56789",
    contactPerson: "David Lee",
    productsSupplied: 6,
    totalOrders: 3,
    totalValue: 890.0,
    lastOrder: "2024-12-20",
    status: "Inactive",
    rating: 3.8,
    paymentTerms: "60 days",
  },
];

const activeSuppliers = suppliers.filter((s) => s.status === "Active");
const totalValue = suppliers.reduce(
  (sum, supplier) => sum + supplier.totalValue,
  0
);
const totalProducts = suppliers.reduce(
  (sum, supplier) => sum + supplier.productsSupplied,
  0
);

const getStatusBadgeVariant = (status: string) => {
  switch (status) {
    case "Active":
      return "default";
    case "Inactive":
      return "outline";
    default:
      return "default";
  }
};

const getRatingColor = (rating: number) => {
  if (rating >= 4.5) return "text-green-600";
  if (rating >= 4.0) return "text-yellow-600";
  if (rating >= 3.5) return "text-orange-600";
  return "text-red-600";
};

export default function SuppliersPage() {
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
          <Button>
            <Plus className="mr-2 h-4 w-4" />
            Add Supplier
          </Button>
        </div>

        {/* Stats Cards */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Total Suppliers
              </CardTitle>
              <Truck className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{suppliers.length}</div>
              <p className="text-xs text-muted-foreground">
                Registered suppliers
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Active Suppliers
              </CardTitle>
              <Package className="h-4 w-4 text-green-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{activeSuppliers.length}</div>
              <p className="text-xs text-muted-foreground">
                Currently active partnerships
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Total Procurement
              </CardTitle>
              <DollarSign className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">${totalValue.toFixed(2)}</div>
              <p className="text-xs text-muted-foreground">
                Total purchase value
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Products Sourced
              </CardTitle>
              <Package className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{totalProducts}</div>
              <p className="text-xs text-muted-foreground">
                Unique products supplied
              </p>
            </CardContent>
          </Card>
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
              {suppliers.map((supplier) => (
                <div
                  key={supplier.id}
                  className="flex items-center justify-between p-4 border rounded-lg hover:bg-accent/50 transition-colors"
                >
                  <div className="flex items-center space-x-4">
                    <div className="h-12 w-12 bg-muted rounded-lg flex items-center justify-center">
                      <Truck className="h-6 w-6 text-muted-foreground" />
                    </div>
                    <div>
                      <h4 className="text-sm font-medium">{supplier.name}</h4>
                      <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                        <span>Contact: {supplier.contactPerson}</span>
                        <span>•</span>
                        <span>{supplier.paymentTerms} payment terms</span>
                      </div>
                      <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                        <Mail className="h-3 w-3" />
                        <span>{supplier.email}</span>
                        <span>•</span>
                        <Phone className="h-3 w-3" />
                        <span>{supplier.phone}</span>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center space-x-4">
                    <div className="text-right">
                      <div className="text-sm font-medium">
                        ${supplier.totalValue.toFixed(2)}
                      </div>
                      <div className="text-xs text-muted-foreground">
                        {supplier.totalOrders} orders •{" "}
                        {supplier.productsSupplied} products
                      </div>
                      <div
                        className={`text-xs font-medium ${getRatingColor(
                          supplier.rating
                        )}`}
                      >
                        ★ {supplier.rating} rating
                      </div>
                    </div>

                    <div className="text-right">
                      <div className="text-xs text-muted-foreground">
                        Last Order
                      </div>
                      <div className="text-sm font-medium">
                        {supplier.lastOrder}
                      </div>
                    </div>

                    <Badge variant={getStatusBadgeVariant(supplier.status)}>
                      {supplier.status}
                    </Badge>

                    <Button variant="ghost" size="icon">
                      <Edit className="h-4 w-4" />
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
