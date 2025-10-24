from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from core.models import Order, ProductOrder
from core.serializers import OrderListSerializer, OrderListCartSerializer, OrderRetrieveSerializer, CreateOrderSerializer, DeliveryManAcceptOrderSerializer, ProductOrderSerializer

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
    
    @action(methods=['GET'], detail=False, url_path='cart')
    def cart(self, request):
        queryset = Order.objects.filter(client=self.request.user.id, status=1).all()
        print(queryset)
        serializer = OrderListCartSerializer(queryset, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
class ProductOrderViewSet(ModelViewSet):
    queryset = ProductOrder.objects.all()
    serializer_class = ProductOrderSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        order = instance.order
        order.totalValue -= instance.product.price * instance.quantity
        order.save()

        self.perform_destroy(instance)

        order_instance = OrderRetrieveSerializer(order).data

        return Response(data=order_instance, status=status.HTTP_200_OK)
