from rest_framework.viewsets import ModelViewSet

from core.models import Favorite
from core.serializers import FavoriteSerializer

class FavoriteViewSet(ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer