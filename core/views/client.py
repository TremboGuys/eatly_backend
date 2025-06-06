from rest_framework.viewsets import ModelViewSet

from core.models import Client
from core.serializers import ClientSerializer

class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer