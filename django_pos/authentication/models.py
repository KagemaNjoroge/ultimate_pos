from django.db import models
from django.contrib.auth.models import AbstractUser
from company.models import Branch
from utils.models import TimestampedModel


class Permission(TimestampedModel):
    """
    Example: 'make_sales', 'view_reports', 'manage_inventory', 'view_all_branches'
    """

    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    """ "
    Roles:
      - Cashier: Can handle transactions and sales.
      - Branch Manager: Can manage the branch operations.
      - Admin: Has full access to the system, including user management.
      - Inventory Manager: Can manage inventory and stock levels.
    """

    ROLES = (
        (
            "Cashier",
            "Cashier",
        ),
        (
            "InventoryManager",
            "InventoryManager",
        ),
        (
            "Admin",
            "Admin",
        ),
        (
            "BranchManager",
            "BranchManager",
        ),
    )
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    permissions = models.ManyToManyField(Permission, blank=True)
    role = models.CharField(max_length=50, choices=ROLES, default="Cashier")
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    id_number = models.CharField(max_length=15, null=True, blank=True)
    profile_pic = models.ImageField(
        upload_to="profile_pics/",
        null=True,
        blank=True,
        default="static/img/profile/user-1.jpg",
    )

    def __str__(self):
        return self.username

    def has_perm_code(self, code):
        return self.permissions.filter(code=code).exists()
