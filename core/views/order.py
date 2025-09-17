from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from core.models import Order
from core.serializers import OrderListSerializer, OrderRetrieveSerializer, CreateOrderSerializer, DeliveryManAcceptOrderSerializer, ProductOrderSerializer

class OrderViewSet(ModelViewSet):
    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Order.objects.all()
        if user.groups.filter(name='client'):
            return Order.objects.filter(client=user)
        elif user.groups.filter(name='restaurant'):
            return Order.objects.filter(restaurant=user.restaurant.id)
        elif user.groups.filter(name='deliveryman'):
            return Order.objects.filter(deliveryman=user)
        else:
            return Order.objects.none()

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        if self.action == "retrieve":
            return OrderRetrieveSerializer
        if self.action == "partial_update":
            return DeliveryManAcceptOrderSerializer
        return CreateOrderSerializer
