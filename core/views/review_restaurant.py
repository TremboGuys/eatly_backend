from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend

from core.models import ReviewRestaurant, ResponseReviewRestaurant, Restaurant
from core.serializers import ReviewRestaurantSerializer, UpdateReviewRestaurantSerializer, ResponseReviewRestaurantSerializer, UpdateResponseReviewRestaurantSerializer

class ReviewRestaurantViewSet(ModelViewSet):
    queryset = ReviewRestaurant.objects.all()
    filter_backends = [DjangoFilterBackend]
    filters_fields = ['restaurant']
    
    def get_serializer_class(self):
        if self.action == "partial_update":
            return UpdateReviewRestaurantSerializer
        else:
            return ReviewRestaurantSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance = ReviewRestaurant.objects.get(id=instance.id)

        restaurant = Restaurant.objects.get(id=instance.restaurant.id)
        quantity_reviews = ReviewRestaurant.objects.filter(restaurant=restaurant.id).count()
        if quantity_reviews == 1:
            note_restaurant = 5.0
        else:
            note_restaurant = ((restaurant.note * quantity_reviews) - instance.note) / (quantity_reviews - 1)
        restaurant.note = note_restaurant
        restaurant.save()

        instance.delete()

        return Response({"message": "Review of restaurant deleted with success!"}, status=status.HTTP_204_NO_CONTENT)      

class ResponseReviewRestaurantViewSet(ModelViewSet):
    queryset = ResponseReviewRestaurant.objects.all()
    
    def get_serializer_class(self):
        if self.action == "partial_update":
            return UpdateResponseReviewRestaurantSerializer
        else:
            return ResponseReviewRestaurantSerializer