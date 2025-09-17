from rest_framework.serializers import ModelSerializer, ValidationError, ImageField, HiddenField, CurrentUserDefault, SerializerMethodField
from rest_framework.response import Response
from rest_framework import status

from core.models import Product
from core.serializers import ProductCategorySerializer
from utils.helpers import create_image, update_image

class ProductSerializer(ModelSerializer):
    file = ImageField(write_only=True)
    restaurant = HiddenField(default=CurrentUserDefault())
    class Meta:
        model = Product
        fields = "__all__"
    
    def create(self, validated_data):
        categories = validated_data.pop("categories", [])
        image = create_image(validated_data.pop('file'))
        validated_data['url_file'] = image['secure_url']
        validated_data['public_id_cloudinary'] = image['public_id']

        product = Product.objects.create(**validated_data)
        
        product.restaurant = self.context['request'].user

        if categories:
            product.categories.set(categories)
        
        return product
    
    def update(self, instance, validated_data):
        file = validated_data.pop("file", None)
        categories = validated_data.pop("categories", [])
        if file is not None:
            image = update_image(file=file, public_id=instance.public_id_cloudinary)
            validated_data['url_file'] = image['secure_url']
            validated_data['public_id'] = image['public_id']

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if categories:
            instance.categories.set(categories)
        
        instance.save()
        
        return instance
    
    def validate(self, attrs):
        if self.context['request'].method == "POST":
            if attrs['file'] == None:
                raise ValidationError({"error": "File is missing!"})
        return attrs

class ListProductSerializer(ModelSerializer):
    categories = ProductCategorySerializer(many=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'is_adult', 'url_file', 'categories']

class RetrieveProductSerializer(ModelSerializer):
    categories = ProductCategorySerializer(many=True)
    restaurant = SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'restaurant', 'is_adult', 'url_file', 'categories']
    
    def get_restaurant(self, obj):
        restaurant = {"id": obj.restaurant.restaurant.id, "name": obj.restaurant.restaurant.name}

        return restaurant