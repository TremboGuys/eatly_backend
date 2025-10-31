import datetime
from django.db import transaction
from rest_framework.serializers import ModelSerializer, ValidationError, HiddenField, CurrentUserDefault, SerializerMethodField

from core.models import Order, ProductOrder, OrderStatusLog, Restaurant

class ProductOrderListSerializer(ModelSerializer):
    product = SerializerMethodField()

    def get_product(self, obj):
        return {
            "id": obj.product.id,
            "name": obj.product.name,
            "description": obj.product.description,
            "price": obj.product.price,
            "url_file": obj.product.url_file,
            "is_adult": obj.product.is_adult,
        }
    class Meta:
        model = ProductOrder
        fields = "__all__"

class ProductOrderCartSerializer(ModelSerializer):
    product = SerializerMethodField()

    def get_product(self, obj):
        return {
            "id": obj.product.id,
            "name": obj.product.name,
            "price": obj.product.price,
            "url_file": obj.product.url_file,
        }
    class Meta:
        model = ProductOrder
        fields = "__all__"

class OrderRetrieveSerializer(ModelSerializer):
    products = ProductOrderListSerializer(many=True)
    restaurant = SerializerMethodField()

    def get_restaurant(self, obj):
        return {
            "id": obj.restaurant.id,
            "name": obj.restaurant.name,
            "photo": obj.restaurant.user.photo
        }
    class Meta:
        model = Order
        fields = "__all__"

class ProductOrderSerializer(ModelSerializer):
    class Meta:
        model = ProductOrder
        fields = "__all__"

    def create(self, validated_data):
        order = validated_data.get('order')
        order_instance = Order.objects.get(id=order.id)

        product_order = ProductOrder.objects.create(**validated_data)
        order_instance.totalValue += product_order.product.price * product_order.quantity
        order_instance.save()

        return order_instance
    
    def update(self, instance, validated_data):
        if validated_data.get('quantity', None) is not None:
            order = instance.order
            add_quantity = validated_data['quantity'] - instance.quantity

            order.totalValue += instance.product.price * add_quantity
            order.save()
        for attr, value in validated_data.items():
            if hasattr(instance, attr):
                setattr(instance, attr, value)
        
        instance.save()

        return instance

class OrderListSerializer(ModelSerializer):
    restaurant = SerializerMethodField()

    def get_restaurant(self, obj):
        return {
            "id": obj.restaurant.id,
            "name": obj.restaurant.name,
            "photo": obj.restaurant.user.photo
        }
    class Meta:
        model = Order
        fields = ['id', 'restaurant', 'totalValue', 'status', 'client']

class OrderListCartSerializer(ModelSerializer):
    client = HiddenField(default=CurrentUserDefault())
    products = ProductOrderCartSerializer(many=True)
    restaurant = SerializerMethodField()

    def get_restaurant(self, obj):
        return {
            "id": obj.restaurant.id,
            "user": obj.restaurant.user.id,
            "photo": obj.restaurant.user.photo,
        }
    class Meta:
        model = Order
        fields = ['id', 'restaurant', 'totalValue', 'dateTime', 'status', 'products', 'client']

class OrderListPreparingSerializer(ModelSerializer):
    client = HiddenField(default=CurrentUserDefault())
    products = SerializerMethodField()
    restaurant = SerializerMethodField()

    def get_products(self, obj):
        return [
            {
                "id": p.product.id,
                "name": p.product.name,
                "quantity": p.quantity,
            }
            for p in obj.products.all()
        ]
    
    def get_restaurant(self, obj):
        return {
            "id": obj.restaurant.id,
            "name": obj.restaurant.name,
            "photo": obj.restaurant.user.photo,
            "average_delivery_time": obj.restaurant.average_delivery_time
        }
    
    class Meta:
        model = Order
        fields = ['id', 'products', 'restaurant', 'client', 'status']

class CreateProductOrderSerializer(ModelSerializer):
    class Meta:
        model = ProductOrder
        fields = ['product', 'quantity', 'observation']

class CreateOrderSerializer(ModelSerializer):
    client = HiddenField(default=CurrentUserDefault())
    products = CreateProductOrderSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', "restaurant", "totalValue", "status", "products", 'client']
    
    def create(self, validated_data):
        with transaction.atomic():
            products = validated_data.pop('products')

            order = Order.objects.create(**validated_data)

            for product in products:
                product['order'] = order
                ProductOrder.objects.create(**product)
            
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