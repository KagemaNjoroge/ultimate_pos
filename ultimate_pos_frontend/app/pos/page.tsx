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
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { ProductImage } from "@/components/ui/product-image";
import { Separator } from "@/components/ui/separator";
import { useCustomers, useProducts } from "@/lib/hooks";
import {
  Calculator,
  CreditCard,
  DollarSign,
  Loader2,
  Minus,
  Plus,
  Receipt,
  Search,
  ShoppingCart,
  Trash2,
  Users,
} from "lucide-react";
import { useState } from "react";

// Product and Customer interfaces
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

interface CartItem {
  id: number;
  name: string;
  price: number;
  quantity: number;
  total: number;
  display_image: string | null;
}

const formatPrice = (price: number) => {
  return new Intl.NumberFormat("en-KE", {
    style: "currency",
    currency: "KES",
    minimumFractionDigits: 0,
  }).format(price);
};

export default function POSPage() {
  // API hooks - use large page size to get most/all items for POS
  const {
    data: apiProducts,
    loading: productsLoading,
    error: productsError,
    loadMore: loadMoreProducts,
    paginationInfo: productsPagination,
  } = useProducts({ limit: 1000 }); // Large limit for POS
  const {
    data: apiCustomers,
    loading: customersLoading,
    loadMore: loadMoreCustomers,
    paginationInfo: customersPagination,
  } = useCustomers({ limit: 1000 }); // Large limit for POS

  // State management
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [selectedCustomer, setSelectedCustomer] = useState<Customer | null>(
    null
  );
  const [showCustomerModal, setShowCustomerModal] = useState(false);
  const [showMpesaModal, setShowMpesaModal] = useState(false);
  const [mpesaPhoneNumber, setMpesaPhoneNumber] = useState("");
  const [isProcessingPayment, setIsProcessingPayment] = useState(false);
  const [productSearchTerm, setProductSearchTerm] = useState("");
  const [customerSearchTerm, setCustomerSearchTerm] = useState("");

  // Type the data arrays
  const products: Product[] = apiProducts || [];
  const customers: Customer[] = apiCustomers || [];

  // Filter products based on search term and active status
  const filteredProducts = products.filter((product) => {
    const searchLower = productSearchTerm.toLowerCase();
    const isActive = product.status === "ACTIVE" || product.status === null;
    const matchesSearch =
      (product.name || "").toLowerCase().includes(searchLower) ||
      (product.description || "").toLowerCase().includes(searchLower);
    return isActive && matchesSearch;
  });

  // Filter customers based on search term and active status
  const filteredCustomers = customers.filter((customer) => {
    const searchLower = customerSearchTerm.toLowerCase();
    const fullName = `${customer.first_name || ""} ${
      customer.last_name || ""
    }`.toLowerCase();
    const matchesSearch =
      fullName.includes(searchLower) ||
      (customer.email || "").toLowerCase().includes(searchLower) ||
      (customer.phone || "").includes(searchLower);
    return customer.is_active && matchesSearch;
  });

  // Cart operations
  const addToCart = (product: Product) => {
    setCartItems((prevItems) => {
      const existingItem = prevItems.find((item) => item.id === product.id);

      if (existingItem) {
        return prevItems.map((item) =>
          item.id === product.id
            ? {
                ...item,
                quantity: item.quantity + 1,
                total: (item.quantity + 1) * item.price,
              }
            : item
        );
      } else {
        return [
          ...prevItems,
          {
            id: product.id,
            name: product.name,
            price: product.price,
            quantity: 1,
            total: product.price,
            display_image: product.display_image,
          },
        ];
      }
    });
  };

  const updateCartItemQuantity = (id: number, change: number) => {
    setCartItems((prevItems) => {
      return prevItems
        .map((item) => {
          if (item.id === id) {
            const newQuantity = Math.max(0, item.quantity + change);
            if (newQuantity === 0) {
              return null; // Will be filtered out
            }
            return {
              ...item,
              quantity: newQuantity,
              total: newQuantity * item.price,
            };
          }
          return item;
        })
        .filter(Boolean) as CartItem[];
    });
  };

  const removeFromCart = (id: number) => {
    setCartItems((prevItems) => prevItems.filter((item) => item.id !== id));
  };

  const clearCart = () => {
    setCartItems([]);
    setSelectedCustomer(null);
  };

  // M-Pesa payment handler
  const handleMpesaPayment = async () => {
    if (!mpesaPhoneNumber.trim()) {
      return;
    }

    // Basic phone number validation
    const phoneRegex = /^254[0-9]{9}$/;
    if (!phoneRegex.test(mpesaPhoneNumber.replace(/\s/g, ""))) {
      alert("Please enter a valid M-Pesa phone number starting with 254");
      return;
    }

    try {
      setIsProcessingPayment(true);

      // Here you would typically call your M-Pesa API
      // For now, we'll simulate the STK push process
      console.log("Processing M-Pesa payment...", {
        phoneNumber: mpesaPhoneNumber,
        amount: total,
        cartItems,
        customer: selectedCustomer,
      });

      // Simulate API call delay
      await new Promise((resolve) => setTimeout(resolve, 2000));

      // Close modal and show success (in real implementation, you'd handle the actual response)
      setShowMpesaModal(false);
      setMpesaPhoneNumber("");

      // You might want to clear the cart after successful payment
      // clearCart();

      // Show success message (you can use toast from sonner)
      alert(
        "STK push sent successfully! Please check your phone to complete the payment."
      );
    } catch (error) {
      console.error("M-Pesa payment failed:", error);
      alert("Failed to process M-Pesa payment. Please try again.");
    } finally {
      setIsProcessingPayment(false);
    }
  };

  const openMpesaModal = () => {
    // Pre-fill phone number if customer is selected
    if (selectedCustomer?.phone) {
      // Format the phone number to start with 254 if it doesn't already
      let phone = selectedCustomer.phone.replace(/\s/g, "");
      if (phone.startsWith("0")) {
        phone = "254" + phone.substring(1);
      } else if (phone.startsWith("+254")) {
        phone = phone.substring(1);
      } else if (!phone.startsWith("254")) {
        phone = "254" + phone;
      }
      setMpesaPhoneNumber(phone);
    }
    setShowMpesaModal(true);
  };

  // Calculate totals
  const subtotal = cartItems.reduce((sum, item) => sum + item.total, 0);
  const tax = subtotal * 0.16; // 16% VAT
  const total = subtotal + tax;

  return (
    <DashboardLayout>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[calc(100vh-8rem)]">
        {/* Product Selection Area */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold">Point of Sale</h2>
            <div className="flex items-center space-x-2">
              <div className="relative flex-1 max-w-sm">
                <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Search products..."
                  className="pl-8"
                  value={productSearchTerm}
                  onChange={(e) => setProductSearchTerm(e.target.value)}
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
              {productsLoading ? (
                <div className="flex items-center justify-center py-8">
                  <Loader2 className="h-8 w-8 animate-spin" />
                  <span className="ml-2">Loading products...</span>
                </div>
              ) : productsError ? (
                <div className="flex flex-col items-center justify-center py-8 text-muted-foreground">
                  <p className="mb-4">Failed to load products</p>
                  <p className="text-sm text-red-500">{productsError}</p>
                </div>
              ) : filteredProducts.length === 0 ? (
                <div className="flex items-center justify-center py-8 text-muted-foreground">
                  <p>
                    {productSearchTerm
                      ? `No products found matching "${productSearchTerm}"`
                      : "No active products available for sale"}
                  </p>
                </div>
              ) : (
                <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-4 max-h-[60vh] overflow-y-auto">
                  {filteredProducts.map((product: Product) => (
                    <div
                      key={product.id}
                      className="border rounded-lg p-4 hover:bg-accent/50 cursor-pointer transition-colors"
                      onClick={() => addToCart(product)}
                    >
                      <div className="h-20 bg-muted rounded-lg flex items-center justify-center mb-3 overflow-hidden">
                        {product.display_image ? (
                          <ProductImage
                            src={product.display_image}
                            alt={product.name}
                            className="h-full w-full object-cover"
                          />
                        ) : (
                          <ShoppingCart className="h-8 w-8 text-muted-foreground" />
                        )}
                      </div>
                      <h3
                        className="font-medium text-sm mb-1 truncate"
                        title={product.name}
                      >
                        {product.name}
                      </h3>
                      <p
                        className="text-xs text-muted-foreground mb-2 truncate"
                        title={product.description}
                      >
                        {product.description}
                      </p>
                      <div className="flex items-center justify-between">
                        <span className="font-bold text-sm">
                          {formatPrice(product.price)}
                        </span>
                        <Badge variant="outline" className="text-xs">
                          ID: {product.id}
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
              )}
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
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setShowCustomerModal(true)}
                >
                  <Users className="mr-2 h-4 w-4" />
                  {selectedCustomer
                    ? `${selectedCustomer.first_name} ${selectedCustomer.last_name}`
                    : "Select Customer"}
                </Button>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Cart Items */}
              <div className="space-y-3 max-h-64 overflow-y-auto">
                {cartItems.length === 0 ? (
                  <div className="text-center py-8 text-muted-foreground">
                    <ShoppingCart className="h-12 w-12 mx-auto mb-2 opacity-50" />
                    <p>Cart is empty</p>
                    <p className="text-xs">Add products to start a sale</p>
                  </div>
                ) : (
                  cartItems.map((item) => (
                    <div
                      key={item.id}
                      className="flex items-center justify-between p-2 border rounded"
                    >
                      <div className="flex items-center space-x-2 flex-1">
                        <div className="h-8 w-8 bg-muted rounded flex items-center justify-center overflow-hidden">
                          {item.display_image ? (
                            <ProductImage
                              src={item.display_image}
                              alt={item.name}
                              className="h-full w-full object-cover"
                            />
                          ) : (
                            <ShoppingCart className="h-4 w-4 text-muted-foreground" />
                          )}
                        </div>
                        <div className="flex-1">
                          <h4 className="text-sm font-medium truncate">
                            {item.name}
                          </h4>
                          <p className="text-xs text-muted-foreground">
                            {formatPrice(item.price)} each
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Button
                          variant="outline"
                          size="icon"
                          className="h-6 w-6"
                          onClick={() => updateCartItemQuantity(item.id, -1)}
                        >
                          <Minus className="h-3 w-3" />
                        </Button>
                        <span className="text-sm font-medium w-8 text-center">
                          {item.quantity}
                        </span>
                        <Button
                          variant="outline"
                          size="icon"
                          className="h-6 w-6"
                          onClick={() => updateCartItemQuantity(item.id, 1)}
                        >
                          <Plus className="h-3 w-3" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="icon"
                          className="h-6 w-6"
                          onClick={() => removeFromCart(item.id)}
                        >
                          <Trash2 className="h-3 w-3 text-red-500" />
                        </Button>
                      </div>
                    </div>
                  ))
                )}
              </div>

              <Separator />

              {/* Totals */}
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Subtotal:</span>
                  <span>{formatPrice(subtotal)}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span>VAT (16%):</span>
                  <span>{formatPrice(tax)}</span>
                </div>
                <Separator />
                <div className="flex justify-between text-lg font-bold">
                  <span>Total:</span>
                  <span>{formatPrice(total)}</span>
                </div>
              </div>

              {/* Payment Buttons */}
              <div className="space-y-2">
                <Button
                  className="w-full"
                  size="lg"
                  disabled={cartItems.length === 0}
                  onClick={openMpesaModal}
                >
                  <CreditCard className="mr-2 h-4 w-4" />
                  Pay with M-Pesa
                </Button>
                <Button
                  variant="outline"
                  className="w-full"
                  size="lg"
                  disabled={cartItems.length === 0}
                >
                  <DollarSign className="mr-2 h-4 w-4" />
                  Cash Payment
                </Button>
              </div>

              {/* Quick Actions */}
              <div className="grid grid-cols-2 gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  disabled={cartItems.length === 0}
                >
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
                onClick={clearCart}
                disabled={cartItems.length === 0}
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
              <Button
                variant="outline"
                className="w-full justify-start"
                onClick={() => setShowCustomerModal(true)}
              >
                <Users className="mr-2 h-4 w-4" />
                {selectedCustomer ? "Change Customer" : "Add Customer"}
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

      {/* Customer Selection Modal */}
      <Dialog open={showCustomerModal} onOpenChange={setShowCustomerModal}>
        <DialogContent className="sm:max-w-[600px]">
          <DialogHeader>
            <DialogTitle>Select Customer</DialogTitle>
            <DialogDescription>
              Choose a customer for this sale or proceed without a customer.
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4">
            {/* Search */}
            <div className="relative">
              <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search customers..."
                className="pl-8"
                value={customerSearchTerm}
                onChange={(e) => setCustomerSearchTerm(e.target.value)}
              />
            </div>

            {/* No Customer Option */}
            <div
              className={`p-3 border rounded-lg cursor-pointer transition-colors ${
                selectedCustomer === null
                  ? "bg-primary/10 border-primary"
                  : "hover:bg-accent/50"
              }`}
              onClick={() => {
                setSelectedCustomer(null);
                setShowCustomerModal(false);
              }}
            >
              <div className="flex items-center space-x-3">
                <div className="h-10 w-10 bg-muted rounded-full flex items-center justify-center">
                  <Users className="h-5 w-5 text-muted-foreground" />
                </div>
                <div>
                  <h4 className="font-medium">Walk-in Customer</h4>
                  <p className="text-sm text-muted-foreground">
                    Proceed without customer details
                  </p>
                </div>
              </div>
            </div>

            {/* Customer List */}
            <div className="max-h-96 overflow-y-auto space-y-2">
              {customersLoading ? (
                <div className="flex items-center justify-center py-8">
                  <Loader2 className="h-6 w-6 animate-spin" />
                  <span className="ml-2">Loading customers...</span>
                </div>
              ) : filteredCustomers.length === 0 ? (
                <div className="text-center py-8 text-muted-foreground">
                  <p>
                    {customerSearchTerm
                      ? `No customers found matching "${customerSearchTerm}"`
                      : "No active customers found"}
                  </p>
                </div>
              ) : (
                filteredCustomers.map((customer) => (
                  <div
                    key={customer.id}
                    className={`p-3 border rounded-lg cursor-pointer transition-colors ${
                      selectedCustomer?.id === customer.id
                        ? "bg-primary/10 border-primary"
                        : "hover:bg-accent/50"
                    }`}
                    onClick={() => {
                      setSelectedCustomer(customer);
                      setShowCustomerModal(false);
                      setCustomerSearchTerm("");
                    }}
                  >
                    <div className="flex items-center space-x-3">
                      <div className="h-10 w-10 bg-muted rounded-full flex items-center justify-center overflow-hidden">
                        {customer.photo ? (
                          <ProductImage
                            src={customer.photo}
                            alt={`${customer.first_name} ${customer.last_name}`}
                            className="h-full w-full object-cover"
                          />
                        ) : (
                          <Users className="h-5 w-5 text-muted-foreground" />
                        )}
                      </div>
                      <div className="flex-1">
                        <h4 className="font-medium">
                          {customer.first_name} {customer.last_name}
                        </h4>
                        <p className="text-sm text-muted-foreground">
                          {customer.email} • {customer.phone}
                        </p>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>

            <div className="flex justify-end space-x-2 pt-4 border-t">
              <Button
                variant="outline"
                onClick={() => {
                  setShowCustomerModal(false);
                  setCustomerSearchTerm("");
                }}
              >
                Cancel
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>

      {/* M-Pesa Payment Modal */}
      <Dialog open={showMpesaModal} onOpenChange={setShowMpesaModal}>
        <DialogContent className="sm:max-w-[400px]">
          <DialogHeader>
            <DialogTitle>M-Pesa Payment</DialogTitle>
            <DialogDescription>
              Enter the phone number to receive the STK push for payment.
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4">
            {/* Order Summary */}
            <div className="bg-muted/50 p-4 rounded-lg">
              <h4 className="font-medium mb-2">Payment Summary</h4>
              <div className="space-y-1 text-sm">
                <div className="flex justify-between">
                  <span>Items:</span>
                  <span>
                    {cartItems.length} item{cartItems.length !== 1 ? "s" : ""}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span>Subtotal:</span>
                  <span>{formatPrice(subtotal)}</span>
                </div>
                <div className="flex justify-between">
                  <span>VAT (16%):</span>
                  <span>{formatPrice(tax)}</span>
                </div>
                <div className="flex justify-between font-medium border-t pt-1">
                  <span>Total:</span>
                  <span>{formatPrice(total)}</span>
                </div>
              </div>
            </div>

            {/* Customer Info */}
            {selectedCustomer && (
              <div className="bg-blue-50 p-3 rounded-lg">
                <div className="flex items-center space-x-2">
                  <Users className="h-4 w-4 text-blue-600" />
                  <div>
                    <p className="font-medium text-sm">
                      {selectedCustomer.first_name} {selectedCustomer.last_name}
                    </p>
                    <p className="text-xs text-muted-foreground">
                      {selectedCustomer.email}
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Phone Number Input */}
            <div className="space-y-2">
              <label className="text-sm font-medium">
                M-Pesa Phone Number *
              </label>
              <Input
                type="tel"
                placeholder="254XXXXXXXXX"
                value={mpesaPhoneNumber}
                onChange={(e) => setMpesaPhoneNumber(e.target.value)}
                className="text-center"
                disabled={isProcessingPayment}
              />
              <p className="text-xs text-muted-foreground">
                Enter the M-Pesa registered phone number (e.g., 254712345678)
              </p>
            </div>

            {/* Action Buttons */}
            <div className="flex space-x-2 pt-4">
              <Button
                variant="outline"
                className="flex-1"
                onClick={() => {
                  setShowMpesaModal(false);
                  setMpesaPhoneNumber("");
                }}
                disabled={isProcessingPayment}
              >
                Cancel
              </Button>
              <Button
                className="flex-1"
                onClick={handleMpesaPayment}
                disabled={!mpesaPhoneNumber.trim() || isProcessingPayment}
              >
                {isProcessingPayment ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Processing...
                  </>
                ) : (
                  <>
                    <CreditCard className="mr-2 h-4 w-4" />
                    Send STK Push
                  </>
                )}
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </DashboardLayout>
  );
}
