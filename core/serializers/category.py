from rest_framework import serializers

from core.models import Category
from infra import UploadCloudinary
from utils.helpers import create_image

class CategorySerializer(serializers.ModelSerializer):
    file = serializers.ImageField(write_only=True)
    
    class Meta:
        model = Category
        fields = "__all__"
    
    def create(self, validated_data):
        validated_data['url_image'] = create_image(validated_data.pop('file'))

        return Category.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        file = validated_data.pop('file', None)
        if file:
            uploader = UploadCloudinary()
            response = uploader.create_image(file)

            instance.url_image = response
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        instance.save()

        return instance