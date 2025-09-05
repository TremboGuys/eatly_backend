from django.db import models

from core.models import Order, Restaurant

from usuario.models import Usuario

class ReviewRestaurant(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="+", unique=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT, related_name="reviews")
    client = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name="reviewsClient")
    note = models.PositiveSmallIntegerField(max_length=5)
    comment = models.TextField(max_length=800, null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.person.name} - {self.restaurant.name}"

class ResponseReview(models.Model):
    review = models.ForeignKey(ReviewRestaurant, on_delete=models.PROTECT, related_name="responses")
    author = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name="+")
    comment = models.TextField(max_length=800)
    date_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return 