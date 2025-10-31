from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from core.models import Order, ProductOrder
from core.serializers import OrderListSerializer, OrderListCartSerializer, OrderListPreparingSerializer, OrderRetrieveSerializer, CreateOrderSerializer, DeliveryManAcceptOrderSerializer, ProductOrderSerializer, ProductOrderListSerializer

class OrderViewSet(ModelViewSet):
    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Order.objects.all()
        if user.groups.filter(name='client'):
            return Order.objects.filter(client=user.id)
        elif user.groups.filter(name='restaurant'):
            return Order.objects.filter(restaurant=user.restaurant.id, status__gte=2)
        elif user.groups.filter(name='deliveryman'):
            return Order.objects.filter(deliveryman=user.id, status__gte=3)
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
    
    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        products_qs = ProductOrder.objects.filter(order=order.id).all()
        products_response = ProductOrderListSerializer(products_qs, many=True).data

        response = {
            **OrderListSerializer(order).data,
            "products": products_response,
        }

        return Response(data=response, status=status.HTTP_200_OK)
    
    @action(methods=['GET'], detail=False, url_path='cart')
    def cart(self, request):
        queryset = Order.objects.filter(client=self.request.user.id, status=1).all()
        serializer = OrderListCartSerializer(queryset, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    @action(methods=['GET'], detail=False, url_path='preparing')
    def preparing(self, request):
        queryset = Order.objects.filter(client=self.request.user.id, status__gte=2, status__lt=4).select_related('restaurant').prefetch_related('products').all()
        serializer = OrderListPreparingSerializer(queryset, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    @action(methods=['GET'], detail=False, url_path='delivered')
    def delivered(self, request):
        queryset = Order.objects.filter(client=self.request.user.id, status=4).select_related('restaurant').prefetch_related('products').all()
        serializer = OrderListPreparingSerializer(queryset, many=True)
        
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
class ProductOrderViewSet(ModelViewSet):
    queryset = ProductOrder.objects.all()
    serializer_class = ProductOrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        response = OrderRetrieveSerializer(Order.objects.get(id=order.id)).data

        return Response(data=response, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        order = OrderRetrieveSerializer(Order.objects.get(id=serializer.data['order'])).data

        return Response(data=order, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        order = instance.order
        order.totalValue -= instance.product.price * instance.quantity
        order.save()

        self.perform_destroy(instance)

        order_instance = OrderRetrieveSerializer(order).data

        return Response(data=order_instance, status=status.HTTP_200_OK)
