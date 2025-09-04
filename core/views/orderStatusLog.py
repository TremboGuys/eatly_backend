from rest_framework.viewsets import ModelViewSet

from core.models import OrderStatusLog
from core.serializers import OrderStatusLogSerializer

class OrderStatusLogViewSet(ModelViewSet):
    queryset = OrderStatusLog.objects.all()
    serializer_class = OrderStatusLogSerializer