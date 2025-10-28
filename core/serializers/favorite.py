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
            "price": obj.product.price,
            "is_adult": obj.product.is_adult,
            "url_file": obj.product.url_file,
            "restaurant": {
                "id": obj.product.restaurant.restaurant.id,
                "photo": obj.product.restaurant.photo,
            }
        }
    class Meta:
        model = Favorite
        fields = "__all__"

class FavoriteSerializer(ModelSerializer):
    client = HiddenField(default=CurrentUserDefault())
    class Meta:
        model = Favorite
        fields = "__all__"

    def create(self, validated_data):
        print(validated_data)
        return super().create(validated_data)