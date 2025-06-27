from django.db import models


class Photo(models.Model):
    image = models.ImageField(upload_to="photos", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        verbose_name_plural = "Photos"
        verbose_name = "Photo"

    def __str__(self) -> str:
        return f"Photo {self.id}"


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"Created at {self.created_at}, Updated at {self.updated_at}"
