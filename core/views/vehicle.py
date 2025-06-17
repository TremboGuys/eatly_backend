from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from core.models import Vehicle
from core.serializers import VehicleSerializer
from core.views.view_helpers import verify_is_active

class VehicleViewSet(ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def create(self, request):
        verify = verify_is_active(request.data)

        if verify == True:
            return Response({"message": "User is already active"}, status=status.HTTP_400_BAD_REQUEST)

        serializer =  VehicleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message": "Vehicle created with success", "data": serializer.data}, status=status.HTTP_201_CREATED)