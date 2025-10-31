from django.db import models

from core.models import Order

class Payment(models.Model):
    class Methods(models.IntegerChoices):
        PIX = 1, "Pix",
        CREDIT = 2, "Credit Card"
        DEBIT = 3, "Debit Card"
    class Status(models.IntegerChoices):
        PENDING = 1, "Pending"
        APPROVED = 2, "Approved"
        REJECTED = 3, "Rejected"
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="payment")
    id_transaction_mp = models.PositiveBigIntegerField()
    qr_code = models.TextField()
    qr_code_base64 = models.TextField()
    method = models.IntegerField(choices=Methods.choices)
    status = models.IntegerField(choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return f"{self.order.id} - {self.status.name}"

class PaymentLog(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT, related_name="+")
    status = models.PositiveSmallIntegerField()
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payment} - {self.status} at {self.date_time}"