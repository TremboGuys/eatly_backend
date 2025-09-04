import datetime
from rest_framework.serializers import ModelSerializer, ValidationError, HiddenField, CurrentUserDefault

from core.models import Order, ProductOrder, OrderStatusLog

class ProductOrderSerializer(ModelSerializer):
    class Meta:
        model = ProductOrder
        fields = "__all__"

class OrderListSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "restaurant", "status"]

class OrderRetrieveSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

class CreateOrderSerializer(ModelSerializer):
    client = HiddenField(default=CurrentUserDefault())
    products = ProductOrderSerializer(many=True)
    class Meta:
        model = Order
        fields = ["client", "restaurant", "totalValue", "status", "products"]
    
    def create(self, validated_data):
        products = validated_data.pop('products')

        order = Order.objects.create(**validated_data)

        for product in products:
            ProductOrder.objects.create(order=order, **product)
        
        OrderStatusLog.objects.create(order=order, status=order.status, dateTime=datetime.datetime.now())
        
        return order

class DeliveryManAcceptOrderSerializer(ModelSerializer):
    deliveryman = HiddenField(default=CurrentUserDefault())
    class Meta:
        model = Order
        fields = ["deliveryman", "status"]
    
    def update(self, instance, validated_data):
        user = self.context['request'].user

        print(user.groups.filter(name="deliveryman").exists())

        if user.groups.filter(name="deliveryman").exists():
            instance.deliveryman = user
            instance.status = validated_data['status']
        else:
            instance.status=validated_data['status']
        
        instance.save()

        OrderStatusLog.objects.create(order=instance, status=instance.status, dateTime=datetime.datetime.now())
        return instance

    # def validate(self, attrs):
    #     deliveryMan = attrs.get('deliveryMan', None)
    #     client = attrs.get('client', None)
    #     if (client is not None and deliveryMan is not None) and client == deliveryMan:
    #         raise ValidationError({"error": "Client and deliveryman can't have the same id"})
    
    #     if verify_group_user(client, None, 'client') == False:
    #         raise ValidationError({"error": "Id client does not have the corresponding group"})
        
    #     if deliveryMan is not None and verify_group_user(deliveryMan, None, 'deliveryman') == False:
    #         raise ValidationError({"error": "Id deliveryman does not have the corresponding group"})
        
    #     return attrs