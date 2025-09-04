from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from core.models import Vehicle
from core.serializers import VehicleSerializer

class VehicleViewSet(ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def create(self, request):
        file = request.FILES['file']
        request.data['file'] = file

        serializer =  VehicleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message": "Vehicle created with success", "data": serializer.data}, status=status.HTTP_201_CREATED)