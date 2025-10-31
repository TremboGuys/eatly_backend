from rest_framework.serializers import ModelSerializer, HiddenField, CurrentUserDefault, SerializerMethodField

from core.models import Favorite

class FavoriteListSerializer(ModelSerializer):
    client = HiddenField(default=CurrentUserDefault())
    product = SerializerMethodField()

    def get_product(self, obj):
        return {
            "id": obj.product.id,
            "name": obj.product.name,
            "description": obj.product.description,
            "url_file": obj.product.url_file,
            "restaurant": obj.product.restaurant.restaurant.id
        }
    class Meta:
        model = Favorite
        fields = "__all__"

class FavoriteSerializer(ModelSerializer):
    client = HiddenField(default=CurrentUserDefault())
    class Meta:
        model = Favorite
        fields = "__all__"