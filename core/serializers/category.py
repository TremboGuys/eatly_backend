from rest_framework import serializers

from core.models import Category

from infra import UploadCloudinary

class CategorySerializer(serializers.ModelSerializer):
    file = serializers.ImageField(write_only=True)
    
    class Meta:
        model = Category
        fields = "__all__"
    
    def create(self, validated_data):
        file = validated_data.pop('file')
        uploader = UploadCloudinary()
        response = uploader.create_image(file)

        validated_data['url_image'] = response['secure_url']

        return Category.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        file = validated_data.pop('file', None)
        if file:
            uploader = UploadCloudinary()
            response = uploader.create_image(file)

            instance.url_image = response['secure_url']
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        instance.save()

        return instance