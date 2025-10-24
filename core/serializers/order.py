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
            "restaurant": obj.product.restaurant.restaurant.id
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
        order = Order.objects.get(id=validated_data['order'])

        product_order = ProductOrder.objects.create(**validated_data)
        order.totalValue += product_order.product.price * product_order.quantity
        order.save()

        response = OrderRetrieveSerializer(Order.objects.get(id=order.id))

        return response
    
    def update(self, instance, validated_data):
        if validated_data.get('quantity', None) is not None:
            order = instance.order
            add_quantity = validated_data['quantity'] - order.quantity

            order.totalValue += instance.product.price * add_quantity
            order.save()
        for attr, value in validated_data.items():
            if hasattr(instance, attr):
                setattr(instance, attr, value)
        
        instance.save()

        response = OrderRetrieveSerializer(Order.objects.get(id=order.id))

        return response

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
            "photo": obj.restaurant.user.photo
        }
    class Meta:
        model = Order
        fields = ['id', 'restaurant', 'totalValue', 'dateTime', 'status', 'products', 'client']

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
                print(product)
                ProductOrder.objects.create(**product)
            
            OrderStatusLog.objects.create(order=order, status=order.status, dateTime=datetime.datetime.now())
            
            products_qs = ProductOrder.objects.filter(order=order.id).all()
            # products_response = ProductOrderListSerializer(products_qs, many=True).data

            # response = {
            #     **OrderListSerializer(order).data,
            #     "products": products_response,
            # }

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