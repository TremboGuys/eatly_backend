from rest_framework.viewsets import ModelViewSet

from core.models import Favorite
from core.serializers import FavoriteSerializer

class FavoriteViewSet(ModelViewSet):
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Favorite.objects.all()
        return Favorite.objects.filter(client=user)