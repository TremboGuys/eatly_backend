from django.db import models

from .restaurant import Restaurant
from .category import Category

class Product(models.Model):
    class Status(models.IntegerChoices):
        ACTIVE = 1, "Active"
        INACTIVE = 2, "Inactive"
        ARCHIVED = 3, "Archived"
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    value = models.DecimalField(max_digits=7, decimal_places=2)
    is_adult = models.BooleanField()
    status = models.IntegerField(choices=Status.choices, default=Status.ACTIVE)
    url_file = models.URLField(null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT, related_name="products")
    categories = models.ManyToManyField(Category, related_name="+")

    def __str__(self):
        return self.name
