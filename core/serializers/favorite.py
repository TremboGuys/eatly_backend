from rest_framework.serializers import ModelSerializer, HiddenField, CurrentUserDefault

from core.models import Favorite

class FavoriteSerializer(ModelSerializer):
    client = HiddenField(default=CurrentUserDefault())
    class Meta:
        model = Favorite
        fields = "__all__"