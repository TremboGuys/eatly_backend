from django.db import models

from core.models import Product, NaturalPerson

class Favorite(models.Model):
    client = models.ForeignKey(NaturalPerson, on_delete=models.CASCADE, related_name="favorite_products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="+")

    def __str__(self):
        return f"{self.client.id} - {self.product.name}"