from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Notifications(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ["-date"]
        db_table = "Notifications"


class License(models.Model):
    key = models.CharField(max_length=100, primary_key=True)
    active = models.BooleanField(default=True)
    expires = models.DateTimeField()
    company_id = models.IntegerField()

    def to_json(self):
        return {
            "key": self.key,
            "active": self.active,
            "expires": self.expires,
            "company_id": self.company_id,
        }

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = "License"
        verbose_name_plural = "Licenses"
        db_table = "Licenses"
