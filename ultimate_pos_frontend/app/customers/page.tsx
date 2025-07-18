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
  Edit,
  Filter,
  Mail,
  Phone,
  Plus,
  Search,
  Star,
  UserCheck,
  Users,
} from "lucide-react";

// Mock data for customers
const customers = [
  {
    id: "CUST-001",
    name: "John Doe",
    email: "john.doe@email.com",
    phone: "+1 (555) 123-4567",
    address: "123 Main St, City, State 12345",
    totalOrders: 15,
    totalSpent: 1245.5,
    lastOrder: "2025-01-15",
    status: "Active",
    loyalty: "Gold",
  },
  {
    id: "CUST-002",
    name: "Jane Smith",
    email: "jane.smith@email.com",
    phone: "+1 (555) 234-5678",
    address: "456 Oak Ave, City, State 12345",
    totalOrders: 8,
    totalSpent: 689.25,
    lastOrder: "2025-01-17",
    status: "Active",
    loyalty: "Silver",
  },
  {
    id: "CUST-003",
    name: "Bob Johnson",
    email: "bob.johnson@email.com",
    phone: "+1 (555) 345-6789",
    address: "789 Pine Rd, City, State 12345",
    totalOrders: 3,
    totalSpent: 234.75,
    lastOrder: "2025-01-10",
    status: "Active",
    loyalty: "Bronze",
  },
  {
    id: "CUST-004",
    name: "Alice Brown",
    email: "alice.brown@email.com",
    phone: "+1 (555) 456-7890",
    address: "321 Elm St, City, State 12345",
    totalOrders: 22,
    totalSpent: 2156.8,
    lastOrder: "2025-01-16",
    status: "VIP",
    loyalty: "Platinum",
  },
  {
    id: "CUST-005",
    name: "Mike Wilson",
    email: "mike.wilson@email.com",
    phone: "+1 (555) 567-8901",
    address: "654 Maple Dr, City, State 12345",
    totalOrders: 1,
    totalSpent: 45.0,
    lastOrder: "2024-12-20",
    status: "Inactive",
    loyalty: "Bronze",
  },
];

const activeCustomers = customers.filter(
  (c) => c.status === "Active" || c.status === "VIP"
);
const totalRevenue = customers.reduce(
  (sum, customer) => sum + customer.totalSpent,
  0
);
const averageOrderValue =
  totalRevenue /
  customers.reduce((sum, customer) => sum + customer.totalOrders, 0);

const getStatusBadgeVariant = (status: string) => {
  switch (status) {
    case "Active":
      return "default";
    case "VIP":
      return "secondary";
    case "Inactive":
      return "outline";
    default:
      return "default";
  }
};

const getLoyaltyColor = (loyalty: string) => {
  switch (loyalty) {
    case "Platinum":
      return "text-purple-600";
    case "Gold":
      return "text-yellow-600";
    case "Silver":
      return "text-gray-600";
    case "Bronze":
      return "text-orange-600";
    default:
      return "text-muted-foreground";
  }
};

export default function CustomersPage() {
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
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Total Customers
              </CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{customers.length}</div>
              <p className="text-xs text-muted-foreground">
                +12% from last month
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
              <div className="text-2xl font-bold">{activeCustomers.length}</div>
              <p className="text-xs text-muted-foreground">
                {((activeCustomers.length / customers.length) * 100).toFixed(1)}
                % of total
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Customer Revenue
              </CardTitle>
              <Star className="h-4 w-4 text-yellow-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                ${totalRevenue.toFixed(2)}
              </div>
              <p className="text-xs text-muted-foreground">
                Total lifetime value
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Avg. Order Value
              </CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                ${averageOrderValue.toFixed(2)}
              </div>
              <p className="text-xs text-muted-foreground">
                Per customer order
              </p>
            </CardContent>
          </Card>
        </div>

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
              {customers.map((customer) => (
                <div
                  key={customer.id}
                  className="flex items-center justify-between p-4 border rounded-lg hover:bg-accent/50 transition-colors"
                >
                  <div className="flex items-center space-x-4">
                    <div className="h-12 w-12 bg-muted rounded-full flex items-center justify-center">
                      <Users className="h-6 w-6 text-muted-foreground" />
                    </div>
                    <div>
                      <h4 className="text-sm font-medium">{customer.name}</h4>
                      <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                        <Mail className="h-3 w-3" />
                        <span>{customer.email}</span>
                      </div>
                      <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                        <Phone className="h-3 w-3" />
                        <span>{customer.phone}</span>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center space-x-4">
                    <div className="text-right">
                      <div className="text-sm font-medium">
                        ${customer.totalSpent.toFixed(2)}
                      </div>
                      <div className="text-xs text-muted-foreground">
                        {customer.totalOrders} orders
                      </div>
                      <div
                        className={`text-xs font-medium ${getLoyaltyColor(
                          customer.loyalty
                        )}`}
                      >
                        {customer.loyalty}
                      </div>
                    </div>

                    <Badge variant={getStatusBadgeVariant(customer.status)}>
                      {customer.status}
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
