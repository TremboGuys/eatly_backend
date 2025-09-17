from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from core.models import Vehicle
from core.serializers import VehicleSerializer, UpdateVehicleSerializer

class VehicleViewSet(ModelViewSet):
    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Vehicle.objects.all()
        return Vehicle.objects.filter(deliveryman=user)
    
    def get_serializer_class(self):
        if self.action == "partial_update":
            return UpdateVehicleSerializer
        else:
            return VehicleSerializer

    def create(self, request):
        file = request.FILES['file']
        request.data['file'] = file

        serializer =  VehicleSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def partial_update(self, request, *args, **kwargs):
        if hasattr(request.FILES, 'file'):
            file = request.FILES['file']
            request.data['file'] = file

        instance = self.get_object()

        serializer = UpdateVehicleSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)