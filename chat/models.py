from django.db import models
from django.conf import settings
from products.models import Product

class Xabar(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="xabarlar")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="yuborgan_xabarlar")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="olgan_xabarlar")
    matn = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}"

