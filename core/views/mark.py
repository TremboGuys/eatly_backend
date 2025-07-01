from rest_framework.viewsets import ModelViewSet

from core.models import Mark
from core.serializers import MarkSerializer

class MarkViewSet(ModelViewSet):
    queryset = Mark.objects.all()
    serializer_class = MarkSerializer