from django.db import models

from .natural_person import NaturalPerson
from .restaurant import Restaurant

class Order(models.Model):
    class Status(models.IntegerChoices):
       PENDING = 1, "Pending"
       PREPARING = 2, "Preparing"
       ROUTE = 3, "Route"
       DELIVERED = 4, "Delivered" 
    deliverymen = models.ForeignKey(NaturalPerson, on_delete=models.PROTECT, related_name="orders_delivery", null=True, blank=True)
    client = models.ForeignKey(NaturalPerson, on_delete=models.PROTECT, related_name="orders_client")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT, related_name="orders")
    total_value = models.DecimalField(max_digits=7, decimal_places=2)
    date_time = models.DateTimeField()
    status = models.IntegerField(choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return f"{self.restaurant.user.first_name} - {self.deliverymen.user.email} - {self.client.user.email}"

    class Meta:
        unique_together = [('deliverymen', 'client')]