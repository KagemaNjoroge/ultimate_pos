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
import { Separator } from "@/components/ui/separator";
import {
  Calculator,
  CreditCard,
  DollarSign,
  Minus,
  Plus,
  Receipt,
  Scan,
  ShoppingCart,
  Trash2,
  Users,
} from "lucide-react";

// Mock data for products available for sale
const availableProducts = [
  {
    id: "1",
    name: "Wireless Headphones",
    sku: "WH-001",
    price: 99.99,
    stock: 45,
    category: "Electronics",
  },
  {
    id: "2",
    name: "Coffee Mug",
    sku: "CM-002",
    price: 12.99,
    stock: 25,
    category: "Kitchenware",
  },
  {
    id: "3",
    name: "Water Bottle",
    sku: "WB-004",
    price: 19.99,
    stock: 120,
    category: "Sports",
  },
  {
    id: "4",
    name: "Desk Lamp",
    sku: "DL-005",
    price: 34.99,
    stock: 25,
    category: "Lighting",
  },
  {
    id: "5",
    name: "Phone Case",
    sku: "PC-006",
    price: 24.99,
    stock: 15,
    category: "Accessories",
  },
  {
    id: "6",
    name: "Notebook",
    sku: "NB-007",
    price: 8.5,
    stock: 80,
    category: "Stationery",
  },
];

// Mock cart items
const cartItems = [
  {
    id: "1",
    name: "Wireless Headphones",
    price: 99.99,
    quantity: 1,
    total: 99.99,
  },
  {
    id: "2",
    name: "Coffee Mug",
    price: 12.99,
    quantity: 2,
    total: 25.98,
  },
];

const subtotal = cartItems.reduce((sum, item) => sum + item.total, 0);
const tax = subtotal * 0.08; // 8% tax
const total = subtotal + tax;

export default function POSPage() {
  return (
    <DashboardLayout>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[calc(100vh-8rem)]">
        {/* Product Selection Area */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold">Point of Sale</h2>
            <div className="flex items-center space-x-2">
              <div className="relative flex-1 max-w-sm">
                <Scan className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Scan or search products..."
                  className="pl-8"
                />
              </div>
            </div>
          </div>

          {/* Product Grid */}
          <Card className="flex-1">
            <CardHeader>
              <CardTitle>Products</CardTitle>
              <CardDescription>
                Select products to add to the current sale
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-4 max-h-[60vh] overflow-y-auto">
                {availableProducts.map((product) => (
                  <div
                    key={product.id}
                    className="border rounded-lg p-4 hover:bg-accent/50 cursor-pointer transition-colors"
                  >
                    <div className="h-20 bg-muted rounded-lg flex items-center justify-center mb-3">
                      <ShoppingCart className="h-8 w-8 text-muted-foreground" />
                    </div>
                    <h3 className="font-medium text-sm mb-1">{product.name}</h3>
                    <p className="text-xs text-muted-foreground mb-2">
                      {product.sku}
                    </p>
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-sm">
                        ${product.price}
                      </span>
                      <Badge variant="outline" className="text-xs">
                        {product.stock} left
                      </Badge>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Cart and Checkout Area */}
        <div className="space-y-4">
          {/* Current Sale */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span>Current Sale</span>
                <Button variant="outline" size="sm">
                  <Users className="mr-2 h-4 w-4" />
                  Customer
                </Button>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Cart Items */}
              <div className="space-y-3 max-h-64 overflow-y-auto">
                {cartItems.map((item) => (
                  <div
                    key={item.id}
                    className="flex items-center justify-between p-2 border rounded"
                  >
                    <div className="flex-1">
                      <h4 className="text-sm font-medium">{item.name}</h4>
                      <p className="text-xs text-muted-foreground">
                        ${item.price} each
                      </p>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Button variant="outline" size="icon" className="h-6 w-6">
                        <Minus className="h-3 w-3" />
                      </Button>
                      <span className="text-sm font-medium w-8 text-center">
                        {item.quantity}
                      </span>
                      <Button variant="outline" size="icon" className="h-6 w-6">
                        <Plus className="h-3 w-3" />
                      </Button>
                      <Button variant="ghost" size="icon" className="h-6 w-6">
                        <Trash2 className="h-3 w-3 text-red-500" />
                      </Button>
                    </div>
                  </div>
                ))}
              </div>

              <Separator />

              {/* Totals */}
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Subtotal:</span>
                  <span>${subtotal.toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span>Tax (8%):</span>
                  <span>${tax.toFixed(2)}</span>
                </div>
                <Separator />
                <div className="flex justify-between text-lg font-bold">
                  <span>Total:</span>
                  <span>${total.toFixed(2)}</span>
                </div>
              </div>

              {/* Payment Buttons */}
              <div className="space-y-2">
                <Button className="w-full" size="lg">
                  <CreditCard className="mr-2 h-4 w-4" />
                  Pay with Card
                </Button>
                <Button variant="outline" className="w-full" size="lg">
                  <DollarSign className="mr-2 h-4 w-4" />
                  Cash Payment
                </Button>
              </div>

              {/* Quick Actions */}
              <div className="grid grid-cols-2 gap-2">
                <Button variant="outline" size="sm">
                  <Receipt className="mr-2 h-4 w-4" />
                  Receipt
                </Button>
                <Button variant="outline" size="sm">
                  <Calculator className="mr-2 h-4 w-4" />
                  Calculator
                </Button>
              </div>

              {/* Clear Sale */}
              <Button
                variant="ghost"
                className="w-full text-red-500 hover:text-red-600"
              >
                <Trash2 className="mr-2 h-4 w-4" />
                Clear Sale
              </Button>
            </CardContent>
          </Card>

          {/* Quick Actions */}
          <Card>
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <Button variant="outline" className="w-full justify-start">
                <Users className="mr-2 h-4 w-4" />
                Add Customer
              </Button>
              <Button variant="outline" className="w-full justify-start">
                <Calculator className="mr-2 h-4 w-4" />
                Apply Discount
              </Button>
              <Button variant="outline" className="w-full justify-start">
                <Receipt className="mr-2 h-4 w-4" />
                Hold Sale
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  );
}
