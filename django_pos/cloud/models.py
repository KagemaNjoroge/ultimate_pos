from django.db import models


# Create your models here.
class Software(models.Model):
    version = models.CharField(max_length=30)
    last_updated = models.DateTimeField(auto_now_add=True)
    download_url = models.URLField(blank=False, null=False)

    def __str__(self) -> str:
        return self.version

    def to_json(self) -> dict:
        return {
            "version": self.version,
            "last_updated": self.last_updated,
            "download_url": self.download_url,
        }

    class Meta:
        db_table = "Software"
        verbose_name_plural = "Software"
        verbose_name = "Software"


class Backup(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to="backups/")

    def __str__(self) -> str:
        return self.name

    def to_json(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "file": self.file.url,
        }

    class Meta:
        db_table = "Backup"
        verbose_name_plural = "Backups"
        verbose_name = "Backup"
