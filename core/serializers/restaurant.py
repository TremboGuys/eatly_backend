from rest_framework.serializers import ModelSerializer, ValidationError, HiddenField, CurrentUserDefault, SerializerMethodField

from core.models import Restaurant
from core.serializers import CategorySerializer

class RestaurantSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    class Meta:
        model = Restaurant
        fields = "__all__"

class RetrieveRestaurantSerializer(ModelSerializer):
    products = SerializerMethodField()
    categories = CategorySerializer(many=True)
    class Meta:
        model = Restaurant
        fields = "__all__"

    def get_products(self, obj):
        from core.serializers import ListProductSerializer
        return ListProductSerializer(obj.user.products.all(), many=True).data

class CreateRestaurantSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"