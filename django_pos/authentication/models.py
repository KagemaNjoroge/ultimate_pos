from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    ROLES = (
        (
            "Cashier",
            "Cashier",
        ),
        (
            "Manager",
            "Manager",
        ),
        (
            "Admin",
            "Admin",
        ),
    )
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
