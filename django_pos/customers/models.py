from django.db import models


class Customer(models.Model):
    """
    Represents a customer in the system.
    """

    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, blank=True, null=True)
    address = models.TextField(max_length=256, blank=True, null=True)
    email = models.EmailField(max_length=256, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    kra_pin = models.CharField(
        max_length=12, default="A000000000Z", blank=True, null=True
    )
    is_active = models.BooleanField(default=True)
    photo = models.FileField(
        upload_to="customers", blank=True, null=True, default="/img/undraw_profile.svg"
    )

    class Meta:
        db_table = "Customers"
        verbose_name_plural = "Customers"
        verbose_name = "Customer"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self) -> str:
        """
        Returns the full name of the customer.

        Returns:
            str: The full name of the customer.
        """
        return f"{self.first_name} {self.last_name}"

    def to_select2(self) -> dict:
        """
        Converts the customer object to a dictionary format compatible with Select2 library.

        Returns:
            dict: A dictionary containing the label and value of the customer object.
        """
        item = {"label": self.get_full_name(), "value": self.id}
        return item

    # override delete to also delete the photo from the filesystem
    def delete(self, *args, **kwargs):
        try:
            # delete the photo from the filesystem
            self.photo.delete()
        except Exception as e:
            # log the error
            pass
        finally:
            # call the parent delete method
            super().delete(*args, **kwargs)
