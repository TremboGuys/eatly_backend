from rest_framework import serializers

from core.models import Vehicle

from infra.cloudinary import UploadCloudinary

class VehicleSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)

    class Meta:
        model = Vehicle
        fields = "__all__"
    
    def create(self, validated_data):
        pdf = validated_data.pop('file')
        uploader = UploadCloudinary()
        url_pdf = uploader.create_pdf(pdf)

        validated_data['url_crlv'] = url_pdf['secure_url']

        return Vehicle.objects.create(**validated_data)