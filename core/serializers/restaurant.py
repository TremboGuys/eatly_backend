from rest_framework.serializers import ModelSerializer, ValidationError, HiddenField, CurrentUserDefault

from core.models import Restaurant

class RestaurantSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    class Meta:
        model = Restaurant
        fields = "__all__"