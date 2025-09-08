from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from core.models import ReviewRestaurant, ResponseReviewRestaurant, Restaurant
from core.serializers import ReviewRestaurantSerializer, ResponseReviewRestaurantSerializer

class ReviewRestaurantViewSet(ModelViewSet):
    queryset = ReviewRestaurant.objects.all()
    serializer_class = ReviewRestaurantSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        restaurant = Restaurant.objects.get(id=instance.restaurant.id)
        quantity_reviews = ReviewRestaurant.objects.filter(restaurant=restaurant.id).count()
        note_restaurant = ((restaurant.note * quantity_reviews) - instance.note) / (quantity_reviews - 1)
        restaurant.note = "{:.1f}".format(note_restaurant)
        restaurant.save()

        instance.delete()

        return Response({"message": "Restaurant deleted with success!"}, status=status.HTTP_204_NO_CONTENT)      

class ResponseReviewRestaurantViewSet(ModelViewSet):
    queryset = ResponseReviewRestaurant.objects.all()
    serializer_class = ResponseReviewRestaurantSerializer