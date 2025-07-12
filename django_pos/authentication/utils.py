from django_pos.authentication.models import Permission


def create_permissions():
    """
    Create predefined permissions for the application.
    This function should be called once to set up the initial permissions.
    """
    permissions = [
        {"code": "branch_customers", "name": "Branch Customers"},
        {"code": "branch_expenses", "name": "Branch Expenses"},
        {"code": "branch_inventory", "name": "Branch Inventory"},
        {"code": "branch_purchases", "name": "Branch Purchases"},
        {"code": "branch_reports", "name": "View Branch Reports"},
        {"code": "branch_sales", "name": "Branch Sales"},
        {"code": "create_sales", "name": "Create Sales"},
        {"code": "daily_reports", "name": "Daily Reports"},
        {"code": "manage_branches", "name": "Manage Branches"},
        {"code": "manage_categories", "name": "Manage Categories"},
        {"code": "manage_customers", "name": "Manage Customers"},
        {"code": "manage_expenses", "name": "Manage Expenses"},
        {"code": "manage_inventory", "name": "Manage Inventory"},
        {"code": "manage_products", "name": "Manage Products"},
        {"code": "manage_purchases", "name": "Manage Purchases"},
        {"code": "manage_sales", "name": "Manage Sales"},
        {"code": "manage_stock", "name": "Manage Stock"},
        {"code": "manage_suppliers", "name": "Manage Suppliers"},
        {"code": "manage_users", "name": "Manage Users"},
        {"code": "stock_transfers", "name": "Stock Transfers"},
        {"code": "system_settings", "name": "System Settings"},
        {"code": "view_customers", "name": "View Customers"},
        {"code": "view_inventory_reports", "name": "Inventory Reports"},
        {"code": "view_products", "name": "View Products"},
        {"code": "view_reports", "name": "View All Reports"},
    ]

    for perm in permissions:
        Permission.objects.get_or_create(code=perm["code"], name=perm["name"])
