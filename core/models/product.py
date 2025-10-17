from django.db import models

from .category import Category
from usuario.models import Usuario

class Product(models.Model):
    class Status(models.IntegerChoices):
        ACTIVE = 1, "Active"
        INACTIVE = 2, "Inactive"
        ARCHIVED = 3, "Archived"
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    is_adult = models.BooleanField()
    status = models.IntegerField(choices=Status.choices, default=Status.ACTIVE)
    url_file = models.URLField(null=True, blank=True)
    public_id_cloudinary = models.CharField(max_length=40, default="")
    restaurant = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name="products")
    categories = models.ManyToManyField(Category, related_name="+")

    def __str__(self):
        return self.name