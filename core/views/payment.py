from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework import status

from core.serializers import PaymentSerializer, PaymentLogSerializer
from core.models import Payment, Order

class PaymentViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Payment.objects.all()
        elif user.groups.filter('client'):
            return Payment.objects.filter(order__client=user.id)
        
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        serializerPayment = self.get_serializer(data=request.data)
        serializerPayment.is_valid(raise_exception=True)
        payment = serializerPayment.save()

        serializerPaymentLog = PaymentLogSerializer(data={"payment": payment.id, "status": payment.status})
        serializerPaymentLog.is_valid(raise_exception=True)
        serializerPaymentLog.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['PATCH'], detail=False, url_path='notifications')
    def notification(self, request, *args, **kwargs):
        id_transaction = request.query_params.get('id_transaction', None)

        if id_transaction is None:
            return Response(data={"error_code": "ID_TRANSACTION_NOT_FOUND", "message": "Id transaction not passed in query params"}, status=status.HTTP_400_BAD_REQUEST)
        instance = Payment.objects.get(id_transaction_mp=id_transaction)
        serializerPayment = self.get_serializer(instance=instance, data=request.data, partial=True)
        serializerPayment.is_valid(raise_exception=True)
        payment = serializerPayment.save()

        serializerPaymentLog = PaymentLogSerializer(data={"payment": payment.id, "status": payment.status})
        serializerPaymentLog.is_valid(raise_exception=True)
        serializerPaymentLog.save()

        if payment.status == 2:
            order = Order.objects.get(id=payment.order.id)
            order.status = 2
            order.save()

        return Response(status=status.HTTP_204_NO_CONTENT)