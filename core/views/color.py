from rest_framework.viewsets import ModelViewSet

from core.models import Color
from core.serializers import ColorSerializer

class ColorViewSet(ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer