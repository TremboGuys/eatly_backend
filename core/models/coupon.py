from django.db import models

from core.models import  NaturalPerson, Order


class Coupon(models.Model):
    name = models.CharField(max_length=50, unique=True)
    decription = models.TextField()
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    min_value = models.DecimalField(max_digits=10, decimal_places=2)
    expiration_date = models.DateField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class CouponClient(models.Model):
    idCoupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name="coupon_clients")
    idClient = models.ForeignKey(NaturalPerson, on_delete=models.CASCADE, related_name="client_coupons")
    active = models.BooleanField(default=True)


    def __str__(self):
        return self.idCoupon.name
    

class CouponClientOrder(models.Model):
    idCoupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name="coupon_client_orders")
    idClient = models.ForeignKey(NaturalPerson, on_delete=models.CASCADE, related_name="client_coupons_orders")
    idOrder = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_coupons")
    dateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.idCouponClient.idCoupon.name} - Order {self.idOrder.id}"