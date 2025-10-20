from django.db import models

from core.models import Restaurant, Product
from usuario.models import Usuario

class Order(models.Model):
    class Status(models.IntegerChoices):
        PENDING = 1, "Pending"
        PREPARING = 2, "Preparing"
        DELIVERING = 3, "Delivering"
        DELIVERED = 4, "Delivered"
    client = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name="ordersClient")
    deliveryman = models.ForeignKey(Usuario, null=True, on_delete=models.PROTECT, related_name="ordersDelivery")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT, related_name="orders")
    totalValue = models.DecimalField(max_digits=8, decimal_places=2)
    dateTime = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=Status.choices, default=Status.PENDING)
    produtct = [
        {

        }
    ]

    def __str__(self):
        return f"{self.id}"

class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="+")
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="products", null=True, blank=True)
    quantity = models.PositiveSmallIntegerField()
    observation = models.TextField(max_length=200, blank=True, null=True)