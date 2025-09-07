from rest_framework.viewsets import ModelViewSet

from core.models import ReviewRestaurant, ResponseReviewRestaurant
from core.serializers import ReviewRestaurantSerializer, ResponseReviewRestaurantSerializer

class ReviewRestaurantViewSet(ModelViewSet):
    queryset = ReviewRestaurant.objects.all()
    serializer_class = ReviewRestaurantSerializer

class ResponseReviewRestaurantViewSet(ModelViewSet):
    queryset = ResponseReviewRestaurant.objects.all()
    serializer_class = ResponseReviewRestaurantSerializer