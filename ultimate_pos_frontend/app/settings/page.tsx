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
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import {
  Bell,
  CreditCard,
  Database,
  Printer,
  RefreshCw,
  Save,
  Settings,
  Shield,
  Store,
  User,
  Wifi,
} from "lucide-react";

// Mock settings data
const businessInfo = {
  businessName: "UltimatePOS Store",
  address: "123 Business Street, City, State 12345",
  phone: "+1 (555) 123-4567",
  email: "info@ultimatepos.com",
  taxId: "TAX123456789",
  currency: "USD",
  timezone: "America/New_York",
};

const userSettings = {
  firstName: "John",
  lastName: "Doe",
  email: "john.doe@ultimatepos.com",
  role: "Admin",
  language: "English",
  dateFormat: "MM/DD/YYYY",
};

const systemSettings = [
  {
    category: "Notifications",
    icon: Bell,
    settings: [
      {
        name: "Email Notifications",
        enabled: true,
        description: "Receive email alerts for important events",
      },
      {
        name: "Low Stock Alerts",
        enabled: true,
        description: "Get notified when inventory is running low",
      },
      {
        name: "Daily Reports",
        enabled: false,
        description: "Receive daily sales and performance reports",
      },
    ],
  },
  {
    category: "Security",
    icon: Shield,
    settings: [
      {
        name: "Two-Factor Authentication",
        enabled: false,
        description: "Add extra security to your account",
      },
      {
        name: "Session Timeout",
        enabled: true,
        description: "Auto-logout after 30 minutes of inactivity",
      },
      {
        name: "Login Alerts",
        enabled: true,
        description: "Get notified of new login attempts",
      },
    ],
  },
  {
    category: "Payment",
    icon: CreditCard,
    settings: [
      {
        name: "Cash Payments",
        enabled: true,
        description: "Accept cash transactions",
      },
      {
        name: "Card Payments",
        enabled: true,
        description: "Accept credit and debit cards",
      },
      {
        name: "Digital Wallets",
        enabled: false,
        description: "Accept mobile payments",
      },
    ],
  },
  {
    category: "Hardware",
    icon: Printer,
    settings: [
      {
        name: "Receipt Printer",
        enabled: true,
        description: "Automatically print receipts",
      },
      {
        name: "Barcode Scanner",
        enabled: true,
        description: "Enable barcode scanning functionality",
      },
      {
        name: "Cash Drawer",
        enabled: true,
        description: "Integrate with cash drawer",
      },
    ],
  },
];

export default function SettingsPage() {
  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-3xl font-bold tracking-tight">Settings</h2>
            <p className="text-muted-foreground">
              Configure your POS system and business settings
            </p>
          </div>
        </div>

        <div className="grid gap-6 md:grid-cols-2">
          {/* Business Information */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Store className="h-5 w-5" />
                <span>Business Information</span>
              </CardTitle>
              <CardDescription>
                Update your business details and contact information
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="businessName">Business Name</Label>
                <Input
                  id="businessName"
                  defaultValue={businessInfo.businessName}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="address">Address</Label>
                <Input id="address" defaultValue={businessInfo.address} />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="phone">Phone</Label>
                  <Input id="phone" defaultValue={businessInfo.phone} />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    defaultValue={businessInfo.email}
                  />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="taxId">Tax ID</Label>
                  <Input id="taxId" defaultValue={businessInfo.taxId} />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="currency">Currency</Label>
                  <Input id="currency" defaultValue={businessInfo.currency} />
                </div>
              </div>
              <Button>
                <Save className="mr-2 h-4 w-4" />
                Save Changes
              </Button>
            </CardContent>
          </Card>

          {/* User Profile */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <User className="h-5 w-5" />
                <span>User Profile</span>
              </CardTitle>
              <CardDescription>
                Manage your personal account settings
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="firstName">First Name</Label>
                  <Input id="firstName" defaultValue={userSettings.firstName} />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="lastName">Last Name</Label>
                  <Input id="lastName" defaultValue={userSettings.lastName} />
                </div>
              </div>
              <div className="space-y-2">
                <Label htmlFor="userEmail">Email Address</Label>
                <Input
                  id="userEmail"
                  type="email"
                  defaultValue={userSettings.email}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="role">Role</Label>
                <div className="flex items-center space-x-2">
                  <Input id="role" defaultValue={userSettings.role} disabled />
                  <Badge variant="secondary">{userSettings.role}</Badge>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="language">Language</Label>
                  <Input id="language" defaultValue={userSettings.language} />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="dateFormat">Date Format</Label>
                  <Input
                    id="dateFormat"
                    defaultValue={userSettings.dateFormat}
                  />
                </div>
              </div>
              <Button>
                <Save className="mr-2 h-4 w-4" />
                Update Profile
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* System Settings */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Settings className="h-5 w-5" />
              <span>System Configuration</span>
            </CardTitle>
            <CardDescription>
              Configure system behavior and integrations
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              {systemSettings.map((category, categoryIndex) => {
                const Icon = category.icon;
                return (
                  <div key={category.category}>
                    <div className="flex items-center space-x-2 mb-4">
                      <Icon className="h-4 w-4" />
                      <h3 className="text-lg font-medium">
                        {category.category}
                      </h3>
                    </div>
                    <div className="space-y-3">
                      {category.settings.map((setting, settingIndex) => (
                        <div
                          key={setting.name}
                          className="flex items-center justify-between p-3 border rounded-lg"
                        >
                          <div>
                            <div className="font-medium text-sm">
                              {setting.name}
                            </div>
                            <div className="text-xs text-muted-foreground">
                              {setting.description}
                            </div>
                          </div>
                          <div className="flex items-center space-x-2">
                            <Badge
                              variant={setting.enabled ? "default" : "outline"}
                            >
                              {setting.enabled ? "Enabled" : "Disabled"}
                            </Badge>
                            <Button variant="ghost" size="sm">
                              {setting.enabled ? "Disable" : "Enable"}
                            </Button>
                          </div>
                        </div>
                      ))}
                    </div>
                    {categoryIndex < systemSettings.length - 1 && (
                      <Separator className="my-6" />
                    )}
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>

        {/* System Status */}
        <div className="grid gap-6 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Database className="h-5 w-5" />
                <span>System Status</span>
              </CardTitle>
              <CardDescription>
                Current system health and performance
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm">Database Connection</span>
                  <Badge variant="default">Connected</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Payment Gateway</span>
                  <Badge variant="default">Active</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Backup Status</span>
                  <Badge variant="secondary">Last: 2 hours ago</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">System Updates</span>
                  <Badge variant="outline">Up to date</Badge>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Wifi className="h-5 w-5" />
                <span>Quick Actions</span>
              </CardTitle>
              <CardDescription>Common system maintenance tasks</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <Button variant="outline" className="w-full justify-start">
                  <RefreshCw className="mr-2 h-4 w-4" />
                  Sync Data
                </Button>
                <Button variant="outline" className="w-full justify-start">
                  <Database className="mr-2 h-4 w-4" />
                  Backup Database
                </Button>
                <Button variant="outline" className="w-full justify-start">
                  <Printer className="mr-2 h-4 w-4" />
                  Test Printer
                </Button>
                <Button variant="outline" className="w-full justify-start">
                  <Settings className="mr-2 h-4 w-4" />
                  Reset Cache
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  );
}
