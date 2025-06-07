from rest_framework.serializers import ModelSerializer

from core.models import Restaurant
from core.serializers.serializer_helpers import make_user_active

class RestaurantSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"
    
    def create(self, validated_data):
        restaurant = make_user_active(validated_data=validated_data, instance=Restaurant)

        return restaurant