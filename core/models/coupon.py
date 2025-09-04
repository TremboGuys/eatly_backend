from django.db import models

from core.models import Order
from usuario.models import Usuario


class Coupon(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    discount = models.DecimalField(max_digits=5, decimal_places=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    min_value = models.DecimalField(max_digits=5, decimal_places=2)
    max_value = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

class CouponClient(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name="coupon_clients")
    client = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="client_coupons")
    active = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.idCoupon.name} - {self.idClient.name}"
    

class CouponClientOrder(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name="coupon_client_orders")
    client = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="client_coupons_orders")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_coupons")
    dateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.coupon.name} - Order {self.order.id}"