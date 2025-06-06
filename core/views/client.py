from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from core.models import Client
from core.serializers import ClientSerializer

from .view_helpers import verify_role_register

class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def create(self, request):
        verify = verify_role_register(request.data)

        if verify == False:
            return Response({"message": "Role_register is already validated"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ClientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message": "Client created with success", "data": serializer.data}, status=status.HTTP_201_CREATED)