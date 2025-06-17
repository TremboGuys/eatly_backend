from rest_framework.serializers import ModelSerializer

from core.models import Vehicle
from core.serializers.serializer_helpers import make_user_active

class VehicleSerializer(ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"
    
    def create(self, validated_data):
        vehicle = make_user_active(validated_data=validated_data, instance=Vehicle)

        return vehicle