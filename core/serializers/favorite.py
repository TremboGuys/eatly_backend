from rest_framework.serializers import ModelSerializer

from core.models import Favorite

class FavoriteSerializer(ModelSerializer):
    class Meta:
        model = Favorite
        fields = "__all__"