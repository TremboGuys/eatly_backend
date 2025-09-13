from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from core.models import Restaurant
from core.serializers import RestaurantSerializer, CreateRestaurantSerializer, RetrieveRestaurantSerializer

class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return RetrieveRestaurantSerializer
        return RestaurantSerializer