from django.db import models

from core.models import Order
from usuario.models import Usuario

class ReviewDeliveryman(models.Model):
    order = models.OneToOneField(Order, on_delete=models.PROTECT, related_name="+")
    client = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name="reviews_deliveryman")
    deliveryman = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name="reviews")
    note = models.PositiveSmallIntegerField()
    comment = models.TextField(max_length=300, null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.person.name} - {self.deliveryman.person.name}"

class ResponseReviewDeliveryman(models.Model):
    review = models.ForeignKey(ReviewDeliveryman, on_delete=models.PROTECT, related_name="responses")
    author = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name="+")
    comment = models.TextField(max_length=300)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.review} - {self.comment}"