from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from core.models import Restaurant
from core.serializers import RestaurantSerializer
from core.views.view_helpers import verify_is_active

class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def create(self, request):
        verify = verify_is_active(request.data)

        if verify == True:
            return Response({"message": "User is already active"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = RestaurantSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message": "Restaurant created with success", "data": serializer.data}, status=status.HTTP_201_CREATED)