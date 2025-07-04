from django.db import models


class ResponseData(models.Model):
    """
    Model to store response data from the payment gateway.
    """

    response_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ResponseData {self.id} - {self.created_at}"
