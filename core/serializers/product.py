from rest_framework.serializers import ModelSerializer, ValidationError, ImageField, HiddenField, CurrentUserDefault
from rest_framework.response import Response
from rest_framework import status

from core.models import Product
from utils.helpers import create_image

class ProductSerializer(ModelSerializer):
    file = ImageField(write_only=True)
    restaurant = HiddenField(default=CurrentUserDefault())
    class Meta:
        model = Product
        fields = "__all__"
    
    def create(self, validated_data):
        categories = validated_data.pop("categories", [])
        validated_data['url_file'] = create_image(validated_data.pop('file'))

        product = Product.objects.create(**validated_data)
        
        product.restaurant = self.context['request'].user

        if categories:
            product.categories.set(categories)
        
        return product
    
    def update(self, instance, validated_data):
        file = validated_data.pop("file", None)
        categories = validated_data.pop("categories", [])
        if file is not None:
            validated_data['url_file'] = create_image(validated_data.pop('file'))

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