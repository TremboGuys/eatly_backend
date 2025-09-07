from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from core.models import Restaurant
from core.serializers import RestaurantSerializer, CreateRestaurantSerializer

class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    
    def get_serializer_class(self):
        if self.action == "create":
            return CreateRestaurantSerializer
        RestaurantSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "Restaurant created with success", "data": response.data}, status=status.HTTP_201_CREATED)