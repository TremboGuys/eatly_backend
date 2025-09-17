from rest_framework import serializers

from core.models import Vehicle

from utils.helpers import create_pdf, update_pdf

class VehicleSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)
    deliveryman = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Vehicle
        fields = ['deliveryman', 'mark', 'color', 'type_vehicle', 'model', 'plate', 'active', 'is_validate', 'url_crlv', 'file']
    
    def create(self, validated_data):
        pdf = validated_data.pop('file')
        url_pdf = create_pdf(pdf)

        validated_data['url_crlv'] = url_pdf['secure_url']
        validated_data['public_id_cloudinary'] = url_pdf['public_id']

        instance = Vehicle.objects.create(**validated_data)
        instance.deliveryman = self.context['request'].user
        instance.save()
        return instance

class UpdateVehicleSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)

    class Meta:
        model = Vehicle
        fields = ['color', 'active', 'file']
    
    def update(self, instance, validated_data):
        pdf = validated_data.pop('file', None)
        if pdf is not None:
            url_pdf = update_pdf(pdf, instance.public_id_cloudinary)
            instance.url_crlv = url_pdf['secure_url']
            instance.public_id_cloudinary = url_pdf['public_id']

        for attr, value in validated_data.items():
            print(attr)
            if hasattr(instance, attr):
                setattr(instance, attr, value)

        instance.save()

        return instance