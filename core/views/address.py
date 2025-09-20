from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from core.models import Address
from core.serializers import AddressSerializer

class AddressViewSet(ModelViewSet):
    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Address.objects.all()
        return Address.objects.filter(user=user)
    serializer_class = AddressSerializer
    permission_classes = [AllowAny]