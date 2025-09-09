from django.db import models

from usuario.models import Usuario

from core.models import Order, Restaurant

class ReviewRestaurant(models.Model):
    order = models.OneToOneField(Order, on_delete=models.PROTECT, related_name="+")
    client = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name="reviews_restaurant")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT, related_name="reviews")
    note = models.PositiveSmallIntegerField()
    comment = models.TextField(max_length=500, null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.person.name - {self.restaurant.name}}"

class ResponseReviewRestaurant(models.Model):
    review = models.ForeignKey(ReviewRestaurant, on_delete=models.PROTECT, related_name="responses")
    author = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name="+")
    comment = models.TextField(max_length=300)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.review} - {self.comment}"
