from rest_framework.serializers import ModelSerializer

from core.models import OrderStatusLog

class OrderStatusLogSerializer(ModelSerializer):
    class Meta:
        model = OrderStatusLog
        fields = "__all__"