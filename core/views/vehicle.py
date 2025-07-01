from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from core.models import Vehicle
from core.serializers import VehicleSerializer
from core.views.view_helpers import verify_group_user

class VehicleViewSet(ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def create(self, request):
        verify = verify_group_user(request.data['idNaturalPerson'], 'deliverymen')

        if verify == False:
            return Response({"message": "User is not a Delivery Men"}, status=status.HTTP_400_BAD_REQUEST)
        
        file = request.FILES['file']
        request.data['file'] = file

        # print(request.data['file'].file.getvalue())
        serializer =  VehicleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message": "Vehicle created with success", "data": serializer.data}, status=status.HTTP_201_CREATED)