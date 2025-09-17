from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from core.models import Favorite
from core.serializers import FavoriteSerializer

class FavoriteViewSet(ModelViewSet):
    serializer_class = FavoriteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['client', 'product']

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Favorite.objects.all()
        return Favorite.objects.filter(client=user)