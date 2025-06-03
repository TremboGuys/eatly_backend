from rest_framework.viewsets import ModelViewSet

from core.models import Address
from core.serializers import AddressSerializer

class AddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer