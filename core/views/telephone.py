from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from core.models import Telephone
from core.serializers import TelephoneSerializer

class TelephoneViewSet(ModelViewSet):
    queryset = Telephone.objects.all()
    serializer_class = TelephoneSerializer
    permission_classes = [AllowAny]