"use client";

import { ThemeToggle } from "@/components/theme-toggle";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { apiService } from "@/lib/api";
import { useApi, User } from "@/lib/hooks";
import { cn } from "@/lib/utils";
import {
  BarChart3,
  Bell,
  FileText,
  LayoutDashboard,
  LogOut,
  Menu,
  Package,
  Settings,
  ShoppingCart,
  Truck,
  Users,
  Warehouse,
  X,
} from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { toast } from "sonner";

const navigationItems = [
  {
    title: "Dashboard",
    href: "/dashboard",
    icon: LayoutDashboard,
  },
  {
    title: "POS",
    href: "/pos",
    icon: ShoppingCart,
  },
  {
    title: "Products",
    href: "/products",
    icon: Package,
  },
  {
    title: "Sales",
    href: "/sales",
    icon: FileText,
  },
  {
    title: "Customers",
    href: "/customers",
    icon: Users,
  },
  {
    title: "Stock",
    href: "/stock",
    icon: Warehouse,
  },
  {
    title: "Reports",
    href: "/reports",
    icon: BarChart3,
  },
  {
    title: "Suppliers",
    href: "/suppliers",
    icon: Truck,
  },
  {
    title: "Settings",
    href: "/settings",
    icon: Settings,
  },
];

// Mock notifications data
const notifications = [
  {
    id: 1,
    title: "Low Stock Alert",
    message: "Product 'Widget A' is running low on stock",
    time: "2 minutes ago",
    read: false,
  },
  {
    id: 2,
    title: "New Order",
    message: "Order #1234 has been placed",
    time: "5 minutes ago",
    read: false,
  },
  {
    id: 3,
    title: "Payment Received",
    message: "Payment for Invoice #INV-001 received",
    time: "1 hour ago",
    read: true,
  },
];

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const router = useRouter();
  const pathname = usePathname();

  // Fetch user profile information
  const {
    data: user,
    loading: userLoading,
    error: userError,
  } = useApi<User>(() => apiService.profile.get(), []);

  // Handle user fetch error silently (log it but don't disrupt UI)
  useEffect(() => {
    if (userError) {
      console.error("Failed to fetch user profile:", userError);
    }
  }, [userError]);
  const handleLogout = async () => {
    try {
      // Call the logout API to clear server-side sessions
      await apiService.auth.logout();
    } catch (error) {
      // Even if the API call fails, we should still clear local tokens
      console.error("Error during logout:", error);
      toast.error("Logout completed, but there was an issue with the server.");
    } finally {
      // Always clear tokens from localStorage and redirect
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");

      // Redirect to login page
      router.push("/auth/login");
    }
  };

  const unreadNotifications = notifications.filter((n) => !n.read).length;

  // Function to check if a route is active
  const isRouteActive = (href: string) => {
    if (href === "/dashboard") {
      return pathname === "/dashboard";
    }
    return pathname.startsWith(href);
  };

  // Function to get current page title
  const getCurrentPageTitle = () => {
    const currentNavItem = navigationItems.find((item) =>
      isRouteActive(item.href)
    );
    if (currentNavItem) {
      return currentNavItem.title;
    }

    // Handle special cases
    if (pathname.startsWith("/categories")) {
      return "Categories";
    }
    if (pathname.startsWith("/auth")) {
      return "Authentication";
    }

    return "Dashboard";
  };

  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar */}
      <div
        className={cn(
          "fixed inset-y-0 left-0 z-50 w-64 bg-card border-r transform transition-transform duration-200 ease-in-out lg:translate-x-0 lg:static lg:inset-0",
          sidebarOpen ? "translate-x-0" : "-translate-x-full"
        )}
      >
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="flex items-center justify-between p-4 border-b h-[73px]">
            <div className="flex items-center space-x-2">
              <Image
                src="/new_logo.svg"
                alt="UltimatePOS"
                width={172}
                height={128}
                className="dark"
              />
            </div>
            <Button
              variant="ghost"
              size="icon"
              className="lg:hidden"
              onClick={() => setSidebarOpen(false)}
            >
              <X className="h-4 w-4" />
            </Button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 overflow-y-auto py-4">
            <div className="space-y-1 px-3">
              {navigationItems.map((item) => {
                const Icon = item.icon;
                const isActive = isRouteActive(item.href);

                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={cn(
                      "flex items-center space-x-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                      "hover:bg-accent hover:text-accent-foreground",
                      "focus:bg-accent focus:text-accent-foreground focus:outline-none",
                      isActive
                        ? "bg-primary text-primary-foreground hover:bg-primary/90"
                        : ""
                    )}
                    onClick={() => setSidebarOpen(false)}
                  >
                    <Icon className="h-4 w-4" />
                    <span>{item.title}</span>
                  </Link>
                );
              })}
            </div>
          </nav>
        </div>
      </div>

      {/* Main content */}
      <div className="flex flex-col flex-1 lg:ml-0">
        {/* Top bar */}
        <header className="flex items-center justify-between p-4 border-b bg-card h-[73px]">
          <div className="flex items-center space-x-4">
            <Button
              variant="ghost"
              size="icon"
              className="lg:hidden"
              onClick={() => setSidebarOpen(true)}
            >
              <Menu className="h-4 w-4" />
            </Button>
            <h1 className="text-lg font-semibold">{getCurrentPageTitle()}</h1>
          </div>

          <div className="flex items-center space-x-4">
            {/* Notifications */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="icon" className="relative">
                  <Bell className="h-4 w-4" />
                  {unreadNotifications > 0 && (
                    <Badge
                      variant="destructive"
                      className="absolute -top-2 -right-2 h-5 w-5 flex items-center justify-center p-0 text-xs"
                    >
                      {unreadNotifications}
                    </Badge>
                  )}
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-80">
                <DropdownMenuLabel>Notifications</DropdownMenuLabel>
                <DropdownMenuSeparator />
                {notifications.length === 0 ? (
                  <div className="p-4 text-center text-sm text-muted-foreground">
                    No notifications
                  </div>
                ) : (
                  notifications.map((notification) => (
                    <DropdownMenuItem
                      key={notification.id}
                      className="flex flex-col items-start p-4 space-y-1"
                    >
                      <div className="flex w-full items-start justify-between">
                        <div className="space-y-1">
                          <p className="text-sm font-medium leading-none">
                            {notification.title}
                          </p>
                          <p className="text-xs text-muted-foreground">
                            {notification.message}
                          </p>
                          <p className="text-xs text-muted-foreground">
                            {notification.time}
                          </p>
                        </div>
                        {!notification.read && (
                          <div className="h-2 w-2 bg-blue-600 rounded-full" />
                        )}
                      </div>
                    </DropdownMenuItem>
                  ))
                )}
              </DropdownMenuContent>
            </DropdownMenu>

            {/* Theme Toggle */}
            <ThemeToggle />

            {/* User Avatar */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button
                  variant="ghost"
                  className="relative h-8 w-8 rounded-full"
                >
                  <Avatar className="h-8 w-8">
                    {user?.profile_pic ? (
                      <AvatarImage
                        src={`${process.env.NEXT_PUBLIC_BACKEND_URL}${user.profile_pic}`}
                        alt={`${user.first_name} ${user.last_name}`}
                      />
                    ) : (
                      <AvatarImage src="/avatars/01.png" alt="User" />
                    )}
                    <AvatarFallback>
                      {userLoading
                        ? "..."
                        : user
                        ? `${user.first_name?.[0] || ""}${
                            user.last_name?.[0] || ""
                          }`
                        : "U"}
                    </AvatarFallback>
                  </Avatar>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-56" align="end" forceMount>
                <DropdownMenuLabel className="font-normal">
                  <div className="flex flex-col space-y-1">
                    <p className="text-sm font-medium leading-none">
                      {userLoading
                        ? "Loading..."
                        : user
                        ? `${user.first_name} ${user.last_name}`
                        : "Unknown User"}
                    </p>
                    <p className="text-xs leading-none text-muted-foreground">
                      {userLoading ? "..." : user?.email || "No email"}
                    </p>
                    {user?.role && (
                      <p className="text-xs leading-none text-muted-foreground">
                        Role: {user.role}
                      </p>
                    )}
                  </div>
                </DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={handleLogout}>
                  <LogOut className="mr-2 h-4 w-4" />
                  <span>Log out</span>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-y-auto p-6">{children}</main>
      </div>

      {/* Sidebar overlay for mobile */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}
    </div>
  );
}
