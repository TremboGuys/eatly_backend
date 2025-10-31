from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db.utils import IntegrityError

from core.models import Favorite
from core.serializers import FavoriteSerializer, FavoriteListSerializer

class FavoriteViewSet(ModelViewSet):

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Favorite.objects.all()
        return Favorite.objects.filter(client=user)
    
    def get_serializer_class(self):
        if self.action == "list":
            return FavoriteListSerializer
        else:
            return FavoriteSerializer
    
    def create(self, request, *args, **kwargs):
        try:
            serializerFavorite = self.get_serializer(data=request.data, context={'request': request})
            serializerFavorite.is_valid(raise_exception=True)
            favorite = serializerFavorite.save()

            listFavorite = FavoriteListSerializer(Favorite.objects.filter(client=favorite.client.id).all(), many=True)

            return Response(data=listFavorite.data, status=status.HTTP_200_OK)
        except IntegrityError as e:
            return Response(data={"error_code": "UNIQUE_VIOLATION", "message": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={"error_code": "GENERIC_ERROR", "message": f"{e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)