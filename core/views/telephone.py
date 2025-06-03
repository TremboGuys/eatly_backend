from rest_framework.viewsets import ModelViewSet

from core.models import Telephone
from core.serializers import TelephoneSerializer

class TelephoneViewSet(ModelViewSet):
    queryset = Telephone.objects.all()
    serializer_class = TelephoneSerializer