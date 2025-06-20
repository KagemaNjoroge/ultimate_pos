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