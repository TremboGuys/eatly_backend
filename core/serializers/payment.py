from rest_framework.serializers import ModelSerializer

from core.models import Payment, PaymentLog

class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"

class PaymentLogSerializer(ModelSerializer):
    class Meta:
        model = PaymentLog
        fields = "__all__"