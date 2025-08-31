from django.db import models

from core.models import NaturalPerson, Restaurant

class Order(models.Model):
    class Status(models.IntegerChoices):
        PENDING = 1, "Pending"
        PREPARING = 2, "Preparing"
        DELIVERING = 3, "Delivering"
        DELIVERED = 4, "Delivered"
    client = models.ForeignKey(NaturalPerson, on_delete=models.PROTECT, related_name="ordersClient")
    deliveryMan = models.ForeignKey(NaturalPerson, null=True, on_delete=models.PROTECT, related_name="ordersDelivery")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT, related_name="orders")
    totalValue = models.DecimalField(max_digits=8, decimal_places=2)
    dateTime = models.DateTimeField(),
    status = models.IntegerField(choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return f"{self.id}"
