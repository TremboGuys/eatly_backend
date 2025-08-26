from rest_framework.serializers import ModelSerializer, ValidationError

from core.models import Restaurant
from core.serializers.serializer_helpers import make_user_active
from utils.helpers import verify_is_active

class RestaurantSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"
    
    def create(self, validated_data):
        categories = validated_data.pop('categories', [])
        restaurant = make_user_active(validated_data=validated_data, instance=Restaurant)

        if categories:
            restaurant.categories.set(categories)

        return restaurant
    
    def validate(self, attrs):
        if self.context['request'].method == "POST":
            if verify_is_active(attrs) == True:
                raise ValidationError({"message": "User is already active"})
        return attrs