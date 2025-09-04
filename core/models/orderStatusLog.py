from django.db import models

from core.models import Order

class OrderStatusLog(models.Model):
   order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="statusLogs")
   status = models.IntegerField(choices=Order.Status.choices)
   dateTime = models.DateTimeField(auto_now_add=True)
   
   def __str__(self):
        return self.Order.Status and self.dateTime
