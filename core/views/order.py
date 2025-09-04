from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from core.models import Order
from core.serializers import OrderListSerializer, OrderRetrieveSerializer, CreateOrderSerializer, DeliveryManAcceptOrderSerializer, ProductOrderSerializer

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        if self.action == "retrieve":
            return OrderRetrieveSerializer
        if self.action == "partial_update":
            return DeliveryManAcceptOrderSerializer
        return CreateOrderSerializer